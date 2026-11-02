import bpy,math,json
from pathlib import Path
from mathutils import Vector,Quaternion,Matrix
P=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(P.parent/'abraham-hunyuan.blend'))
s=bpy.context.scene;coll=bpy.data.collections['Abraham | Hunyuan character'];mesh=next(o for o in coll.objects if o.type=='MESH')
# Bake the import transform into the working mesh only, preserving original source file.
bpy.context.view_layer.update();world=mesh.matrix_world.copy();mesh.parent=None;mesh.matrix_world=Matrix.Identity(4);mesh.data.transform(world)
for o in list(coll.objects):
 if o.type=='EMPTY':bpy.data.objects.remove(o,do_unlink=True)
arm=bpy.data.armatures.new('Abraham skeleton');rig=bpy.data.objects.new('Abraham_RIG',arm);coll.objects.link(rig);rig.show_in_front=True;arm.display_type='OCTAHEDRAL'
bpy.context.view_layer.objects.active=rig;rig.select_set(True);bpy.ops.object.mode_set(mode='EDIT')
def bone(name,h,t,parent=None,deform=True):
 b=arm.edit_bones.new(name);b.head=h;b.tail=t;b.use_deform=deform
 if parent:b.parent=arm.edit_bones[parent]
 return b
bone('root',(0,0,0),(0,0,.18),deform=False)
bone('pelvis',(0,0,.28),(0,0,.52),'root');bone('chest',(0,0,.52),(0,0,.91),'pelvis');bone('head',(0,0,.98),(0,0,1.64),'chest')
for side,sign in [('L',1),('R',-1)]:
 bone('ear.'+side,(sign*.42,.04,1.73),(sign*.50,.04,2.02),'head')
 bone('upper_arm.'+side,(sign*.39,0,.87),(sign*.55,-.01,.65),'chest')
 bone('paw.'+side,(sign*.55,-.01,.65),(sign*.61,-.05,.49),'upper_arm.'+side)
 bone('leg.'+side,(sign*.23,0,.34),(sign*.24,0,.16),'pelvis')
 bone('foot.'+side,(sign*.24,0,.16),(sign*.24,-.20,.09),'leg.'+side)
bpy.ops.object.mode_set(mode='OBJECT')
for b in rig.pose.bones:b.rotation_mode='QUATERNION'
for b in arm.bones:
 if b.use_deform:mesh.vertex_groups.new(name=b.name)
def smooth(a,b,x):
 t=max(0,min(1,(x-a)/(b-a)));return t*t*(3-2*t)
for v in mesh.data.vertices:
 x,y,z=v.co;side='L' if x>0 else 'R';a=abs(x);w={}
 if z>1.06:
  e=smooth(1.73,1.89,z)*smooth(.28,.43,a)
  w={'head':1-e,'ear.'+side:e}
 elif z>.91:
  h=smooth(.91,1.06,z);w={'head':h,'chest':1-h}
 elif z<.32:
  leg=1-smooth(.23,.32,z);foot=1-smooth(.13,.20,z)
  w={'pelvis':1-leg,'leg.'+side:leg*(1-foot),'foot.'+side:leg*foot}
 else:
  # Limit arm influence to outer sleeves/paws; central cape, clasp and bag follow torso.
  aweight=smooth(.47,.62,a)*(1-smooth(.81,.94,z))*smooth(.35,.47,z)
  paw=1-smooth(.53,.67,z)
  torso=smooth(.35,.58,z)
  w={'chest':(1-aweight)*torso,'pelvis':(1-aweight)*(1-torso),'upper_arm.'+side:aweight*(1-paw),'paw.'+side:aweight*paw}
 for n,val in w.items():
  if val>0:mesh.vertex_groups[n].add([v.index],val,'REPLACE')
mesh.parent=rig;mod=mesh.modifiers.new('Abraham skin deformation','ARMATURE');mod.object=rig;mod.use_deform_preserve_volume=True
# Each clip begins and ends at the neutral pose, so app transitions remain predictable.
rig.animation_data_create()
def reset():
 for b in rig.pose.bones:b.location=(0,0,0);b.rotation_quaternion=(1,0,0,0);b.scale=(1,1,1)
