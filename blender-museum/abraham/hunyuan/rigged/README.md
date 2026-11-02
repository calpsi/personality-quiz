# Abraham — Hunyuan animation rig

## Deliverables

- `abraham-rigged.blend`: editable character, 14-bone FK skeleton, skinned mesh, original packed textures, four actions and studio.
- `abraham-rigged.glb`: portable skinned character with four named animation clips and embedded PBR textures.
- `../../../quiet-collection-with-abraham-rigged.blend`: separate museum scene with repeating idle animation.
- `abraham-animation-preview.mp4`: Idle → Curious → Nod → Welcome, played in sequence.
- `animation-preview.blend`: the preview's sequenced NLA timeline.
- `renders/`: neutral and deformation pose checks.
- `rig-checks.json`: weight normalisation and pose stretch measurements.

## Animation clips

| Clip | Duration | Motion |
|---|---:|---|
| Idle | 4 s | Subtle breathing, head movement and ear movement |
| Curious | 3 s | Gentle head tilt with one ear adjustment |
| Nod | 2 s | Small acknowledging nod |
| Welcome | 3 s | Modest paw/arm greeting with a head tilt |

Clips begin and end at neutral for blending. Original action keys span frames 1–97, 1–73, 1–49 and 1–73 at 24 fps respectively; play through the frame before the duplicate endpoint when looping.

## Editing

Select `Abraham_RIG` and enter Pose Mode. `root` moves the complete character. `pelvis`, `chest` and `head` control the body. `.L`/`.R` identify paired ear, upper-arm, paw, leg and foot controls. These are forward-kinematics bones, not IK handles. The Action Editor selects the four named clips. The muted NLA tracks retain those clips without stacking them over the active action. Clear the active action before manually posing.

The generated source is a single fused mesh, including the cape and accessories. Skin weights are based on anatomical regions with blended transitions. This is suitable for the supplied small gestures; large arm raises, deep bends and walking need further weight refinement and potentially separation of the clothing. Feet and leg bones are provided for editing, but no walk cycle is included. No facial-expression rig, blink shape keys or lip sync is included: the eyes and mouth are part of the generated textured surface.

The museum copy has a separate placement parent and repeats Idle across its timeline. No AI endpoint was added. An application can map animation cues to the exported clip names later. The source GLB and unrigged Blender files are unchanged.

`rig_abraham.py` rebuilds the rig, exports the GLB and renders test poses. `preview_and_place.py` builds the museum copy and preview video. Rebuilding overwrites only these rigged deliverables.
