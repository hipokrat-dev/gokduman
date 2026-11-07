import bpy, os, math, ast, random
from mathutils import Vector, Euler, Quaternion
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
tree=ast.parse(open(os.path.join(ROOT,'scripts/refine_study.py')).read());exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef)],type_ignores=[]),'<modeling helpers>','exec'))
def drop(prefixes):
 for o in list(bpy.data.objects):
  if any(o.name.startswith(p) for p in prefixes):bpy.data.objects.remove(o,do_unlink=True)
def area(name,loc,target,power,color,size):
 bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.name=name;o.data.energy=power;o.data.color=color;o.data.shape='DISK';o.data.size=size;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();return o
for mobile in [False,True]:
 mode='mobile' if mobile else 'desktop';bpy.ops.wm.open_mainfile(filepath=os.path.join(ROOT,'assets/office-reference-'+mode+'.blend'));random.seed(91)
 black=bpy.data.materials['Powder coated graphite'];brass=bpy.data.materials['Brushed brass'];cream=bpy.data.materials['Warm ceramic'];steel=bpy.data.materials['Brushed stainless steel'];paper=bpy.data.materials['Ivory paper edges']
 # Correct book text orientation: text plane faces visitor, baseline runs vertically.
 for o in bpy.data.objects:
  if o.type=='FONT' and ('spine title' in o.name or 'book title' in o.name):o.rotation_mode='QUATERNION';o.rotation_quaternion=Euler((math.pi/2,0,0)).to_quaternion() @ Quaternion((0,0,1),math.pi/2)
 # Clear a shelf edge by scaling the entire monitor, including its screen and feet.
 if mobile:
  pivot=Vector((.15,.27,1.035))
  for o in bpy.data.objects:
   if o.name.startswith(('Monitor','Display glass','Screen landscape','Power LED')):o.location=pivot+(o.location-pivot)*.67;o.scale*=.67
   if o.name.startswith(('Keyboard','Keycap','Key legend')):o.location.x*=.77;o.location.y=-.35+(o.location.y+.35)*.77;o.scale*=.77
   if o.name.startswith(('Nameplate','Stethoscope','Steel diaphragm')):o.location.z-=.05;o.location.y+=1.12
   if o.type=='MESH' and abs(o.location.x-1.27)<.01 and abs(o.location.z-1.13)<.01:o.location.x-=2.0
  # Avoid cup/planter overlap after shifting mug.
  for o in bpy.data.objects:
   if o.name.startswith(('Cup base','Cup rim','Cup handle','Coffee')):o.location.x+=.22;o.location.y-=.10
   if o.type=='MESH' and abs(o.location.x+.73)<.01 and abs(o.location.z-1.13)<.01:o.location.x+=.22;o.location.y-=.10
 # Place small plants on the middle and lower shelves, as in the mobile reference.
 if mobile:
  prefixes=('Tabletop lance leaf','Faceted terracotta planter','Soil surface')
  sources=[o for o in bpy.data.objects if o.name.startswith(prefixes) and abs(o.location.x+.7917)<.06 and o.location.z<1.8]
  for original in sources:
   clone=original.copy();clone.data=original.data.copy();bpy.context.collection.objects.link(clone);clone.location+=Vector((.7417,.59,2.0875))
  for o in list(bpy.data.objects):
   if o.name.startswith(prefixes) and abs(o.location.x-.9657)<.06 and o.location.z<1.8:o.location+=Vector((-.2457,.24,1.2075))
 # More articulated lamp, open shade tilted toward viewer.
 shift=1.15 if mobile else 0
 drop(['Lamp arm','Lamp joint','Lamp diffuser'])
 for o in list(bpy.data.objects):
  if o.name.startswith('Cone') and o.location.x<0:bpy.data.objects.remove(o,do_unlink=True)
 points=[(-2.43+shift,.17,1.07),(-2.55+shift,.17,1.64),(-2.15+shift,.12,2.02)]
 for a,b in zip(points[:-1],points[1:]):
  d=Vector(b)-Vector(a);o=cyl('Articulated lamp rod',(Vector(a)+Vector(b))/2,.018,d.length,black);o.rotation_euler=d.to_track_quat('Z','Y').to_euler()
 for pos in points[1:]:cyl('Lamp hinge',pos,.033,.05,black,(math.pi/2,0,0));cyl('Lamp hinge screw',(pos[0],pos[1]-.027,pos[2]),.012,.005,steel,(math.pi/2,0,0))
 center=Vector((-2.1+shift,.10,1.94));rot=Euler((-.5,0,-.15));bpy.ops.mesh.primitive_cone_add(vertices=64,radius1=.18,radius2=.06,depth=.19,end_fill_type='NOTHING',location=center);o=bpy.context.object;o.name='Open task lamp shade';o.rotation_euler=rot;o.data.materials.append(black);o.modifiers.new('Shade thickness','SOLIDIFY').thickness=.004
 for f in o.data.polygons:f.use_smooth=True
 bottom=center+rot.to_matrix()@Vector((0,0,-.096));o=cyl('Visible lamp diffuser',bottom,.173,.005,bpy.data.materials['Warm lamp diffuser']);o.rotation_euler=rot
 lamp=bpy.data.objects['Warm task lamp'];lamp.location=bottom+rot.to_matrix()@Vector((0,0,-.025));lamp.rotation_euler=(Vector((-1.7+shift,-.10,1.02))-lamp.location).to_track_quat('-Z','Y').to_euler();lamp.data.energy=90 if not mobile else 45
 area('Task lamp wall bounce',(-2.1+shift,.20,1.86),(-1.85+shift,1.13,1.65),24,(1,.53,.18),.6)
 area('Warm front softbox',(-1.8,-2.2,3.1),(0,.1,1.1),110 if not mobile else 65,(1,.72,.44),2.8)
 # Shift wallpaper palette to reference's blue/purple evening mountains.
 screen=bpy.data.materials['Midnight blue screen'];p=screen.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(.022,.035,.11,1);p.inputs['Emission Color'].default_value=(.035,.065,.27,1);p.inputs['Emission Strength'].default_value=.8
 for m in bpy.data.materials:
  if m.name.startswith('Landscape ridge '):
   i=int(m.name.split()[-1]);t=i/7;p=m.node_tree.nodes.get('Principled BSDF');col=(.12*(1-t)+.008*t,.115*(1-t)+.025*t,.30*(1-t)+.10*t,1);p.inputs['Base Color'].default_value=col;p.inputs['Emission Color'].default_value=col;p.inputs['Emission Strength'].default_value=.9
 # The raven is a long-bodied perched bird, rather than a vertical figurine.
 body=bpy.data.objects.get('Raven body');wing=[o for o in bpy.data.objects if o.name.startswith('Raven layered')]
 if body:body.rotation_euler.y=-.46;body.scale.z*=1.08
 for o in wing:o.rotation_euler.y=-.7;o.scale.z*=1.18
 # Approximate globe continents are reprojected onto the sphere surface.
 for o in bpy.data.objects:
  if o.name.startswith('Globe brass continents'):
   bpy.context.view_layer.objects.active=o;o.select_set(True);mod=o.modifiers.new('Continental tessellation','TRIANGULATE');bpy.ops.object.modifier_apply(modifier=mod.name);mod=o.modifiers.new('Continent subdivisions','SUBSURF');mod.subdivision_type='SIMPLE';mod.levels=3;bpy.ops.object.modifier_apply(modifier=mod.name)
   center=Vector((.13,.89,2.97))
   # Mesh coordinates stay in desktop space, mobile translates the object.
   for v in o.data.vertices:v.co=center+(v.co-center).normalized()*.193
   o.select_set(False)
 # Short front rails make the enclosure read as a real printer.
 # Render a clean image; no browser UI or drawn phone frame is included.
 scene=bpy.context.scene;scene.cycles.samples=128
 if mobile:scene.camera.data.lens=52;scene.camera.rotation_euler=(Vector((0,.3,2.22))-scene.camera.location).to_track_quat('-Z','Y').to_euler()
 else:scene.render.resolution_y=850;scene.camera.location.z=2.13;scene.camera.rotation_euler=(Vector((0,.3,2.05))-scene.camera.location).to_track_quat('-Z','Y').to_euler()
 scene.render.filepath=os.path.join(ROOT,'renders/office-reference-'+mode+'-v2.png');bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT,'assets/office-reference-'+mode+'-v2.blend'));bpy.ops.render.render(write_still=True)
