import bpy
import os
import subprocess


class MYADDON_OT_open_in_vscode(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_open_in_vscode"
    bl_label = "VSCodeで開く"
    bl_description = "プロジェクトフォルダをVSCodeで開きます"

    def execute(self, context):
        addon_dir = os.path.dirname(os.path.dirname(__file__))
        try:
            subprocess.Popen(["code", addon_dir], shell=True)
            self.report({'INFO'}, f"VSCodeで起動中: {addon_dir}")
        except Exception as e:
            self.report({'ERROR'}, f"VSCodeの起動に失敗しました: {str(e)}")
        return {'FINISHED'}
