import bpy
from pathlib import Path
from mathutils import Vector
P=Path(__file__).resolve().parent;M=P.parents[2]
bpy.ops.wm.open_mainfile(filepath=str(M/'quiet-collection-illustrated-museum.blend'))
with bpy.data.libraries.load(str(P/'abraham-facial-rig.blend'),link=False) as (src,dst):dst.collections=['Abraham | Hunyuan character']
s=bpy.context.scene;char=dst.collections[0];s.collection.children.link(char);rig=bpy.data.objects['Abraham_RIG'];mesh=next(o for o in char.objects if o.type=='MESH');shape=mesh.data.shape_keys
parent=bpy.data.objects.new('Abraham | placement',None);char.objects.link(parent);rig.parent=parent;parent.location=(.15,-6.1,.08);parent.scale=(.62,)*3;parent.rotation_euler.z=-.20
idle=rig.animation_data.action;rig.animation_data.action=None
track=rig.animation_data.nla_tracks.new();track.name='Museum idle';st=track.strips.new('Idle loop',1,idle);st.repeat=8
track=shape.animation_data.nla_tracks.new();track.name='Museum blinking';st=track.strips.new('Blink loop',1,bpy.data.actions['Face_Idle']);st.repeat=8
light=bpy.data.lights.new('Reception character light','AREA');o=bpy.data.objects.new(light.name,light);s.collection.objects.link(o);o.location=(0,-7.4,2.7);light.energy=70;light.shape='DISK';light.size=2;light.color=(1,.83,.64);o.rotation_euler=(Vector((.15,-6.1,.9))-o.location).to_track_quat('-Z','Y').to_euler()
d=bpy.data.cameras.new('09 | Expressive Abraham');cam=bpy.data.objects.new(d.name,d);s.collection.objects.link(cam);cam.location=(1.4,-8,1.5);cam.rotation_euler=(Vector((.1,-6.1,.85))-cam.location).to_track_quat('-Z','Y').to_euler();d.lens=35;s.camera=cam;s.frame_set(1)
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(M/'quiet-collection-with-abraham-facial.blend'))
# A face-focused movie, with each expression returning to neutral between clips.
bpy.ops.wm.open_mainfile(filepath=str(P/'abraham-facial-rig.blend'));s=bpy.context.scene;rig=bpy.data.objects['Abraham_RIG'];mesh=next(o for o in bpy.data.collections['Abraham | Hunyuan character'].objects if o.type=='MESH');shape=mesh.data.shape_keys
rig.animation_data.action=None
for t in rig.animation_data.nla_tracks:t.mute=True
shape.animation_data.action=None
for t in list(shape.animation_data.nla_tracks):shape.animation_data.nla_tracks.remove(t)
track=shape.animation_data.nla_tracks.new();track.name='Expression preview';start=1
for name in ['Face_Idle','Face_Curious','Face_Worried','Face_Delighted','Face_Blink']:
 st=track.strips.new(name,start,bpy.data.actions[name]);st.scale=.5;s.timeline_markers.new(name,frame=start);start=int(st.frame_end)
s.camera=bpy.data.objects['02-front'];s.camera.location=(0,-6,1.65);s.camera.rotation_euler=(Vector((0,-.1,1.43))-s.camera.location).to_track_quat('-Z','Y').to_euler();s.camera.data.ortho_scale=1.65
s.frame_start=1;s.frame_end=start-1;s.render.fps=12;s.render.engine='BLENDER_EEVEE'
if hasattr(s,'eevee') and hasattr(s.eevee,'taa_render_samples'):s.eevee.taa_render_samples=24
s.render.resolution_x=640;s.render.resolution_y=640;s.render.resolution_percentage=100;s.render.image_settings.media_type='VIDEO';s.render.image_settings.file_format='FFMPEG';s.render.ffmpeg.format='MPEG4';s.render.ffmpeg.codec='H264';s.render.ffmpeg.constant_rate_factor='MEDIUM';s.render.filepath=str(P/'abraham-facial-preview.mp4')
bpy.ops.wm.save_as_mainfile(filepath=str(P/'facial-preview.blend'));bpy.ops.render.render(animation=True)
print('FACIAL_PREVIEW_COMPLETE',flush=True)
