"""Reference-led low-poly Abraham. Standalone asset plus a museum placement copy."""
import bpy, math, random, json
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parent;MUSEUM=ROOT.parent
random.seed(9)
bpy.ops.wm.read_factory_settings(use_empty=True)
C=bpy.data.collections.new('Abraham | character');bpy.context.scene.collection.children.link(C)
def mat(name,col):
 m=bpy.data.materials.new(name);m.diffuse_color=(*col,1);m.use_nodes=True
 b=m.node_tree.nodes.get('Principled BSDF');b.inputs['Base Color'].default_value=(*col,1);b.inputs['Roughness'].default_value=.83
 return m
fur=mat('Abraham | honey fur',(.83,.43,.13));cream=mat('Abraham | cream muzzle',(.96,.78,.46));ear=mat('Abraham | inner ear',(.58,.24,.08));brown=mat('Abraham | warm outlines',(.16,.055,.025));eye=mat('Abraham | dark eyes',(.065,.019,.012));white=mat('Abraham | eye shine',(.99,.92,.72));olive=mat('Abraham | olive coat',(.16,.19,.075));gold=mat('Abraham | gold embroidery',(.88,.47,.10));vest=mat('Abraham | brown waistcoat',(.31,.115,.045));red=mat('Abraham | burgundy ribbon',(.36,.065,.05));leather=mat('Abraham | satchel leather',(.26,.085,.025));badge=mat('Abraham | ivory badge',(.91,.77,.48))
def move(o,name,m):
 for c in list(o.users_collection):c.objects.unlink(o)
 C.objects.link(o);o.name=name
 if m:o.data.materials.append(m)
 return o
def sphere(name,loc,scale,m,seg=16,rings=10):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=seg,ring_count=rings,radius=1,location=loc)
 o=move(bpy.context.object,name,m);o.scale=scale;return o
def box(name,loc,scale,m,bevel=.035):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=move(bpy.context.object,name,m);o.dimensions=scale
 bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 if bevel:
  mod=o.modifiers.new('Soft chunky edges','BEVEL');mod.width=bevel;mod.segments=2
 return o
def poly(name,verts,faces,m):
 d=bpy.data.meshes.new(name);d.from_pydata(verts,[],faces);o=bpy.data.objects.new(name,d);C.objects.link(o);d.materials.append(m);return o
def line(name,pts,r,m):
 d=bpy.data.curves.new(name,'CURVE');d.dimensions='3D';d.bevel_depth=r;d.bevel_resolution=1
 sp=d.splines.new('POLY');sp.points.add(len(pts)-1)
 for p,co in zip(sp.points,pts):p.co=(*co,1)
 o=bpy.data.objects.new(name,d);C.objects.link(o);d.materials.append(m);return o
def empty(name,loc):
 o=bpy.data.objects.new(name,None);C.objects.link(o);o.location=loc;o.empty_display_size=.1;return o
root=empty('Abraham_ROOT',(0,0,0));bodyctrl=empty('Abraham_body',(0,0,.75));headctrl=empty('Abraham_head',(0,0,1.65))
def parent(o,p):
 bpy.context.view_layer.update();mw=o.matrix_world.copy();o.parent=p;o.matrix_world=mw
parent(bodyctrl,root);parent(headctrl,bodyctrl)
body_parts=[];head_parts=[]
body_parts.append(sphere('Round cream body',(0,0,.66),(.53,.35,.55),cream))
for x in [-.24,.24]:
 body_parts.append(sphere('Little leather shoe',(x,-.11,.13),(.17,.23,.11),leather,12,8))
