"""Extend the approved illustration style, refine typography, animate the reveal title."""
import bpy, math, random
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parent

# Reuse the approved study's authored palette and strokes with full-museum scope.
source=(ROOT/'illustrated_hall.py').read_text().split("s.render.engine='BLENDER_EEVEE'")[0]
source=source.replace("return -4.3<=x<=4.3 and -5.3<=y<=5.3", "return o.name != 'Diorama ground'")
source=source.replace("08 | Illustrated hall — ink and brush marks", "08 | Museum illustration — ink and brush marks")
source=source.replace("base=tuple(original.diffuse_color[:3])", "base=tuple(original.diffuse_color[:3])\n    if original.use_nodes:\n        shader=original.node_tree.nodes.get('Principled BSDF')\n        if shader:base=tuple(shader.inputs['Base Color'].default_value[:3])")
source=source.replace("'lantern base'])", "'lantern base','front raised panel','botanical frame','trace frame'])")
source=source.replace("if 'pane' in o.name.lower():o.hide_render=True", "if o.name.startswith('Frosted reveal pane'):o.hide_render=True")
exec(compile(source,str(ROOT/'illustrated_hall.py'),'exec'))

# Curved specimen geometry receives the same palette treatment as mesh props.
for obj in list(s.objects):
    if obj.type=='CURVE' and not obj.name.startswith(('Broken hand','Selective painted')):
        for slot in obj.material_slots:
            original=slot.material
            if original and not original.name.startswith('Illustration |'):
                slot.link='OBJECT';slot.material=illustrated(original)
    if obj.type=='MESH' and any('glass' in slot.material.name.lower() for slot in obj.material_slots if slot.material):
        obj.hide_render=True;obj.hide_viewport=True

font=bpy.data.fonts.load(str(ROOT/'assets/fonts/CormorantGaramond-Variable.ttf'))
gold=emission('Typography | antique ivory',(.88,.67,.36))
labelink=emission('Typography | label ink',(.055,.023,.025))
for obj in list(s.objects):
    if obj.type!='FONT':continue
    obj.data=obj.data.copy();obj.data.font=font
    obj.data.extrude=.0008;obj.data.bevel_depth=0
    body=obj.data.body
    if body=='YOUR EXHIBIT':
        bpy.data.objects.remove(obj,do_unlink=True);continue
    if '/' in body:
        number,title=body.split('/',1)
        obj.data.body=number.strip()+'  ·  '+title.strip().title()
        obj.data.size=.105;obj.data.space_character=1.02
        obj.data.materials.clear();obj.data.materials.append(labelink)
        obj.location.z-=.006
        limit=1.44
    else:
        obj.data.size=.235;obj.data.space_character=1.15
        obj.data.materials.clear();obj.data.materials.append(gold)
        limit=2.42 if body!='NATURAL HISTORY' else 4.0
    # Fit the actual font outline inside each existing plaque.
    bpy.context.view_layer.update()
    if obj.dimensions.x>limit:obj.scale.x*=limit/obj.dimensions.x

titlecollection=bpy.data.collections.new('09 | WHAT ARE YOU — floating title');s.collection.children.link(titlecollection)
amber=emission('Title | warm ivory',(1,.77,.43))
teal=emission('Title glitch | muted teal',(.27,.73,.67))
coral=emission('Title glitch | faded coral',(.88,.29,.22))
def title_object(name,material):
    data=bpy.data.curves.new(name,'FONT');data.body='WHAT ARE YOU?';data.font=font;data.size=.28
    data.space_character=1.12;data.align_x='CENTER';data.align_y='CENTER';data.extrude=.0008
    obj=bpy.data.objects.new(name,data);titlecollection.objects.link(obj);obj.rotation_euler=(math.pi/2,0,-.14)
    data.materials.append(material);return obj
main=title_object('WHAT ARE YOU? | always-readable main title',amber)
ghost1=title_object('WHAT ARE YOU? | teal ghost',teal)
ghost2=title_object('WHAT ARE YOU? | coral ghost',coral)

