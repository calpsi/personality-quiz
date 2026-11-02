import bpy,json,struct,math
from pathlib import Path
P=Path(__file__).resolve().parent
b=(P/'abraham-facial-rig.glb').read_bytes();n,t=struct.unpack_from('<II',b,12);g=json.loads(b[20:20+n]);names={a['name'] for a in g['animations']};expected={'Idle','Curious','Nod','Welcome','Face_Idle','Face_Blink','Face_Curious','Face_Worried','Face_Delighted'};assert names==expected,names
assert len(g['skins'][0]['joints'])==14
assert len(g['meshes'][0]['extras']['targetNames'])==6
assert all('bufferView' in i for i in g['images'])
bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(P/'abraham-facial-rig.glb'))
meshes=[o for o in bpy.context.scene.objects if o.type=='MESH'];m=next(o for o in meshes if o.data.shape_keys);sk=m.data.shape_keys
for tr in sk.animation_data.nla_tracks:tr.mute=True
check={}
for action in bpy.data.actions:
 if not action.name.startswith('Face_'):continue
 sk.animation_data.action=action
 frame=44 if action.name=='Face_Idle' else 11 if action.name=='Face_Blink' else 36
 bpy.context.scene.frame_set(frame);bpy.context.view_layer.update();values={k.name:float(k.value) for k in sk.key_blocks if k.name!='Basis'};assert max(values.values())>.9,(action.name,values);check[action.name]=values
(P/'export-checks.json').write_text(json.dumps({'skin_joints':14,'morph_targets':g['meshes'][0]['extras']['targetNames'],'clips':sorted(names),'embedded_images':len(g['images']),'roundtrip_face_weights':check},indent=2))
print('FACE_GLB_ROUNDTRIP_VERIFIED',flush=True)
