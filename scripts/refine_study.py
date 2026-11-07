"""Refine the initial office study with scanned PBR wood and modeled detail."""
import bpy, math, random, os
from mathutils import Vector
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
bpy.ops.wm.open_mainfile(filepath=os.path.join(ROOT,'assets/office-study.blend'))
random.seed(62)
def mat(name,c,rough=.5,metal=0):
 m=bpy.data.materials.new(name);m.diffuse_color=(*c,1);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*c,1);p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal;return m
def box(name,loc,size,m,bevel=.005):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=name;o.dimensions=size;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(m)
 if bevel:mod=o.modifiers.new('Rounded edges','BEVEL');mod.width=bevel;mod.segments=3;o.modifiers.new('Weighted normals','WEIGHTED_NORMAL')
 return o
def cyl(name,loc,r,depth,m,rotation=None):
 bpy.ops.mesh.primitive_cylinder_add(vertices=40,radius=r,depth=depth,location=loc);o=bpy.context.object;o.name=name;o.data.materials.append(m)
 if rotation:o.rotation_euler=rotation
 mod=o.modifiers.new('Machined edges','BEVEL');mod.width=.002;mod.segments=3;o.modifiers.new('Weighted normals','WEIGHTED_NORMAL');return o
def tube(name,pts,r,m):
 c=bpy.data.curves.new(name,'CURVE');c.dimensions='3D';c.bevel_depth=r;c.bevel_resolution=3;s=c.splines.new('BEZIER');s.bezier_points.add(len(pts)-1)
 for p,v in zip(s.bezier_points,pts):p.co=v;p.handle_left_type='AUTO';p.handle_right_type='AUTO'
 o=bpy.data.objects.new(name,c);bpy.context.collection.objects.link(o);o.data.materials.append(m);return o
def text(name,body,loc,size,m,rot=(math.pi/2,0,0)):
 c=bpy.data.curves.new(name,'FONT');c.body=body;c.size=size;c.align_x='CENTER';c.align_y='CENTER';c.extrude=.0001;o=bpy.data.objects.new(name,c);bpy.context.collection.objects.link(o);o.location=loc;o.rotation_euler=rot;o.data.materials.append(m);return o
black=bpy.data.materials['Powder coated graphite'];rubber=bpy.data.materials['Soft black rubber'];brass=bpy.data.materials['Brushed brass'];cream=bpy.data.materials['Warm ceramic'];paper=bpy.data.materials['Ivory paper edges'];steel=mat('Brushed stainless steel',(.45,.49,.51),.24,.88);darkcloth=mat('Anthracite woven fabric',(.025,.03,.028),.92)
# Scanned real wood: color, roughness and OpenGL normals, consistently projected.
wood=bpy.data.materials['Oiled American walnut'];n=wood.node_tree.nodes;l=wood.node_tree.links;n.clear();out=n.new('ShaderNodeOutputMaterial');p=n.new('ShaderNodeBsdfPrincipled');l.new(p.outputs[0],out.inputs[0]);p.inputs['Coat Weight'].default_value=.16;p.inputs['Coat Roughness'].default_value=.32
tex=n.new('ShaderNodeTexCoord');mp=n.new('ShaderNodeMapping');mp.inputs['Scale'].default_value=(1.6,.65,.65);mp.inputs['Rotation'].default_value=(0,0,math.pi/2);l.new(tex.outputs['Generated'],mp.inputs['Vector'])
for kind,target in [('diff','Base Color'),('rough','Roughness'),('nor_gl','Normal')]:
 im=bpy.data.images.load(os.path.join(ROOT,'assets/textures/dark_wood/dark_wood_'+kind+'_2k.jpg'),check_existing=True);im.pack();node=n.new('ShaderNodeTexImage');node.image=im;node.projection='BOX';node.projection_blend=.18;l.new(mp.outputs[0],node.inputs[0])
 if kind!='diff':im.colorspace_settings.name='Non-Color'
 if kind=='nor_gl':normal=n.new('ShaderNodeNormalMap');normal.inputs['Strength'].default_value=.3;l.new(node.outputs['Color'],normal.inputs['Color']);l.new(normal.outputs[0],p.inputs[target])
 else:l.new(node.outputs['Color'],p.inputs[target])
# More subtle plaster instead of large cloudy patches.
wall=bpy.data.materials['Limewashed umber'];r=next(n for n in wall.node_tree.nodes if n.type=='VALTORGB');r.color_ramp.elements[0].color=(.073,.059,.045,1);r.color_ramp.elements[1].color=(.105,.088,.068,1)
for node in wall.node_tree.nodes:
 if node.type=='BUMP':node.inputs['Distance'].default_value=.003
# Fine woven microstructure shared by book covers and desk mat.
for m in [darkcloth,rubber]+[m for m in bpy.data.materials if m.name.startswith('Book cloth')]:
 n=m.node_tree.nodes;l=m.node_tree.links;p=n.get('Principled BSDF');noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=230;noise.inputs['Detail'].default_value=2;b=n.new('ShaderNodeBump');b.inputs['Strength'].default_value=.22;b.inputs['Distance'].default_value=.0015;l.new(noise.outputs['Fac'],b.inputs['Height']);l.new(b.outputs[0],p.inputs['Normal'])
