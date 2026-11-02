"""Resize embedded texture images only; preserve geometry, skin, morphs and clips."""
import json,struct,io
from pathlib import Path
from PIL import Image
p=Path(__file__).resolve().parents[1]/'public/assets/abraham.glb'
b=p.read_bytes();n=struct.unpack_from('<I',b,12)[0];j=json.loads(b[20:20+n]);binary=b[28+n:];images={im['bufferView'] for im in j.get('images',[])};out=bytearray()
for i,view in enumerate(j['bufferViews']):
 data=binary[view.get('byteOffset',0):view.get('byteOffset',0)+view['byteLength']]
 if i in images:
  im=Image.open(io.BytesIO(data));im.thumbnail((1024,1024));buff=io.BytesIO();im.save(buff,format='PNG',optimize=True);data=buff.getvalue()
 out.extend(b'\x00'*((-len(out))%4));view['byteOffset']=len(out);view['byteLength']=len(data);out.extend(data)
j['buffers'][0]['byteLength']=len(out);out.extend(b'\x00'*((-len(out))%4));meta=json.dumps(j,separators=(',',':')).encode();meta+=b' '*((-len(meta))%4)
p.write_bytes(struct.pack('<III',0x46546c67,2,28+len(meta)+len(out))+struct.pack('<II',len(meta),0x4e4f534a)+meta+struct.pack('<II',len(out),0x004e4942)+out)
print('Abraham texture-optimized bytes:',p.stat().st_size)