# A six-second loop repeated across the original thirty-second walkthrough.
# Sparse short offsets; the main lettering never disappears.
burst={50,51,52,54,55,103,104,106}
for frame in range(1,721):
    phase=(frame-1)%144+1
    bob=.038*math.sin((phase-1)*math.tau/144)
    active=phase in burst
    jitter=({50:-.028,51:.045,52:-.014,54:.035,55:0,103:.045,104:-.035,106:.018}.get(phase,0))
    for obj,offset in [(main,0),(ghost1,1),(ghost2,-1)]:
        obj.location=(jitter+offset*(.028 if active else .012),-1.00+abs(offset)*.009,3.01+bob+offset*(.008 if active else 0))
        if frame==1 or frame%4==1 or active or phase-1 in burst or phase+1 in burst or frame==720:
            obj.keyframe_insert(data_path='location',frame=frame)
        if offset:
            obj.hide_render=not active;obj.hide_viewport=not active
            obj.keyframe_insert(data_path='hide_render',frame=frame)
            obj.keyframe_insert(data_path='hide_viewport',frame=frame)
main['Animation']='6-second float loop with short chromatic-offset bursts; main title stays visible. Frames 1–720 at 24fps.'
main['Reduced motion']='Mute title actions and hide the two ghost objects for a static title.'

# Short horizontal fragments reinforce the sliced glitch effect, using title-local coordinates.
for index,(xx,zz,width) in enumerate([(-.65,.07,.32),(.51,-.035,.25),(.13,.12,.17)]):
    mesh=bpy.data.meshes.new('Glitch fragment mesh')
    mesh.from_pydata([(-width/2,0,-.003),(width/2,0,-.003),(width/2,0,.003),(-width/2,0,.003)],[],[(0,1,2,3)])
    obj=bpy.data.objects.new('Glitch fragment '+str(index+1),mesh);titlecollection.objects.link(obj);mesh.materials.append(teal if index%2 else coral)
    obj.location=(xx,-1.02,3.01+zz)
    for frame in range(1,721):
        phase=(frame-1)%144+1;obj.hide_render=phase not in burst;obj.hide_viewport=phase not in burst
        obj.keyframe_insert(data_path='hide_render',frame=frame);obj.keyframe_insert(data_path='hide_viewport',frame=frame)

# Move the central pendant back so it does not compete with the floating lettering.
for obj in s.objects:
    if obj.name.startswith('Pendant') and abs(obj.location.x)<.01 and abs(obj.location.y)<.01:
        obj.location.y+=2.4

# A fixed close view makes the hover/glitch easy to review without camera motion.
d=bpy.data.cameras.new('08 | Floating title close view');cam=bpy.data.objects.new(d.name,d);bpy.data.collections['06 | Cameras and navigation'].objects.link(cam)
cam.location=(-1.7,-4.4,2.8);cam.rotation_euler=(Vector((0,-.7,2.45))-cam.location).to_track_quat('-Z','Y').to_euler();d.lens=32
s.render.engine='BLENDER_EEVEE'
if hasattr(s.eevee,'taa_render_samples'):s.eevee.taa_render_samples=96
s.render.resolution_x=1440;s.render.resolution_y=960;s.render.resolution_percentage=100
s.render.image_settings.media_type='IMAGE';s.render.image_settings.file_format='PNG'
s.render.use_compositing=False;s.view_settings.view_transform='Standard';s.view_settings.look='None';s.view_settings.exposure=0
s.camera=bpy.data.objects['03 | Hall atmosphere'];s.frame_set(1)
s['Art direction']='Approved illustrated treatment extended throughout museum. Cormorant Garamond typography; floating WHAT ARE YOU? title. Render with Eevee.'
s['Typography']='Cormorant Garamond, The Cormorant Project Authors, SIL OFL. Source and licence in assets/fonts.'
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'quiet-collection-illustrated-museum.blend'))
for camera,filename,frame in [
    ('03 | Hall atmosphere','08-illustrated-hall-final.png',1),
    ('04 | Deep Time','09-illustrated-deep-time.png',1),
    ('05 | Earth and Space','10-illustrated-earth-space.png',1),
    ('06 | Living Systems','11-illustrated-living-systems.png',1),
    ('08 | Floating title close view','12-floating-title-glitch.png',51)]:
    s.camera=bpy.data.objects[camera];s.frame_set(frame);s.render.filepath=str(ROOT/'renders'/filename)
    bpy.ops.render.render(write_still=True)
print('FULL_ILLUSTRATED_MUSEUM_COMPLETE',flush=True)
