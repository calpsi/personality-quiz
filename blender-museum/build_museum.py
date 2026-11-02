import bpy, bmesh, math, random, json, sys
from pathlib import Path
from mathutils import Vector

ROOT=Path(__file__).resolve().parent
random.seed(21)
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
for c in list(bpy.data.collections):
    if c.name != 'Collection': bpy.data.collections.remove(c)
base=bpy.data.collections.get('Collection'); base.name='00 | Architecture'
def collection(name):
    c=bpy.data.collections.new(name); bpy.context.scene.collection.children.link(c); return c
front=collection('01 | Cutaway walls — enable for interiors')
roof=collection('02 | Ceilings — enable for interiors')
decor=collection('03 | Joinery and lamps')
exhibits=collection('04 | Eight quiz exhibits')
assets=collection('05 | Kenney CC0 nature assets')
cams=collection('06 | Cameras and navigation')
COL=base
def move(o):
    for c in list(o.users_collection): c.objects.unlink(o)
    COL.objects.link(o); return o
def mat(name,color,metal=0,rough=.65,emission=0):
    m=bpy.data.materials.new(name); m.diffuse_color=(*color,1); m.use_nodes=True
    bs=m.node_tree.nodes.get('Principled BSDF'); bs.inputs['Base Color'].default_value=(*color,1)
    bs.inputs['Metallic'].default_value=metal; bs.inputs['Roughness'].default_value=rough
    if emission:
        bs.inputs['Emission Color'].default_value=(*color,1); bs.inputs['Emission Strength'].default_value=emission
    return m
wood=mat('Walnut | subtle downloaded grain',(.20,.065,.028))
nt=wood.node_tree; tex=nt.nodes.new('ShaderNodeTexImage');tex.image=bpy.data.images.load(str(ROOT/'assets/wood_table_diff_1k.jpg'));tex.projection='BOX';tex.projection_blend=.2
coord=nt.nodes.new('ShaderNodeTexCoord');nt.links.new(coord.outputs['Generated'],tex.inputs['Vector'])
mix=nt.nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=.72;mix.inputs[2].default_value=(.38,.14,.055,1)
nt.links.new(tex.outputs['Color'],mix.inputs[1]);nt.links.new(mix.outputs[0],nt.nodes.get('Principled BSDF').inputs['Base Color'])
dark=mat('Espresso edges',(.055,.021,.014)); oak=mat('Honey wood highlights',(.38,.16,.052)); brass=mat('Aged brass',(.54,.31,.09),.65,.32)
green=mat('Moss green plaster',(.105,.16,.105)); blue=mat('Petrol blue gallery',(.055,.115,.13)); cream=mat('Warm limestone',(.46,.37,.24)); bone=mat('Ivory replica',(.78,.65,.42)); velvet=mat('Oxblood velvet',(.23,.025,.028)); black=mat('Midnight display lining',(.018,.035,.033)); paper=mat('Cream labels',(.78,.66,.43)); glow=mat('Amber luminous glass',(1,.56,.18),rough=.3,emission=3)
purple=mat('Amethyst',(.32,.15,.48),.12,.28);jade=mat('Malachite',(.07,.34,.22),.15,.3); stone=mat('Meteorite',(.065,.075,.09),.5,.4)
glass=mat('Case glass',(.48,.68,.59),rough=.12)
g=glass.node_tree.nodes.get('Principled BSDF');g.inputs['Transmission Weight'].default_value=1;g.inputs['IOR'].default_value=1.12;g.inputs['Alpha'].default_value=.20
glass.surface_render_method='DITHERED'
floorM=[mat('Floor plank %02d'%i,(.085+i*.007,.024+i*.003,.009+i*.0015),rough=.7) for i in range(7)]
def cube(name,loc,size,m,bevel=.025):
    verts=[(x*size[0]/2,y*size[1]/2,z*size[2]/2) for x,y,z in [(-1,-1,-1),(-1,-1,1),(-1,1,-1),(-1,1,1),(1,-1,-1),(1,-1,1),(1,1,-1),(1,1,1)]]
    mesh=bpy.data.meshes.new(name);mesh.from_pydata(verts,[],[(0,4,6,2),(1,3,7,5),(0,1,5,4),(2,6,7,3),(0,2,3,1),(4,5,7,6)])
    o=bpy.data.objects.new(name,mesh);COL.objects.link(o);o.location=loc
    if m:o.data.materials.append(m)
    if bevel:
        mod=o.modifiers.new('Soft game edges','BEVEL');mod.width=bevel;mod.segments=2
        mod=o.modifiers.new('Weighted normals','WEIGHTED_NORMAL')
    return o
