"""Replace only the desktop raven with a lean, perched corvid sculpture."""
import bpy, os, math, ast
from mathutils import Vector
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
bpy.ops.wm.open_mainfile(filepath=os.path.join(ROOT,'assets/office-reference-desktop-v2.blend'))
tree=ast.parse(open(os.path.join(ROOT,'scripts/refine_study.py')).read());exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef)],type_ignores=[]),'<helpers>','exec'))
for o in list(bpy.data.objects):
 if o.name.startswith('Raven'):bpy.data.objects.remove(o,do_unlink=True)
origin=Vector((-.43,.84,2.735))
plumage=mat('Raven charcoal blue plumage',(.008,.012,.019),.43,.12)
feathermat=mat('Raven wing charcoal',(.011,.016,.023),.48,.08)
beakmat=mat('Raven keratin',(.009,.011,.014),.32,.08)
eye=mat('Raven glossy eye',(.0015,.0018,.002),.08)
black=bpy.data.materials['Powder coated graphite']
def ellipsoid(name,loc,scale,m,axis=None):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=32,ring_count=20,location=origin+Vector(loc));o=bpy.context.object;o.name=name;o.scale=scale;o.data.materials.append(m)
 if axis:o.rotation_euler=Vector(axis).to_track_quat('Z','Y').to_euler()
 for p in o.data.polygons:p.use_smooth=True
 return o

def facet(name,vertices,faces,m):
 mesh=bpy.data.meshes.new(name);mesh.from_pydata(vertices,[],faces);mesh.update();o=bpy.data.objects.new(name,mesh);bpy.context.collection.objects.link(o);o.location=origin;o.data.materials.append(m);return o
box('Raven plinth',origin+Vector((-.04,.02,-.012)),(.38,.23,.025),black,.004)
ellipsoid('Raven tapered torso',(-.025,.015,.212),(.078,.073,.157),plumage,(.55,-.03,.82))
ellipsoid('Raven sloping shoulder',(.035,.012,.295),(.065,.063,.098),plumage,(.45,0,.9))
ellipsoid('Raven neck',(.078,.005,.342),(.047,.049,.080),plumage,(.24,-.02,.96))
ellipsoid('Raven crown',(.105,-.002,.397),(.059,.047,.048),plumage,(.55,0,.83))
# Fuse the overlapping torso, shoulder, neck and crown into one sculpted surface.
parts=[o for o in bpy.data.objects if o.name in ['Raven tapered torso','Raven sloping shoulder','Raven neck','Raven crown']]
bpy.ops.object.select_all(action='DESELECT')
for o in parts:o.select_set(True)
bpy.context.view_layer.objects.active=parts[0];bpy.ops.object.convert(target='MESH');bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);bpy.ops.object.join();body=bpy.context.object;body.name='Raven unified sculpt';mod=body.modifiers.new('Fused organic form','REMESH');mod.mode='VOXEL';mod.voxel_size=.003;bpy.ops.object.modifier_apply(modifier=mod.name);mod=body.modifiers.new('Smooth sculpt','SMOOTH');mod.factor=.65;mod.iterations=5;bpy.ops.object.modifier_apply(modifier=mod.name)
for f in body.data.polygons:f.use_smooth=True
# Strong corvid bill with a gently hooked tip, rather than a thin cone.
facet('Raven upper bill',[(.135,-.036,.405),(.145,.027,.405),(.205,.015,.399),(.251,-.004,.38),(.199,-.021,.389),(.14,-.03,.379),(.147,.025,.38)],[(0,1,2,3,4),(0,4,5),(1,6,3,2),(5,4,3,6),(0,5,6,1)],beakmat)
facet('Raven lower bill',[(.14,-.028,.377),(.147,.024,.378),(.242,-.004,.377),(.177,-.012,.367)],[(0,1,2),(0,2,3),(1,3,2),(0,3,1)],beakmat)
for side in [-1,1]:
 ellipsoid('Raven eye socket',(.120,side*.048,.409),(.012,.005,.011),beakmat)
 ellipsoid('Raven eye',(.122,side*.052,.410),(.007,.004,.007),eye)
# A shallow closed wing with overlapping volumetric flight feathers.
ellipsoid('Raven closed wing cover',(-.055,-.061,.23),(.057,.018,.115),feathermat,(.65,0,.76))
for i in range(8):
 start=Vector((.018-i*.009,-.078-i*.0004,.298-i*.010));end=Vector((-.198+i*.010,-.057-i*.0005,.115+i*.004));d=end-start;side=Vector((d.z,0,-d.x)).normalized();vertices=[]
 for j in range(9):
  t=j/8;center=start+d*t;width=.010*math.sin(math.pi*(.08+.92*t))**.7;depth=.0035*math.sin(math.pi*t)
  vertices.extend([tuple(center+side*width),tuple(center+Vector((0,-depth,0))),tuple(center-side*width),tuple(center+Vector((0,depth,0)))])
 faces=[]
 for j in range(8):
  for k in range(4):faces.append((j*4+k,j*4+(k+1)%4,(j+1)*4+(k+1)%4,(j+1)*4+k))
 feather=facet('Raven sculpted flight feather',vertices,faces,plumage if i%2 else feathermat)
 for f in feather.data.polygons:f.use_smooth=True
# Far wing and a wedge-shaped tail extending beyond the body.
facet('Raven far folded wing',[(.015,.067,.29),(-.09,.073,.21),(-.19,.045,.1),(-.085,.061,.16)],[(0,1,2,3)],plumage)
for i in range(5):
 y=.008+(i-2)*.013
 facet('Raven tapered tail feather',[(-.08,y-.008,.14),(-.08,y+.008,.14),(-.245-abs(i-2)*.005,y+.009,.075),(-.262-abs(i-2)*.005,y,.067),(-.245-abs(i-2)*.005,y-.009,.075)],[(0,1,2,3,4)],plumage)
# Legs begin inside the lower torso and bend toward the gripping toes.
for x,y in [(-.08,-.030),(-.045,.033)]:
 tube('Raven scaled leg',[origin+Vector((x,y,.16)),origin+Vector((x+.025,y,.065)),origin+Vector((x+.035,y-.009,.008))],.0065,beakmat)
 for j in [-1,0,1]:
  tube('Raven gripping toe',[origin+Vector((x+.035,y-.009,.008)),origin+Vector((x+.055+j*.015,y-.045,.006)),origin+Vector((x+.063+j*.018,y-.058,.001))],.0038,beakmat)
 tube('Raven rear toe',[origin+Vector((x+.035,y-.009,.008)),origin+Vector((x-.005,y+.025,.003))],.0035,beakmat)
scene=bpy.context.scene;scene.cycles.samples=128;scene.render.filepath=os.path.join(ROOT,'renders/office-reference-desktop-v2.png')
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT,'assets/office-reference-desktop-v2.blend'))
bpy.ops.render.render(write_still=True)
# A second camera makes the revised silhouette and feet reviewable at useful size.
cam=scene.camera;cam.location=(-.14,-1.15,3.12);cam.rotation_euler=(origin+Vector((-.01,0,.22))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=85
scene.render.resolution_x=1100;scene.render.resolution_y=900;scene.render.filepath=os.path.join(ROOT,'renders/raven-detail.png');bpy.ops.render.render(write_still=True)
