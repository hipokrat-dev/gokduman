"""Desktop and mobile compositions based on the supplied office references."""
import bpy, math, random, os, ast
from mathutils import Vector
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
bpy.ops.wm.open_mainfile(filepath=os.path.join(ROOT,'assets/office-refined.blend'))
# Reuse modeling primitives without running the prior study or its renderer.
tree=ast.parse(open(os.path.join(ROOT,'scripts/refine_study.py')).read());exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef)],type_ignores=[]),'<modeling helpers>','exec'))
random.seed(29)
black=bpy.data.materials['Powder coated graphite'];rubber=bpy.data.materials['Soft black rubber'];brass=bpy.data.materials['Brushed brass'];cream=bpy.data.materials['Warm ceramic'];wood=bpy.data.materials['Oiled American walnut'];paper=bpy.data.materials['Ivory paper edges'];leaf=bpy.data.materials['Leaf green'];steel=bpy.data.materials['Brushed stainless steel']
def sphere(name,loc,scale,m,segments=24):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=segments,ring_count=12,location=loc);o=bpy.context.object;o.name=name;o.scale=scale;o.data.materials.append(m)
 for f in o.data.polygons:f.use_smooth=True
 return o
def relocate(prefixes,delta):
 objs=[o for o in bpy.data.objects if any(o.name.startswith(p) for p in prefixes)]
 for o in objs:o.location+=Vector(delta)
 return objs
def drop(prefixes):
 for o in list(bpy.data.objects):
  if any(o.name.startswith(p) for p in prefixes):bpy.data.objects.remove(o,do_unlink=True)
def area(name,loc,target,power,color,size):
 bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.name=name;o.data.energy=power;o.data.color=color;o.data.shape='DISK';o.data.size=size;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();return o
# Remove the earlier two-shelf composition and all duplicate books/foliage.
drop(['Floating walnut shelf','Bracket','Cloth book','Page block','Spine','Gold foil band','Embossed spine','Volume number','Cloth hinge','Ceramic planter','Soil','Plant stem','Thin botanical leaf','Sculpture pedestal','Suzanne'])
vr=relocate(['VR ','Tracking lens','Head strap','Top head strap','Optical glass'],(-1.37,-.77,-1.33))
printer=relocate(['Printer','Print bed','Print head','Gantry','Linear guide','Drive belt','Hex bolt','Bolt slot','Nozzle shroud','Hotend fan','Fan grille','Filament feed','Spool flange','Wound filament'],(.15,-.63,-1.33))
# Single upper shelf, with two book clusters and ornaments centered between.
box('Reference shelf',(-.3,.94,2.65),(4.5,.53,.085),wood,.012)
for x in [-2.25,1.65]:box('Reference bracket',(x,1.1,2.54),(.035,.10,.22),black)
navy=mat('Deep navy linen',(.018,.035,.054),.85);teal=mat('Petrol book cloth',(.019,.07,.076),.85);wine=mat('Oxide red book',(.16,.032,.019),.85)
titles=['ANATOMY','MEDICINE','DESIGN','NEUROSCIENCE','CREATIVE CODE','HUMAN FACTORS','FORM & LIGHT','VIRTUAL WORLDS']
book_objects=[]
for start,count in [(-1.77,8),(.55,7)]:
 x=start
 for i in range(count):
  before=set(bpy.data.objects);w=random.uniform(.09,.13);h=random.uniform(.40,.49);m=[navy,navy,teal,cream,wine][i%5];z=2.697
  box('Reference book cover',(x,.84,z+h/2),(w,.26,h),m,.004);box('Reference pages',(x,.85,z+h/2),(w*.82,.25,h*.96),paper,.001);box('Reference book spine',(x,.701,z+h/2),(w,.018,h),m,.004)
  text('Reference spine title',titles[i%8],(x,.689,z+h/2),.017,brass,(math.pi/2,0,math.pi/2))
  for zz in [.04,h-.045]:box('Reference foil band',(x,.688,z+zz),(w*.6,.002,.003),brass,.0004)
  text('Reference volume',str(i+1),(x,.687,z+.065),.018,brass)
  book_objects+=list(set(bpy.data.objects)-before);x+=w+.013
# Thin heart-shaped leaves with a central vein; trailing ivy at both shelf ends.
leaflight=mat('Ivy leaf olive',(.09,.14,.026),.46);leafdark=mat('Ivy leaf forest',(.025,.071,.016),.48)
for m in [leaflight,leafdark]:
 p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Subsurface Weight'].default_value=.08

