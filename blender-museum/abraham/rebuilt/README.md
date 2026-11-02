# Abraham — rounded rebuild

New geometry built from the user's Abraham character sheets. This is not an extraction or conversion of the Meshy model. The rejected version is preserved in the parent directory.

- `abraham-character.blend`: editable character, packed painted face texture, studio and four cameras.
- `abraham-character.glb`: portable character with embedded materials/texture and rigid idle animation.
- `../../quiet-collection-with-abraham-rebuilt.blend`: separate museum scene containing this version near the entrance.
- `renders/`: front, three-quarter, side, rear and museum previews.
- `model-stats.json`: evaluated triangle count.
- `face-paint.png`, `paint_face.py`: original UV face paint and reproducible texture source (Python + Pillow).
- `build_abraham.py`: reproducible Blender build, export and render source.

The rebuild replaces the overlapping muzzle with one continuous cheek-shaped head and UV-painted cream fur. Eyes have smaller dark silhouettes, tiny highlights and a gentle smile. Shorter body proportions, rounded ears, smoother clothing and softer accessories replace the earlier faceted treatment. It retains the olive cape, gold laurel details, flower clasp, burgundy ribbon, badge and satchel.

Faces -Y, Z up. `Abraham_ROOT` controls placement. `Abraham_body`, `Abraham_head`, and arm pivots form a rigid hierarchy. Frames 1–96 provide an idle bob/head tilt. This is not yet a skinned character with walking, lip sync or facial expression animation. Standard materials preserve the painted face in Blender and GLB; the museum's surrounding Shader-to-RGB materials remain Blender-specific. Further mesh merging/LOD work may be useful for mobile delivery.

The personality prompt remains at `../abraham-system-prompt.md`; no live API connection was added.

Rebuild from the project root with Blender's `--background --python blender-museum/abraham/rebuilt/build_abraham.py`. Rebuilding replaces files within this rebuild directory and the separate rebuilt museum scene. Preserve manual edits first.