body_parts.append(sphere('Waistcoat',(0,-.11,.88),(.45,.30,.38),vest))
head_parts.append(sphere('Large honey head',(0,-.005,1.65),(.66,.42,.58),fur,20,12))
head_parts.append(sphere('Cream lower face',(0,-.15,1.43),(.575,.345,.275),cream,20,10))
for x in [-.46,.46]:
 head_parts.append(sphere('Dark ear rim',(x,.025,2.11),(.265,.135,.29),brown,14,10))
 head_parts.append(sphere('Golden outer ear',(x,-.015,2.11),(.235,.135,.255),fur,14,10))
 head_parts.append(sphere('Inner ear',(x,-.143,2.10),(.139,.035,.16),ear,12,8))
 head_parts.append(sphere('Inner ear gold',(x,-.158,2.12),(.09,.018,.11),gold,12,8))
for side in [-1,1]:
 x=side*.235
 head_parts.append(sphere('Eye cream surround',(x,-.388,1.75),(.132,.045,.18),white,16,10))
 head_parts.append(sphere('Dark expressive eye',(x+side*.013,-.427,1.745),(.095,.027,.143),eye,16,10))
 head_parts.append(sphere('Eye catchlight',(x-.025,-.454,1.81),(.026,.012,.036),white,10,6))
 head_parts.append(sphere('Tiny eye catchlight',(x+.022,-.456,1.71),(.010,.008,.013),white,8,6))
head_parts.append(sphere('Button nose',(0,-.490,1.59),(.068,.045,.047),brown,12,8))
head_parts.append(sphere('Nose highlight',(-.014,-.528,1.607),(.022,.009,.012),ear,8,6))
mouth=line('Small surprised mouth',[(-.028,-.492,1.452),(0,-.504,1.50),(.028,-.492,1.452),(.015,-.50,1.432),(-.014,-.50,1.432),(-.028,-.492,1.452)],.010,brown);head_parts.append(mouth)
head_parts.append(poly('Mouth warm centre',[(-.018,-.503,1.448),(0,-.509,1.478),(.018,-.503,1.448)],[(0,1,2)],red))
head_parts.append(line('Forehead curl',[(-.09,-.32,2.09),(-.045,-.35,2.04),(.01,-.35,2.07),(-.005,-.30,2.14),(.07,-.32,2.10),(.12,-.29,2.14),(.09,-.24,2.18)],.023,brown))
for x in [-.08,.03,.12]:
 head_parts.append(poly('Crown fur tuft',[(x-.05,.02,2.18),(x+.08,.04,2.29),(x+.04,-.04,2.19),(x-.04,-.06,2.16)],[(0,1,2),(0,2,3)],fur))

# Open-front cape: broad shoulder mantle with continuous gold hem and collar.
N=28;verts=[]
for z,rx,ry in [(1.28,.35,.25),(1.12,.51,.34),(.73,.66,.40)]:
 for i in range(N+1):
  t=.25+i/N*(math.tau-.5);verts.append((rx*math.sin(t),-ry*math.cos(t),z))
faces=[]
for ring in range(2):
 for i in range(N):
  a=ring*(N+1)+i;faces.append((a,a+1,a+N+2,a+N+1))
cape=poly('Olive open-front museum cape',verts,faces,olive);body_parts.append(cape)
sol=cape.modifiers.new('Cape cloth thickness','SOLIDIFY');sol.thickness=.035
for z,rx,ry in [(.745,.69,.435),(1.285,.355,.257)]:
 body_parts.append(line('Cape gold border',[(rx*math.sin(.25+i/N*(math.tau-.5)),-ry*math.cos(.25+i/N*(math.tau-.5)),z) for i in range(N+1)],.024,gold))
