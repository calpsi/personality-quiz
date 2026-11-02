"""Render a 6 fps, 24-second lightweight reference movie; source .blend is not modified."""
import bpy
from pathlib import Path
ROOT=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'quiet-collection-museum.blend'))
s=bpy.context.scene
for name in ['01 | Cutaway walls — enable for interiors','02 | Ceilings — enable for interiors']:
    bpy.data.collections[name].hide_render=False
    bpy.data.collections[name].hide_viewport=False
bpy.data.collections['07 | Overview studio fill'].hide_render=True
original=bpy.data.objects['07 | Animated walkthrough']
from mathutils import Vector
for frame,loc,target in [(250,(-8.5,-4.1,1.75),(-10,-2.8,1.65)),(280,(-6,-.8,1.75),(-4,0,1.8))]:
    original.location=loc
    original.rotation_euler=(Vector(target)-original.location).to_track_quat('-Z','Y').to_euler()
    original.keyframe_insert(data_path='location',frame=frame)
    original.keyframe_insert(data_path='rotation_euler',frame=frame)
poses=[]
for i in range(144):
    s.frame_set(1+i*5)
    poses.append(original.matrix_world.copy())
data=original.data.copy();cam=bpy.data.objects.new('Reference video camera',data);s.collection.objects.link(cam)
for i,matrix in enumerate(poses):
    cam.matrix_world=matrix
    cam.keyframe_insert(data_path='location',frame=i+1)
    cam.keyframe_insert(data_path='rotation_euler',frame=i+1)
s.camera=cam;s.frame_start=1;s.frame_end=144;s.frame_set(1);s.render.fps=6
s.render.engine='BLENDER_EEVEE'
if hasattr(s,'eevee') and hasattr(s.eevee,'taa_render_samples'):s.eevee.taa_render_samples=16
for obj in s.objects:
    if any(m and m.name=='Case glass' for m in getattr(obj.data,'materials',[])):
        obj.hide_render=True
for lamp in bpy.data.lights:
    if lamp.type=='POINT':lamp.use_shadow=False
s.render.use_compositing=False
s.render.resolution_x=720;s.render.resolution_y=480;s.render.resolution_percentage=100
s.render.image_settings.media_type='VIDEO';s.render.image_settings.file_format='FFMPEG';s.render.ffmpeg.format='MPEG4';s.render.ffmpeg.codec='H264'
s.render.ffmpeg.constant_rate_factor='MEDIUM'
s.render.filepath=str(ROOT/'museum-walkthrough.mp4')
bpy.ops.render.render(animation=True)
print('WALKTHROUGH_COMPLETE',flush=True)
