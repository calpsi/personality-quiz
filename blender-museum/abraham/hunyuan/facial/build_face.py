import bpy,math,json,numpy as np
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from mathutils.geometry import barycentric_transform
P=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(P.parent/'rigged/abraham-rigged.blend'))
s=bpy.context.scene;coll=bpy.data.collections['Abraham | Hunyuan character'];mesh=next(o for o in coll.objects if o.type=='MESH');rig=bpy.data.objects['Abraham_RIG']
# Fit a smooth front facial surface for the animated lid/mouth patches.
original_count=len(mesh.data.vertices)
pts=np.array([v.co[:] for v in mesh.data.vertices]);sel=(pts[:,1]<-.27)&(pts[:,2]>1.10)&(pts[:,2]<1.70)&(np.abs(pts[:,0])<.48)
q=pts[sel];exponents=[(i,j) for i in range(5) for j in range(5-i)]
A=np.column_stack([q[:,0]**i*(q[:,2]-1.4)**j for i,j in exponents]);coef=np.linalg.lstsq(A,q[:,1],rcond=None)[0]
def surface(x,z):return float(sum(c*x**i*(z-1.4)**j for c,(i,j) in zip(coef,exponents)))
# Add thin expression geometry to the same skinned mesh; neutral shapes sit beneath the face.
old=mesh.data;bvh=BVHTree.FromPolygons([v.co for v in old.vertices],[tuple(f.vertices) for f in old.polygons])
def face_surface_y(x,z):
 hit,normal,index,dist=bvh.ray_cast(Vector((x,-3,z)),Vector((0,1,0)))
 return hit.y if hit else surface(x,z)
# Smooth local skin surfaces fitted around, rather than through, the eye sockets and mouth.
regions={'eye_-1':(-.255,1.438,.145,.128),'eye_1':(.255,1.438,.145,.128),'mouth':(0,1.242,.070,.064)}
fits={}
for region,(cx,cz,rx,rz) in regions.items():
 samples=[];ys=[]
 for ring in [1.08,1.20,1.32]:
  for i in range(64):
   a=i*math.tau/64;dx=rx*ring*math.cos(a);dz=rz*ring*math.sin(a);samples.append([1,dx,dz,dx*dx,dx*dz,dz*dz]);ys.append(face_surface_y(cx+dx,cz+dz))
 fits[region]=np.linalg.lstsq(np.array(samples),np.array(ys),rcond=None)[0]
def patch_y(part,x,z):
 region=('eye_'+part.rsplit('_',1)[1]) if part.startswith('lid_') or part.startswith('covereye_') else 'mouth'
 cx,cz,rx,rz=regions[region];dx=x-cx;dz=z-cz;r2=(dx/rx)**2+(dz/rz)**2
 y=float(np.dot(fits[region],[1,dx,dz,dx*dx,dx*dz,dz*dz]))
 base=y-.004-.030*max(0,1-r2)
 r=math.sqrt(r2);edge=max(0,min(1,(r-.78)/.22));edge=edge*edge*(3-2*edge)
 base=base*(1-edge)+(face_surface_y(x,z)-.0008)*edge
 return base-(.008 if part=='tongue' else .004 if not part.startswith('cover') else 0)
verts=[v.co[:] for v in old.vertices];faces=[tuple(f.vertices) for f in old.polygons];mids=[f.material_index for f in old.polygons];old_uv=[tuple(x.uv) for x in old.uv_layers.active.data];patches=[]
def material(name,col):
 m=bpy.data.materials.new(name);m.diffuse_color=(*col,1);m.use_nodes=True;b=m.node_tree.nodes.get('Principled BSDF');b.inputs['Base Color'].default_value=(*col,1);b.inputs['Roughness'].default_value=.8;return m
mats=list(old.materials)+[material('Abraham expression ink',(.10,.028,.012)),material('Abraham tongue',(.64,.20,.14))]
def patch(name,coords,polys,mat,cx,cz):
 if not name.startswith('cover'):
  tris=[]
  for f in polys:
   for j in range(1,len(f)-1):tris.append((f[0],f[j],f[j+1]))
  for _ in range(3):
   refined=[];cache={}
   def mid(a,b):
    k=tuple(sorted((a,b)))
    if k not in cache:cache[k]=len(coords);coords.append(((coords[a][0]+coords[b][0])/2,(coords[a][1]+coords[b][1])/2))
    return cache[k]
   for a,b,c in tris:
    ab=mid(a,b);bc=mid(b,c);ca=mid(c,a);refined.extend([(a,ab,ca),(ab,b,bc),(ca,bc,c),(ab,bc,ca)])
   tris=refined
  polys=tris
 offset=len(verts)
 for x,z in coords:verts.append((cx,surface(cx,cz)+.04,cz))
 for f in polys:faces.append(tuple(offset+i for i in f));mids.append(mat)
 patches.append((name,offset,coords,cx,cz))