for t in [.25,math.tau-.25]:body_parts.append(line('Cape gold front seam',[(.35*math.sin(t),-.26*math.cos(t),1.28),(.51*math.sin(t),-.35*math.cos(t),1.12),(.66*math.sin(t),-.415*math.cos(t),.73)],.022,gold))
for side in [-1,1]:
 body_parts.append(poly('Cream collar',[(side*.02,-.35,1.28),(side*.21,-.32,1.32),(side*.15,-.40,1.16)],[(0,1,2)],cream))
 body_parts.append(poly('Ribbon tail',[(side*.025,-.41,1.20),(side*.12,-.40,.98),(side*.055,-.43,1.015),(side*.02,-.43,.96),(0,-.42,1.17)],[(0,1,2,3,4)],red))
 # Rigid arm pivot for editable gestures.
 ctrl=empty('Abraham_arm_'+('L' if side<0 else 'R'),(side*.44,0,1.04));parent(ctrl,bodyctrl)
 paw=sphere('Little paw',(side*.58,-.14,.70),(.13,.14,.16),fur,12,8);parent(paw,ctrl)
 sleeve=sphere('Olive sleeve',(side*.49,-.02,.86),(.18,.20,.24),olive,12,8);parent(sleeve,ctrl)
 for j in [-1,0,1]:parent(line('Paw digit',[(side*.58+j*.035,-.265,.66),(side*.58+j*.035,-.27,.71)],.006,ear),ctrl)
 for j in range(5):
  # embroidery follows the cape side, visible from front and rear.
  t=side*(.72+j*.15);z=.81+j*.032;rx=.695-(z-.73)*.385;ry=.44-(z-.73)*.154
  loc=(rx*math.sin(t),-ry*math.cos(t)-.02,z)
  leaf=sphere('Gold laurel leaf',loc,(.055,.018,.022),gold,8,6);leaf.rotation_euler.y=side*(-.6);body_parts.append(leaf)
  t=math.pi+side*(.25+j*.17);loc=(rx*math.sin(t),-ry*math.cos(t)+.02,z)
  leaf=sphere('Back gold laurel leaf',loc,(.055,.018,.025),gold,8,6);leaf.rotation_euler.y=side*.6;body_parts.append(leaf)
for side in [-1,1]:
 for back in [False,True]:
  pts=[]
  for j in range(6):
   z=.81+j*.028;t=(math.pi+side*(.25+j*.14)) if back else side*(.66+j*.14)
   rx=.701-(z-.73)*.385;ry=.45-(z-.73)*.154
   pts.append((rx*math.sin(t),-ry*math.cos(t),z))
  body_parts.append(line('Laurel embroidered stem',pts,.008,gold))
  for x,y,z in pts[1:-1]:
   for sign in [-1,1]:
    leaf=sphere('Paired laurel embroidery',(x+sign*.015,y+(.012 if back else -.012),z+sign*.026),(.038,.015,.018),gold,8,6);leaf.rotation_euler.y=sign*.65;body_parts.append(leaf)
for z in [1.00,.88]:body_parts.append(sphere('Waistcoat gold button',(0,-.408,z),(.025,.015,.028),gold,10,6))
body_parts.append(sphere('Flower brooch gold base',(0,-.435,1.24),(.11,.025,.11),gold,12,8))
for i in range(5):
 t=i*math.tau/5;body_parts.append(sphere('Flower clasp petal',(.054*math.sin(t),-.466,1.24+.054*math.cos(t)),(.037,.018,.04),cream,10,6))
body_parts.append(sphere('Flower clasp centre',(0,-.49,1.24),(.03,.012,.031),gold,10,6))

