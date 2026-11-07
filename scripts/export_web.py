"""Bake fixed office lighting into interactive GLB meshes for the browser."""
import bpy, os, math, json, sys
from mathutils import Vector
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
mode=sys.argv[-1] if sys.argv[-1] in ['desktop','mobile'] else 'desktop'
bpy.ops.wm.open_mainfile(filepath=os.path.join(ROOT,'assets/office-reference-'+mode+'-v2.blend'))
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=24;scene.cycles.use_denoising=True;scene.cycles.max_bounces=5
DEST=os.path.join(ROOT,'public/models');os.makedirs(DEST,exist_ok=True)
# Explicit semantic grouping keeps click/hover on real modeled objects.
def category(name):
 if name.startswith(('Monitor','Display glass','Screen landscape','Power LED')):return 'projects'
 if name.startswith(('VR ','Tracking lens','Head strap','Top head strap','Optical glass')):return 'vr'
 if name.startswith(('Printer','Print bed','Print head','Gantry','Linear guide','Drive belt','Hex bolt','Bolt slot','Nozzle shroud','Hotend fan','Fan grille','Filament feed','Spool flange','Wound filament','Fox ')):return 'design'
 if name.startswith(('Phone','Phone glass','Phone dock')):return 'contact'
 if name.startswith(('Nameplate','Stethoscope','Steel diaphragm','Soft eartip')):return 'about'
 if name.startswith(('Back wall','Side wall','Floorboard','Woven floor rug')):return 'architecture'
 return 'furniture'
# Evaluate modifiers/text/curves once. Geometry remains in world coordinates.
depsgraph=bpy.context.evaluated_depsgraph_get();groups={}; originals=[]
for original in list(scene.objects):
 if original.hide_render:continue
 if original.type not in {'MESH','CURVE','FONT','SURFACE'}:continue
 evaluated=original.evaluated_get(depsgraph);mesh=bpy.data.meshes.new_from_object(evaluated,preserve_all_data_layers=True,depsgraph=depsgraph)
 if not mesh.polygons:continue
 o=bpy.data.objects.new(original.name+' web',mesh);scene.collection.objects.link(o);o.matrix_world=original.matrix_world.copy();groups.setdefault(category(original.name),[]).append(o);originals.append(original)
for o in originals:bpy.data.objects.remove(o,do_unlink=True)
merged={}
for key,objs in groups.items():
 bpy.ops.object.select_all(action='DESELECT')
 for o in objs:o.select_set(True)
 bpy.context.view_layer.objects.active=objs[0];bpy.ops.object.join();o=bpy.context.object;o.name=key;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 # Keep close-up objects detailed; remove redundant triangles from high-poly foliage/raven.
 if len(o.data.polygons)>60000:
  mod=o.modifiers.new('Web geometry budget','DECIMATE');mod.ratio=60000/len(o.data.polygons);bpy.ops.object.modifier_apply(modifier=mod.name)
 bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT');bpy.ops.uv.smart_project(angle_limit=math.radians(68),island_margin=.004);bpy.ops.object.mode_set(mode='OBJECT');merged[key]=o
# Freeze generated-coordinate materials per source before join is not possible here;
# existing PBR textures still provide surface variation; baked maps preserve scene lighting.
# Bake all groups before replacing materials so later groups see original illumination.
baked={}
for key,o in merged.items():
 resolution=2048 if key in ['architecture','furniture'] else (1024 if key in ['projects','vr','design'] else 512)
 image=bpy.data.images.new(mode+'-'+key,width=resolution,height=resolution,alpha=False)
 # Material copies prevent a shared material's target node from changing another group.
 for slot in o.material_slots:
  if not slot.material:continue
  slot.material=slot.material.copy();nodes=slot.material.node_tree.nodes;node=nodes.new('ShaderNodeTexImage');node.image=image;nodes.active=node
 bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
 scene.render.bake.use_clear=True;scene.render.bake.margin=8
 print('BAKING',mode,key,len(o.data.polygons),flush=True)
 bpy.ops.object.bake(type='COMBINED',use_selected_to_active=False)
 image.filepath_raw=os.path.join(DEST,mode+'-'+key+'.jpg');image.file_format='JPEG';image.save();baked[key]=image
for key,o in merged.items():
 m=bpy.data.materials.new(mode+' '+key+' baked');m.use_nodes=True;n=m.node_tree.nodes;n.clear();out=n.new('ShaderNodeOutputMaterial');emit=n.new('ShaderNodeEmission');tex=n.new('ShaderNodeTexImage');tex.image=baked[key];m.node_tree.links.new(tex.outputs['Color'],emit.inputs['Color']);m.node_tree.links.new(emit.outputs[0],out.inputs['Surface']);o.data.materials.clear();o.data.materials.append(m)
 for p in o.data.polygons:p.material_index=0
 o['section']=key if key in ['projects','vr','design','contact','about'] else ''
bpy.ops.object.select_all(action='DESELECT')
for o in merged.values():o.select_set(True)
bpy.ops.export_scene.gltf(filepath=os.path.join(DEST,'office-'+mode+'.glb'),export_format='GLB',use_selection=True,export_lights=False,export_cameras=False,export_extras=True,export_image_format='JPEG',export_jpeg_quality=88)
info={key:{'polygons':len(o.data.polygons)} for key,o in merged.items()};json.dump(info,open(os.path.join(DEST,mode+'-stats.json'),'w'),indent=2)
print('EXPORTED',mode,flush=True)
