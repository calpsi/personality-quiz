# Abraham — museum administrator

Reference-led low-poly interpretation of the two supplied character sheets. No downloaded character model or generated bitmap is substituted for the editable 3D asset.

## Files
- `abraham-character.blend`: standalone editable character, studio cameras, neutral face, cape, badge, flower clasp, ribbon, satchel, and rigid controller hierarchy.
- `abraham-character.glb`: reusable mesh/material asset with exported idle animation.
- `../quiet-collection-with-abraham.blend`: separate copy of the illustrated museum with Abraham near the entrance desk and a “Meet Abraham” camera.
- `renders/`: three-quarter, front, side, back and in-museum views.
- `model-stats.json`: measured evaluated triangle count, not the reference image's illustrative 1,562-triangle claim.
- `abraham-system-prompt.md`: revised character prompt for later backend integration.

## Controls and scope

The character faces -Y; Z is up. Root height is approximately 2.4 model units. In the museum he is scaled to 62%, approximately 1.5 metres for visibility as a game companion. Scale `Abraham_ROOT` to change this.

Controllers: `Abraham_ROOT`, `Abraham_body`, `Abraham_head`, `Abraham_arm_L`, `Abraham_arm_R`. Parts are rigid-parented; there is no skinned armature. Frames 1–96 contain a four-second idle bob and head tilt. Arm controllers allow later simple poses.

The reference sheets' four facial expressions are not all implemented: this model has the neutral, slightly surprised face. Optional spectacles are omitted. Detailed facial deformation, lip sync, walking, and final mobile optimisation remain later work. The model uses separate meshes and curves for editability; see measured complexity rather than assuming the reference triangle target.

Standalone materials are conventional matte PBR materials for GLB portability. The museum copy receives Eevee palette shading to match its surroundings. The museum's Toon Shader-to-RGB materials are not automatically portable to a web engine.

## Prompt revisions

- Keeps Abraham's earnest, inquisitive, slightly anxious character and concise voice.
- Explicitly acknowledges the personality quiz, resolving the original prohibition on mentioning its mechanics.
- Allows a playful specimen match while forbidding literal cataloguing of the visitor.
- Keeps deterministic result selection authoritative; the model explains the supplied result only.
- Uses one optional reflection exchange, no repeated follow-up questions.
- Requires real evidence IDs and a graceful host fallback for insufficient context.
- Allows truthful disclosure when directly asked whether Abraham is AI-powered.
- Separates character text from a small allowlist of animation cues supported by the current model.
- Limits scientific claims to supplied museum facts.

## Later API integration

No API key was read, created, stored, or used for this deliverable. No live API endpoint has been implemented. This is a character asset and prompt-writing task.

When connecting Abraham, the backend should validate exact resultId/title, real distinct evidence IDs, lengths, and animation allowlists. Render strings as text. Keep credentials server-side; retain a complete local result and authored dialogue when generation fails. Never put the model in charge of scoring, navigation permissions, or scene execution.

Suggested authored welcome: “Welcome to the Quiet Collection. I'm Abraham, the administrator. This is a personality quiz with a little room to wander—eight stops, then we'll find your specimen match.”

Suggested reflection skip: “Of course. We can keep going.”

Suggested technical fallback: “I'll use the notes we already have. Your visit can carry on.”

Rebuild with Blender `--background --python blender-museum/abraham/build_abraham.py`. Existing outputs with the same names are replaced; preserve manual edits before rebuilding.
