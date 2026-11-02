import bpy
from pathlib import Path
from mathutils import Vector
P=Path(__file__).resolve().parent;M=P.parents[2]
bpy.ops.wm.open_mainfile(filepath=str(M/'quiet-collection-illustrated-museum.blend'))
with bpy.data.libraries.load(str(P/'abraham-rigged.blend'),link=False) as (src,dst):dst.collections=['Abraham | Hunyuan character']
s=bpy.context.scene;char=dst.collections[0];s.collection.children.link(char);rig=bpy.data.objects['Abraham_RIG']
placement=bpy.data.objects.new('Abraham | placement',None);char.objects.link(placement);rig.parent=placement;placement.location=(.15,-6.1,.08);placement.scale=(.62,)*3;placement.rotation_euler.z=-.20
idle=rig.animation_data.action;rig.animation_data.action=None
track=rig.animation_data.nla_tracks.new();track.name='Museum idle loop';strip=track.strips.new('Idle loop',1,idle);strip.repeat=8
light=bpy.data.lights.new('Reception character light','AREA');o=bpy.data.objects.new(light.name,light);s.collection.objects.link(o);o.location=(0,-7.4,2.7);light.energy=70;light.shape='DISK';light.size=2;light.color=(1,.83,.64);o.rotation_euler=(Vector((.15,-6.1,.9))-o.location).to_track_quat('-Z','Y').to_euler()
d=bpy.data.cameras.new('09 | Rigged Abraham');cam=bpy.data.objects.new(d.name,d);s.collection.objects.link(cam);cam.location=(1.4,-8,1.5);cam.rotation_euler=(Vector((.1,-6.1,.85))-cam.location).to_track_quat('-Z','Y').to_euler();d.lens=35;s.camera=cam;s.frame_set(1)
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(M/'quiet-collection-with-abraham-rigged.blend'))
# Build a separate preview timeline with the four clips played in sequence at original speed.
bpy.ops.wm.open_mainfile(filepath=str(P/'abraham-rigged.blend'));s=bpy.context.scene;rig=bpy.data.objects['Abraham_RIG'];rig.animation_data.action=None
for track in list(rig.animation_data.nla_tracks):rig.animation_data.nla_tracks.remove(track)
track=rig.animation_data.nla_tracks.new();track.name='Preview sequence';start=1
for name in ['Idle','Curious','Nod','Welcome']:
 action=bpy.data.actions[name];strip=track.strips.new(name,start,action);strip.scale=.5;s.timeline_markers.new(name,frame=start);start=int(strip.frame_end)
s.frame_start=1;s.frame_end=start-1;s.render.fps=12;s.camera=bpy.data.objects['01-three-quarter'];s.render.engine='BLENDER_EEVEE'
if hasattr(s,'eevee') and hasattr(s.eevee,'taa_render_samples'):s.eevee.taa_render_samples=16
s.render.resolution_x=560;s.render.resolution_y=560;s.render.resolution_percentage=100
s.render.image_settings.media_type='VIDEO';s.render.image_settings.file_format='FFMPEG';s.render.ffmpeg.format='MPEG4';s.render.ffmpeg.codec='H264';s.render.ffmpeg.constant_rate_factor='MEDIUM';s.render.filepath=str(P/'abraham-animation-preview.mp4')
bpy.ops.wm.save_as_mainfile(filepath=str(P/'animation-preview.blend'));bpy.ops.render.render(animation=True)
print('PREVIEW_AND_MUSEUM_COMPLETE',flush=True)
