"""Illustrated hall revision: graphic shading, drawn edges, authored paint marks."""
import bpy, math, random
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parent
random.seed(58)
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'quiet-collection-museum.blend'))
s=bpy.context.scene
for name in ['01 | Cutaway walls — enable for interiors','02 | Ceilings — enable for interiors']:
    bpy.data.collections[name].hide_render=False;bpy.data.collections[name].hide_viewport=False
bpy.data.collections['07 | Overview studio fill'].hide_render=True
bpy.data.collections['07 | Overview studio fill'].hide_viewport=True
s.frame_set(1);bpy.context.view_layer.update()
marks=bpy.data.collections.new('08 | Illustrated hall — ink and brush marks');s.collection.children.link(marks)

def emission(name,color):
    m=bpy.data.materials.new(name);m.use_nodes=True;n=m.node_tree.nodes;n.clear()
    e=n.new('ShaderNodeEmission');e.inputs['Color'].default_value=(*color,1)
    out=n.new('ShaderNodeOutputMaterial');m.node_tree.links.new(e.outputs[0],out.inputs['Surface']);m.diffuse_color=(*color,1);return m
ink=emission('Illustration | warm ink',(.035,.018,.026))
edge=emission('Illustration | ochre edge paint',(.47,.24,.09))
wallpaint=[emission('Illustration | wall daub '+str(i),c) for i,c in enumerate([(.20,.235,.12),(.14,.17,.085),(.23,.24,.135)])]
paintwood=[emission('Illustration | wood stroke '+str(i),c) for i,c in enumerate([(.32,.115,.045),(.20,.064,.035),(.42,.18,.07)])]
copies={}
def illustrated(original):
    name=original.name
    if name in copies:return copies[name]
    if name=='Case glass':
        m=original.copy();m.name='Illustration | simplified glass'
        bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Alpha'].default_value=.025;bs.inputs['Roughness'].default_value=.5
        copies[name]=m;return m
    if name=='Amber luminous glass':m=emission('Illustration | warm lamp',(1,.65,.25));copies[name]=m;return m
    base=tuple(original.diffuse_color[:3])
    if name.startswith('Walnut'):base=(.39,.15,.065)
    elif name=='Espresso edges':base=(.12,.045,.03)
    elif name=='Honey wood highlights':base=(.54,.28,.10)
    elif name=='Aged brass':base=(.68,.40,.15)
    elif name=='Moss green plaster':base=(.28,.33,.17)
    elif name=='Petrol blue gallery':base=(.13,.24,.24)
    elif name=='Oxblood velvet':base=(.40,.085,.085)
    elif name=='Midnight display lining':base=(.09,.12,.14)
    elif name.startswith('Floor plank'):base=(.32+random.random()*.065,.13+random.random()*.025,.065)
    elif name=='Cream labels':base=(.73,.57,.34)
    m=bpy.data.materials.new('Illustration | '+name);m.use_nodes=True;m.diffuse_color=(*base,1)
    n=m.node_tree.nodes;n.clear();lk=m.node_tree.links
    diff=n.new('ShaderNodeBsdfDiffuse');diff.inputs['Color'].default_value=(.8,.8,.8,1);diff.inputs['Roughness'].default_value=1
    rgb=n.new('ShaderNodeShaderToRGB');lk.new(diff.outputs[0],rgb.inputs[0]);bw=n.new('ShaderNodeRGBToBW');lk.new(rgb.outputs[0],bw.inputs[0])
    ramp=n.new('ShaderNodeValToRGB');ramp.label='Illustrated shadow, midtone and light';ramp.color_ramp.interpolation='CONSTANT'
    cols=[(0,(base[0]*.20+.006,base[1]*.14+.004,base[2]*.22+.013)),(.12,tuple(c*.55 for c in base)),(.33,base),(.75,(min(base[0]*1.25+.06,1),min(base[1]*1.20+.045,1),min(base[2]*1.08+.02,1)))]
    cr=ramp.color_ramp;cr.elements.remove(cr.elements[1]);cr.elements[0].color=(*cols[0][1],1)
    for p,c in cols[1:]:cr.elements.new(p).color=(*c,1)
    lk.new(bw.outputs[0],ramp.inputs[0])
    # Quiet surface variation only; the drawn marks carry the painted character.
    coord=n.new('ShaderNodeTexCoord');noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=7;noise.inputs['Detail'].default_value=1
    lk.new(coord.outputs['Generated'],noise.inputs['Vector'])
    pigment=n.new('ShaderNodeValToRGB');pigment.color_ramp.elements[0].color=(.72,.65,.70,1);pigment.color_ramp.elements[1].color=(1,1,.94,1);lk.new(noise.outputs['Fac'],pigment.inputs[0])
    mix=n.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=.12;lk.new(ramp.outputs[0],mix.inputs[1]);lk.new(pigment.outputs[0],mix.inputs[2])
    e=n.new('ShaderNodeEmission');lk.new(mix.outputs[0],e.inputs[0]);out=n.new('ShaderNodeOutputMaterial');lk.new(e.outputs[0],out.inputs[0])
    copies[name]=m;return m

def inhall(o):
    x,y,z=o.matrix_world.translation
    return -4.3<=x<=4.3 and -5.3<=y<=5.3

selected=[o for o in s.objects if o.type=='MESH' and inhall(o)]
for o in selected:
    for slot in o.material_slots:
        original=slot.material
        if original:slot.link='OBJECT';slot.material=illustrated(original)
    # Slightly imperfect large joinery, preserving circulation and connections.
    if any(t in o.name for t in ['walnut cabinet','Raised panel','Panel inset','reveal canopy','Reveal canopy']):
        o.data=o.data.copy()
        for v in o.data.vertices:
            v.co.x+=random.uniform(-.012,.012);v.co.z+=random.uniform(-.009,.009)