def cyl(name,loc,r,depth,m,vertices=12,r2=None):
    top=r if r2 is None else r2
    verts=[(radius*math.cos(i*math.tau/vertices),radius*math.sin(i*math.tau/vertices),z) for radius,z in [(r,-depth/2),(top,depth/2)] for i in range(vertices)]
    faces=[tuple(reversed(range(vertices))),tuple(range(vertices,vertices*2))]+[(i,(i+1)%vertices,(i+1)%vertices+vertices,i+vertices) for i in range(vertices)]
    mesh=bpy.data.meshes.new(name);mesh.from_pydata(verts,[],faces);o=bpy.data.objects.new(name,mesh);COL.objects.link(o);o.location=loc;o.data.materials.append(m);return o
def ico(name,loc,scale,m,sub=1):
    mesh=bpy.data.meshes.new(name);bm=bmesh.new();bmesh.ops.create_icosphere(bm,subdivisions=sub,radius=1);bm.to_mesh(mesh);bm.free()
    o=bpy.data.objects.new(name,mesh);COL.objects.link(o);o.location=loc;o.scale=scale;o.data.materials.append(m);return o
def rod(name,a,b,r,m):
    a,b=Vector(a),Vector(b);o=cyl(name,(a+b)/2,r,(b-a).length,m,8);o.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler();return o
def curve(name,pts,r,m):
    d=bpy.data.curves.new(name,'CURVE');d.dimensions='3D';d.bevel_depth=r;d.bevel_resolution=1;d.resolution_u=1
    s=d.splines.new('POLY');s.points.add(len(pts)-1)
    for p,co in zip(s.points,pts):p.co=(*co,1)
    o=bpy.data.objects.new(name,d);COL.objects.link(o);o.data.materials.append(m);return o
def text(body,loc,size=.18,m=paper,rot=(math.pi/2,0,0)):
    d=bpy.data.curves.new(body,'FONT');d.body=body;d.align_x='CENTER';d.size=size;d.extrude=.0015
    o=bpy.data.objects.new('Lettering | '+body,d);COL.objects.link(o);o.location=loc;o.rotation_euler=rot;d.materials.append(m);return o
def light(name,loc,power,color=(1,.63,.3),size=1,target=None):
    d=bpy.data.lights.new(name,'AREA' if target is not None else 'POINT');d.energy=power;d.color=color
    if target is None:d.shadow_soft_size=size
    else:d.shape='DISK';d.size=size
    o=bpy.data.objects.new(name,d);COL.objects.link(o);o.location=loc
    if target is not None:o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
    return o

# Floors form a cross around the central hall. Everything uses Z up and metres.
rooms=[('Hall',0,0,8,10),('Deep Time',-8,0,8,10),('Earth and Space',8,0,8,10),('Living Systems',0,9,8,8),('Vestibule',0,-7,6,4)]
for name,x,y,w,d in rooms:
    cube(name+' foundation',(x,y,-.3),(w+.2,d+.2,.6),dark,.09)
    cube(name+' brass foundation inlay',(x,y,-.07),(w+.25,d+.25,.055),brass,.01)
    for j in range(round(d/.5)):
        yy=y-d/2+.25+j*.5
        for k in range(round(w/2)):
            xx=x-w/2+1+k*2
            cube(name+' floorboard',(xx,yy,.015),(1.98,.485,.09),random.choice(floorM),.012)
    COL=roof;cube(name+' ceiling',(x,y,3.8),(w,d,.16),dark)
    for xx in [x-w/2+.3,x+w/2-.3]:cube('Ceiling beam',(xx,y,3.6),(.22,d,.28),wood)
    COL=base

