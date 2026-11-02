"""Add a reversible dream layer to the latest facial-rig museum."""
import bpy, math, random, json
from pathlib import Path
from mathutils import Vector
P=Path(__file__).resolve().parent; ROOT=P.parent
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'quiet-collection-with-abraham-facial.blend'))
s=bpy.context.scene;s.frame_set(1);random.seed(83)
col=bpy.data.collections.new('10 | Dream anomalies');s.collection.children.link(col)
def move(o):
 for c in list(o.users_collection):c.objects.unlink(o)
 col.objects.link(o);return o
def material(name,c,glow=False):
 m=bpy.data.materials.new(name);m.diffuse_color=(*c,1);m.use_nodes=True
 n=m.node_tree.nodes;n.clear();e=n.new('ShaderNodeEmission' if glow else 'ShaderNodeBsdfDiffuse');e.inputs['Color'].default_value=(*c,1)
 out=n.new('ShaderNodeOutputMaterial');m.node_tree.links.new(e.outputs[0],out.inputs['Surface']);return m
ivory=material('Dream | softly luminous lettering',(.76,.62,.38),True)
teal=material('Dream | quiet turquoise',(.09,.43,.40),True)
night=material('Dream | midnight inside the drawer',(.012,.019,.043),True)
paper=bpy.data.materials['Illustration | Cream labels'];brass=bpy.data.materials['Illustration | Aged brass'];wood=bpy.data.materials['Illustration | Walnut | subtle downloaded grain'];ink=bpy.data.materials['Illustration | warm ink']
font=next((f for f in bpy.data.fonts if 'Cormorant' in f.name),None)
def cube(name,loc,size,mat):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=move(bpy.context.object);o.name=name;o.dimensions=size;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(mat);return o
def ball(name,loc,r,mat):
 bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1,radius=r,location=loc);o=move(bpy.context.object);o.name=name;o.data.materials.append(mat);return o
def line(name,pts,mat,r=.008):
 d=bpy.data.curves.new(name,'CURVE');d.dimensions='3D';d.bevel_depth=r;d.bevel_resolution=0;sp=d.splines.new('POLY');sp.points.add(len(pts)-1)
 for q,p in zip(sp.points,pts):q.co=(*p,1)
 o=bpy.data.objects.new(name,d);col.objects.link(o);d.materials.append(mat);return o
def text(name,body,loc,size=.15,mat=ivory):
 d=bpy.data.curves.new(name,'FONT');d.body=body;d.size=size;d.align_x='CENTER';d.align_y='CENTER';d.extrude=.0005
 if font:d.font=font
 o=bpy.data.objects.new(name,d);col.objects.link(o);o.location=loc;o.rotation_euler=(math.pi/2,0,0);d.materials.append(mat);return o
def root(name,loc,id):
 o=bpy.data.objects.new(name,None);col.objects.link(o);o.location=loc;o['interaction_id']=id;o['unscored']=True;return o
def attach(o,r):o.parent=r;return o
def bob(o,height=.09,phase=0):
 base=o.location.copy();rot=Vector(o.rotation_euler)
 for f in range(1,722,12):
  a=(f-1)*math.tau/240+phase;o.location=base+Vector((.018*math.sin(a),0,height*math.sin(a)));o.rotation_euler=rot+Vector((0,.025*math.sin(a),.025*math.cos(a)))
  o.keyframe_insert('location',frame=f);o.keyframe_insert('rotation_euler',frame=f)
 o['rest_location']=list(base);o['rest_rotation']=list(rot);o['dream_motion']=True
# Preserve all original palette ramps and lighting without modifications.
# Pendants and original labels remain anchored: a few selected objects break the rules.
clock=root('Dream | clock assembly',(-2.65,4.75,2.55),'clock')
# A solid wooden clock case sits directly against the north hall wall.
bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=.55, depth=.14, location=(0,.07,0), rotation=(math.pi/2,0,0))
back=move(bpy.context.object);back.name='Dream | wall clock case';back.data.materials.append(wood);attach(back,clock)
for radius,mat,r in [(.55,brass,.035),(.48,ivory,.008)]:
 attach(line('Clock bezel',[(radius*math.sin(a*math.tau/64),0,radius*math.cos(a*math.tau/64)) for a in range(65)],mat,r),clock)
for i in range(12):
 a=i*math.tau/12;attach(line('Clock hour mark',[(r*math.sin(a),-.012,r*math.cos(a)) for r in [.40,.45]],ivory,.009),clock)
for name,length,period in [('Minute hand',.36,240),('Hour hand',.24,720)]:
 o=attach(line('Dream | '+name,[(0,-.025,0),(0,-.025,length)],brass,.014),clock)
 for f in [1,721]:o.rotation_euler.y=(f-1)*math.tau/period;o.keyframe_insert('rotation_euler',frame=f)
 if o.animation_data:
  for layer in o.animation_data.action.layers:
   for strip in layer.strips:
    for bag in strip.channelbags:
     for fc in bag.fcurves:
      for k in fc.keyframe_points:k.interpolation='LINEAR'
attach(ball('Clock pin',(0,-.03,0),.04,ivory),clock)
attach(text('Clock caption','PLEASE DO NOT WIND', (0,-.02,-.68),.115),clock)
# Cards have slipped free, with generous negative space and readable primary text.
labels=root('Dream | escaped labels',(2.45,.25,1.9),'labels')
for i,(x,z,a) in enumerate([(-.15,0,-.12),(.22,.43,.16),(-.07,.85,-.08)]):
 card=cube('Dream | floating accession card',(x,0,z),(.64,.018,.24),paper);attach(card,labels);card.rotation_euler.y=a
 caption=text('Dream | card number', ['000','001','000'][i],(x,-.016,z),.13,ink);attach(caption,labels);caption.rotation_euler.y=a
