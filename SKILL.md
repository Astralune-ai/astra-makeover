---
name: astra-makeover
description: |
  Turn property photos into a photorealistic renovation analysis board through a guided
  interview. Drop a room photo, answer a short design brief, and get ONE image: the
  renovated render + before + annotated callouts + material board + budget (Low/Med/High)
  + ROI + priorities + recommendation. Built for real-estate agents, staging companies and
  flippers to show clients the renovated potential of a property. Self-contained (only needs
  an OpenAI API key) and portable across agents (Claude Code, Codex, …).
  Trigger words: astra-makeover, makeover, renovation board, 装修分析板, 房产改造图, 虚拟装修,
  给这个房子出改造图, stage this property, show the renovated potential, before and after reno,
  property makeover, 房子翻新效果图.
---

# astra-makeover — renovation analysis board from a photo

Produce a **renovation analysis board**: one AI-generated, multi-panel image built from
property photo(s) — hero render, before thumbnail, annotated render, material board, budget
(Low/Medium/High), ROI, priority matrix, risks, and final recommendation.

The board is generated in **one shot** by feeding the full renovation prompt + a short
client brief + the room photo(s) to **OpenAI gpt-image-2** via `scripts/makeover.py`.

## ⛔ Generation invariant — always use the API path

**Always generate through `scripts/makeover.py` (the OpenAI API). NEVER use the host agent's
built-in image generation.** The API path does a true image-edit on the real room, passes the
complete prompt, and runs at `quality=high` — materially better and consistent across agents.
Built-in agent image tools test far worse (no high quality, photos not used as a real edit,
prompt truncation). This rule holds in every agent, including Codex.

## The flow (per room)

Run these stages in order. One room per run; for multiple rooms, repeat per room.

### Stage 0 — Setup (first run only, idempotent)

Check for a usable OpenAI API key. If `makeover.py --check-key` fails (or no key is set),
run the **key onboarding** (below) before anything else. If a valid key already exists, skip.

### Stage 1 — Intake

Get the room's photo(s) from the user (one or more, multiple angles of the **same** room are
fine) and which property + room it is. Confirm the room.

### Stage 2 — Space Analysis

Read the photo(s) and give a concise analysis only — room type, layout, materials, condition,
strengths, weaknesses, opportunities. **Do not generate anything yet.**

### Stage 3 — Design Brief (the interview)

Ask the brief in `references/design-brief.md`, **skipping anything the user already stated**
in Stage 1 (smart-skip). In Claude Code, batch the questions with the choice UI (max 4 per
batch). In other agents, ask them as plain grouped questions. **Then stop and wait for the
answers** — do not generate before the brief is answered.

### Stage 4 — Generate (API only)

Assemble the answers into `--brief key=value` pairs and call the engine:

```bash
python3 scripts/makeover.py \
  --ref <photo1> [--ref <photo2> …] \
  --brief Style=<…> --brief Objective=<…> --brief Budget=<…> \
  --brief 'Keep flooring=<…>' --brief 'Keep cabinetry=<…>' \
  --brief 'Must keep=<…>' --brief Priority=<…> \
  --property "<property name>" --room <room>
```

Run it once **without `--confirm` first** (dry run) to self-check that the brief prefix is
present and the photos are attached, then re-run **with `--confirm`** to generate.

### Stage 5 — Deliver

Show the saved board image. Offer tweaks — change a brief answer and regenerate, re-roll, or
render a longer portrait if the small print is too small. The image and the assembled prompt
are saved to `~/makeover-outputs/<property>/<room>-board-<timestamp>.png`.

## Key onboarding

When no valid key is found, run `python3 scripts/makeover.py --setup`. It:
1. Explains the key is needed (pay-per-image, ~a few cents/board) and stays local.
2. Points to https://platform.openai.com/api-keys → Create new secret key.
3. Takes the pasted key (hidden input), validates it, and saves it to
   `~/.config/astra-makeover/config.env` (chmod 600, gitignored).

Re-validate any time with `--check-key`. The key is resolved as: `OPENAI_API_KEY` env →
`~/.config/astra-makeover/config.env`.

## Design brief (summary)

Style · Objective (owner/resale/investment/airbnb) · Budget (<$20k / $20–40k / $40–80k / $80k+) ·
Keep flooring? · Keep cabinetry? (yes/reface/no) · Keep furniture? · Must-keep items ·
Reference images (if any, pass as extra `--ref`) · Priority (highest ROI / lowest cost /
premium / fast build / best resale / rental-friendly). Full list + smart-skip rules in
`references/design-brief.md`. Style list in `references/styles.md`.

## Notes

- **Self-contained:** only needs `pip install openai` + an API key. The renovation prompt
  (`prompt/makeover-board.md`) and engine (`scripts/makeover.py`) ship with the skill.
- **Boards are clean / unbranded** so the agency presents them as their own.
- **Multiple rooms:** one board per room; run the flow per room.
- **Cross-agent:** the flow is written in plain actions; any agent that can run a shell and
  ask the user questions can run it. Generation is always the API path (see the invariant).