# Local wall runs: local X follows the wall; the decorated face points local -Y.
def wall(cx,cy,length,theta=0,material=green,cut=False):
    global COL
    old=COL;COL=front if cut else base
    co,si=math.cos(theta),math.sin(theta)
    def item(name,u,v,z,sz,m):
        o=cube(name,(cx+u*co-v*si,cy+u*si+v*co,z),sz,m);o.rotation_euler.z=theta;return o
    item('Plaster wall',0,0,1.8,(length,.20,3.6),material)
    item('Walnut wainscot',0,-.13,.66,(length,.13,1.32),wood)
    item('Reverse walnut wainscot',0,.13,.66,(length,.13,1.32),wood)
    item('Reverse chair rail',0,.20,1.3,(length,.16,.12),oak)
    for z,h,m in [(.12,.18,dark),(1.3,.12,oak),(1.39,.055,brass),(3.48,.15,wood),(3.58,.08,oak)]:item('Continuous moulding',0,-.19,z,(length+.03,.16,h),m)
    count=max(1,int(length/.9))
    for j in range(count):
        u=-length/2+(j+.5)*length/count
        item('Raised panel',u,-.23,.70,(length/count-.16,.055,.92),dark)
        item('Panel inset',u,-.27,.70,(length/count-.23,.035,.83),wood)
        item('Reverse panel',u,.23,.70,(length/count-.16,.055,.92),dark)
        item('Reverse panel inset',u,.27,.70,(length/count-.23,.035,.83),wood)
        if j%2==0:
            o=item('Wallpaper brass diamond',u,-.115,2.35,(.095,.012,.095),brass);o.rotation_euler.rotate_axis('Y',math.pi/4)
    for u in [-length/2+.09,length/2-.09]:item('Timber pilaster',u,-.24,1.85,(.20,.23,3.45),wood)
    COL=old

# Outer walls. South and east-facing facades can be hidden for the dollhouse view.
wall(-8,5,8);wall(8,5,8,material=blue)
wall(-12,0,10,math.pi/2);wall(12,0,10,-math.pi/2,blue,True)
wall(-8,-5,8,math.pi,cut=True);wall(8,-5,8,math.pi,blue,True)
wall(0,13,8);wall(-4,9,8,math.pi/2);wall(4,9,8,-math.pi/2,cut=True)
wall(-3,-7,4,math.pi/2);wall(3,-7,4,-math.pi/2,cut=True)
wall(-2,-9,2,math.pi,cut=True);wall(2,-9,2,math.pi,cut=True)
# Interior walls with generous central openings.
for x,theta in [(-4,math.pi/2),(4,-math.pi/2)]:
    for y in [-3.25,3.25]:wall(x,y,3.5,theta)
for x in [-2.75,2.75]:wall(x,5,2.5)
for x in [-2.75,2.75]:wall(x,-5,2.5,math.pi,cut=True)

COL=decor
def portal(cx,cy,theta,title):
    co,si=math.cos(theta),math.sin(theta)
    def pos(u,v,z):return (cx+co*u-si*v,cy+si*u+co*v,z)
    for u in [-1.5,1.5]:
        o=cube('Door jamb',pos(u,0,1.65),(.28,.46,3.3),wood);o.rotation_euler.z=theta
        o=cube('Jamb brass strip',pos(u,-.25,1.7),(.045,.025,2.9),brass);o.rotation_euler.z=theta
    o=cube('Door lintel',pos(0,0,3.18),(3.35,.48,.48),wood);o.rotation_euler.z=theta
    o=cube('Gallery title plaque',pos(0,-.27,3.18),(2.65,.045,.32),black);o.rotation_euler.z=theta
    text(title,pos(0,-.30,3.13),.18,brass,(math.pi/2,0,theta))
portal(-4,0,math.pi/2,'DEEP TIME');portal(4,0,-math.pi/2,'EARTH & SPACE');portal(0,5,0,'LIVING SYSTEMS');portal(0,-5,0,'THE QUIET COLLECTION')

def sconce(x,y,z=2.45):
    cyl('Lamp finial',(x,y,z+.45),.055,.20,brass)
    cyl('Lantern crown',(x,y,z+.28),.23,.10,brass,8)
    cyl('Lantern amber pane',(x,y,z),.17,.48,glow,8)
    cyl('Lantern base',(x,y,z-.28),.23,.10,brass,8)
    for a in range(4):
        t=a*math.pi/2;rod('Lantern mullion',(x+.18*math.cos(t),y+.18*math.sin(t),z-.25),(x+.18*math.cos(t),y+.18*math.sin(t),z+.25),.018,brass)
    light('Amber lantern',(x,y,z),75,size=.28)