def blade(name,loc,length,width,rot,m):
 verts=[]
 for j in range(13):
  t=j/12;w=width*math.sin(math.pi*t)**.75*(1-.25*t);verts.extend([(-w,.018*math.sin(t*math.pi),length*t),(0,.032*math.sin(t*math.pi),length*t),(w,.018*math.sin(t*math.pi),length*t)])
 faces=[]
 for j in range(12):
  for k in range(2):a=j*3+k;faces.append((a,a+1,a+4,a+3))
 mesh=bpy.data.meshes.new(name);mesh.from_pydata(verts,[],faces);o=bpy.data.objects.new(name,mesh);bpy.context.collection.objects.link(o);o.location=loc;o.rotation_euler=rot;o.data.materials.append(m)
 for f in mesh.polygons:f.use_smooth=True
 return o

def pot(x,y,z,r=.14):
 bpy.ops.mesh.primitive_cone_add(vertices=12,radius1=r*.7,radius2=r,depth=r*1.7,location=(x,y,z+r*.85));o=bpy.context.object;o.name='Faceted terracotta planter';o.data.materials.append(cream);cyl('Soil surface',(x,y,z+r*1.7),r*.93,.008,rubber);return z+r*1.7
ivy=[]
for x in [-2.26,1.64]:
 before=set(bpy.data.objects);y=.88;z=pot(x,y,2.697,.16)
 for i in range(45):
  a=i*2.4;r=random.uniform(.04,.23);base=(x+math.sin(a)*r,y+math.cos(a)*r,z+random.uniform(-.01,.14));blade('Ivy crown leaf',base,.13,.055,(random.uniform(-1.5,1.5),random.uniform(-1.5,1.5),a),random.choice([leaflight,leafdark]))
 for k in range(6):
  length=random.uniform(.40,.91);xx=x+(k-2.5)*.06;pts=[]
  for j in range(13):
   t=j/12;pos=(xx+math.sin(t*8+k)*.045,.61-.03*math.sin(t*4),z-.06-t*length);pts.append(pos)
   if j>0:blade('Trailing ivy leaf',pos,.11,.045,(math.pi*.72,(-1 if j%2 else 1)*.6,(-1 if j%2 else 1)*.7),random.choice([leaflight,leafdark]))
  tube('Trailing ivy vine',pts,.0035,leafdark)
 ivy+=list(set(bpy.data.objects)-before)
# Small tabletop plants, set clear of the interactive objects.
plants=[]
for x,y,z in [(-.91,.21,1.03),(1.11,.48,1.03)]:
 before=set(bpy.data.objects);base=pot(x,y,z,.115)
 for i in range(22):
  a=i*2.4;blade('Tabletop lance leaf',(x+math.sin(a)*.035,y+math.cos(a)*.035,base),random.uniform(.20,.37),.028,(math.cos(a)*.8,math.sin(a)*.8,a),random.choice([leaflight,leafdark]))
 plants+=list(set(bpy.data.objects)-before)
# Sculpted black raven silhouette: overlapping wing feathers and pointed beak.
ravenmat=mat('Raven satin obsidian',(.012,.017,.026),.32,.2)
raven=[];before=set(bpy.data.objects)
box('Raven plinth',(-.4,.85,2.715),(.42,.26,.035),black)
sphere('Raven body',(-.43,.85,2.92),(.105,.12,.20),ravenmat)
sphere('Raven neck',(-.37,.84,3.065),(.07,.08,.13),ravenmat)
sphere('Raven head',(-.33,.82,3.14),(.075,.073,.07),ravenmat)
# Cone axis points along the beak.
bpy.ops.mesh.primitive_cone_add(vertices=8,radius1=.036,radius2=.004,depth=.15,location=(-.235,.81,3.135));o=bpy.context.object;o.name='Raven beak';o.rotation_euler.y=math.pi/2;o.data.materials.append(black)
sphere('Raven eye',(-.304,.755,3.155),(.009,.006,.009),black)
for i in range(7):
 o=sphere('Raven layered wing feather',(-.46-i*.012,.741-i*.002,2.965-i*.023),(.048,.022,.14),ravenmat);o.rotation_euler.y=-.45
for i in range(3):
 o=sphere('Raven tail feather',(-.53+i*.02,.90,2.80),(.022,.025,.15),ravenmat);o.rotation_euler.y=-.65
for x in [-.46,-.38]:
 tube('Raven leg',[(x,.84,2.84),(x+.015,.84,2.75)],.009,black)
 for j in range(3):tube('Raven claw',[(x+.015,.84,2.75),(x+.015+(j-1)*.03,.77,2.74)],.005,black)
