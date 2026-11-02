# Abraham — animated facial expressions

This extends the Hunyuan body rig with six facial morph controls. The original GLB, unrigged scene and earlier body-rig files are preserved.

## Files

- `abraham-facial-rig.blend`: editable body skeleton and facial shape keys, original packed textures, animation actions and studio.
- `abraham-facial-rig.glb`: skinned character with six named morph targets and nine animation clips.
- `abraham-facial-preview.mp4`: face-focused expression demonstration.
- `facial-preview.blend`: the demonstration timeline.
- `../../../quiet-collection-with-abraham-facial.blend`: museum copy with body idle and periodic blinking.
- `renders/expression-sheet.png`: expression comparison.

## Facial controls

Select the character mesh, open Object Data Properties → Shape Keys, and set expression values to 0 (off) or 1 (on):

- All zero: original neutral face.
- `Blink_L`, `Blink_R`: independent eye closure.
- `Curious`: asymmetric eye lift and small mouth adjustment.
- `Worried`: concerned eye angles and a small downturned mouth.
- `Delighted`: closed smiling eyes and an open smile with a tongue.
- `Mouth_Open`: a simple opening control, not a phoneme or lip-sync system.

Use one main expression at a time, switching through neutral. The supplied face clips use stepped keys: slow interpolation reveals the fused original eyes beneath the closing overlays. Avoid crossfading the face clips; body clips can still blend normally. Avoid adding full blink values on top of Delighted, which already closes the eyes. The mouth/eyelid controls are designed for the supplied expressions, not unrestricted face sculpting.

The Hunyuan eyes and mouth were fused into the textured head. Expression changes therefore combine subtle eye deformations with small skinned eyelid and mouth surfaces. These are cartoon expression changes, not continuous anatomical eyelid deformation. The closed-eye covers use a fur atlas sampled from the surrounding texture. The added shapes are hidden beneath the face in neutral. They are stylized surface expressions, rather than a fully retopologised facial rig; close-up inspection can reveal the eyelid and muzzle patches. They share the head bone and export as morph targets; they do not depend on Blender drivers or texture switching.

## Animation clips

Body clips retained: `Idle` (4 s), `Curious` (3 s), `Nod` (2 s), `Welcome` (3 s).

Face clips: `Face_Idle` (4 s, periodic blink), `Face_Curious` (3 s), `Face_Worried` (3 s), `Face_Delighted` (3 s), `Face_Blink` (1 s). Body and face clips target different properties and can play together. The face clips start/end neutral. Names beginning `Face_` animate morph weights; the others animate bones.

In Blender, the shape-key datablock owns the face actions; the armature owns body actions. Clear their active action and mute NLA playback before manually testing values. The museum copy has separate body-idle and blink NLA tracks.

No live API connection, automatic expression classification, audio lip sync or walking cycle is added. Existing personality instructions remain in `../../abraham-system-prompt.md`.

Export verification: the GLB was re-imported into Blender and all five facial clips were checked for active morph weights. The 14-joint skeleton and four body clips are retained. See `export-checks.json`.