for x,y in [(-3.5,-3.3),(3.5,-3.3),(-3.5,3.3),(3.5,3.3),(-11.6,-2.6),(-11.6,2.6),(-8,4.6),(11.6,-2.6),(11.6,2.6),(8,4.6),(-3.6,8),(-3.6,11.7),(3.6,8),(3.6,11.7),(0,12.6),(-2.6,-7.5),(2.6,-7.5)]:sconce(x,y)

# Hall rug, upholstered bench, admission desk, central reveal case.
cube('Oxblood hall carpet',(0,0,.09),(4.8,7.9,.035),velvet,.04)
for x in [-2.28,2.28]:cube('Carpet gold border',(x,0,.113),(.045,7.7,.008),brass,0)
for y in [-3.78,3.78]:cube('Carpet gold border',(0,y,.113),(4.6,.045,.008),brass,0)
for y in [-3.2,-2.9,2.9,3.2]:
    for x in [-1.5,-1,-.5,0,.5,1,1.5]:
        o=cube('Carpet woven motif',(x,y,.119),(.12,.12,.006),oak,0);o.rotation_euler.z=math.pi/4
def table(name,x,y,w=2,d=1):
    cube(name+' top',(x,y,.95),(w,d,.14),wood,.06)
    cube(name+' brass edge',(x,y,1.025),(w+.02,d+.02,.025),brass,.01)
    for xx in [-w/2+.13,w/2-.13]:
        for yy in [-d/2+.13,d/2-.13]:cube(name+' leg',(x+xx,y+yy,.46),(.15,.15,.9),wood)
table('Visitor desk',-1.6,-6.7,1.8,.8)
cube('Admission book',(-1.6,-6.7,1.08),(.55,.38,.08),paper)
text('NATURAL HISTORY',(0,-8.75,2.85),.30,brass,(math.pi/2,0,math.pi))
table('Bench',2.9,-2.7,1.2,.65);cube('Bench velvet cushion',(2.9,-2.7,1.1),(1.25,.7,.23),velvet,.1)
cyl('Reveal octagonal footing',(0,.3,.23),1.32,.25,dark,8)
cyl('Reveal plinth moulding',(0,.3,.40),1.21,.13,brass,8)
cyl('Reveal walnut cabinet',(0,.3,.82),1.14,.78,wood,8)
cyl('Reveal black velvet stage',(0,.3,1.25),1.17,.09,black,8)
for a in range(8):
    t=a*math.tau/8;rod('Reveal brass frame',(1.10*math.cos(t),.3+1.10*math.sin(t),1.25),(1.10*math.cos(t),.3+1.10*math.sin(t),2.45),.032,brass)
    o=cube('Frosted reveal pane',(1.02*math.cos(t+math.pi/8),.3+1.02*math.sin(t+math.pi/8),1.83),(.82,.016,1.12),glass,0);o.rotation_euler.z=t+math.pi/8+math.pi/2
cyl('Reveal canopy rim',(0,.3,2.46),1.22,.12,brass,8)
cyl('Reveal canopy',(0,.3,2.65),1.25,.28,wood,8,r2=.60)
cyl('Reveal crown',(0,.3,2.88),.19,.22,brass,8,r2=.07)
cyl('Reserved specimen pedestal',(0,.3,1.35),.36,.16,dark,8)
ico('Concealed specimen placeholder',(0,.3,1.71),(.36,.28,.36),brass,2)
text('YOUR EXHIBIT',(0,-.85,.83),.17,brass)
light('Reveal spotlight',(0,.3,3.4),180,size=1.8,target=(0,.3,.5))
for x,y,energy in [(0,0,200),(-8,0,230),(8,0,200),(0,9,250),(0,-7,90)]:
    light('Gallery soft overhead',(x,y,3.55),energy,(1,.72,.43),4,target=(x,y,0))
    cyl('Pendant shade',(x,y,3.34),.60,.30,dark,12,r2=.32)
    cyl('Pendant luminous underside',(x,y,3.18),.49,.035,glow,12)
    rod('Pendant suspension',(x,y,3.5),(x,y,3.77),.025,brass)