raven=list(set(bpy.data.objects)-before)
# Small black and brass globe with approximate continent silhouettes.
before=set(bpy.data.objects);gx,gy,gz=.13,.89,2.97
cyl('Globe foot',(gx,gy,2.72),.105,.035,black);cyl('Globe stand',(gx,gy,2.78),.025,.1,brass);sphere('Globe ocean',(gx,gy,gz),(.19,.19,.19),black,48)
for latpoly in [[(-15,-15),(5,-22),(32,-15),(37,12),(12,35),(-5,37),(-30,20),(-35,5)],[(-10,-78),(10,-70),(13,-52),(-5,-35),(-20,-42),(-50,-65)],[ (15,-100),(30,-115),(55,-130),(68,-100),(53,-55),(30,-85)],[(35,0),(55,-12),(65,20),(48,45),(65,90),(48,145),(20,120),(10,70)], [(-12,115),(-10,137),(-28,152),(-39,135),(-25,113)]]:
 verts=[]
 for lat,lon in latpoly:
  a=math.radians(lat);b=math.radians(lon);r=.191;verts.append((gx+r*math.cos(a)*math.sin(b),gy-r*math.cos(a)*math.cos(b),gz+r*math.sin(a)))
 mesh=bpy.data.meshes.new('Globe land');mesh.from_pydata(verts,[],[list(range(len(verts)))]);o=bpy.data.objects.new('Globe brass continents',mesh);bpy.context.collection.objects.link(o);o.data.materials.append(brass)
for orientation in ['equator','meridian']:
 pts=[]
 for i in range(65):
  a=i*math.tau/64;r=.212;pts.append((gx+r*math.cos(a),gy+r*math.sin(a),gz) if orientation=='equator' else (gx+r*math.cos(a),gy,gz+r*math.sin(a)))
 tube('Globe '+orientation,pts,.007,brass)
globe=list(set(bpy.data.objects)-before)
# Ivory low-poly fox on the printer bed, replacing the Blender monkey primitive.
foxmat=mat('Ivory printed resin',(.80,.59,.30),.38);before=set(bpy.data.objects);fx,fy,fz=1.73,.18,1.17
sphere('Fox seated body',(fx,fy,fz+.10),(.065,.055,.105),foxmat,8);sphere('Fox head',(fx,fy-.014,fz+.22),(.08,.065,.073),foxmat,8)
for dx in [-.052,.052]:
 bpy.ops.mesh.primitive_cone_add(vertices=4,radius1=.038,radius2=0,depth=.095,location=(fx+dx,fy,fz+.30));bpy.context.object.name='Fox pointed ear';bpy.context.object.data.materials.append(foxmat)
for dx in [-.026,.026]:sphere('Fox eye',(fx+dx,fy-.073,fz+.235),(.007,.005,.007),black,12)
sphere('Fox muzzle',(fx,fy-.065,fz+.20),(.023,.035,.022),foxmat,8);sphere('Fox nose',(fx,fy-.094,fz+.20),(.008,.006,.006),black,8)
tube('Fox curled tail',[(fx+.04,fy+.02,fz+.04),(fx+.12,fy,fz+.02),(fx+.08,fy-.08,fz+.02),(fx,fy-.08,fz+.025)],.028,foxmat)
fox=list(set(bpy.data.objects)-before)
# Pencil cup and desk nameplate sit to the right, matching the reference hierarchy.
before=set(bpy.data.objects);cyl('Pencil holder',(2.49,.27,1.15),.075,.24,black)
for i in range(9):
 x=2.49+random.uniform(-.045,.045);y=.27+random.uniform(-.045,.045);h=random.uniform(.35,.45);tube('Pencil',[(x,y,1.08),(x+random.uniform(-.07,.07),y,1.08+h)],.008,brass)
pencils=list(set(bpy.data.objects)-before)
box('Nameplate brass frame',(1.05,-.54,1.105),(.66,.045,.16),brass,.006);box('Nameplate black face',(1.05,-.566,1.105),(.63,.004,.13),black,.003)
text('Nameplate name','Dr. Murat Gökduman',(1.05,-.570,1.128),.046,brass);text('Nameplate subtitle','Ed Tech | VR Dev',(1.05,-.570,1.077),.025,brass)
# Black mug near printer rather than on the left.
relocate(['Cup base','Cup rim','Cup handle','Coffee'],(3.13,.04,0))
# The mug wall was unnamed in the source; identify its open cylindrical mesh by geometry/location.
for o in bpy.data.objects:
 if o.type=='MESH' and abs(o.location.x+1.86)<.001 and abs(o.location.z-1.13)<.001:o.location.x+=3.13;o.location.y+=.04;o.data.materials.clear();o.data.materials.append(black)
for o in bpy.data.objects:
 if o.name.startswith(('Cup base','Cup rim','Cup handle')):o.data.materials.clear();o.data.materials.append(black)
