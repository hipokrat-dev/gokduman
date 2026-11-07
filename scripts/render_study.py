import bpy, math, random, os
from mathutils import Vector
random.seed(17)
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
def mat(name,col,rough=.5,metal=0):
 m=bpy.data.materials.new(name);m.diffuse_color=(*col,1);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*col,1);p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal;return m
def grain(m,scale,colors,bump=.08):
 n=m.node_tree.nodes;l=m.node_tree.links;p=n.get('Principled BSDF');t=n.new('ShaderNodeTexCoord');v=n.new('ShaderNodeVectorMath');v.operation='MULTIPLY';v.inputs[1].default_value=scale;l.new(t.outputs['Generated'],v.inputs[0]);noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=4;noise.inputs['Detail'].default_value=5;noise.inputs['Roughness'].default_value=.7;l.new(v.outputs[0],noise.inputs['Vector']);r=n.new('ShaderNodeValToRGB');r.color_ramp.elements[0].position=.18;r.color_ramp.elements[0].color=(*colors[0],1);r.color_ramp.elements[1].position=.82;r.color_ramp.elements[1].color=(*colors[1],1);l.new(noise.outputs['Fac'],r.inputs[0]);l.new(r.outputs[0],p.inputs['Base Color']);b=n.new('ShaderNodeBump');b.inputs['Strength'].default_value=bump;b.inputs['Distance'].default_value=.018;l.new(noise.outputs['Fac'],b.inputs['Height']);l.new(b.outputs[0],p.inputs['Normal'])
wood=mat('Oiled American walnut',(.18,.07,.025),.32);grain(wood,(.65,32,5),((.055,.018,.008),(.32,.15,.059)),.18)
plaster=mat('Limewashed umber',(.18,.15,.12),.94);grain(plaster,(8,8,8),((.12,.095,.073),(.24,.205,.16)),.13)
black=mat('Powder coated graphite',(.018,.023,.025),.29,.6);rubber=mat('Soft black rubber',(.012,.015,.017),.8);paper=mat('Ivory paper edges',(.7,.65,.52),.9);cream=mat('Warm ceramic',(.62,.59,.51),.28);brass=mat('Brushed brass',(.42,.24,.075),.27,.82);leaf=mat('Leaf green',(.035,.095,.027),.4);screen=mat('Midnight blue screen',(.018,.05,.075),.24)
p=screen.node_tree.nodes.get('Principled BSDF');p.inputs['Emission Color'].default_value=(.025,.11,.19,1);p.inputs['Emission Strength'].default_value=.6
books=[mat('Book cloth '+str(i),c,.85) for i,c in enumerate([(.075,.12,.15),(.25,.1,.055),(.24,.23,.17),(.07,.09,.07),(.32,.24,.13)])]
def box(name,loc,size,m,b=.012):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=name;o.dimensions=size;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(m)
 if b:mod=o.modifiers.new('Edge highlights','BEVEL');mod.width=b;mod.segments=3;o.modifiers.new('Weighted normals','WEIGHTED_NORMAL')
 return o
def sphere(name,loc,scale,m):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=24,ring_count=12,location=loc);o=bpy.context.object;o.name=name;o.scale=scale;o.data.materials.append(m)
 for f in o.data.polygons:f.use_smooth=True
 return o
def cyl(name,loc,r,depth,m):
 bpy.ops.mesh.primitive_cylinder_add(vertices=48,radius=r,depth=depth,location=loc);o=bpy.context.object;o.name=name;o.data.materials.append(m);mod=o.modifiers.new('Edge','BEVEL');mod.width=.008;mod.segments=3;o.modifiers.new('Normals','WEIGHTED_NORMAL');return o
def tube(name,points,r,m):
 c=bpy.data.curves.new(name,'CURVE');c.dimensions='3D';c.bevel_depth=r;c.bevel_resolution=3;s=c.splines.new('BEZIER');s.bezier_points.add(len(points)-1)
 for p,co in zip(s.bezier_points,points):p.co=co;p.handle_left_type='AUTO';p.handle_right_type='AUTO'
 o=bpy.data.objects.new(name,c);bpy.context.collection.objects.link(o);o.data.materials.append(m);return o
def light(name,loc,target,power,color,size):
 bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.name=name;o.data.energy=power;o.data.color=color;o.data.shape='DISK';o.data.size=size;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
def plant(x,y,z,r=.18):
 cyl('Ceramic planter',(x,y,z+.16),r,.32,cream);cyl('Soil',(x,y,z+.322),r*.9,.012,rubber)
 for i in range(18):
  a=i*2.4;h=random.uniform(.2,.56);end=(x+math.sin(a)*.23,y+math.cos(a)*.23,z+.32+h);tube('Plant stem',[(x,y,z+.3),end],.006,leaf);
  mesh=bpy.data.meshes.new('Thin curved leaf');verts=[]
  for j in range(9):
   t=j/8;w=math.sin(t*math.pi)*.065;verts.extend([(-w,.035*math.sin(t*math.pi),t*.32),(0,.052*math.sin(t*math.pi),t*.32),(w,.035*math.sin(t*math.pi),t*.32)])
  faces=[]
  for j in range(8):
   for k in range(2):i=j*3+k;faces.append((i,i+1,i+4,i+3))
  mesh.from_pydata(verts,[],faces);o=bpy.data.objects.new('Thin botanical leaf',mesh);bpy.context.collection.objects.link(o);o.location=end;o.rotation_euler=(math.cos(a)*.9,math.sin(a)*.9,a);o.data.materials.append(leaf)
  for f in mesh.polygons:f.use_smooth=True