COL=exhibits
def case(name,x,y,w=2,d=1.2):
    cube(name+' foot',(x,y,.14),(w+.12,d+.12,.23),dark,.04)
    cube(name+' walnut body',(x,y,.66),(w,d,1.0),wood,.055)
    cube(name+' front inset',(x,y-d/2-.012,.66),(w-.22,.04,.70),dark,.018)
    cube(name+' front raised panel',(x,y-d/2-.04,.66),(w-.32,.035,.59),wood,.018)
    cube(name+' brass rim',(x,y,1.19),(w+.09,d+.09,.045),brass,.01)
    cube(name+' lining',(x,y,1.23),(w-.1,d-.1,.04),black,.015)
    for dx in [-w/2,w/2]:
        for dy in [-d/2,d/2]:rod(name+' case corner',(x+dx,y+dy,1.24),(x+dx,y+dy,2.15),.025,brass)
    cube(name+' glass back',(x,y+d/2,1.7),(w,.012,.9),glass,0)
    cube(name+' glass top',(x,y,2.16),(w,d,.012),glass,0)
    light(name+' exhibit light',(x,y,2.8),100,size=1.3,target=(x,y,1.4))
    return 1.28
def plaque(num,title,x,y,z=1.0):
    cube('Stop '+num+' plaque',(x,y,z),(1.60,.045,.30),paper,.025)
    text(num+' / '+title,(x,y-.03,z-.025),.075,dark)
def ammonite(x,y,z,s=1):
    pts=[]
    for i in range(130):
        t=i/129*math.pi*4.5;r=.04+.038*t
        pts.append((x+s*r*math.cos(t),y,z+s*r*math.sin(t)))
    curve('Ammonite coiled fossil',pts,.10*s,bone)
    for i in range(25,130,4):
        p=Vector(pts[i]);ico('Ammonite ribs',p,(.10*s,.16*s,.045*s),cream,1)
    ico('Fossil limestone matrix',(x,y+.13,z),(.8*s,.20*s,.73*s),cream,2)
case('01 fossil',-10.1,-2.8,2.2,1.3);ammonite(-10.1,-2.95,1.8,.82);plaque('01','THE SMALL DETAIL',-10.1,-3.49)

# A stylised, explicitly replica skeleton with a recognisable rib cage and tail.
cube('02 skeleton platform',(-9,1.8,.2),(4.6,2.4,.3),dark,.12)
spine=[(-10.8,1.8,1.15),(-10.3,1.8,1.5),(-9.8,1.8,1.8),(-9.3,1.8,1.92),(-8.8,1.8,1.96),(-8.3,1.8,2.05),(-7.9,1.8,2.4),(-7.6,1.8,2.65)]
curve('Replica vertebral column',spine,.09,bone)
for i in range(7):
    x=-10.0+i*.27; z=1.86+(x+9.6)*.08
    ico('Replica vertebra',(x,1.8,z),(.14,.15,.13),bone)
    for side in [-1,1]:
        pts=[(x,1.8,z),(x+.06,1.8+side*.4,z-.08),(x+.14,1.8+side*.64,z-.43),(x+.24,1.8+side*.43,z-.83),(x+.22,1.8+side*.10,z-.92)]
        if i!=3:curve('Replica rib',pts,.045,bone)
for x in [-9.8,-8.45]:
    for side in [-1,1]:
        a=(x,1.8+side*.4,1.6);b=(x-.12,1.8+side*.55,.91);c=(x+.12,1.8+side*.65,.38)
        rod('Replica limb',a,b,.07,bone);rod('Replica limb',b,c,.055,bone);ico('Replica joint',b,(.09,.09,.10),bone)
        for toe in [-.1,0,.1]:rod('Replica toe',c,(x+.43,1.8+side*.65+toe,.34),.035,bone)