# Satchel at the wearer's left, visible on image right, with diagonal strap.
body_parts.append(line('Satchel cross-body strap',[(-.29,-.25,1.27),(-.13,-.36,1.10),(.13,-.38,.91),(.40,-.35,.69)],.035,leather))
body_parts.append(box('Rounded satchel',(.43,-.31,.54),(.38,.21,.30),leather,.065))
body_parts.append(box('Satchel flap',(.43,-.435,.63),(.38,.045,.17),vest,.04))
body_parts.append(line('Satchel gold stitching',[(.28,-.465,.64),(.30,-.469,.57),(.43,-.469,.55),(.58,-.465,.58)],.008,gold))
body_parts.append(box('Satchel buckle',(.45,-.474,.56),(.09,.025,.08),gold,.012))
body_parts.append(box('Buckle dark opening',(.45,-.491,.56),(.045,.008,.042),leather,.004))
body_parts.append(box('Administrator badge backing',(.33,-.388,1.07),(.255,.045,.18),gold,.018))
body_parts.append(box('Administrator ivory badge',(.33,-.417,1.07),(.216,.016,.14),badge,.01))
body_parts.append(line('Badge clip',[(.31,-.415,1.16),(.31,-.415,1.20),(.35,-.415,1.20),(.35,-.415,1.16)],.012,leather))
for x in [.25,.28,.31]:body_parts.append(box('Badge museum column',(x,-.430,1.055),(.013,.006,.045),gold,0))
body_parts.append(poly('Badge museum pediment',[(.233,-.434,1.08),(.28,-.434,1.106),(.327,-.434,1.08)],[(0,1,2)],gold))
for z in [1.085,1.05]:body_parts.append(box('Badge record line',(.37,-.434,z),(.06,.006,.009),ear,0))
body_parts.append(sphere('Tiny hamster tail',(0,.34,.43),(.10,.10,.09),fur,12,8))
for o in body_parts:parent(o,bodyctrl)
for o in head_parts:parent(o,headctrl)

# A small idle loop and a gentle head tilt, with arm controllers ready for gestures.
for frame,z,tilt in [(1,.75,0),(25,.765,-.025),(49,.75,0),(73,.76,.025),(97,.75,0)]:
 bodyctrl.location.z=z;bodyctrl.keyframe_insert(data_path='location',frame=frame)
 headctrl.rotation_euler.y=tilt;headctrl.keyframe_insert(data_path='rotation_euler',frame=frame)

s=bpy.context.scene;s.frame_start=1;s.frame_end=96;s.render.fps=24;s.frame_set(1)
studio=bpy.data.collections.new('Studio | hide when importing');s.collection.children.link(studio)
def studio_move(o):
 for c in list(o.users_collection):c.objects.unlink(o)
 studio.objects.link(o)
bpy.ops.mesh.primitive_plane_add(size=200);plane=bpy.context.object;plane.name='Studio ground';studio_move(plane);plane.data.materials.append(mat('Studio warm paper',(.52,.41,.30)))
for name,loc,power,size,col in [('Key',(-3,-4,5),450,4,(1,.78,.54)),('Fill',(3,-2,3),250,3,(1,.88,.7)),('Rim',(1,3,4),500,3,(1,.65,.33))]:
 d=bpy.data.lights.new(name,'AREA');o=bpy.data.objects.new(name,d);studio.objects.link(o);o.location=loc;d.energy=power;d.shape='DISK';d.size=size;d.color=col;o.rotation_euler=(Vector((0,0,1.2))-o.location).to_track_quat('-Z','Y').to_euler()
def camera(name,loc,target,ortho=3.1):
 d=bpy.data.cameras.new(name);o=bpy.data.objects.new(name,d);studio.objects.link(o);o.location=loc;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();d.type='ORTHO';d.ortho_scale=ortho;return o
cameras=[camera('Abraham | three-quarter',(3,-6,2.8),(0,0,1.2)),camera('Abraham | front',(0,-6,2),(0,0,1.2)),camera('Abraham | side',(6,-.2,2),(0,0,1.2)),camera('Abraham | back',(0,6,2),(0,0,1.2))]
s.camera=cameras[0];s.render.engine='CYCLES';s.cycles.samples=32;s.cycles.use_denoising=True
s.world=bpy.data.worlds.new('Studio world');s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs[0].default_value=(.42,.34,.28,1);s.world.node_tree.nodes['Background'].inputs[1].default_value=.4
s.render.resolution_x=1000;s.render.resolution_y=1000;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG'
s.view_settings.view_transform='AgX';s.view_settings.look='AgX - Medium High Contrast'
s['Character']='Abraham, hamster museum administrator. Reference-led low-poly interpretation. No live API connection.'
s['Rig']='Rigid hierarchy: ROOT > body > head and arms. Idle frames 1–96 at 24fps. Not a deforming skin/armature rig.'
deps=bpy.context.evaluated_depsgraph_get();tri=0
for o in C.objects:
 if o.type in {'MESH','CURVE'}:
  ev=o.evaluated_get(deps);mesh=ev.to_mesh();mesh.calc_loop_triangles();tri+=len(mesh.loop_triangles);ev.to_mesh_clear()
