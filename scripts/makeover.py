#!/usr/bin/env python3
"""astra-makeover — turn property photos into a renovation analysis board.

Reads the full renovation prompt (prompt/makeover-board.md), prepends an optional
CLIENT BRIEF, attaches the room photo(s), and calls OpenAI gpt-image-2 (images.edit)
to produce ONE image: the full multi-panel analysis board (render + before + annotated
render + material board + budget + ROI + priority + recommendation).

DESIGN INVARIANT — generation ALWAYS goes through this OpenAI API path, never an agent's
built-in image tool. The API path keeps full control (true image-edit on the real room +
the complete prompt + quality=high), which is materially better than native agent image
generation.

Only dependency: `pip install openai` + an OPENAI_API_KEY.

Usage:
  makeover.py --setup                       # first-run: configure the API key
  makeover.py --check-key                   # validate the configured key
  makeover.py --ref room.jpg [--ref a2.jpg] \
              --brief Style=Japandi --brief Objective=Resale --brief Budget='$20-40k' \
              --property "12 King St" --room kitchen           # DRY RUN (no spend)
  makeover.py ... --confirm                  # actually generate
"""
import argparse
import base64
import os
import sys
import time
from getpass import getpass
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
PROMPT_FILE = SKILL_DIR / "prompt" / "makeover-board.md"
CONFIG_FILE = Path.home() / ".config" / "astra-makeover" / "config.env"
DEFAULT_OUT = Path.home() / "makeover-outputs"
MODEL = "gpt-image-2"


# ---------- API key ----------

def load_key():
    """Resolve the key: env OPENAI_API_KEY → config.env → None."""
    k = os.environ.get("OPENAI_API_KEY")
    if k:
        return k.strip()
    if CONFIG_FILE.exists():
        for line in CONFIG_FILE.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("OPENAI_API_KEY="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    return None


def save_key(key):
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(f"OPENAI_API_KEY={key}\n", encoding="utf-8")
    os.chmod(CONFIG_FILE, 0o600)


def make_client(key):
    try:
        from openai import OpenAI
    except ImportError:
        sys.exit("❌ Missing dependency. Run:  pip install openai")
    return OpenAI(api_key=key)


def validate_key(key):
    """Cheap validation: list models. Returns (ok, error_str)."""
    try:
        make_client(key).models.list()
        return True, None
    except Exception as e:  # noqa: BLE001 — surface any auth/network failure to the user
        return False, str(e)


def cmd_setup():
    print("astra-makeover needs an OpenAI API key.")
    print("  • Pay-per-image: roughly a few cents per board.")
    print("  • The key stays on this machine (never uploaded, never committed).")
    print("  • Get one at: https://platform.openai.com/api-keys  → Create new secret key\n")
    key = getpass("Paste your OpenAI API key (input hidden): ").strip()
    if not key:
        sys.exit("No key entered. Nothing changed.")
    print("Validating…")
    ok, err = validate_key(key)
    if not ok:
        sys.exit(f"❌ Key validation failed: {err}")
    save_key(key)
    print(f"✅ Key saved to {CONFIG_FILE} (chmod 600). You're ready to generate.")


def cmd_check_key():
    key = load_key()
    if not key:
        sys.exit("❌ No key found. Run:  makeover.py --setup")
    ok, err = validate_key(key)
    print("✅ Key valid." if ok else f"❌ Key invalid: {err}")
    sys.exit(0 if ok else 1)


# ---------- prompt assembly ----------

def build_brief(pairs):
    """Build the CLIENT BRIEF steering prefix from key=value pairs."""
    items = []
    for p in pairs:
        p = p.strip()
        if not p or p.startswith("#"):
            continue
        if "=" in p:
            k, v = p.split("=", 1)
            items.append(f"{k.strip()}={v.strip()}")
    if not items:
        return ""
    return ("CLIENT BRIEF (honour these strictly):\n  "
            + "; ".join(items) + "\n"
            + "─" * 40 + "\n\n")


# ---------- main ----------

def main():
    ap = argparse.ArgumentParser(
        prog="makeover.py",
        description="Generate a renovation analysis board from property photo(s).")
    ap.add_argument("--ref", action="append", default=[],
                    help="room photo path (repeatable; multiple angles of the SAME room ok)")
    ap.add_argument("--brief", action="append", default=[],
                    help="client brief key=value (repeatable), e.g. --brief Style=Japandi")
    ap.add_argument("--brief-file", help="file with one key=value per line (# comments ok)")
    ap.add_argument("--property", default="property", help="property name → output subfolder")
    ap.add_argument("--room", default="room", help="room label → output filename")
    ap.add_argument("--out", help="output dir (default ~/makeover-outputs/<property>/)")
    ap.add_argument("--size", default="1024x1536", help="gpt-image-2 size (default portrait)")
    ap.add_argument("--quality", default="high", choices=["low", "medium", "high"])
    ap.add_argument("--confirm", action="store_true", help="actually generate (default: dry run)")
    ap.add_argument("--setup", action="store_true", help="configure the OpenAI API key")
    ap.add_argument("--check-key", dest="check_key", action="store_true",
                    help="validate the configured key")
    args = ap.parse_args()

    if args.setup:
        cmd_setup()
        return
    if args.check_key:
        cmd_check_key()
        return

    if not PROMPT_FILE.exists():
        sys.exit(f"❌ Prompt file missing: {PROMPT_FILE}")
    if not args.ref:
        sys.exit("❌ Need at least one --ref <room photo>.  (or --setup / --check-key)")
    for r in args.ref:
        if not Path(r).expanduser().exists():
            sys.exit(f"❌ Photo not found: {r}")

    body = PROMPT_FILE.read_text(encoding="utf-8")
    brief_pairs = list(args.brief)
    if args.brief_file:
        brief_pairs += Path(args.brief_file).expanduser().read_text(encoding="utf-8").splitlines()
    brief = build_brief(brief_pairs)
    prompt = brief + body

    print("─" * 60)
    print(f"astra-makeover · {MODEL} · size {args.size} · quality {args.quality}")
    print(f"property: {args.property}   room: {args.room}")
    print(f"refs ({len(args.ref)}): " + ", ".join(args.ref))
    if brief:
        print("\n" + brief, end="")
    print(f"prompt: brief {len(brief)} + body {len(body)} = {len(prompt)} chars")
    print("─" * 60)

    if not args.confirm:
        print("🟡 DRY RUN (no spend). Re-run with --confirm to generate.")
        return

    key = load_key()
    if not key:
        sys.exit("❌ No OpenAI API key. Run:  makeover.py --setup")
    client = make_client(key)

    imgs = [open(Path(r).expanduser(), "rb") for r in args.ref]
    print("⏳ generating via gpt-image-2…")
    try:
        resp = client.images.edit(model=MODEL, image=imgs, prompt=prompt,
                                   size=args.size, quality=args.quality)
    except Exception as e:  # noqa: BLE001
        sys.exit(f"❌ Generation failed: {e}")
    finally:
        for f in imgs:
            f.close()

    out_dir = Path(args.out).expanduser() if args.out else (DEFAULT_OUT / args.property)
    out_dir.mkdir(parents=True, exist_ok=True)
    ts = time.strftime("%Y%m%d-%H%M%S")
    stem = f"{args.room}-board-{ts}"
    out_path = out_dir / f"{stem}.png"
    out_path.write_bytes(base64.b64decode(resp.data[0].b64_json))
    # keep the assembled prompt next to the image for reproducibility
    (out_dir / f"{stem}.prompt.txt").write_text(prompt, encoding="utf-8")
    print(f"✅ {out_path}")


if __name__ == "__main__":
    main()
