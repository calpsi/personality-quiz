# Illustrated hall study

Reference: Exnioc, *How to make this Stylized Painterly Environment in Blender — Hand Painting Tutorial Part One*: https://www.youtube.com/watch?v=2-2fnzKUcwY

The reference's opening artwork and description informed this revision: simplified shapes, clear colour blocking, drawn outlines and intentional paint marks. No video images or creator assets were copied into the scene.

Open `quiet-collection-illustrated-study.blend`. Use **Eevee**, as the new hall materials use Shader to RGB and a palette ramp to make discrete lighting shapes. Cycles will not reproduce these shaders correctly.

This separate study retains the original hall camera and layout. It adds:

- Graphic shadow/midtone/highlight palettes.
- Thin, deliberately broken brown edge strokes, modelled in 3D.
- Flat irregular wall daubs, wood pigment strokes, and drawn wear marks.
- Slightly imperfect cabinet/panel geometry.
- Painted rather than metallic brass, with restrained surface variation.
- Simplified glass suggested by the frame and drawn glints.

The other galleries retain their original materials. The fully built museum and previous painterly study remain untouched.

Output: `renders/07-illustrated-hall.png`. Rebuild script: `illustrated_hall.py`.

The strokes and palette materials are generated artwork, not manually brush-painted textures. A later web implementation will need a compatible toon shader or baked material treatment. This is an art-direction study, not a finished mobile export.