ico('Replica skull',(-7.28,1.8,2.65),(.48,.26,.25),bone,1)
ico('Replica eye socket',(-7.36,1.555,2.72),(.12,.025,.10),dark,1)
rod('Jaw',(-7.55,1.8,2.45),(-6.95,1.8,2.48),.07,bone)
for x in [-9.5,-8]:rod('Skeleton museum mount',(x,1.8,.35),(x,1.8,1.7),.025,brass)
plaque('02','THE MISSING PIECE',-9,.55,.6)
light('Skeleton pool',(-9,1.8,3.4),220,size=2,target=(-9,1.8,1))
# Framed trace plaques on back wall.
for i in range(3):
    x=-10.5+i*2.0
    cube('03 trace frame',(x,4.72,2.25),(1.5,.15,1.55),wood)
    cube('03 trace stone',(x,4.61,2.25),(1.27,.08,1.32),cream)
    for j in range(3):
        xx=x-.27+j*.25;zz=1.9+j*.27
        ico('Fossil footprint',(xx,4.54,zz),(.11,.035,.15),dark)
        for t in [-1,0,1]:rod('Footprint digit',(xx,4.52,zz+.06),(xx+t*.09,4.52,zz+.22),.025,dark)
plaque('03','WHAT GETS REMEMBERED',-6.6,4.52,1.05)

case('04 mineral drawers',10,-2.8,2.5,1.4)
for row in range(3):
    for col in range(4):
        x=9.12+col*.58;z=.38+row*.25
        cube('Mineral drawer front',(x,-3.53,z),(.52,.08,.20),oak)
        ico('Drawer brass pull',(x,-3.61,z),(.06,.025,.025),brass)
def crystal(x,y,z,h,m,r=.18):
    cyl('Crystal shaft',(x,y,z+h*.34),r,h*.68,m,6)
    cyl('Crystal termination',(x,y,z+h*.84),r,h*.32,m,6,r2=0)