box('Back wall',(0,1.25,2.6),(8,.2,6),plaster);box('Side wall',(-3.2,-.4,2.5),(.18,3.4,6),plaster)
for i in range(25):box('Floorboard',(0,-4+i*.28,-.055),(8,.275,.08),wood,.004)
box('Solid walnut desk',(0,0,.98),(5.6,1.4,.10),wood)
for x in [-2.56,2.56]:
 for y in [-.5,.5]:box('Desk steel leg',(x,y,.47),(.065,.065,.96),black)
box('Drawer cabinet',(-2.02,.15,.48),(.94,.95,.92),black)
for z in [.23,.48,.73]:box('Drawer front',(-2.02,-.341,z),(.88,.022,.22),black);box('Drawer pull',(-2.02,-.365,z+.06),(.24,.025,.013),brass)
for z in [2.32,3.28]:
 box('Floating walnut shelf',(0,.94,z),(5.65,.53,.065),wood)
 for x in [-2.45,2.45]:box('Bracket',(x,1.1,z-.10),(.035,.11,.22),black)
for start,z,count in [(-2.1,2.36,8),(.3,3.32,13),(-2.4,3.32,7)]:
 x=start
 for i in range(count):
  w=random.uniform(.09,.17);h=random.uniform(.36,.49);m=random.choice(books);box('Cloth book spine',(x,.83,z+h/2),(w,.27,h),m,.005);box('Page block',(x,.86,z+h/2),(w*.82,.25,h*.94),paper,.002);box('Spine',(x,.689,z+h/2),(w,.016,h),m,.003)
  for zz in [.05,h-.055]:box('Gold foil band',(x,.677,z+zz),(w*.78,.003,.004),brass,.001)
  x+=w+.018
# Monitor, desktop peripherals
box('Monitor bezel',(.15,.27,1.75),(1.91,.085,1.1),black,.022);box('Display glass',(.15,.219,1.75),(1.82,.008,1.015),screen,.01)
# Abstract landscape on the display, no instructions or typography.
for i in range(5):
 m=mat('Screen mountain '+str(i),(.018+i*.008,.045+i*.013,.065+i*.022),.6)
 p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Emission Color'].default_value=(.025+i*.015,.07+i*.02,.12+i*.028,1);p.inputs['Emission Strength'].default_value=.28
 verts=[(-.76,.209-i*.001,1.25), (1.06,.209-i*.001,1.25)]+[(1.06-j*.182,.209-i*.001,1.4+i*.08+random.uniform(0,.16)) for j in range(11)]
 mesh=bpy.data.meshes.new('mountain');mesh.from_pydata(verts,[],[list(range(len(verts)))]);o=bpy.data.objects.new('Screen landscape',mesh);bpy.context.collection.objects.link(o);o.data.materials.append(m)
box('Monitor stand',(.15,.32,1.12),(.075,.08,.22),black);box('Monitor foot',(.15,.17,1.04),(.46,.3,.025),black)
box('Desk mat',(.35,-.36,1.038),(2.35,.51,.008),rubber,.025);box('Keyboard',(.02,-.35,1.068),(1.12,.34,.045),black,.025)
for row in range(5):
 for col in range(15):box('Keycap',(-.49+col*.071,-.48+row*.06,1.099),(.061,.05,.018),rubber,.005)
