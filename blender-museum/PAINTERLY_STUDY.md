# Central hall — painterly material study

Open `quiet-collection-painterly-study.blend`. The original `quiet-collection-museum.blend` is unchanged.

The study opens in the same hall camera used for `renders/02-hall.png`, with the enclosing walls and ceiling enabled. This is a central-hall test; neighbouring galleries retain their original materials.

Changes:
- Replaced the photographic walnut grain in the hall with procedural, directional pigment marks.
- Added broad colour patches and subtle brush relief to painted surfaces.
- Changed brass and wood to matte, illustrated finishes.
- Shifted deep browns toward muted plum and walls toward olive.
- Reduced glass reflections and lamp emission; retained the amber practical lighting with a soft violet fill.
- All paint variation is attached to object coordinates, not applied as a moving screen-space filter.

The render is `renders/05-painterly-hall.png`. No full-screen painterly filter or heavy black outlines are used. This is a procedural approximation of brushwork, not a claim of hand-painted artwork. The materials remain editable in Blender; procedural shaders will need baking for a later web/game export.

Reproduce the study with Blender in background mode and `--python blender-museum/painterly_hall.py`. It reads the original file and replaces only the separate study outputs.
