import bpy,json,runpy
from pathlib import Path
P=Path(__file__).resolve().parent
def palette_and_lights():
 ramps={m.name:[(n.name,[(e.position,list(e.color)) for e in n.color_ramp.elements]) for n in m.node_tree.nodes if n.type=='VALTORGB'] for m in bpy.data.materials if m.name.startswith('Illustration |') and m.use_nodes}
 lights={o.name:(list(o.location),list(o.rotation_euler),o.data.energy,list(o.data.color)) for o in bpy.context.scene.objects if o.type=='LIGHT'}
 return ramps,lights
bpy.ops.wm.open_mainfile(filepath=str(P.parent/'quiet-collection-with-abraham-facial.blend'))
original=palette_and_lights()
bpy.ops.wm.open_mainfile(filepath=str(P.parent/'quiet-collection-dreamscape.blend'))
assert palette_and_lights()==original, 'Original palette and lights must be unchanged'
assert bpy.data.objects['Dream | clock assembly'].animation_data is None
assert bpy.data.objects['Dream | drawer sliding tray'].parent==bpy.data.objects['Dream | star drawer cabinet']

runpy.run_path(str(P/'museum_interactions.py'),run_name='__main__')
s=bpy.context.scene
for key in ['abraham','help','chat','strange','clock','labels','meteorite','drawer','leaves']:
 assert bpy.ops.museum.interact(key=key)=={'FINISHED'}
 assert s.museum_talk_open and s.museum_reply
 if key in ['clock','labels','drawer','leaves']:bpy.ops.museum.interact(key=key)
assert bpy.data.objects['Dream | drawer sliding tray']['open']
assert not s['clock_paused']
assert bpy.data.objects['Dream | Minute hand'].animation_data.action
assert bpy.data.objects['Dream | escaped labels'].animation_data.action
bpy.ops.museum.close_talk();assert not s.museum_talk_open
char=bpy.data.collections['Abraham | Hunyuan character']
assert all(o.get('interaction_id')=='abraham' for o in char.all_objects if o.type=='MESH')
report={'scene':'quiet-collection-dreamscape.blend','operatorChecks':'all nine dialogue/interaction operators passed; toggles restored; close passed','characterHitTargets':'all character meshes tagged','paletteAndLights':'identical to original facial-rig museum','clockCase':'fixed to wall; no transform animation','drawer':'wall-adjacent cabinet; tray slides in local coordinates','liveAI':False,'raycastUI':'not manually exercised; sidebar operators checked in Blender','originalCharacterRig':bpy.data.objects['Abraham_RIG'].type,'objectCount':len(s.objects)}
(P/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print('INTERACTION_CHECKS_PASSED',flush=True)
# Reload so the preview uses the exact delivered starting state.
bpy.ops.wm.open_mainfile(filepath=str(P.parent/'quiet-collection-dreamscape.blend'));s=bpy.context.scene
s.render.resolution_x=800;s.render.resolution_y=534;s.eevee.taa_render_samples=16
s.frame_start=1;s.frame_end=145;s.frame_step=2;s.render.fps=12
s.render.image_settings.media_type='VIDEO';s.render.image_settings.file_format='FFMPEG';s.render.ffmpeg.format='MPEG4';s.render.ffmpeg.codec='H264';s.render.ffmpeg.constant_rate_factor='MEDIUM';s.render.filepath=str(P/'dreamscape-preview.mp4')
bpy.ops.render.render(animation=True)
print('PREVIEW_COMPLETE',flush=True)
