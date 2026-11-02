import bpy,json,math
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2]; OUT=ROOT/'museum-site/public/assets'
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'blender-museum/quiet-collection-dreamscape.blend'))
s=bpy.context.scene;s.frame_set(51)
print('OBJECTS',[(o.name,tuple(round(v,2) for v in o.location)) for o in s.objects if o.type=='CAMERA' or o.name.startswith('Dream |')][:80])
# Export snapshots of painted geometry; keep the source Blender file untouched.
selected=[]
for o in list(s.objects):
 if o.type not in {'MESH','CURVE','FONT'} or o.hide_render or any(c.hide_render for c in o.users_collection):continue
 if any('Abraham' in c.name or 'Hunyuan' in c.name or 'Facial' in c.name for c in o.users_collection) or 'Abraham' in o.name or 'Hunyuan' in o.name:continue
 if o.type=='FONT' and ('WHAT ARE' in o.data.body or 'ABRAHAM' in o.data.body):continue
 selected.append(o)
# Snapshot evaluated mesh (curves + ink strokes included), preserve warm colour values.
dg=bpy.context.evaluated_depsgraph_get();meshes=[];matcache={}
for o in selected:
 try: mesh=bpy.data.meshes.new_from_object(o.evaluated_get(dg),depsgraph=dg)
 except: continue
 if not mesh.vertices:continue
 obj=bpy.data.objects.new('Web '+o.name,mesh);s.collection.objects.link(obj);obj.matrix_world=o.matrix_world.copy()
 for j,m in enumerate(list(mesh.materials)):
  if not m:continue
  if m.name not in matcache:
   nm=bpy.data.materials.new('Web '+m.name);nm.use_nodes=True
   bs=nm.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=m.diffuse_color;bs.inputs['Roughness'].default_value=.95
   if 'glass' in m.name.lower() and 'lamp' not in m.name.lower():bs.inputs['Alpha'].default_value=.04
   if any(k in m.name.lower() for k in ['lamp','luminous','star glow']):bs.inputs['Emission Color'].default_value=m.diffuse_color;bs.inputs['Emission Strength'].default_value=1
   matcache[m.name]=nm
  mesh.materials[j]=matcache[m.name]
 # Preserve interaction names for raycasting and gentle animation; batch static geometry.
 obj['interaction_id']=o.get('interaction_id','')
 if 'clock' in o.name.lower():obj['interaction_id']='clock'
 if 'drawer' in o.name.lower() and 'Dream' in o.name:obj['interaction_id']='drawer'
 meshes.append(obj)
# Join static geometry, then split by material in Three via glTF primitives (low draw count).
bpy.ops.object.select_all(action='DESELECT')
static=[o for o in meshes if not o.get('interaction_id') and not o.name.startswith('Web Dream')]
for o in static:o.select_set(True)
if static:
 bpy.context.view_layer.objects.active=static[0];bpy.ops.object.join();static[0].name='Museum painted architecture'
exports=[o for o in meshes if o.name in bpy.data.objects] if False else [o for o in s.objects if o.name.startswith('Web ') or o.name=='Museum painted architecture']
bpy.ops.object.select_all(action='DESELECT')
for o in exports:o.select_set(True)
bpy.ops.export_scene.gltf(filepath=str(OUT/'museum.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False,export_extras=True,export_cameras=False,export_lights=False,export_draco_mesh_compression_enable=True,export_draco_mesh_compression_level=6)
print('EXPORTED',len(exports),'objects', (OUT/'museum.glb').stat().st_size)
