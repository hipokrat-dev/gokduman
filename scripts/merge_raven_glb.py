"""Replace old raven triangles and append its new baked mesh without rebaking the room."""
import json, struct, pathlib, copy
ROOT=pathlib.Path(__file__).resolve().parents[1]
def read(path):
 data=path.read_bytes();n=struct.unpack_from('<I',data,12)[0];j=json.loads(data[20:20+n]);start=20+n;size=struct.unpack_from('<I',data,start)[0];return j,bytearray(data[start+8:start+8+size])
base,blob=read(ROOT/'public/models/office-desktop.glb');new,extra=read(ROOT/'assets/raven-reference-v3.glb');lo,hi=json.loads((ROOT/'assets/raven-replaced-bounds.json').read_text())
def values(index):
 a=base['accessors'][index];v=base['bufferViews'][a['bufferView']];fmt={5126:'f',5125:'I',5123:'H',5121:'B'}[a['componentType']];width={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4}[a['type']];length=struct.calcsize(fmt)*width;stride=v.get('byteStride',length);offset=v.get('byteOffset',0)+a.get('byteOffset',0);return [struct.unpack_from('<'+fmt*width,blob,offset+i*stride) for i in range(a['count'])]
node=next(n for n in base['nodes'] if n['name']=='furniture');translation=node.get('translation',[0,0,0]);assert not node.get('rotation') and not node.get('scale')
removed=0
for prim in base['meshes'][node['mesh']]['primitives']:
 positions=values(prim['attributes']['POSITION']);indices=[v[0] for v in values(prim['indices'])];kept=[]
 for i in range(0,len(indices),3):
  tri=indices[i:i+3];center=[sum(positions[k][axis] for k in tri)/3+translation[axis] for axis in range(3)]
  if all(lo[a]<=center[a]<=hi[a] for a in range(3)):removed+=1
  else:kept.extend(tri)
 while len(blob)%4:blob.append(0)
 offset=len(blob);data=struct.pack('<'+'I'*len(kept),*kept);blob.extend(data);view=len(base['bufferViews']);base['bufferViews'].append({'buffer':0,'byteOffset':offset,'byteLength':len(data),'target':34963});a=base['accessors'][prim['indices']];a.update(bufferView=view,byteOffset=0,count=len(kept),componentType=5125,min=[min(kept)],max=[max(kept)])
assert removed>100, 'Expected the old raven to be present'
while len(blob)%4:blob.append(0)
byte_offset=len(blob);offsets={k:len(base.get(k,[])) for k in ['bufferViews','accessors','images','samplers','textures','materials','meshes','nodes']};blob.extend(extra)
for v in new.get('bufferViews',[]):v['buffer']=0;v['byteOffset']=v.get('byteOffset',0)+byte_offset
for a in new.get('accessors',[]):a['bufferView']+=offsets['bufferViews']
for im in new.get('images',[]):
 if 'bufferView'in im:im['bufferView']+=offsets['bufferViews']
for t in new.get('textures',[]):
 if 'source'in t:t['source']+=offsets['images']
 if 'sampler'in t:t['sampler']+=offsets['samplers']
def texture_indices(obj):
 if isinstance(obj,dict):
  for k,v in obj.items():
   if k.endswith('Texture') and isinstance(v,dict) and 'index'in v:v['index']+=offsets['textures']
   else:texture_indices(v)
 elif isinstance(obj,list):
  for v in obj:texture_indices(v)
for m in new.get('materials',[]):texture_indices(m)
for m in new.get('meshes',[]):
 for p in m['primitives']:
  p['attributes']={k:v+offsets['accessors'] for k,v in p['attributes'].items()}
  if 'indices'in p:p['indices']+=offsets['accessors']
  if 'material'in p:p['material']+=offsets['materials']
for n in new.get('nodes',[]):
 if 'mesh'in n:n['mesh']+=offsets['meshes']
 if 'children'in n:n['children']=[i+offsets['nodes'] for i in n['children']]
for k in offsets:base.setdefault(k,[]).extend(new.get(k,[]))
base['scenes'][base.get('scene',0)]['nodes'].extend(i+offsets['nodes'] for i in new['scenes'][new.get('scene',0)]['nodes'])
for k in ['extensionsUsed','extensionsRequired']:
 if new.get(k):base[k]=sorted(set(base.get(k,[])+new[k]))
base['buffers']=[{'byteLength':len(blob)}];encoded=json.dumps(base,separators=(',',':')).encode();encoded+=b' '*((-len(encoded))%4);blob+=b'\0'*((-len(blob))%4)
out=struct.pack('<III',0x46546c67,2,12+8+len(encoded)+8+len(blob))+struct.pack('<II',len(encoded),0x4e4f534a)+encoded+struct.pack('<II',len(blob),0x004e4942)+blob
(ROOT/'public/models/office-desktop.glb').write_bytes(out)
print('Removed old raven triangles:',removed,'New GLB bytes:',len(out))
