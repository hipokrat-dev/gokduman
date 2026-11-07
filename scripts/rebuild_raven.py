"""Reference-shaped desktop raven; bake it separately to retain existing room textures."""
import bpy, math, os, ast, json
from mathutils import Vector
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
bpy.ops.wm.open_mainfile(filepath=ROOT+'/assets/office-reference-desktop-v2.blend')
tree=ast.parse(open(ROOT+'/scripts/refine_study.py').read());exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef)],type_ignores=[]),'<helpers>','exec'))
old=[o for o in bpy.data.objects if o.name.startswith('Raven')]
points=[o.matrix_world@Vector(c) for o in old for c in o.bound_box]
# Blender to glTF axes: (x,z,-y).
points=[Vector((p.x,p.z,-p.y)) for p in points]
bounds=[[min(p[i] for p in points)-.003 for i in range(3)],[max(p[i] for p in points)+.003 for i in range(3)]]
if os.path.exists(ROOT+'/assets/raven-replaced-bounds.json'):bounds=json.load(open(ROOT+'/assets/raven-replaced-bounds.json'))
for o in old:bpy.data.objects.remove(o,do_unlink=True)
origin=Vector((-.43,.84,2.735))
black=bpy.data.materials['Powder coated graphite']
plume=mat('Corvid midnight plumage',(.002,.004,.009),.58,.03)
wingmat=mat('Corvid blue black feathers',(.003,.006,.014),.54,.03)
edge=mat('Corvid flight feather edges',(.004,.008,.017),.58,.02)
beak=mat('Corvid charcoal keratin',(.006,.009,.014),.3,.08)
eye=mat('Corvid obsidian eye',(.001,.001,.001),.065,.1)
def mesh(name,verts,faces,material):
 m=bpy.data.meshes.new(name);m.from_pydata(verts,[],faces);m.update();o=bpy.data.objects.new('Raven '+name,m);bpy.context.collection.objects.link(o);o.location=origin;o.data.materials.append(material);return o
def ell(name,center,radii,material,axis=None):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=32,ring_count=20,location=origin+Vector(center));o=bpy.context.object;o.name='Raven '+name;o.scale=radii;o.data.materials.append(material)
 if axis:o.rotation_euler=Vector(axis).to_track_quat('Z','Y').to_euler()
 for f in o.data.polygons:f.use_smooth=True
 return o
box('Raven rectangular plinth',origin+Vector((-.045,0,-.014)),(.39,.22,.028),black,.003)
parts=[ell('breast',(-.035,.008,.225),(.092,.075,.165),plume,(.79,0,.61)),ell('shoulder',(.035,.005,.30),(.084,.071,.105),plume,(.68,0,.73)),ell('thick neck',(.093,0,.345),(.063,.058,.086),plume,(.4,0,.92)),ell('angular crown',(.126,-.003,.399),(.065,.051,.039),plume)]
bpy.ops.object.select_all(action='DESELECT')
for o in parts:o.select_set(True)
bpy.context.view_layer.objects.active=parts[0];bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);bpy.ops.object.join();o=bpy.context.object;o.name='Raven unified body';m=o.modifiers.new('Organic fusion','REMESH');m.mode='VOXEL';m.voxel_size=.0028;bpy.ops.object.modifier_apply(modifier=m.name);m=o.modifiers.new('Surface polish','SMOOTH');m.factor=.55;m.iterations=4;bpy.ops.object.modifier_apply(modifier=m.name)
for face in o.data.polygons:face.use_smooth=True
# Heavy wedge bill, arched upper ridge and hooked point.
mesh('upper bill',[(.158,-.038,.412),(.158,.032,.412),(.197,.025,.418),(.249,.011,.403),(.28,-.002,.383),(.224,-.024,.391),(.164,-.033,.382),(.165,.027,.382)],[(0,1,2),(0,2,5),(2,3,4,5),(1,7,4,3,2),(6,5,4,7),(0,5,6),(0,6,7,1)],beak)
mesh('lower bill',[(.163,-.03,.379),(.164,.025,.379),(.27,-.002,.381),(.206,-.006,.367)],[(0,1,2),(0,2,3),(1,3,2),(0,3,1)],beak)
for side in [-1,1]:
 ell('eye surround',(.145,side*.047,.409),(.009,.003,.008),beak)
 ell('glossy eye',(.147,side*.052,.410),(.004,.002,.004),eye)
 ell('nostril',(.187,side*.027,.400),(.009,.0018,.0035),eye)
