import bpy

class MYADDON_OT_add_disabled(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_add_disabled"
    bl_label = "無効フラグ追加"
    bl_description = "選択中のオブジェクトに無効フラグを追加します"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.object is None:
            self.report({'WARNING'}, "オブジェクトが選択されていません")
            return {'CANCELLED'}

        if "disabled" in context.object:
            self.report({'INFO'}, "すでに無効フラグが存在します")
            return {'FINISHED'}

        context.object["disabled"] = True
        self.report({'INFO'}, "無効フラグを追加しました")
        return {'FINISHED'}


class OBJECT_PT_disabled(bpy.types.Panel):
    bl_idname = "OBJECT_PT_disabled"
    bl_label = "無効フラグ設定"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    def draw(self, context):
        layout = self.layout

        if context.object is None:
            layout.label(text="オブジェクトが選択されていません")
            return

        if "disabled" in context.object:
            layout.prop(
                context.object,
                '["disabled"]',
                text="無効化 (disabled)"
            )
        else:
            layout.operator(
                MYADDON_OT_add_disabled.bl_idname,
                text=MYADDON_OT_add_disabled.bl_label
            )