sphere('Mouse',(1.11,-.34,1.09),(.10,.16,.055),black);tube('Mouse seam',[(1.11,-.49,1.10),(1.11,-.38,1.14)],.002,rubber)
# Phone and notebook
box('Phone dock',(-1.18,-.15,1.06),(.25,.19,.04),black)
o=box('Phone',(-1.18,-.09,1.28),(.21,.024,.4),black,.02);o.rotation_euler.x=math.radians(-12)
o=box('Phone glass',(-1.18,-.11,1.28),(.18,.006,.36),screen,.014);o.rotation_euler.x=math.radians(-12)
box('Notebook paper',(-1.75,-.42,1.07),(.62,.38,.05),paper);box('Leather notebook',(-1.75,-.42,1.1),(.65,.4,.018),books[3]);tube('Brass pen',[(-1.95,-.48,1.12),(-1.54,-.4,1.12)],.012,brass)
# Mug with real opening
cyl('Cup base',(-1.86,.03,1.045),.095,.015,cream)
pts=[(-1.86+.095*math.cos(i*math.tau/48),.03+.095*math.sin(i*math.tau/48),1.22) for i in range(49)];tube('Cup rim',pts,.008,cream)
bpy.ops.mesh.primitive_cylinder_add(vertices=64,radius=.095,depth=.17,end_fill_type='NOTHING',location=(-1.86,.03,1.13));bpy.context.object.data.materials.append(cream);mod=bpy.context.object.modifiers.new('Ceramic thickness','SOLIDIFY');mod.thickness=.008
cyl('Coffee',(-1.86,.03,1.195),.086,.005,mat('Coffee',(.025,.012,.006),.18));tube('Cup handle',[(-1.95,.03,1.19),(-2.025,.03,1.18),(-2.025,.03,1.08),(-1.95,.03,1.075)],.015,cream)
# Articulated task lamp
cyl('Lamp base',(-2.43,.17,1.055),.17,.04,black);tube('Lamp arm',[(-2.43,.17,1.07),(-2.58,.19,1.62),(-2.14,.13,2.02)],.019,black)
for pos in [(-2.58,.19,1.62),(-2.14,.13,2.02)]:sphere('Lamp joint',pos,(.039,.039,.039),brass)
bpy.ops.mesh.primitive_cone_add(vertices=48,radius1=.18,radius2=.055,depth=.19,location=(-2.10,.12,1.94));bpy.context.object.data.materials.append(black)
for f in bpy.context.object.data.polygons:f.use_smooth=True
light('Warm task lamp',(-2.1,.12,1.84),(-1.9,-.1,.98),35,(1,.62,.28),.15)
# VR headset on shelf
box('VR stand',(-.48,.92,2.39),(.42,.28,.035),black);box('VR stem',(-.48,1.0,2.59),(.04,.04,.4),black)
box('VR padded face',(-.48,.83,2.78),(.57,.23,.27),rubber,.08);box('VR ivory body',(-.48,.68,2.78),(.59,.14,.28),cream,.08)
for x in [-.69,-.27]:sphere('Tracking lens',(x,.601,2.79),(.018,.007,.018),black)
tube('Head strap',[(-.76,.8,2.79),(-.68,1.03,3.02),(-.3,1.03,3.02),(-.2,.8,2.79)],.025,rubber)
# Printer enclosure and carriage
for x in [1.23,1.93]:
 for y in [.67,1.06]:box('Printer extrusion',(x,y,2.73),(.042,.042,.72),black,.005)
for z in [2.39,3.08]:box('Printer frame',(1.58,.86,z),(.79,.48,.065),black)
box('Print bed',(1.58,.84,2.48),(.57,.34,.022),black);tube('Gantry',[(1.25,.81,2.94),(1.92,.81,2.94)],.018,brass);box('Print head',(1.59,.81,2.93),(.11,.12,.1),black)
bpy.ops.mesh.primitive_monkey_add(location=(1.58,.81,2.66));o=bpy.context.object;o.scale=(.13,.13,.13);o.data.materials.append(brass);mod=o.modifiers.new('Sculpt surface','SUBSURF');mod.levels=2
light('Printer warm light',(1.58,.83,3.02),(1.58,.82,2.48),5,(1,.55,.2),.25)
plant(2.39,.34,1.03,.16);plant(-2.5,.91,3.32,.16)
# Stethoscope, earpieces and metal chestpiece on desk
pts=[(1.65,-.38,1.055),(1.48,-.23,1.055),(1.58,.02,1.055),(1.96,.02,1.055),(2.06,-.26,1.055),(1.83,-.39,1.055)]
tube('Stethoscope tubing',pts,.018,rubber);tube('Stethoscope steel',[(1.65,-.38,1.055),(1.63,-.52,1.06),(1.5,-.56,1.06)],.01,brass);cyl('Stethoscope diaphragm',(1.84,-.4,1.067),.065,.025,black);cyl('Steel diaphragm',(1.84,-.4,1.083),.052,.008,brass)
cyl('Sculpture pedestal',(1.58,.81,2.525),.09,.08,brass)
# Soft window fill plus warm practical lighting
light('Large soft window',(-3,-2,3.9),(0,.2,1.4),100,(.70,.82,1),3)
light('Warm ceiling bounce',(1,-.5,4.6),(0,.5,1),110,(1,.74,.49),3)
light('Shelf wash',(0,.4,3.15),(0,1.2,2.8),35,(1,.62,.31),2)
scene=bpy.context.scene;scene.world.color=(.08,.08,.08);scene.render.engine='CYCLES';scene.cycles.samples=96;scene.cycles.use_denoising=True
bpy.ops.object.camera_add(location=(.3,-7.65,3.05));cam=bpy.context.object;cam.rotation_euler=(Vector((0,.3,2.05))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=43;scene.camera=cam
scene.render.resolution_x=1600;scene.render.resolution_y=1100;scene.render.resolution_percentage=100;scene.view_settings.view_transform='AgX';scene.render.image_settings.file_format='PNG';scene.render.filepath=os.path.join(ROOT,'renders/office-study.png')
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT,'assets/office-study.blend'));bpy.ops.render.render(write_still=True)