for i in range(9):crystal(9.2+(i%5)*.36,-2.8+(i//5)*.28,1.27,random.uniform(.25,.64),purple if i%2 else jade,.14)
plaque('04','THE SURPRISE DRAWER',10,-3.56,1.03)
case('05 meteorite',10,1.4,2,1.6)
rock=ico('Meteorite specimen',(10,1.4,1.7),(.65,.5,.5),stone,2)
for p in rock.data.vertices:p.co*=random.uniform(.8,1.15)
for a in [0,2,4]:rod('Meteorite cradle',(10+.42*math.cos(a),1.4+.42*math.sin(a),1.27),(10+.3*math.cos(a),1.4+.3*math.sin(a),1.5),.025,brass)
plaque('05','THE NEXT TEST',10,.55)
case('06 comparison',6.1,3.4,2.5,1.2)
for x,m in [(5.55,purple),(6.65,jade)]:
    for i in range(5):crystal(x+random.uniform(-.2,.2),3.4+random.uniform(-.2,.2),1.27,random.uniform(.3,.7),m,.15)
plaque('06','TWO VIEWS',6.1,2.75)

# Living gallery furnished using downloaded game-ready nature assets.
def import_asset(filename,loc,height):
    path=ROOT/'assets/kenney-nature/kenney-nature-kit/Models/GLTF format'/filename
    if not path.exists():return None
    before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(path));objs=list(set(bpy.data.objects)-before)
    meshes=[o for o in objs if o.type=='MESH']
    if not meshes:return None
    bpy.context.view_layer.update()
    bounds=[o.matrix_world@Vector(v) for o in meshes for v in o.bound_box]
    lo=Vector([min(v[i] for v in bounds) for i in range(3)]);hi=Vector([max(v[i] for v in bounds) for i in range(3)])
    factor=height/max(.001,hi.z-lo.z)
    empty=bpy.data.objects.new('Kenney | '+filename,None);assets.objects.link(empty)
    for o in objs:
        for c in list(o.users_collection):c.objects.unlink(o)
        assets.objects.link(o)
        if o.parent is None:o.parent=empty
    empty.scale=(factor,)*3;empty.location=(loc[0]-(lo.x+hi.x)*.5*factor,loc[1]-(lo.y+hi.y)*.5*factor,loc[2]-lo.z*factor)
    return empty
case('07 habitat',-1.9,9.8,2.9,1.9)
import_asset('stump_old.glb',(-2.2,9.8,1.27),.64)
import_asset('rock_largeA.glb',(-1.2,10,1.27),.30)
def branch(a,b,r,depth):
    rod('Coral branch',a,b,r,bone)
    if depth:
        for side in [-1,1]:
            c=(b[0]+side*.18*depth,b[1]+random.uniform(-.16,.16),b[2]+.24)
            branch(b,c,r*.65,depth-1)
branch((-1.3,9.6,1.28),(-1.3,9.6,1.65),.06,2)
plaque('07','ROOM TO CHANGE',-1.9,8.8)
table('08 fieldwork desk',2,9.5,2.5,1.35)
for i in range(3):
    cube('Field guide book',(1.35,9.5,1.08+i*.1),(.65,.5,.075),green if i%2 else velvet)
cube('Folded field map',(2.1,9.3,1.07),(.65,.65,.025),paper,.008)
for i in range(4):rod('Map contour',(1.85,9.1+i*.12,1.09),(2.32,9.17+i*.12,1.09),.007,green)
cube('Camera body',(2.8,9.5,1.23),(.46,.3,.28),dark)
lens=cyl('Camera lens',(2.8,9.27,1.23),.12,.18,brass,12);lens.rotation_euler.x=math.pi/2
plaque('08','THE SHARED FIELD KIT',2,8.79,.82)
for x in [-2.7,-.9,.9,2.7]:
    cube('Botanical frame',(x,12.7,2.3),(1.2,.14,1.55),wood)
    cube('Botanical paper',(x,12.60,2.3),(1,.03,1.35),paper)
    rod('Pressed plant stem',(x,12.55,1.83),(x,12.55,2.8),.018,green)
    for j in range(5):
        side=(-1)**j
        o=ico('Pressed botanical leaf',(x+side*.14,12.52,2+j*.14),(.18,.025,.065),green,1);o.rotation_euler.y=side*.4
# Pot plants reuse Kenney models, kept clear of circulation.
for x,y in [(-2.9,6.3),(2.9,6.3),(-10.7,3.7),(10.8,3.9)]:
    cyl('Terracotta pot',(x,y,.35),.32,.55,oak,10,r2=.43)
    import_asset('tree_palmDetailedShort.glb',(x,y,.6),1.3)

# Museum atmosphere: hanging constellation instrument in the east gallery.
COL=decor
for angle in [0,math.pi/3,2*math.pi/3]:
    pts=[]
    for i in range(49):
        t=i/48*math.tau;pts.append((8+.7*math.cos(t),.7*math.sin(t)*math.cos(angle),2.85+.7*math.sin(t)*math.sin(angle)))
    curve('Brass armillary ring',pts,.022,brass)
ico('Armillary centre',(8,0,2.85),(.13,.13,.13),brass,2)

COL=base
cube('Diorama ground',(0,2,-.75),(200,200,.15),mat('Backdrop brown plum',(.055,.035,.045)),0)
COL=cams
def camera(name,loc,target,lens=30,ortho=None):
    d=bpy.data.cameras.new(name);o=bpy.data.objects.new(name,d);cams.objects.link(o);o.location=loc;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();d.lens=lens
    if ortho:d.type='ORTHO';d.ortho_scale=ortho
    d.clip_end=200;return o
overview=camera('01 | Cutaway overview',(29,-36,31),(0,2,0),ortho=34)
entrance=camera('02 | Entrance walkthrough',(0,-7.8,1.75),(0,3,1.75),21)
hallcam=camera('03 | Hall atmosphere',(-2.8,-3.8,2.05),(.3,2,1.6),22)
fossilcam=camera('04 | Deep Time',(-5.5,-3.8,2.1),(-9,1.4,1.6),23)
earthcam=camera('05 | Earth and Space',(5.4,-3.5,2.05),(9,1.9,1.5),24)
livingcam=camera('06 | Living Systems',(0,5.8,1.9),(0,10,1.6),23)
tour=camera('07 | Animated walkthrough',(0,-7.8,1.75),(0,3,1.75),23)
waypoints=[(1,(0,-7.8,1.75),(0,2,1.7)),(65,(0,-3.2,1.75),(0,1,1.7)),(120,(-2.4,-1.3,1.75),(-8,1,1.65)),(190,(-6,-.8,1.75),(-9,1.8,1.65)),(250,(-8.5,-4.1,1.75),(-10,-2.8,1.65)),(280,(-6,-.8,1.75),(-4,0,1.8)),(310,(-2,-1,1.75),(4,0,1.8)),(380,(6,-.8,1.75),(10,1.4,1.65)),(440,(6,-.8,1.75),(10,-2.8,1.65)),(510,(2,2.4,1.75),(0,8,1.7)),(580,(0,6.7,1.75),(-1.9,9.8,1.65)),(640,(0,6.7,1.75),(2,9.5,1.4)),(720,(0,3.3,1.75),(0,.3,1.7))]
for frame,loc,target in waypoints:
    tour.location=loc;tour.rotation_euler=(Vector(target)-tour.location).to_track_quat('-Z','Y').to_euler();tour.keyframe_insert(data_path='location',frame=frame);tour.keyframe_insert(data_path='rotation_euler',frame=frame)
for frame,loc,target in waypoints:
    marker=bpy.context.scene.timeline_markers.new('Visit '+str(frame),frame=frame)
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=32;scene.cycles.use_denoising=True
scene.cycles.max_bounces=5;scene.cycles.transparent_max_bounces=5
scene.world.color=(.06,.06,.06);scene.world.use_nodes=True
scene.world.node_tree.nodes.get('Background').inputs[0].default_value=(.22,.27,.40,1);scene.world.node_tree.nodes.get('Background').inputs[1].default_value=.22
scene.render.resolution_x=1440;scene.render.resolution_y=1200;scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG';scene.render.fps=24;scene.frame_end=720
scene.view_settings.view_transform='AgX';scene.view_settings.look='AgX - Medium High Contrast';scene.view_settings.exposure=-.25
nt=bpy.data.node_groups.new('Museum warm bloom','CompositorNodeTree');scene.compositing_node_group=nt
nt.interface.new_socket(name='Image',in_out='OUTPUT',socket_type='NodeSocketColor')
rl=nt.nodes.new('CompositorNodeRLayers');gl=nt.nodes.new('CompositorNodeGlare');gl.inputs['Type'].default_value='Fog Glow';gl.inputs['Quality'].default_value='Medium';gl.inputs['Threshold'].default_value=1.8;gl.inputs['Strength'].default_value=.25
out=nt.nodes.new('NodeGroupOutput');nt.links.new(rl.outputs['Image'],gl.inputs['Image']);nt.links.new(gl.outputs['Image'],out.inputs['Image'])
# Soft studio fill for the cutaway only.
COL=front # assigned separately below; do not couple fill to cutaway walls.
studio=collection('07 | Overview studio fill');COL=studio
light('Overview warm key',(-10,-10,18),1100,(1,.65,.35),12,target=(0,2,0))
light('Overview cool edge',(10,12,16),1000,(.53,.67,1),10,target=(0,2,0))
scene['Design']='Warm, low-poly natural history personality quiz museum. Eight stops plus central reveal.'
scene['Asset credits']='Kenney Nature Kit CC0; Poly Haven wood_table CC0. See ASSET_CREDITS.md.'
scene['Interior instructions']='Enable collections 01 and 02, disable collection 07, then select a visitor camera. 07 Animated walkthrough has 720 frames at 24fps.'
scene['Scientific note']='Exhibits are stylised artistic replicas, not species-accurate scientific reconstructions.'
front.hide_render=True;front.hide_viewport=True;roof.hide_render=True;roof.hide_viewport=True
scene.camera=overview;scene.frame_set(1)
for screen in bpy.data.screens:
    for area in screen.areas:
        if area.type=='VIEW_3D':area.spaces.active.region_3d.view_perspective='CAMERA'
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'quiet-collection-museum.blend'))
scene.render.filepath=str(ROOT/'renders/01-cutaway.png');bpy.ops.render.render(write_still=True)
front.hide_render=False;roof.hide_render=False;studio.hide_render=True
scene.render.resolution_x=1440;scene.render.resolution_y=960
for cam,filename in [(hallcam,'02-hall.png'),(fossilcam,'03-deep-time.png'),(livingcam,'04-living-systems.png')]:
    scene.camera=cam;scene.render.filepath=str(ROOT/'renders'/filename);bpy.ops.render.render(write_still=True)
print('MUSEUM_BUILD_COMPLETE',flush=True)
