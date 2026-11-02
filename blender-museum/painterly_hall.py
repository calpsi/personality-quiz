"""Central-hall material study. Writes a separate .blend and comparison render."""
import bpy
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'quiet-collection-museum.blend'))
s=bpy.context.scene
for name in ['01 | Cutaway walls — enable for interiors','02 | Ceilings — enable for interiors']:
    bpy.data.collections[name].hide_render=False
    bpy.data.collections[name].hide_viewport=False
bpy.data.collections['07 | Overview studio fill'].hide_render=True
bpy.data.collections['07 | Overview studio fill'].hide_viewport=True

def paint(original):
    m=original.copy();m.name='Gouache | '+original.name
    nodes=m.node_tree.nodes;links=m.node_tree.links
    bs=next((n for n in nodes if n.type=='BSDF_PRINCIPLED'),None)
    if not bs:return m
    name=original.name
    if name=='Case glass':
        bs.inputs['Roughness'].default_value=.28
        bs.inputs['IOR'].default_value=1.04
        bs.inputs['Alpha'].default_value=.11
        return m
    if name=='Amber luminous glass':
        bs.inputs['Emission Strength'].default_value=1.5
        bs.inputs['Base Color'].default_value=(1,.64,.30,1)
        return m
    base=tuple(bs.inputs['Base Color'].default_value[:3])
    if name.startswith('Walnut'):base=(.23,.084,.043)
    elif name=='Espresso edges':base=(.075,.035,.043)
    elif name=='Moss green plaster':base=(.18,.215,.125)
    elif name=='Aged brass':base=(.49,.28,.095)
    elif name=='Oxblood velvet':base=(.24,.048,.045)
    elif name=='Midnight display lining':base=(.042,.065,.066)
    elif name.startswith('Floor plank'):base=(base[0]*1.2,base[1]*1.45,base[2]*1.65)
    for link in list(bs.inputs['Base Color'].links):links.remove(link)
    bs.inputs['Metallic'].default_value=.08 if name=='Aged brass' else 0
    bs.inputs['Roughness'].default_value=.88
    bs.inputs['Specular IOR Level'].default_value=.17
    coord=nodes.new('ShaderNodeTexCoord');coord.label='Object-bound paint, stable during movement'
    mapping=nodes.new('ShaderNodeVectorMath');mapping.operation='MULTIPLY'
    woody=any(word in name for word in ['Walnut','wood','Floor','Espresso'])
    mapping.inputs[1].default_value=(2,34,6) if name.startswith('Floor') else ((22,14,2) if woody else (4,3,7))
    links.new(coord.outputs['Generated'],mapping.inputs[0])
    noise=nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=3.2;noise.inputs['Detail'].default_value=2;noise.inputs['Roughness'].default_value=.65
    links.new(mapping.outputs['Vector'],noise.inputs['Vector'])
    ramp=nodes.new('ShaderNodeValToRGB');ramp.label='Four pigment values';ramp.color_ramp.interpolation='EASE'
    colors=[(.22,(base[0]*.48+.014,base[1]*.40+.007,base[2]*.55+.020)),(.43,tuple(v*.82 for v in base)),(.60,base),(.79,(min(base[0]*1.5+.045,1),min(base[1]*1.5+.032,1),min(base[2]*1.35+.018,1)))]
    cr=ramp.color_ramp
    cr.elements.remove(cr.elements[1]);cr.elements[0].position=colors[0][0];cr.elements[0].color=(*colors[0][1],1)
    for pos,col in colors[1:]:cr.elements.new(pos).color=(*col,1)
    links.new(noise.outputs['Fac'],ramp.inputs[0])
    # Broad overlapping pigment patches, separate from finer directional bristles.
    patch=nodes.new('ShaderNodeTexNoise');patch.inputs['Scale'].default_value=4;patch.inputs['Detail'].default_value=1
    links.new(coord.outputs['Generated'],patch.inputs['Vector'])
    patches=nodes.new('ShaderNodeValToRGB');patches.color_ramp.elements[0].color=(.40,.31,.40,1);patches.color_ramp.elements[1].color=(1,.94,.76,1)
    links.new(patch.outputs['Fac'],patches.inputs[0])
    mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=.34
    links.new(ramp.outputs['Color'],mix.inputs[1]);links.new(patches.outputs['Color'],mix.inputs[2]);links.new(mix.outputs[0],bs.inputs['Base Color'])
    bump=nodes.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.16;bump.inputs['Distance'].default_value=.018
    links.new(noise.outputs['Fac'],bump.inputs['Height']);links.new(bump.outputs['Normal'],bs.inputs['Normal'])
    m.diffuse_color=(*base,1)
    return m

copies={};count=0
for o in list(s.objects):
    if o.type not in {'MESH','CURVE'}:continue
    # The hall only: gallery props/materials remain original for this art-direction test.
    x,y,z=o.matrix_world.translation
    if not(-4.3<=x<=4.3 and -5.3<=y<=5.3):continue
    if 'plaque' in o.name.lower():continue
    for slot in o.material_slots:
        m=slot.material
        if not m:continue
        if m.name not in copies:copies[m.name]=paint(m)
        slot.link='OBJECT';slot.material=copies[m.name]
    count+=1

# Muted violet fill keeps shadows coloured while amber practical lamps remain dominant.
d=bpy.data.lights.new('Painterly | violet shadow fill','AREA');d.energy=85;d.color=(.49,.36,.64);d.shape='DISK';d.size=4
o=bpy.data.objects.new(d.name,d);s.collection.objects.link(o);o.location=(-2,1,2.9);o.rotation_euler=(Vector((0,0,0))-o.location).to_track_quat('-Z','Y').to_euler()
s.camera=bpy.data.objects['03 | Hall atmosphere'];s.frame_set(1)
s.render.engine='CYCLES';s.cycles.samples=64;s.cycles.use_denoising=True
s.render.resolution_x=1440;s.render.resolution_y=960;s.render.resolution_percentage=100
s.render.image_settings.media_type='IMAGE';s.render.image_settings.file_format='PNG'
s.view_settings.exposure=.05
s['Art direction']='Central hall gouache study: object-space pigment variation, directional brush marks, matte painted metals, muted glass. Galleries intentionally retain original materials.'
s['Study objects']=count
s.render.filepath=str(ROOT/'renders/05-painterly-hall.png')
bpy.ops.file.pack_all()
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'quiet-collection-painterly-study.blend'))
bpy.ops.render.render(write_still=True)
print('PAINTERLY_STUDY_COMPLETE',count,'objects',len(copies),'materials',flush=True)
