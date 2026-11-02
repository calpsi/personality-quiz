"""Run in Blender Text Editor; N sidebar > Museum. Local authored preview, no API calls."""
import bpy, math, textwrap
from bpy_extras import view3d_utils
LINES={'abraham': 'Oh, hello! What can I help you with?', 'clock': 'Oh, it does that. You haven’t missed anything—we’re still open.', 'labels': 'Those go by the minerals. I’ll put them back when they come down.', 'meteorite': 'Oh, you can see underneath it now! That’s handy.', 'drawer': 'Yes! Mind your sleeves. They’re quite difficult to get out.', 'leaves': 'Mind your head. They tickle if they get in your ears.', 'help': 'Anywhere you like! Deep Time is on the left, Earth & Space is on the right, and Living Systems is straight ahead.', 'strange': 'Is it? Would you like me to come with you?', 'chat': 'I found my pencil! It was right here the whole time. What have you been looking at?'}

def reply(scene,key):
 scene.museum_reply=LINES[key];scene.museum_talk_open=True
 if key=='drawer':
  tray=bpy.data.objects.get('Dream | drawer sliding tray')
  if tray:
   is_open=not tray.get('open',True);tray['open']=is_open;tray.location.y=0 if is_open else .58
 elif key=='labels':
  o=bpy.data.objects.get('Dream | escaped labels')
  if o:
   settled=not o.get('settled',False);o['settled']=settled
   if o.animation_data:
    if settled:
     if o.animation_data.action:o['saved_action']=o.animation_data.action.name
     o.animation_data.action=None
    elif o.get('saved_action'):o.animation_data.action=bpy.data.actions.get(o['saved_action'])
   o.location.z=1.55 if settled else 1.9
 elif key=='meteorite':
  o=bpy.data.objects.get('Meteorite specimen')
  if o:
   material=o.active_material
   # A local inspect state; base artwork and scoring remain untouched.
   o['inspected']=not o.get('inspected',False)
   # The authored line already describes the inspection.
 elif key=='clock':
  frozen=not scene.get('clock_paused',False);scene['clock_paused']=frozen
  for o in bpy.data.objects:
   if o.name.startswith(('Dream | Minute hand','Dream | Hour hand')) and o.animation_data:
    if frozen:
     if o.animation_data.action:o['saved_action']=o.animation_data.action.name
     o.animation_data.action=None
    elif o.get('saved_action'):o.animation_data.action=bpy.data.actions.get(o['saved_action'])
 elif key=='leaves':
  o=bpy.data.objects.get('Dream | drifting leaves')
  if o:o.scale=(.6,.6,.6) if o.scale.x>.8 else (1,1,1)
class MUSEUM_OT_interact(bpy.types.Operator):
 bl_idname='museum.interact';bl_label='Talk / inspect';bl_options={'UNDO'}
 key:bpy.props.StringProperty(default='abraham')
 def execute(self,context):reply(context.scene,self.key);return {'FINISHED'}
class MUSEUM_OT_close(bpy.types.Operator):
 bl_idname='museum.close_talk';bl_label='Back to the museum'
 def execute(self,context):context.scene.museum_talk_open=False;return {'FINISHED'}
class MUSEUM_OT_pick(bpy.types.Operator):
 bl_idname='museum.pick';bl_label='Enable click interactions'
 def invoke(self,context,event):
  if context.area.type!='VIEW_3D':return {'CANCELLED'}
  context.window_manager.modal_handler_add(self);context.area.header_text_set('Museum preview: click Abraham or an oddity. Esc to stop.');return {'RUNNING_MODAL'}
 def modal(self,context,event):
  if event.type=='ESC':context.area.header_text_set(None);return {'CANCELLED'}
  if event.type=='LEFTMOUSE' and event.value=='PRESS':
   region=next((r for r in context.area.regions if r.type=='WINDOW'),None)
   if not region:return {'PASS_THROUGH'}
   coord=(event.mouse_x-region.x,event.mouse_y-region.y)
   if not(0<=coord[0]<region.width and 0<=coord[1]<region.height):return {'PASS_THROUGH'}
   rv=context.space_data.region_3d;origin=view3d_utils.region_2d_to_origin_3d(region,rv,coord);direction=view3d_utils.region_2d_to_vector_3d(region,rv,coord)
   hit,loc,normal,index,obj,matrix=context.scene.ray_cast(context.evaluated_depsgraph_get(),origin,direction)
   if hit:
    while obj:
     if obj.get('interaction_id'):
      reply(context.scene,obj['interaction_id']);context.area.tag_redraw();return {'RUNNING_MODAL'}
     obj=obj.parent
  return {'PASS_THROUGH'}
class MUSEUM_PT_preview(bpy.types.Panel):
 bl_label='Museum interaction preview';bl_idname='MUSEUM_PT_preview';bl_space_type='VIEW_3D';bl_region_type='UI';bl_category='Museum'
 def draw(self,context):
  l=self.layout;s=context.scene;l.label(text='Local dialogue preview · no live AI',icon='INFO');l.operator('museum.pick')
  l.operator('museum.interact',text='Talk to Abraham',icon='OUTLINER_OB_ARMATURE').key='abraham'
  if s.museum_talk_open:
   box=l.box();box.label(text='Abraham')
   for line in textwrap.wrap(s.museum_reply,42):box.label(text=line)
   for key,label in [('help','Where should I go?'),('strange','Is this normal?'),('chat','Just chatting')]:box.operator('museum.interact',text=label).key=key
   box.operator('museum.close_talk')
  l.separator();l.label(text='Unscored discoveries')
  for key,label in [('clock','Touch the backwards clock'),('labels','Straighten the floating labels'),('meteorite','Inspect the hovering meteorite'),('drawer','Open / close the night drawer'),('leaves','Gather / release the leaves')]:l.operator('museum.interact',text=label).key=key
classes=(MUSEUM_OT_interact,MUSEUM_OT_close,MUSEUM_OT_pick,MUSEUM_PT_preview)
def register():
 for cls in classes:
  old=getattr(bpy.types,cls.__name__,None)
  if old:bpy.utils.unregister_class(old)
  bpy.utils.register_class(cls)
 bpy.types.Scene.museum_reply=bpy.props.StringProperty(default=LINES['abraham'])
 bpy.types.Scene.museum_talk_open=bpy.props.BoolProperty(default=False)
if __name__=='__main__':register()
