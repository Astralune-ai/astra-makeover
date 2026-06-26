# Design Brief — the interview

Ask these per room in Stage 3. **Smart-skip:** never ask anything the user already gave in
Stage 1 (or in the trigger message, e.g. "makeover this kitchen, Japandi, resale, $30k").
Stop and wait for the answers before generating.

In Claude Code, batch with the choice UI (max 4 questions per batch → ~2 batches). In other
agents, ask as plain grouped questions. Map each answer to a `--brief key=value` pair.

## Batch 1 — direction (the four that shape the board most)

| # | Question | Options | → brief key |
|---|----------|---------|-------------|
| 1 | Design style? | Modern Australian (default) · Japandi · Coastal · Hamptons · Scandinavian · Contemporary · … (see styles.md) | `Style` |
| 2 | Renovation objective? | Owner-occupied · Resale · Investment / rental · Airbnb | `Objective` |
| 3 | Budget range? | <$20k · $20–40k · $40–80k · $80k+ | `Budget` |
| 4 | Priority? | Highest ROI · Lowest cost · Premium appearance · Fast build · Best resale · Rental-friendly | `Priority` |

## Batch 2 — keep / constraints

| # | Question | Options | → brief key |
|---|----------|---------|-------------|
| 5 | Keep existing flooring? | Yes · No | `Keep flooring` |
| 6 | Keep existing cabinetry? | Yes · Reface · No | `Keep cabinetry` |
| 7 | Keep existing furniture? | Yes · No | `Keep furniture` |
| 8 | Any items that must remain? | free text (e.g. "oven", "none") | `Must keep` |

## Optional

- **Reference images?** If the user has a style reference photo, collect it and pass it as an
  extra `--ref` (the model reads it for style, keeps the room's structure).

## Defaults (state them as assumptions if not asked)

If the user wants to move fast and skips some: Style=Modern Australian, Objective=Resale,
Budget=$20–40k, Keep flooring=Yes, Keep cabinetry=Reface, Priority=Best Resale. Always tell
the user which defaults you assumed.
