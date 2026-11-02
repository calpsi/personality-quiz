import bpy,json,math
from pathlib import Path
from mathutils import Vector
P=Path(__file__).resolve().parent
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=str(P/'abraham-original.glb'))
scene=bpy.context.scene
char=bpy.data.collections.new('Abraham | Hunyuan character');scene.collection.children.link(char)
meshes=[o for o in scene.objects if o.type=='MESH']
for o in list(scene.objects):
 for c in list(o.users_collection):c.objects.unlink(o)
 char.objects.link(o)
bpy.context.view_layer.update()
coords=[o.matrix_world@Vector(p) for o in meshes for p in o.bound_box]
lo=Vector([min(p[i] for p in coords) for i in range(3)]);hi=Vector([max(p[i] for p in coords) for i in range(3)])
root=bpy.data.objects.new('Abraham_Hunyuan_ROOT',None);char.objects.link(root)
# Preserve original meshes/UVs and normalise the character to 2.1 m tall.
for ob in list(char.objects):
 if ob!=root and ob.parent is None:ob.parent=root
scale=2.1/(hi.z-lo.z);root.scale=(scale,)*3;root.location=(-scale*(lo.x+hi.x)/2,-scale*(lo.y+hi.y)/2,-scale*lo.z)
tri=0
for ob in meshes:ob.data.calc_loop_triangles();tri+=len(ob.data.loop_triangles)
(P/'model-stats.json').write_text(json.dumps({'triangles':tri,'meshes':len(meshes),'source_bounds':[list(lo),list(hi)],'normalised_height':2.1,'animations':0,'armatures':len([o for o in char.objects if o.type=='ARMATURE'])},indent=2))
studio=bpy.data.collections.new('Studio');scene.collection.children.link(studio)
def move(ob):
 for c in list(ob.users_collection):c.objects.unlink(ob)
 studio.objects.link(ob)
bpy.ops.mesh.primitive_plane_add(size=200);ground=bpy.context.object;move(ground)
m=bpy.data.materials.new('Warm paper');m.diffuse_color=(.62,.53,.41,1);ground.data.materials.append(m)
for name,loc,power,size,color in [('Key',(-3,-4,5),400,4,(1,.87,.7)),('Fill',(3,-2,3),200,3,(.8,.88,1)),('Rim',(0,3,4),400,3,(1,.72,.44))]:
 d=bpy.data.lights.new(name,'AREA');o=bpy.data.objects.new(name,d);studio.objects.link(o);o.location=loc;d.energy=power;d.shape='DISK';d.size=size;d.color=color;o.rotation_euler=(Vector((0,0,1.1))-o.location).to_track_quat('-Z','Y').to_euler()
cams=[]
for name,loc in [('01-three-quarter',(3,-6,2.8)),('02-front',(0,-6,1.65)),('03-back',(0,6,1.65))]:
 d=bpy.data.cameras.new(name);o=bpy.data.objects.new(name,d);studio.objects.link(o);o.location=loc;o.rotation_euler=(Vector((0,0,1.05))-o.location).to_track_quat('-Z','Y').to_euler();d.type='ORTHO';d.ortho_scale=2.7;cams.append(o)
scene.world=bpy.data.worlds.new('Studio world');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs[0].default_value=(.45,.40,.34,1);scene.world.node_tree.nodes['Background'].inputs[1].default_value=.35
scene.render.engine='CYCLES';scene.cycles.samples=32;scene.cycles.use_denoising=True;scene.render.resolution_x=1000;scene.render.resolution_y=1000;scene.render.resolution_percentage=100;scene.view_settings.view_transform='AgX';scene.camera=cams[0]
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(P/'abraham-hunyuan.blend'))
for cam in cams:
 scene.camera=cam;scene.render.filepath=str(P/'renders'/f'{cam.name}.png');bpy.ops.render.render(write_still=True)
print('IMPORT_COMPLETE',tri,flush=True)