attach(text('Dream | misplaced label caption','AWAITING A PLACE',(0,-.03,-.3),.12),labels);bob(labels,.13,1)
# Floating specimen above its visibly empty cradle.
meteor=bpy.data.objects['Meteorite specimen'];meteor.location.z+=.47;meteor['interaction_id']='meteorite';meteor['unscored']=True;bob(meteor,.08,.7)
# Several small geological fragments orbit above the central pedestal.
center=bpy.data.objects['Concealed specimen placeholder'];center.location.z+=.20;bob(center,.08,1.4)
for i in range(5):
 a=i*math.tau/5;o=ball('Dream | suspended fragment',(.46*math.cos(a),.3+.46*math.sin(a),1.9+.14*math.sin(a)),.045,brass);bob(o,.05,a)
# Tiny star drawer, unscored and separate from the existing mineral quiz drawer.
drawer=root('Dream | star drawer cabinet',(-2.65,4.35,.07),'drawer')
attach(cube('Dream | cabinet body',(0,0,.55),(.82,.65,1.1),wood),drawer)
attach(cube('Dream | cabinet rim',(0,0,1.12),(.89,.71,.05),brass),drawer)
tray=root('Dream | drawer sliding tray',(0,0,0),'drawer');tray.parent=drawer;tray['open']=True
attach(cube('Dream | drawer bottom',(0,-.48,.89),(.65,.65,.035),night),tray)
attach(cube('Dream | drawer face',(0,-.83,1.00),(.75,.06,.25),wood),tray)
attach(ball('Dream | drawer handle',(0,-.88,1.0),.055,brass),tray)
for x in [-.34,.34]:attach(cube('Dream | drawer side',(x,-.5,.98),(.025,.65,.18),brass),tray)
for i in range(16):
 attach(ball('Dream | drawer star',(random.uniform(-.28,.28),random.uniform(-.76,-.22),random.uniform(.93,1.12)),random.uniform(.007,.018),ivory),tray)
attach(text('Dream | drawer plaque','NIGHT COLLECTION',(0,-.338,.50),.085),drawer)
# Botanical motes: a few floating leaves, kept out of navigation routes.
leafroot=root('Dream | drifting leaves',(-1.5,9.6,2.35),'leaves')
for i in range(5):
 a=i*1.45;o=ball('Dream | airborne leaf',(.45*math.cos(a),.22*math.sin(a),.2*math.sin(a*2)),.13,bpy.data.materials['Illustration | Malachite']);o.scale=(.38,1,.15);attach(o,leafroot)
bob(leafroot,.14,.3)
# A restrained echo of the main title rather than more signs everywhere.
whisper=text('Dream | hovering annotation','YOU MAY HAVE BEEN HERE BEFORE',(-.2,3.6,2.7),.12,teal);bob(whisper,.035,2)
for i in range(18):
 o=ball('Dream | dust mote',(random.uniform(-2.4,2.4),random.uniform(-.5,3.8),random.uniform(1.5,3.0)),random.uniform(.006,.014),ivory);bob(o,.08,i)
# Abraham remains the original facial-rig character. All his visible meshes are clickable.
char=bpy.data.collections['Abraham | Hunyuan character']
for o in char.all_objects:
 if o.type=='MESH':o['interaction_id']='abraham';o['unscored']=True
ab=bpy.data.objects['Abraham | placement'];ab.location=(2.15,-.75,.12);ab.rotation_euler.z=-.22
hint=text('Dream | Abraham talk prompt','ABRAHAM  ·  TALK',(2.15,-.81,1.65),.12);hint['interaction_id']='abraham'
# Camera shows the hall and its new quiet anomalies.
d=bpy.data.cameras.new('10 | Dream hall');cam=bpy.data.objects.new(d.name,d);s.collection.objects.link(cam);cam.location=(0,-4.4,2.05);cam.rotation_euler=(Vector((.05,.7,1.65))-cam.location).to_track_quat('-Z','Y').to_euler();d.lens=20
s.camera=cam;s.render.engine='BLENDER_EEVEE';s.render.resolution_x=1440;s.render.resolution_y=960;s.render.resolution_percentage=100
s.render.image_settings.media_type='IMAGE';s.render.image_settings.file_format='PNG';s.render.use_compositing=False
s.eevee.taa_render_samples=48;s.frame_start=1;s.frame_end=720;s.frame_set(51)
s['Dreamscape notes']='Additive dream layer. Original warm illustrated museum preserved. Interaction preview script in Text Editor; run manually, then use N sidebar > Museum.'
s['Gameplay status']='Scene and Blender interaction prototype. No browser gameplay or live AI service wired yet. All anomalies and conversation are unscored.'
script=P/'museum_interactions.py'
if script.exists():t=bpy.data.texts.load(str(script));t.use_module=False
s.camera=cam
for a in bpy.context.screen.areas:
 if a.type=='VIEW_3D':a.spaces.active.region_3d.view_perspective='CAMERA'
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'quiet-collection-dreamscape.blend'))
s.render.filepath=str(P/'dream-hall.png');bpy.ops.render.render(write_still=True)
s.camera=bpy.data.objects['05 | Earth and Space'];s.render.filepath=str(P/'dream-earth-space.png');bpy.ops.render.render(write_still=True)
print('DREAMSCAPE_COMPLETE',flush=True)
