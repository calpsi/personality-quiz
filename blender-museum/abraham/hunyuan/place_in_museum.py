import bpy
from pathlib import Path
from mathutils import Vector
P=Path(__file__).resolve().parent;M=P.parent.parent
bpy.ops.wm.open_mainfile(filepath=str(M/'quiet-collection-illustrated-museum.blend'))
with bpy.data.libraries.load(str(P/'abraham-hunyuan.blend'),link=False) as (src,dst):dst.collections=['Abraham | Hunyuan character']
s=bpy.context.scene;char=dst.collections[0];s.collection.children.link(char)
root=bpy.data.objects['Abraham_Hunyuan_ROOT']
placement=bpy.data.objects.new('Abraham | museum placement',None);char.objects.link(placement);root.parent=placement
placement.location=(.15,-6.1,.08);placement.scale=(.62,)*3;placement.rotation_euler.z=-.20
# Soft reception light leaves the imported texture and material setup intact.
d=bpy.data.lights.new('Reception character light','AREA');o=bpy.data.objects.new(d.name,d);s.collection.objects.link(o);o.location=(0,-7.4,2.7);d.energy=70;d.shape='DISK';d.size=2;d.color=(1,.83,.64);o.rotation_euler=(Vector((.15,-6.1,.9))-o.location).to_track_quat('-Z','Y').to_euler()
d=bpy.data.cameras.new('09 | Meet Abraham Hunyuan');cam=bpy.data.objects.new(d.name,d);s.collection.objects.link(cam);cam.location=(1.4,-8,1.5);cam.rotation_euler=(Vector((.1,-6.1,.85))-cam.location).to_track_quat('-Z','Y').to_euler();d.lens=35;s.camera=cam
s.frame_set(1);s.render.resolution_x=1200;s.render.resolution_y=900;s.render.resolution_percentage=100;s.render.image_settings.media_type='IMAGE';s.render.image_settings.file_format='PNG'
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(M/'quiet-collection-with-abraham-hunyuan.blend'))
s.render.filepath=str(P/'renders/04-in-museum.png');bpy.ops.render.render(write_still=True)
