import bpy
import mathutils
from .utils import VectorUtility


class MYADDON_OT_add_ico_sphere(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_add_ico_sphere"
    bl_label = "ICO球追加"
    bl_description = "ICO球のEmptyを追加します"

    def execute(self, context):
        empty = bpy.data.objects.new("ICO球", None)
        context.collection.objects.link(empty)

        empty.empty_display_type = 'SPHERE'
        empty.empty_display_size = 1.0
        empty.location = context.scene.cursor.location

        return {'FINISHED'}


class MYADDON_OT_add_cube(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_add_cube"
    bl_label = "Cube追加"
    bl_description = "Cubeを追加します"

    def execute(self, context):
        bpy.ops.mesh.primitive_cube_add(
            size=1.0,
            location=context.scene.cursor.location
        )

        cube = context.object
        cube.name = "Cube"

        return {'FINISHED'}


class MYADDON_OT_add_filename(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_add_filename"
    bl_label = "FileName追加"
    bl_description = "選択中のオブジェクトにfile_nameを追加します"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.object is None:
            self.report({'WARNING'}, "オブジェクトが選択されていません")
            return {'CANCELLED'}

        context.object["file_name"] = ""

        return {'FINISHED'}


class MYADDON_OT_add_collider(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_add_collider"
    bl_label = "Collider追加"
    bl_description = "選択中のオブジェクトにColliderを追加します"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.object is None:
            self.report({'WARNING'}, "オブジェクトが選択されていません")
            return {'CANCELLED'}

        context.object["collider"] = "BOX"
        context.object["collider_center"] = mathutils.Vector((0.0, 0.0, 0.0))
        context.object["collider_size"] = mathutils.Vector((2.0, 2.0, 2.0))

        return {'FINISHED'}


class MYADDON_OT_add_trigger_box(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_add_trigger_box"
    bl_label = "TriggerBox追加"
    bl_description = "選択中のオブジェクトにTriggerBoxを追加します"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.object is None:
            self.report({'WARNING'}, "オブジェクトが選択されていません")
            return {'CANCELLED'}

        context.object["trigger"] = "BOX"
        context.object["trigger_name"] = "Trigger"
        context.object["trigger_center"] = mathutils.Vector((0.0, 0.0, 0.0))
        context.object["trigger_size"] = mathutils.Vector((2.0, 2.0, 2.0))

        return {'FINISHED'}


class MYADDON_OT_add_enemy_spawn_point(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_add_enemy_spawn_point"
    bl_label = "EnemySpawnPoint追加"
    bl_description = "選択中のオブジェクトにEnemySpawnPointを追加します"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.object is None:
            self.report({'WARNING'}, "オブジェクトが選択されていません")
            return {'CANCELLED'}

        context.object["enemy_spawn"] = True
        context.object["enemy_type"] = "NormalEnemy"
        context.object["enemy_spawn_id"] = "EnemySpawn"
        context.object["enemy_spawn_delay"] = 0.0

        return {'FINISHED'}


class MYADDON_OT_add_camera_point(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_add_camera_point"
    bl_label = "CameraPoint追加"
    bl_description = "選択中のオブジェクトにCameraPointを追加します"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.object is None:
            self.report({'WARNING'}, "オブジェクトが選択されていません")
            return {'CANCELLED'}

        context.object["camera_point"] = True
        context.object["camera_point_name"] = "CameraPoint"
        context.object["camera_target"] = mathutils.Vector((0.0, 0.0, 0.0))
        context.object["camera_move_time"] = 1.0

        return {'FINISHED'}


class MYADDON_OT_add_camera_fov_point(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_add_camera_fov_point"
    bl_label = "CameraFovPoint追加"
    bl_description = "選択中のオブジェクトにCameraFovPointを追加します"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.object is None:
            self.report({'WARNING'}, "オブジェクトが選択されていません")
            return {'CANCELLED'}

        context.object["camera_fov_point"] = True
        context.object["camera_fov"] = 45.0
        context.object["camera_fov_time"] = 1.0

        return {'FINISHED'}
