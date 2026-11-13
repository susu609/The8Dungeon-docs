---
name: minecraft-entity-model
description: Design, build and screenshot a vanilla-style Minecraft entity model for Blockbench (modded_entity, box UV) without opening Blockbench. Use when the user asks to suggest/design/create/fix a mob, pet, NPC or entity model, a .bbmodel, an entity texture, or a preview render of one, for this MCreator mod (The8Dungeon) or any Java Edition mod. Produces .bbmodel + 64x64 texture + 4-angle preview PNG from a JSON spec, following the Minecraft Style Guide.
---

# Minecraft entity model (Blockbench, box UV)

Pipeline: **ask → write JSON spec → run script → look at the render → fix → deliver.**

## 1. Ask the user, step by step (one AskUserQuestion round each)

Skip a step only if the user already answered it.

1. Role in game (NPC, pet, boss, mob, decoration) and overall shape/reference.
2. Behaviour hint (affects pivots/groups for later animation) and target size in blocks
   (1 block = 16 px; 0.6 block ≈ 10 px tall).
3. Accessories, texture resolution (default 64x64) and main colour.
4. Confirm the design + which preview angles + where to save (scratchpad vs. repo).
   Never commit unless the user asks.

## 2. Write the spec (see `examples/clawd_agent.json`)

```jsonc
{
  "name": "snake_case_id",
  "texture_size": 64,
  "palette": {                 // 5-tone hue-shifted ramp + detail colours, NOTHING else
    "light": "#..", "mid": "#..", "dark": "#..", "darker": "#..", "darkest": "#..",
    "eye": "#.."
  },
  "face_tones": {},            // optional override of the default per-face tone
  "bottom_shadow": true,       // one darker row at the bottom of side faces
  "group_pivots": {"legs": [0,3,0]},
  "cubes": [
    {"name": "body", "group": "body", "from": [x,y,z], "size": [w,h,d],
     "pivot": [x,y,z], "uv": [u,v], "face_tones": {"north": "light"}}
  ],
  "details": [["body","north", x, y, "eye"]]   // single pixels on one face, face-local coords
}
```

- `uv` is optional; omitted islands are shelf-packed automatically.
- Default face tones: up=light, north=mid, east/west=dark, south=darker, down=darkest.
- North (-Z) is the **front**: put the face/eyes there.
- `details` coordinates are inside that face, (0,0) = top-left as seen from outside.

## 3. Run

```bash
python3 .claude/skills/minecraft-entity-model/scripts/build_entity.py SPEC.json OUT_DIR
```

Outputs in OUT_DIR: `<name>.bbmodel` (texture embedded), `<name>.png`,
`<name>_texture_preview.png` (8x nearest-neighbour), `<name>_views.png`
(FRONT, 3/4, SIDE, BACK 3/4). The script prints a `lint:` line; fix every warning.

Then **Read `<name>_views.png` and check it yourself** before sending: eyes on the front,
nothing floating, legs touching y=0, silhouette recognisable. Send files with SendUserFile.

## 4. Style rules (Minecraft Style Guide — enforce them)

Modelling
- Lowest element count that still reads correctly; shape from the model, detail from the texture.
- Whole-pixel sizes only — no element < 1 px, no inflate (no mixels).
- No stair-stepped curves; round things are one box. Rotate an element only when justified.
- Prefer one element + transparent pixels over many tiny elements.
- Big head / small body = cute; big torso/arms = strong.

Texturing
- Restricted palette: one ramp of ~5 tones, hue-shifted (shadows toward red/brown,
  highlights toward yellow), plus a few detail colours. Lint warns above 8 colours.
- **Entity rule:** top and front brighter than bottom and back — both across faces and within a face.
- Do NOT: smooth gradients, banding (rows/diagonals of stepped tones), pillow shading (concentric
  rims), pancake shading (light one side, dark the other regardless of form), brush noise,
  random speckles, unnecessary dithering, anti-aliasing on box edges.
- Add surface detail deliberately, pixel by pixel, through `details`.

## 5. Honest caveats to tell the user

- The preview is this script's own renderer, not Blockbench; Blockbench's view may differ slightly.
- The `.bbmodel` targets Blockbench 4.x "Modded Entity"; say if it hasn't been opened there.
- MCreator import: Blockbench → File → Export → Export Java Entity (1.17+), then
  MCreator → Resources → Models → Import Java model, and assign `<name>.png`.