(ROOT/'model-stats.json').write_text(json.dumps({'evaluated_triangles':tri,'character_objects':len(C.objects),'rig':'rigid part hierarchy','reference_triangle_count_matched':False},indent=2))
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'abraham-character.blend'))
for cam,name in zip(cameras,['01-three-quarter','02-front','03-side','04-back']):
 s.camera=cam;s.render.filepath=str(ROOT/'renders'/f'{name}.png');bpy.ops.render.render(write_still=True)

# Export actual geometry, materials and idle animation as a reusable GLB.
bpy.ops.object.select_all(action='DESELECT')
for o in C.objects:o.select_set(True)
bpy.ops.export_scene.gltf(filepath=str(ROOT/'abraham-character.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=True)

# Place a copy in the illustrated museum, keeping all earlier deliverables untouched.
bpy.ops.wm.open_mainfile(filepath=str(MUSEUM/'quiet-collection-illustrated-museum.blend'))
with bpy.data.libraries.load(str(ROOT/'abraham-character.blend'),link=False) as (src,dst):dst.collections=['Abraham | character']
char=dst.collections[0];bpy.context.scene.collection.children.link(char)
root=bpy.data.objects['Abraham_ROOT'];root.location=(.15,-6.1,.08);root.scale=(.62,.62,.62);root.rotation_euler.z=-.20
s=bpy.context.scene;s.frame_set(1)
# Match the museum's palette shading, retaining recognisable eyes and outfit detail.
for m in list(bpy.data.materials):
 if not m.name.startswith('Abraham |'):continue
 col=tuple(m.diffuse_color);n=m.node_tree.nodes;n.clear();lk=m.node_tree.links
 diff=n.new('ShaderNodeBsdfDiffuse');diff.inputs[0].default_value=(.8,.8,.8,1)
 rgb=n.new('ShaderNodeShaderToRGB');lk.new(diff.outputs[0],rgb.inputs[0]);r=n.new('ShaderNodeValToRGB');r.color_ramp.interpolation='CONSTANT'
 r.color_ramp.elements[0].position=.04;r.color_ramp.elements[0].color=(col[0]*.4,col[1]*.35,col[2]*.45,1)
 r.color_ramp.elements[1].position=.35;r.color_ramp.elements[1].color=col
 e=n.new('ShaderNodeEmission');lk.new(rgb.outputs[0],r.inputs[0]);lk.new(r.outputs[0],e.inputs[0]);out=n.new('ShaderNodeOutputMaterial');lk.new(e.outputs[0],out.inputs[0])
d=bpy.data.cameras.new('09 | Meet Abraham');cam=bpy.data.objects.new(d.name,d);s.collection.objects.link(cam);cam.location=(1.4,-8.0,1.5);cam.rotation_euler=(Vector((.1,-6.1,.85))-cam.location).to_track_quat('-Z','Y').to_euler();d.lens=35;s.camera=cam
s.render.resolution_x=1440;s.render.resolution_y=960;s.render.resolution_percentage=100;s.render.image_settings.media_type='IMAGE';s.render.image_settings.file_format='PNG'
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(MUSEUM/'quiet-collection-with-abraham.blend'))
s.render.filepath=str(ROOT/'renders/05-in-museum.png');bpy.ops.render.render(write_still=True)
print('ABRAHAM_COMPLETE',tri,'evaluated triangles',flush=True)