for side in [-1,1]:
 cx=side*.255;coords=[]
 for i in range(25):
  dx=-.108+i/24*.216
  for edge in [-1,1]:coords.append((cx+dx,1.438+edge*.004))
 patch('lid_'+str(side),coords,[(2*i,2*i+1,2*i+3,2*i+2) for i in range(24)],1,cx,1.438)
coords=[(0,1.245)]+[(.078*math.cos(i*math.tau/48),1.265+(.003 if math.sin(i*math.tau/48)>0 else .059)*math.sin(i*math.tau/48)) for i in range(48)]
patch('smile',coords,[(0,i+1,(i+1)%48+1) for i in range(48)],1,0,1.24)
coords=[(0,1.219)]+[(.032*math.cos(i*math.tau/32),1.219+.009*math.sin(i*math.tau/32)) for i in range(32)]
patch('tongue',coords,[(0,i+1,(i+1)%32+1) for i in range(32)],2,0,1.24)
coords=[]
for i in range(25):
 x=-.048+i*.004
 for edge in [-1,1]:coords.append((x,1.226+.023*(1-(x/.048)**2)+edge*.0035))
patch('frown',coords,[(2*i,2*i+1,2*i+3,2*i+2) for i in range(24)],1,0,1.24)
# Smooth skin covers keep the original eye/cheek geometry intact during closures.
for title,cx,cz,rx,rz,matidx in [('covereye_-1',-.255,1.438,.145,.128,3),('covereye_1',.255,1.438,.145,.128,3),('covermouth',0,1.242,.070,.064,4)]:
 coords=[(cx,cz)];polys=[];segments=64;rings=8
 for j in range(1,rings+1):
  for i in range(segments):
   a=i*math.tau/segments;r=j/rings;coords.append((cx+rx*r*math.cos(a),cz+rz*r*math.sin(a)))
 for i in range(segments):polys.append((0,1+i,1+(i+1)%segments))
 for j in range(rings-1):
  for i in range(segments):
   a=1+j*segments+i;b=1+j*segments+(i+1)%segments;polys.append((a,a+segments,b+segments,b))
 patch(title,coords,polys,matidx,cx,cz)
