import bpy,json
from pathlib import Path
p=Path(__file__).resolve().parents[1]
bpy.ops.wm.open_mainfile(filepath=str(p/'quiet-collection-with-abraham-facial.blend'))
s=bpy.context.scene
print('SCENE',len(s.objects))
print('MATS',[(m.name) for m in bpy.data.materials if 'Illustration' in m.name][:45])
print('CLOCK',[(o.name,list(o.location)) for o in s.objects if any(k in o.name.lower() for k in ['clock','drawer','placement','book'])][:40])