def stroke_object(name,material,radius):
    d=bpy.data.curves.new(name,'CURVE');d.dimensions='3D';d.bevel_depth=radius;d.bevel_resolution=0
    o=bpy.data.objects.new(name,d);marks.objects.link(o);d.materials.append(material);return d
lines=stroke_object('Broken hand-drawn edge lines',ink,.006)
highlights=stroke_object('Selective painted edge accents',edge,.009)
def stroke(data,pts):
    spl=data.splines.new('POLY');spl.points.add(len(pts)-1)
    for p,co in zip(spl.points,pts):p.co=(*co,1)

for o in selected:
    name=o.name.lower()
    chosen=any(k in name for k in ['raised panel','panel inset','jamb','reveal walnut','reveal canopy','reveal plinth','carpet gold','bench velvet','lantern crown','lantern base'])
    if 'floorboard' in name:chosen=random.random()<.12
    if not chosen:continue
    for e in o.data.edges:
        a=o.matrix_world@o.data.vertices[e.vertices[0]].co;b=o.matrix_world@o.data.vertices[e.vertices[1]].co
        if (b-a).length<.18 or random.random()<.28:continue
        v=b-a;p=a+v*.04;q=a+v*random.uniform(.72,.96)
        mid=(p+q)*.5+Vector((random.uniform(-.008,.008),random.uniform(-.008,.008),random.uniform(-.007,.007)))
        stroke(lines,[p,mid,q])
        if abs(v.z)<.02 and random.random()<.12:stroke(highlights,[p+Vector((0,0,.012)),mid+Vector((0,0,.012))])

def daub(name,pts,mat):
    mesh=bpy.data.meshes.new(name);mesh.from_pydata(pts,[],[tuple(range(len(pts)))]);o=bpy.data.objects.new(name,mesh);marks.objects.link(o);mesh.materials.append(mat)

# Deliberate, irregular paint shapes on the wall and wood faces, not full-screen noise.
for o in selected:
    if o.name.startswith('Plaster wall') and o in bpy.data.collections['00 | Architecture'].objects.values():
        xs=[v.co.x for v in o.data.vertices];ys=[v.co.y for v in o.data.vertices]
        lo,hi=min(xs),max(xs)
        for j in range(max(2,int(hi-lo)*2)):
            cx=random.uniform(lo+.15,hi-.15);cz=random.uniform(-.25,1.25);w=random.uniform(.10,.28);h=random.uniform(.025,.09)
            pts=[(cx-w,cz-h),(cx+w*.65,cz-h*.8),(cx+w,cz+h*.25),(cx+w*.1,cz+h),(cx-w*.9,cz+h*.7)]
            world=[o.matrix_world@Vector((x,min(ys)-.009,z)) for x,z in pts]
            daub('Flat wall brush mark',world,random.choice(wallpaint))
    if o.name.startswith('Panel inset'):
        xs=[v.co.x for v in o.data.vertices];ys=[v.co.y for v in o.data.vertices];zs=[v.co.z for v in o.data.vertices]
        for j in range(3):
            x=random.uniform(min(xs)*.7,max(xs)*.7);z=random.uniform(min(zs)*.5,max(zs)*.5)
            width=random.uniform(.012,.025);height=random.uniform(.10,.22)
            pts=[(x-width,z-height),(x+width,z-height*.7),(x+width*.6,z+height),(x-width*.3,z+height*.7)]
            daub('Wood pigment stroke',[o.matrix_world@Vector((xx,min(ys)-.008,zz)) for xx,zz in pts],random.choice(paintwood))
        # Small pen marks echo drawn wear without covering the whole material.
        z=max(zs)*.78;x=min(xs)*.8
        stroke(lines,[o.matrix_world@Vector((x,min(ys)-.01,z)),o.matrix_world@Vector((x+.16,min(ys)-.012,z-.025))])

# Omit most specular panes; the frame and drawn glints suggest glass.
for o in selected:
    if 'pane' in o.name.lower():o.hide_render=True
for x in [-.78,.78]:
    stroke(highlights,[(x,-.73,1.7),(x+.10,-.73,1.93)])
letterpaint=emission('Illustration | painted gold lettering',(.72,.47,.20))
for obj in s.objects:
    if obj.type=='FONT' and inhall(obj):
        for slot in obj.material_slots:
            if slot.material and slot.material.name=='Aged brass':
                slot.link='OBJECT';slot.material=letterpaint
for lamp in bpy.data.lights:
    if lamp.type=='POINT':lamp.use_shadow=False
    elif lamp.type=='AREA':lamp.size=min(lamp.size,1.1)
s.render.engine='BLENDER_EEVEE'
if hasattr(s.eevee,'taa_render_samples'):s.eevee.taa_render_samples=128
s.camera=bpy.data.objects['03 | Hall atmosphere'];s.frame_set(1)
s.render.resolution_x=1440;s.render.resolution_y=960;s.render.resolution_percentage=100
s.render.image_settings.media_type='IMAGE';s.render.image_settings.file_format='PNG'
s.render.use_compositing=False;s.view_settings.view_transform='Standard';s.view_settings.look='None';s.view_settings.exposure=0
s['Art direction']='Illustrated hall revision informed by Exnioc reference: flat colour blocks, drawn ink edges and deliberate pigment marks. Toon materials require Eevee.'
s.render.filepath=str(ROOT/'renders/07-illustrated-hall.png')
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'quiet-collection-illustrated-study.blend'))
bpy.ops.render.render(write_still=True)
print('ILLUSTRATED_STUDY_COMPLETE',flush=True)