# Book spines: foil titles, publisher ornament, subtle alignment variations.
titles=['ANATOMY','DESIGN','NEUROSCIENCE','CREATIVE CODE','MEDICINE','FORM & LIGHT','VIRTUAL WORLDS','HUMAN FACTORS']
for i,o in enumerate(sorted([o for o in bpy.data.objects if o.name.startswith('Spine')],key=lambda o:o.location.x)):
 x,y,z=o.location;h=o.dimensions.z;w=o.dimensions.x
 title=text('Embossed spine title',titles[i%len(titles)],(x,y-.012,z),min(.025,w*.23),brass,(math.pi/2,0,math.pi/2))
 text('Volume number',str(i%9+1),(x,y-.012,z-h*.35),.022,brass)
 # Bookbinding hinge grooves along spine.
 for dx in [-w*.42,w*.42]:box('Cloth hinge',(x+dx,y-.01,z),(.002,.001,h*.92),darkcloth,.0004)
# Small key legends sit on the actual top surface, preserving geometric keycaps.
rows=['1234567890-=','QWERTYUIOP[]','ASDFGHJKL;','ZXCVBNM,./']
keys=sorted([o for o in bpy.data.objects if o.name.startswith('Keycap')],key=lambda o:(round(o.location.y,3),o.location.x))
for i,o in enumerate(keys):
 row=i//15;col=i%15;char=rows[row][col] if row<4 and col<len(rows[row]) else ''
 if char:text('Key legend',char,(o.location.x,o.location.y,1.109),.016,paper,(0,0,0))
# Monitor hardware: lower bezel, indicator, back shell, cables, side seam.
box('Monitor bottom chin',(.15,.208,1.235),(1.88,.018,.045),black)
led=mat('LED blue',(.05,.3,.7),.2);p=led.node_tree.nodes.get('Principled BSDF');p.inputs['Emission Color'].default_value=(.08,.4,1,1);p.inputs['Emission Strength'].default_value=2
cyl('Power LED',(.98,.196,1.235),.004,.002,led,(math.pi/2,0,0))
box('Monitor back shell',(.15,.34,1.75),(1.64,.10,.88),black,.04)
tube('Monitor cable',[(.15,.43,1.4),(.26,.49,1.06),(.7,.6,1.04),(1.1,.69,.81)],.009,rubber)
# Atmospheric layered mountain wallpaper with far ridges behind near ridges.
for o in list(bpy.data.objects):
 if o.name.startswith('Screen landscape'):bpy.data.objects.remove(o,do_unlink=True)
for i in range(8):
 t=i/7;color=(.09*(1-t)+.008*t,.12*(1-t)+.025*t,.19*(1-t)+.047*t);m=mat('Landscape ridge '+str(i),color,.55);p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Emission Color'].default_value=(*color,1);p.inputs['Emission Strength'].default_value=.7
 y=.204-i*.0008;verts=[(-.76,y,1.25),(1.06,y,1.25)]
 for j in range(81):
  x=1.06-j*1.82/80;z=1.91-i*.075+.07*math.sin(j*.23+i*1.5)+.04*math.sin(j*.47+i)+random.uniform(-.025,.025);verts.append((x,y,z))
 me=bpy.data.meshes.new('Ridge silhouette');me.from_pydata(verts,[],[list(range(len(verts)))]);o=bpy.data.objects.new('Screen landscape detailed',me);bpy.context.collection.objects.link(o);o.data.materials.append(m)
# VR molded seams, optical sensors, fabric strap, side arms and ventilation.
for x in [-.69,-.27]:
 box('VR side hinge',(x,.75,2.78),(.065,.23,.09),cream,.018)
for x in [-.63,-.48,-.33]:
 box('VR sensor housing',(x,.602,2.78),(.045,.012,.105),black,.021)
 cyl('VR camera lens',(x,.593,2.8),.012,.003,steel,(math.pi/2,0,0));cyl('Optical glass',(x,.590,2.8),.008,.003,rubber,(math.pi/2,0,0))
for i in range(15):box('VR vent',(-.67+i*.027,.64,2.915),(.012,.035,.003),rubber,.001)
tube('Top head strap',[(-.48,.70,2.91),(-.48,.91,3.065),(-.48,1.08,2.86)],.036,darkcloth)
# Printer rods, belts, bolt heads, screen, fan and spool.
for x in [1.29,1.87]:
 cyl('Linear guide',(x,.92,2.75),.009,.57,steel)
 box('Drive belt',(x,.94,2.73),(.012,.008,.52),rubber,.001)
 for z in [2.43,3.07]:cyl('Hex bolt',(x,.635,z),.013,.012,steel,(math.pi/2,0,0));box('Bolt slot',(x,.627,z),(.014,.002,.002),black,.0002)
