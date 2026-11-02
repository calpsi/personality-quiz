import bpy,runpy
from pathlib import Path
P=Path(__file__).resolve().parent
path=P.parent/'quiet-collection-dreamscape.blend'
bpy.ops.wm.open_mainfile(filepath=str(path))
t=bpy.data.texts.get('museum_interactions.py');assert t
t.clear();t.write((P/'museum_interactions.py').read_text())
runpy.run_path(str(P/'museum_interactions.py'),run_name='__main__')
s=bpy.context.scene
for key in ['abraham','clock','labels','meteorite','drawer','leaves','help','strange','chat']:
 bpy.ops.museum.interact(key=key);assert s.museum_reply
 if key in ['clock','labels','drawer','leaves']:bpy.ops.museum.interact(key=key)
bpy.ops.museum.close_talk()
s.museum_reply='Oh, hello! What can I help you with?'
s.frame_set(51)
bpy.ops.wm.save_as_mainfile(filepath=str(path))
print('EMBEDDED_DIALOGUE_UPDATED_AND_CHECKED',flush=True)