# Broad closed wings form angular layered planes rather than smooth oval pads.
for side in [-1,1]:
 y=side*.071
 mesh('scapular shield',[(.085,y,.334),(.014,y+side*.015,.343),(-.10,y+side*.022,.288),(-.219,y,.166),(-.105,y+side*.02,.185),(.045,y+side*.014,.254)],[(0,1,2),(0,2,5),(2,3,4,5)],wingmat)
 for i in range(9):
  start=Vector((.045-i*.013,y+side*(.042+i*.0006),.312-i*.009));end=Vector((-.255+i*.011,y+side*.035,.132+i*.006));d=end-start;cross=Vector((d.z,0,-d.x)).normalized();verts=[]
  for j in range(12):
   t=j/11;center=start+d*t;width=.017*math.sin(math.pi*(.10+.90*t))**.6;ridge=side*.004*math.sin(math.pi*t)
   verts.extend([tuple(center-cross*width),tuple(center+Vector((0,ridge,0))),tuple(center+cross*width)])
  faces=[]
  for j in range(11):faces.extend([(3*j,3*j+1,3*j+4,3*j+3),(3*j+1,3*j+2,3*j+5,3*j+4)])
  feather=mesh('long primary feather',verts,faces,wingmat if i%3 else edge)
  for face in feather.data.polygons:face.use_smooth=True
# Six long pointed tail feathers, the central pair forms the raven's wedge.
for i in range(6):
 y=(i-2.5)*.018;length=.33-abs(i-2.5)*.013
 mesh('wedge tail feather',[(-.10,y-.008,.19),(-.10,y+.008,.14),(-length+.015,y+.008,.066+i*.004),(-length,y,.071+i*.004),(-length+.02,y-.008,.105+i*.004)],[(0,1,2,3,4)],wingmat if i%2 else plume)
for x,y in [(-.055,-.036),(.007,.037)]:
 tube('Raven jointed leg',[origin+Vector((x,y,.17)),origin+Vector((x-.015,y,.08)),origin+Vector((x+.016,y-.01,.012))],.007,beak)
 for i in [-1,0,1]:tube('Raven toe',[origin+Vector((x+.016,y-.01,.012)),origin+Vector((x+.04+i*.014,y-.045,.009)),origin+Vector((x+.058+i*.016,y-.061,.003))],.004,beak)
 tube('Raven rear claw',[origin+Vector((x+.016,y-.01,.012)),origin+Vector((x-.025,y+.035,.004))],.0035,beak)
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=48
bpy.ops.wm.save_as_mainfile(filepath=ROOT+'/assets/office-reference-desktop-v2.blend')
# Detail preview and updated initial loading poster.
scene.render.filepath=ROOT+'/renders/office-reference-desktop-v2.png';bpy.ops.render.render(write_still=True)
cam=scene.camera;oldloc=cam.location.copy();oldrot=cam.rotation_euler.copy();lens=cam.data.lens;rx=scene.render.resolution_x;ry=scene.render.resolution_y
cam.location=(-.38,-1.10,3.08);cam.rotation_euler=(origin+Vector((-.03,0,.22))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=80;scene.render.resolution_x=1100;scene.render.resolution_y=900;scene.render.filepath=ROOT+'/renders/raven-reference-v3.png';bpy.ops.render.render(write_still=True)
# Convert only the raven, preserving original room lighting for its bake.
deps=bpy.context.evaluated_depsgraph_get();parts=[]
for original in list(scene.objects):
 if not original.name.startswith('Raven'):continue
 evaluated=original.evaluated_get(deps);m=bpy.data.meshes.new_from_object(evaluated,depsgraph=deps);o=bpy.data.objects.new('Baked raven part',m);scene.collection.objects.link(o);o.matrix_world=original.matrix_world.copy();parts.append(o);bpy.data.objects.remove(original,do_unlink=True)
bpy.ops.object.select_all(action='DESELECT')
for o in parts:o.select_set(True)
bpy.context.view_layer.objects.active=parts[0];bpy.ops.object.join();raven=bpy.context.object;raven.name='Reference raven';bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT');bpy.ops.uv.smart_project(angle_limit=math.radians(66),island_margin=.008);bpy.ops.object.mode_set(mode='OBJECT')
im=bpy.data.images.new('Reference raven lighting',width=1024,height=1024,alpha=False)
for slot in raven.material_slots:
 slot.material=slot.material.copy();node=slot.material.node_tree.nodes.new('ShaderNodeTexImage');node.image=im;slot.material.node_tree.nodes.active=node
scene.cycles.samples=32;scene.render.bake.margin=8;bpy.ops.object.bake(type='COMBINED')
m=bpy.data.materials.new('Raven baked midnight');m.use_nodes=True;n=m.node_tree.nodes;n.clear();out=n.new('ShaderNodeOutputMaterial');emit=n.new('ShaderNodeEmission');tex=n.new('ShaderNodeTexImage');tex.image=im;m.node_tree.links.new(tex.outputs['Color'],emit.inputs['Color']);m.node_tree.links.new(emit.outputs[0],out.inputs['Surface']);raven.data.materials.clear();raven.data.materials.append(m)
for p in raven.data.polygons:p.material_index=0
bpy.ops.export_scene.gltf(filepath=ROOT+'/assets/raven-reference-v3.glb',export_format='GLB',use_selection=True,export_lights=False,export_cameras=False,export_image_format='JPEG',export_jpeg_quality=95)
json.dump(bounds,open(ROOT+'/assets/raven-replaced-bounds.json','w'))
print('RAVEN_READY',flush=True)