for title in ['Eyelid fur','Muzzle fur']:
 m=old.materials[0].copy();m.name='Abraham | '+title
 bs=next(n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED')
 for socket in ['Normal','Roughness','Metallic','Specular IOR Level','Specular Tint']:
  for link in list(bs.inputs[socket].links):m.node_tree.links.remove(link)
 bs.inputs['Roughness'].default_value=.85;bs.inputs['Metallic'].default_value=0;bs.inputs['Specular IOR Level'].default_value=.15;bs.inputs['Specular Tint'].default_value=(1,1,1,1)
 mats.append(m)
# Sample clean nearby fur from the source UV texture for each cover.
def sample_uv(cx,cz):
 vi=min((v.index for v in old.vertices if v.co.y<-.25),key=lambda i:(old.vertices[i].co.x-cx)**2+(old.vertices[i].co.z-cz)**2)
 li=next(l.index for l in old.loops if l.vertex_index==vi);return old_uv[li]
# Paint a small fur atlas from samples around each feature, matching the surrounding colours.
source_bs=next(n for n in old.materials[0].node_tree.nodes if n.type=='BSDF_PRINCIPLED');source_image=source_bs.inputs['Base Color'].links[0].from_node.image
pixels=np.array(source_image.pixels[:]).reshape(source_image.size[1],source_image.size[0],4)
def colour_at(x,z):
 hit,normal,index,dist=bvh.ray_cast(Vector((x,-3,z)),Vector((0,1,0)))
 if hit is None:return np.array([.8,.6,.4,1])
 f=old.polygons[index];ids=list(f.vertices);lis=list(f.loop_indices)
 uvpoint=barycentric_transform(hit,old.vertices[ids[0]].co,old.vertices[ids[1]].co,old.vertices[ids[2]].co,Vector((*old_uv[lis[0]],0)),Vector((*old_uv[lis[1]],0)),Vector((*old_uv[lis[2]],0)))
 return pixels[min(source_image.size[1]-1,max(0,int(uvpoint.y*source_image.size[1]))),min(source_image.size[0]-1,max(0,int(uvpoint.x*source_image.size[0])))]
atlas=np.ones((256,768,4));cover_names=['covereye_-1','covereye_1','covermouth']
for tile,region in enumerate(['eye_-1','eye_1','mouth']):
 cx,cz,rx,rz=regions[region];boundary=np.array([colour_at(cx+rx*math.cos(i*math.tau/128),cz+rz*math.sin(i*math.tau/128)) for i in range(128)]);centre=boundary.mean(axis=0)
 for j in range(256):
  for i in range(256):
   dx=(i/255-.5)*2;dz=(j/255-.5)*2;r=min(1,math.hypot(dx,dz));a=(math.atan2(dz,dx)%math.tau)/math.tau*128;k=int(a)%128;colour=boundary[k]*(1-(a%1))+boundary[(k+1)%128]*(a%1);atlas[j,tile*256+i]=centre*(1-r)+colour*r
im=bpy.data.images.new('Abraham eyelid and muzzle fur',width=768,height=256);im.colorspace_settings.name=source_image.colorspace_settings.name;im.pixels.foreach_set(atlas.astype(np.float32).ravel());im.filepath_raw=str(P/'expression-fur.png');im.file_format='PNG';im.save();im.pack()
for m in mats[3:]:
 bs=next(n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED');tex=bs.inputs['Base Color'].links[0].from_node;tex.image=im
new=bpy.data.meshes.new('Abraham mesh with expression patches');new.from_pydata(verts,[],faces);new.update()
for m in mats:new.materials.append(m)
for f,mi in zip(new.polygons,mids):f.material_index=mi
uv=new.uv_layers.new(name='UVMap')
for i,co in enumerate(old_uv):uv.data[i].uv=co
for title,offset,coords,cx,cz in patches:
 if title in cover_names:
  for f in new.polygons:
   if offset<=f.vertices[0]<offset+len(coords):
    f.use_smooth=True
    for li in f.loop_indices:
     vi=new.loops[li].vertex_index;x,z=coords[vi-offset];region='eye_'+title.rsplit('_',1)[1] if title.startswith('covereye') else 'mouth';cx,cz,rx,rz=regions[region];uv.data[li].uv=((cover_names.index(title)+.5+(x-cx)/(2*rx))/3,.5+(z-cz)/(2*rz))
weights=[[(g.group,g.weight) for g in v.groups] for v in old.vertices]
names=[g.name for g in mesh.vertex_groups]
for f,source in zip(new.polygons,old.polygons):f.use_smooth=source.use_smooth
mesh.data=new
for name in names:mesh.vertex_groups.new(name=name)
for i,gs in enumerate(weights):
 for gi,w in gs:mesh.vertex_groups[gi].add([i],w,'REPLACE')
mesh.vertex_groups['head'].add(list(range(original_count,len(verts))),1,'REPLACE')
base=mesh.shape_key_add(name='Basis');keys={name:mesh.shape_key_add(name=name) for name in ['Blink_L','Blink_R','Curious','Worried','Delighted','Mouth_Open']}
def smooth(a,b,x):
 t=max(0,min(1,(x-a)/(b-a)));return t*t*(3-2*t)
def taper(a,b,x):return 1-smooth(a,b,abs(x))
def compress(d,h,outer,scale):
 a=abs(d)
 if a<h:r=a*scale
 elif a<outer:r=h*scale+(a-h)*(outer-h*scale)/(outer-h)
 else:r=a
 return math.copysign(r,d)
def eye_delta(x,y,z,side,kind):
 cx=side*.255;cz=1.438;dx=x-cx;dz=z-cz
 w=taper(.118,.192,dx)*(1-smooth(-.29,-.19,y))
 if abs(dz)>.225 or w==0:return Vector((0,0,0))
 zone=taper(.12,.225,dz)
 if kind=='blink':return Vector((0,0,(compress(dz,.115,.225,.003)-dz)*w))
 if kind=='happy':
  arch=.042*(1-min(1,(dx/.125)**2))*zone
  return Vector((0,0,(compress(dz,.115,.225,.003)-dz+arch)*w))
 if kind=='worried':return Vector((-side*.008*zone*w,0,(-side*.32*dx-.012-.12*dz)*zone*w))
 if kind=='curious':return Vector((0,0,((.030 if side>0 else -.009)+(.06 if side>0 else -.10)*dz)*zone*w))
 return Vector((0,0,0))
for v in list(mesh.data.vertices)[:original_count]:
 x,y,z=v.co
 front=1-smooth(-.46,-.34,y);mx=taper(.05,.145,x);mz=taper(.045,.08,z-1.24);mw=front*mx*mz
 for name,key in keys.items():
  delta=Vector((0,0,0))
  for side in [-1,1]:
   if name=='Blink_L' and side==1 or name=='Blink_R' and side==-1:delta+=eye_delta(x,y,z,side,'blink')
   elif name=='Delighted':delta+=eye_delta(x,y,z,side,'happy')
   elif name=='Worried':delta+=eye_delta(x,y,z,side,'worried')
   elif name=='Curious':delta+=eye_delta(x,y,z,side,'curious')
  if mw:
   dz=z-1.24
   if name=='Delighted':delta+=Vector((-x*.99,0,-dz*.99))*mw
   elif name=='Worried':delta+=Vector((-x*.99,0,-dz*.99))*mw
   elif name=='Curious':delta+=Vector((.008-x*.10,0,dz*.12))*mw
   elif name=='Mouth_Open':delta+=Vector((x*.15,-.008,-.012+dz*.55))*mw
  target=v.co+delta
  if delta.length>1e-8:
   # Reproject deformed regions onto a smooth face, preventing accordion folds.
   ew=max(taper(.118,.192,x-side*.255)*taper(.12,.225,z-1.438)*(1-smooth(-.29,-.19,y)) for side in [-1,1])
   fac=max(ew,mw) if name in ['Delighted','Worried'] else ew if name.startswith('Blink') else max(ew,mw)*.35
   target.y=y+(surface(target.x,target.z)-y)*fac
  if name.startswith('Blink') or name=='Delighted':target=v.co.copy()
  elif name=='Worried':target=v.co+eye_delta(x,y,z,-1,'worried')+eye_delta(x,y,z,1,'worried')
  key.data[v.index].co=target
# Morph the added ink shapes into view only for their corresponding expression.
for name,key in keys.items():
 for part,offset,coords,cx,cz in patches:
  active=part.startswith('lid') and (name=='Delighted' or name==('Blink_L' if part=='lid_1' else 'Blink_R')) or part in ['smile','tongue'] and name=='Delighted' or part=='frown' and name=='Worried'
  if part.startswith('covereye'):active=name=='Delighted' or name==('Blink_L' if part=='covereye_1' else 'Blink_R')
  elif part=='covermouth':active=name in ['Delighted','Worried']
  if not active:continue
  for i,(x,z) in enumerate(coords):
   if part.startswith('lid') and name=='Delighted':z+=.042*(1-((x-cx)/.125)**2)
   key.data[offset+i].co=(x,patch_y(part,x,z),z)
# Independent morph clips can be blended with the existing skeleton clips in a game engine.
shape=mesh.data.shape_keys;shape.animation_data_create();clips={}
for name,length in [('Face_Idle',96),('Face_Curious',72),('Face_Worried',72),('Face_Delighted',72),('Face_Blink',24)]:
 action=bpy.data.actions.new(name);shape.animation_data.action=action
 frames=[1,length+1]
 if name=='Face_Idle':frames=[1,40,44,47,51,97]
 elif name=='Face_Blink':frames=[1,8,11,14,18,25]
 else:frames=[1,18,54,73]
 for f in frames:
  for key in keys.values():key.value=0
  if name in ['Face_Idle','Face_Blink']:
   closed=(f in ([44,47] if name=='Face_Idle' else [11,14]))
   keys['Blink_L'].value=keys['Blink_R'].value=float(closed)
  else:keys[name.removeprefix('Face_')].value=1 if f in [18,54] else 0
  for key in keys.values():key.keyframe_insert(data_path='value',frame=f)
 action.use_fake_user=True;clips[name]=action
for action in clips.values():
 for layer in action.layers:
  for strip in layer.strips:
   for bag in strip.channelbags:
    for fc in bag.fcurves:
     for point in fc.keyframe_points:point.interpolation='CONSTANT'
shape.animation_data.action=None
for name,action in clips.items():
 t=shape.animation_data.nla_tracks.new();t.name=name;st=t.strips.new(name,1,action);t.mute=True
for key in keys.values():key.value=0
s.frame_set(1);rig.animation_data.action=bpy.data.actions['Idle'];s.camera=bpy.data.objects['01-three-quarter']
s['Facial controls']='Shape keys on character mesh: Blink_L, Blink_R, Curious, Worried, Delighted, Mouth_Open. Neutral is all keys zero.'
bpy.ops.object.select_all(action='DESELECT');mesh.select_set(True);rig.select_set(True);bpy.context.view_layer.objects.active=rig
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(P/'abraham-facial-rig.blend'))
bpy.ops.export_scene.gltf(filepath=str(P/'abraham-facial-rig.glb'),export_format='GLB',use_selection=True,export_animations=True,export_animation_mode='ACTIONS',export_skins=True,export_morph=True,export_morph_normal=True,export_force_sampling=False)
for name in ['Delighted','Blink','Worried','Neutral','Curious']:
 for key in keys.values():key.value=0
 if name=='Blink':keys['Blink_L'].value=keys['Blink_R'].value=1
 elif name!='Neutral':keys[name].value=1
 bpy.context.view_layer.update();s.render.filepath=str(P/'renders'/f'{name.lower()}.png');bpy.ops.render.render(write_still=True)
print('FACE_BUILD_COMPLETE',flush=True)