def rotate(name,axis,angle):
 pb=rig.pose.bones[name];q=pb.bone.matrix_local.to_quaternion();pb.rotation_quaternion=q.inverted()@Quaternion(Vector(axis),angle)@q
clips={}
for name,length in [('Idle',96),('Curious',72),('Nod',48),('Welcome',72)]:
 action=bpy.data.actions.new(name);rig.animation_data.action=action
 for f in range(1,length+2,3):
  t=(f-1)/length;reset();wave=math.sin(math.pi*t)**2
  if name=='Idle':
   rig.pose.bones['chest'].location.y=.009*wave
   rotate('head',(0,1,0),.025*math.sin(math.tau*t));rotate('ear.L',(0,1,0),.025*math.sin(math.tau*t))
  elif name=='Curious':
   rotate('head',(0,1,0),.14*wave)
   rotate('ear.R',(0,1,0),-.07*wave)
  elif name=='Nod':rotate('head',(1,0,0),.10*math.sin(4*math.pi*t)*wave)
  elif name=='Welcome':
   rotate('upper_arm.R',(0,1,0),.35*wave);rotate('paw.R',(0,1,0),-.08*math.sin(6*math.pi*t)*wave)
   rotate('head',(0,1,0),-.07*wave)
  for pb in rig.pose.bones:
   pb.keyframe_insert(data_path='location',frame=f,group=pb.name);pb.keyframe_insert(data_path='rotation_quaternion',frame=f,group=pb.name)
 action.use_fake_user=True;clips[name]=action
# Expose one independent NLA track per clip for glTF export; mute in Blender by default.
rig.animation_data.action=None
for name,action in clips.items():
 track=rig.animation_data.nla_tracks.new();track.name=name;strip=track.strips.new(name,1,action);track.mute=True
rig.animation_data.action=clips['Idle'];s.frame_start=1;s.frame_end=96;s.render.fps=24;s.frame_set(1)
# Validate every vertex has finite normalised skin weights.
sums=[sum(g.weight for g in v.groups) for v in mesh.data.vertices]
assert all(math.isfinite(v) and abs(v-1)<1e-5 for v in sums)
# Evaluate maximum edge stretch at meaningful gesture poses.
rest=[v.co.copy() for v in mesh.data.vertices];report={}
for name,frame in [('Curious',37),('Nod',16),('Welcome',37)]:
 rig.animation_data.action=clips[name];s.frame_set(frame);deps=bpy.context.evaluated_depsgraph_get();ev=mesh.evaluated_get(deps);m=ev.to_mesh();ratios=[]
 for e in mesh.data.edges:
  a,b=e.vertices;d=(rest[a]-rest[b]).length
  if d>.0001:ratios.append((m.vertices[a].co-m.vertices[b].co).length/d)
 ratios.sort();report[name]={'edge_stretch_p99':ratios[int(len(ratios)*.99)],'max_edge_stretch':max(ratios)};ev.to_mesh_clear()
(P/'rig-checks.json').write_text(json.dumps({'bones':len(arm.bones),'weighted_vertices':len(sums),'max_weight_error':max(abs(v-1) for v in sums),'pose_checks':report,'clips':list(clips)},indent=2))
rig.animation_data.action=clips['Idle'];s.frame_set(1);s.camera=bpy.data.objects['01-three-quarter']
bpy.ops.object.select_all(action='DESELECT');rig.select_set(True);mesh.select_set(True);bpy.context.view_layer.objects.active=rig
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(P/'abraham-rigged.blend'))
# Export named actions as separate clips. Keep original PBR materials and textures.
bpy.ops.export_scene.gltf(filepath=str(P/'abraham-rigged.glb'),export_format='GLB',use_selection=True,export_animations=True,export_animation_mode='ACTIONS',export_skins=True,export_force_sampling=True)
for name,f in [('Idle',1),('Curious',37),('Welcome',37)]:
 rig.animation_data.action=clips[name];s.frame_set(f);s.render.filepath=str(P/'renders'/f'{name.lower()}.png');bpy.ops.render.render(write_still=True)
print('RIG_COMPLETE',flush=True)
