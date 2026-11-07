import bpy, math, random, os
from mathutils import Vector
root=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
def material(name,color,metal=0,rough=.6):
 m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True
 p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=rough
 return m
wood=material('Smoked walnut',(.25,.125,.055));wall=material('Warm mineral plaster',(.28,.25,.21));metal=material('Blackened steel',(.035,.041,.042),.75,.3)
# Small embedded grain image keeps the GLB portable and material compatible with web renderers.
random.seed(41);im=bpy.data.images.new('Walnut grain',width=512,height=512)
pixels=[]
for y in range(512):
 for x in range(512):
  grain=.8+.12*math.sin(y*.42+math.sin(x*.025)*1.5)+random.uniform(-.045,.045)
  pixels.extend((.36*grain,.205*grain,.105*grain,1))
im.pixels=pixels;im.pack()
n=wood.node_tree.nodes.new('ShaderNodeTexImage');n.image=im;wood.node_tree.links.new(n.outputs['Color'],wood.node_tree.nodes.get('Principled BSDF').inputs['Base Color'])
def box(name,loc,scale,mat,bevel=.02):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=name;o.dimensions=scale;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(mat)
 mod=o.modifiers.new('Soft manufactured edges','BEVEL');mod.width=bevel;mod.segments=3;bpy.context.view_layer.objects.active=o;bpy.ops.object.modifier_apply(modifier=mod.name)
 for p in o.data.polygons:p.use_smooth=True
 return o
# Blender Z up becomes Three.js Y up; Blender Y negative faces the visitor.
box('Plaster wall',(0,1.7,2),(12,.15,6),wall)
for i in range(30):
 for j in range(4):box('Walnut floorboard',(j*3-4.5+(i%2)*.3,-4+i*.32,-.13),(2.98,.312,.08),wood,.006)
box('Walnut desktop',(0,0,.85),(5.9,1.8,.16),wood)
for x in [-2.7,2.7]:
 for y in [-.65,.65]:box('Steel leg',(x,y,.33),(.09,.09,1),metal)
 box('Desk crossbar',(x,0,-.08),(.09,1.5,.08),metal)
for z in [2.55,3.6]:
 box('Floating walnut shelf',(0,1.25,z),(5.8,.65,.10),wood)
 for x in [-2.35,2.35]:box('Shelf bracket',(x,1.52,z-.14),(.035,.08,.3),metal)
# Reference lighting for opening the authoring file. Runtime lighting is in Scene.tsx.
bpy.ops.object.light_add(type='AREA',location=(-3,-3,5));bpy.context.object.data.energy=650;bpy.context.object.data.shape='DISK';bpy.context.object.data.size=4
bpy.context.object.rotation_euler=(Vector((0,0,1))-bpy.context.object.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add(location=(0,-6.5,2.6));cam=bpy.context.object;cam.rotation_euler=(Vector((0,0,1.35))-cam.location).to_track_quat('-Z','Y').to_euler();bpy.context.scene.camera=cam;cam.data.lens=45
bpy.context.scene.render.engine='CYCLES';bpy.context.scene.cycles.samples=32
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(root,'assets/office-room.blend'))
bpy.ops.export_scene.gltf(filepath=os.path.join(root,'public/models/office-room.glb'),export_format='GLB',export_lights=False,export_cameras=False)
