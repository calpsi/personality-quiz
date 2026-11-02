"""Six-second, 24fps preview of the floating title in the finished illustrated museum."""
import bpy
from pathlib import Path
ROOT=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'quiet-collection-illustrated-museum.blend'))
s=bpy.context.scene;s.camera=bpy.data.objects['08 | Floating title close view']
s.frame_start=1;s.frame_end=144;s.render.fps=24
s.render.engine='BLENDER_EEVEE'
if hasattr(s.eevee,'taa_render_samples'):s.eevee.taa_render_samples=32
s.render.resolution_x=960;s.render.resolution_y=640;s.render.resolution_percentage=100
s.render.image_settings.media_type='VIDEO';s.render.image_settings.file_format='FFMPEG'
s.render.ffmpeg.format='MPEG4';s.render.ffmpeg.codec='H264';s.render.ffmpeg.constant_rate_factor='MEDIUM'
s.render.filepath=str(ROOT/'what-are-you-title.mp4')
bpy.ops.render.render(animation=True)
print('TITLE_PREVIEW_COMPLETE',flush=True)