box('Printer electronics',(1.58,.67,2.395),(.72,.16,.095),black,.012)
box('Printer control screen',(1.51,.582,2.40),(.20,.006,.052),bpy.data.materials['Midnight blue screen'],.003)
text('Printer display','READY',(1.51,.577,2.40),.019,paper)
cyl('Printer encoder',(1.82,.568,2.40),.028,.021,black,(math.pi/2,0,0));cyl('Encoder trim',(1.82,.555,2.40),.021,.004,steel,(math.pi/2,0,0))
for i in range(9):box('Printer cooling grille',(1.28+i*.012,.581,2.4),(.005,.003,.04),rubber,.001)
box('Nozzle shroud',(1.59,.74,2.92),(.105,.10,.115),black,.012)
cyl('Hotend fan',(1.59,.681,2.93),.036,.013,rubber,(math.pi/2,0,0))
for i in range(7):
 a=i*math.tau/7;tube('Fan grille',[(1.59,.670,2.93),(1.59+math.sin(a)*.03,.670,2.93+math.cos(a)*.03)],.002,steel)
tube('Filament feed',[(1.59,.80,2.99),(1.58,1.04,3.22),(1.86,1.06,3.26)],.004,cream)
for y in [1.025,1.095]:cyl('Spool flange',(1.91,y,3.18),.12,.014,black,(math.pi/2,0,0))
cyl('Wound filament',(1.91,1.06,3.18),.10,.064,cream,(math.pi/2,0,0))
# Improved medical instrument, silver binaurals and soft eartips.
for pts in [[(1.65,-.38,1.06),(1.58,-.48,1.065),(1.44,-.47,1.07)],[(1.65,-.38,1.06),(1.72,-.52,1.065),(1.57,-.59,1.07)]]:
 tube('Stethoscope binaural',pts,.009,steel);cyl('Soft eartip',pts[-1],.016,.028,rubber,(0,math.pi/2,0))
bpy.data.objects['Steel diaphragm'].data.materials.clear();bpy.data.objects['Steel diaphragm'].data.materials.append(steel)
# Desk edge joining detail and discreet screws.
for x in [-2.6,2.6]:
 for y in [-.56,.56]:cyl('Recessed desk fastener',(x,y,.922),.012,.009,black)
# Woven rug fills the floor and gives the room a less showroom-like composition.
rug=mat('Woven charcoal kilim',(.055,.047,.035),.96);n=rug.node_tree.nodes;l=rug.node_tree.links;p=n.get('Principled BSDF');tex=n.new('ShaderNodeTexCoord');wave=n.new('ShaderNodeTexWave');wave.wave_type='BANDS';wave.bands_direction='X';wave.inputs['Scale'].default_value=150;l.new(tex.outputs['Generated'],wave.inputs['Vector']);b=n.new('ShaderNodeBump');b.inputs['Strength'].default_value=.35;b.inputs['Distance'].default_value=.004;l.new(wave.outputs['Color'],b.inputs['Height']);l.new(b.outputs[0],p.inputs['Normal'])
box('Woven floor rug',(.2,-1.15,.002),(4.75,1.7,.018),rug,.008)
for x in [-2.12,2.52]:box('Rug border',(x,-1.15,.013),(.035,1.65,.003),brass,.001)
# Lighting balances localized pools of warm light against a low cool fill.
world=bpy.context.scene.world;world.use_nodes=True;world.node_tree.nodes.get('Background').inputs['Color'].default_value=(.12,.16,.23,1);world.node_tree.nodes.get('Background').inputs['Strength'].default_value=.10
bpy.data.objects['Large soft window'].data.energy=65
bpy.data.objects['Warm ceiling bounce'].data.energy=65
bpy.data.objects['Shelf wash'].data.energy=26
bpy.data.objects['Warm task lamp'].data.energy=55
bpy.data.objects['Printer warm light'].data.energy=9
# Visible practical lamp diffuser.
diffuser=mat('Warm lamp diffuser',(1,.72,.35),.5);p=diffuser.node_tree.nodes.get('Principled BSDF');p.inputs['Emission Color'].default_value=(1,.52,.18,1);p.inputs['Emission Strength'].default_value=2
cyl('Lamp diffuser',(-2.1,.12,1.842),.164,.004,diffuser)
# Keep actual lamp illumination below diffuser so it is not occluded.
bpy.data.objects['Warm task lamp'].location.z=1.831
scene=bpy.context.scene;scene.cycles.samples=160;scene.cycles.use_denoising=True;scene.camera.location=(.4,-7.75,2.98);scene.camera.rotation_euler=(Vector((0,.25,2.02))-scene.camera.location).to_track_quat('-Z','Y').to_euler();scene.camera.data.lens=44
scene.render.resolution_x=1800;scene.render.resolution_y=1238;scene.render.filepath=os.path.join(ROOT,'renders/office-refined.png')
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT,'assets/office-refined.blend'));bpy.ops.render.render(write_still=True)