# Blue screen and warm illuminated desktop; no captions or navigation text in the scene.
bpy.data.objects['Warm task lamp'].data.energy=85;bpy.data.objects['Large soft window'].data.energy=45;bpy.data.objects['Warm ceiling bounce'].data.energy=35;bpy.data.objects['Shelf wash'].data.energy=12
# Right pendant and its distinct pool of light.
cyl('Pendant cable',(2.43,.5,3.22),.014,.8,black)
bpy.ops.mesh.primitive_cone_add(vertices=48,radius1=.25,radius2=.095,depth=.31,location=(2.43,.5,2.96));o=bpy.context.object;o.name='Right pendant shade';o.data.materials.append(black)
cyl('Pendant diffuser',(2.43,.5,2.802),.235,.005,bpy.data.materials['Warm lamp diffuser']);area('Pendant warm light',(2.43,.5,2.79),(2.1,1.13,1.85),65,(1,.55,.22),.25)
area('Monitor soft blue spill',(.15,.15,1.56),(.15,-.4,1.02),3,(.20,.42,1),.8)
# Framing: desktop is an intimate, front-facing view of the tabletop and one shelf.
scene=bpy.context.scene;scene.cycles.samples=96;scene.camera.location=(0,-7.2,2.1);scene.camera.rotation_euler=(Vector((0,.35,2.03))-scene.camera.location).to_track_quat('-Z','Y').to_euler();scene.camera.data.lens=45
scene.render.resolution_x=1800;scene.render.resolution_y=1050;scene.render.resolution_percentage=100;scene.render.filepath=os.path.join(ROOT,'renders/office-reference-desktop.png')
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT,'assets/office-reference-desktop.blend'));bpy.ops.render.render(write_still=True)
# Mobile is recomposed, not a crop: three shelves and a full-height desk view.
# Transform every cluster as a group; preserve all model details.
def shift(objs,d):
 for o in objs:
  if o.name in bpy.data.objects:o.location+=Vector(d)
# Narrow furniture while retaining the central workstation.
bpy.data.objects['Solid walnut desk'].dimensions.x=3.0
for o in bpy.data.objects:
 if o.name.startswith('Desk steel leg'):o.location.x=math.copysign(1.36,o.location.x)
 if o.name.startswith(('Drawer cabinet','Drawer front','Drawer pull')):o.location.x+=.97;o.scale.x*=.7
 if o.name.startswith('Reference shelf'):o.location.z=3.82;o.dimensions.x=2.9;o.location.x=0
 if o.name.startswith('Reference bracket'):o.location.z+=1.17;o.location.x=math.copysign(1.2,o.location.x)
 if o.name.startswith(('Nameplate','Stethoscope')):o.location.z+=2.12;o.location.x-=1.0
 if o.name.startswith('Steel diaphragm'):o.location.z+=2.12;o.location.x-=1.0
# Books are independently arranged across the top and third shelves.
for o in book_objects:
 if o.location.x<0:o.location.x+=.90;o.location.z+=1.17
 else:o.location.x-=.15;o.location.z+=1.17
shift(ivy,(0,0,1.17))
for o in ivy:o.location.x+=.98 if o.location.x<0 else -.45
box('Mobile middle shelf',(0,.72,3.08),(2.9,.65,.075),wood,.012);box('Mobile lower shelf',(0,.72,2.20),(2.9,.65,.075),wood,.012)
shift(vr,(.78,.5,2.06));shift(printer,(-2.73,.5,1.17));shift(fox,(-2.73,.5,1.17));shift(raven,(1.4,0,-.49));shift(globe,(0,0,1.17))
relocate(['Phone','Phone glass','Phone dock'],(.7,.6,2.06))
# Move tabletop accessories inward and clear the tall composition.
for o in bpy.data.objects:
 if o.name.startswith(('Lamp base','Lamp arm','Lamp joint','Lamp diffuser','Warm task lamp')):o.location.x+=1.15
 if o.name.startswith('Cone') and o.location.x<-2:o.location.x+=1.15
 if o.name.startswith(('Cup base','Cup rim','Cup handle','Coffee')):o.location.x-=2.0
 if o.name.startswith(('Leather notebook','Notebook paper','Brass pen')):o.location.x+=.9
 if o.name.startswith(('Right pendant','Pendant')):o.hide_render=True
for o in plants:o.location.x*=.87
shift(pencils,(-1.22,0,0))
# Fill lower shelf with a compact library and a small plant.
for i in range(6):
 x=-.34+i*.13;h=.41+random.uniform(-.03,.04);box('Mobile lower books',(x,.77,2.24+h/2),(.11,.23,h),[navy,teal,cream][i%3],.004);text('Mobile book title',titles[i],(x,.648,2.24+h/2),.019,brass,(math.pi/2,0,math.pi/2))
scene.camera.location=(0,-7.8,2.45);scene.camera.rotation_euler=(Vector((0,.3,2.23))-scene.camera.location).to_track_quat('-Z','Y').to_euler();scene.camera.data.lens=44
scene.render.resolution_x=900;scene.render.resolution_y=1600;scene.render.filepath=os.path.join(ROOT,'renders/office-reference-mobile.png')
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT,'assets/office-reference-mobile.blend'));bpy.ops.render.render(write_still=True)
