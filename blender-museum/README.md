# The Quiet Collection — Blender museum

**Latest version:** `quiet-collection-illustrated-museum.blend` — the illustrated treatment across all galleries, Cormorant Garamond lettering, and animated floating “WHAT ARE YOU?” title. See `ILLUSTRATED_MUSEUM.md` for this version's controls and rendering instructions. The six-second title preview is `what-are-you-title.mp4`. The original version described below is preserved.

An editable, warm low-poly museum environment for the planned personality quiz. Eight exhibit stops, three galleries, central reveal case, entry vestibule, and 30-second camera animation.

## Main file

Open `quiet-collection-museum.blend` in Blender. It is saved in cutaway overview mode, with textures packed. It was authored with Blender 5.2.1 LTS.

### View modes

The numbered collections separate scene systems:

- `00 | Architecture`: foundations, floors, fixed walls.
- `01 | Cutaway walls — enable for interiors`: front/east walls hidden for the overview.
- `02 | Ceilings — enable for interiors`: roof planes and beams hidden for the overview.
- `03 | Joinery and lamps`: furniture, practical lights, doorway labels.
- `04 | Eight quiz exhibits`: question stations and replica specimens.
- `05 | Kenney CC0 nature assets`: imported props.
- `06 | Cameras and navigation`: overview, visitor views, animated tour.
- `07 | Overview studio fill`: additional lights for the cutaway only.

For interior rendering, enable render visibility for collections 01 and 02 and disable collection 07. Enable viewport visibility too if inspecting the enclosed space interactively.

Select a camera in the Outliner, then use View > Cameras > Set Active Object as Camera. Numpad 0 views the active camera. The camera called `07 | Animated walkthrough` contains frames 1–720 at 24 fps. Scrub the timeline to inspect it; the camera route is an authored reference, not gameplay controls.

## What is included

- A single-floor, approximately 24 × 22 m cross-shaped layout.
- Dark timber panelling, moss/petrol walls, brass mouldings, amber lanterns, warm wood floors and an oxblood hall runner.
- A faceted central glass reveal cabinet, fossil displays, a stylised skeleton, mineral drawers, meteorite, comparative crystals, habitat case, botanical prints, and fieldwork table.
- Editable separate objects and collections, reusable assets, named cameras, and packed materials.
- Preview renders in `renders/`.
- A lightweight `museum-walkthrough.mp4` reference tour, 24 seconds at 6 fps. This uses Eevee with simplified lamp shadows and glass panes hidden to avoid transparency noise. The stills use Cycles and are the better reference for final lighting and glass. Glass remains present in the editable Blender scene.
- Reproducible construction script: `build_museum.py`.

## Scope

This is the Blender environment and visual direction, not the playable quiz. Hotspot logic, audio-guide companion, questions, scoring, and API calls belong in the later application. Case labels identify intended stations. The skeleton and other specimens are decorative replicas; the incomplete-skeleton interaction would swap or hide a chosen bone during implementation.

The .blend is the source of truth. Web export needs a separate optimisation pass (join repeated geometry where suitable, bake lighting, optimise glass, create collision/navigation meshes). The scene has deliberately editable repeated objects rather than a finished mobile-game draw-call budget. The saved scene contains 1,726 objects and seven cameras; the used wood image is packed.

## Rebuild

From the project directory on this Mac:

```sh
/Applications/Blender.app/Contents/MacOS/Blender --background --python blender-museum/build_museum.py
```

This regenerates the scene and previews, replacing outputs with the same filenames. Preserve a copy first if you have made manual edits.

Asset sources and licences are documented in `ASSET_CREDITS.md`.

To regenerate only the lightweight reference movie, run Blender in background mode with `--python blender-museum/render_walkthrough.py`. It reads the saved scene and does not replace it. For a smoother final movie, render the original 720-frame camera animation at 24 fps after switching to the interior collection settings.
