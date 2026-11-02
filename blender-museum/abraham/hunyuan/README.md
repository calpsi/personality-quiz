# Abraham — user-supplied Hunyuan model

Source: `/Users/phillicia/Downloads/2b51e9ca8a55e2be744c6159977ebadd.glb`.

- `abraham-original.glb`: unmodified copy of the supplied file.
- `abraham-hunyuan.blend`: imported character, packed original textures, studio cameras and lighting. Placement is normalised to 2.1 units tall using a parent transform; source geometry and UVs are unchanged.
- `../../quiet-collection-with-abraham-hunyuan.blend`: separate illustrated museum copy using the Hunyuan character at reception, with a soft character light and a close camera.
- `renders/`: studio front, three-quarter, back and museum previews.
- `model-stats.json`: inspected geometry counts.
- `import_abraham.py` and `place_in_museum.py`: reproducible import and placement scripts.

The supplied asset contains one mesh, 50,000 triangles, one material and three embedded texture images (base color, normal, and packed metallic/roughness). It contains no armature or animation. Original material settings are retained. The museum instance is scaled to 62% of the normalised character height, about 1.30 metres tall for game visibility.

Earlier character versions and museum scenes remain unchanged. This version has no facial rig, walking animation or live AI integration. The character prompt remains at `../abraham-system-prompt.md`.
