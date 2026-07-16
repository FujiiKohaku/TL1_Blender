import bpy
import bpy_extras
import math
import mathutils
import gpu
import gpu_extras.batch
import copy
import json
import os
import subprocess


bl_info = {
    "name": "レベルエディタ",
    "author": "Taro Kamata",
    "version": (1, 1),
    "blender": (4, 4, 0),
    "location": "",
    "description": "レベルエディタ",
    "warning": "",
    "support": "TESTING",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Object"
}


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


class VectorUtility:
    @staticmethod
    def get_vector3(custom_property, default_value):
        if custom_property is None:
            return [default_value[0], default_value[1], default_value[2]]

        return [
            float(custom_property[0]),
            float(custom_property[1]),
            float(custom_property[2])
        ]

    @staticmethod
    def get_transform_data(object):
        trans, rot, scale = object.matrix_local.decompose()
        rot = rot.to_euler()

        return {
            "translation": [float(trans.x), float(trans.y), float(trans.z)],
            "rotation": [
                float(math.degrees(rot.x)),
                float(math.degrees(rot.y)),
                float(math.degrees(rot.z))
            ],
            "scale": [float(scale.x), float(scale.y), float(scale.z)]
        }


class DrawUtility:
    @staticmethod
    def add_box_lines(vertices, indices, object_matrix, center, size):
        offsets = [
            [-0.5, -0.5, -0.5],
            [+0.5, -0.5, -0.5],
            [-0.5, +0.5, -0.5],
            [+0.5, +0.5, -0.5],
            [-0.5, -0.5, +0.5],
            [+0.5, -0.5, +0.5],
            [-0.5, +0.5, +0.5],
            [+0.5, +0.5, +0.5],
        ]

        start = len(vertices["pos"])

        for offset in offsets:
            local_pos = mathutils.Vector((
                center[0] + offset[0] * size[0],
                center[1] + offset[1] * size[1],
                center[2] + offset[2] * size[2]
            ))

            world_pos = object_matrix @ local_pos

            vertices["pos"].append(world_pos)

        indices.append([start + 0, start + 1])
        indices.append([start + 2, start + 3])
        indices.append([start + 0, start + 2])
        indices.append([start + 1, start + 3])

        indices.append([start + 4, start + 5])
        indices.append([start + 6, start + 7])
        indices.append([start + 4, start + 6])
        indices.append([start + 5, start + 7])

        indices.append([start + 0, start + 4])
        indices.append([start + 1, start + 5])
        indices.append([start + 2, start + 6])
        indices.append([start + 3, start + 7])

    @staticmethod
    def draw_lines(vertices, indices, color):
        if len(vertices["pos"]) == 0:
            return

        shader = gpu.shader.from_builtin("UNIFORM_COLOR")
        batch = gpu_extras.batch.batch_for_shader(
            shader,
            "LINES",
            vertices,
            indices=indices
        )

        shader.bind()
        shader.uniform_float("color", color)
        batch.draw(shader)


class DrawCollider:
    handle = None

    @staticmethod
    def draw_collider():
        vertices = {"pos": []}
        indices = []

        for object in bpy.context.scene.objects:
            if "collider" not in object:
                continue

            if object["collider"] != "BOX":
                continue

            collider_center = VectorUtility.get_vector3(
                object.get("collider_center"),
                [0.0, 0.0, 0.0]
            )

            collider_size = VectorUtility.get_vector3(
                object.get("collider_size"),
                [2.0, 2.0, 2.0]
            )

            DrawUtility.add_box_lines(
                vertices,
                indices,
                object.matrix_world,
                collider_center,
                collider_size
            )

        DrawUtility.draw_lines(vertices, indices, [0.5, 1.0, 1.0, 1.0])


class DrawTrigger:
    handle = None

    @staticmethod
    def draw_trigger():
        vertices = {"pos": []}
        indices = []

        for object in bpy.context.scene.objects:
            if "trigger" not in object:
                continue

            if object["trigger"] != "BOX":
                continue

            trigger_center = VectorUtility.get_vector3(
                object.get("trigger_center"),
                [0.0, 0.0, 0.0]
            )

            trigger_size = VectorUtility.get_vector3(
                object.get("trigger_size"),
                [2.0, 2.0, 2.0]
            )

            DrawUtility.add_box_lines(
                vertices,
                indices,
                object.matrix_world,
                trigger_center,
                trigger_size
            )

        DrawUtility.draw_lines(vertices, indices, [1.0, 0.8, 0.2, 1.0])


class MYADDON_OT_export_scene(bpy.types.Operator, bpy_extras.io_utils.ExportHelper):
    bl_idname = "myaddon.myaddon_ot_export_scene"
    bl_label = "シーン出力"
    bl_description = "シーン情報をExportします"

    filename_ext = ".scene"

    def write_and_print(self, file, text):
        print(text)
        file.write(text)
        file.write("\n")

    def parse_scene_recursive(self, file, object, level):
        indent = ""
        for i in range(level):
            indent += "\t"

        self.write_and_print(file, indent + object.type + " - " + object.name)

        trans, rot, scale = object.matrix_local.decompose()
        rot = rot.to_euler()

        rot.x = math.degrees(rot.x)
        rot.y = math.degrees(rot.y)
        rot.z = math.degrees(rot.z)

        self.write_and_print(
            file,
            indent + "Trans(%f,%f,%f)" % (trans.x, trans.y, trans.z)
        )

        self.write_and_print(
            file,
            indent + "Rot(%f,%f,%f)" % (rot.x, rot.y, rot.z)
        )

        self.write_and_print(
            file,
            indent + "Scale(%f,%f,%f)" % (scale.x, scale.y, scale.z)
        )

        if "file_name" in object:
            self.write_and_print(
                file,
                indent + "N %s" % object["file_name"]
            )

        if "collider" in object:
            self.write_and_print(
                file,
                indent + "Collider %s" % object["collider"]
            )

            collider_center = VectorUtility.get_vector3(
                object.get("collider_center"),
                [0.0, 0.0, 0.0]
            )

            collider_size = VectorUtility.get_vector3(
                object.get("collider_size"),
                [2.0, 2.0, 2.0]
            )

            self.write_and_print(
                file,
                indent + "ColliderCenter(%f,%f,%f)" % (
                    collider_center[0],
                    collider_center[1],
                    collider_center[2]
                )
            )

            self.write_and_print(
                file,
                indent + "ColliderSize(%f,%f,%f)" % (
                    collider_size[0],
                    collider_size[1],
                    collider_size[2]
                )
            )

        if "trigger" in object:
            self.write_and_print(
                file,
                indent + "Trigger %s" % object["trigger"]
            )

            self.write_and_print(
                file,
                indent + "TriggerName %s" % object.get("trigger_name", "Trigger")
            )

            trigger_center = VectorUtility.get_vector3(
                object.get("trigger_center"),
                [0.0, 0.0, 0.0]
            )

            trigger_size = VectorUtility.get_vector3(
                object.get("trigger_size"),
                [2.0, 2.0, 2.0]
            )

            self.write_and_print(
                file,
                indent + "TriggerCenter(%f,%f,%f)" % (
                    trigger_center[0],
                    trigger_center[1],
                    trigger_center[2]
                )
            )

            self.write_and_print(
                file,
                indent + "TriggerSize(%f,%f,%f)" % (
                    trigger_size[0],
                    trigger_size[1],
                    trigger_size[2]
                )
            )

        if "enemy_spawn" in object:
            self.write_and_print(file, indent + "EnemySpawn true")
            self.write_and_print(
                file,
                indent + "EnemyType %s" % object.get("enemy_type", "NormalEnemy")
            )
            self.write_and_print(
                file,
                indent + "EnemySpawnId %s" % object.get("enemy_spawn_id", "EnemySpawn")
            )
            self.write_and_print(
                file,
                indent + "EnemySpawnDelay %f" % float(object.get("enemy_spawn_delay", 0.0))
            )

        if "camera_point" in object:
            self.write_and_print(file, indent + "CameraPoint true")
            self.write_and_print(
                file,
                indent + "CameraPointName %s" % object.get("camera_point_name", "CameraPoint")
            )

            camera_target = VectorUtility.get_vector3(
                object.get("camera_target"),
                [0.0, 0.0, 0.0]
            )

            self.write_and_print(
                file,
                indent + "CameraTarget(%f,%f,%f)" % (
                    camera_target[0],
                    camera_target[1],
                    camera_target[2]
                )
            )

            self.write_and_print(
                file,
                indent + "CameraMoveTime %f" % float(object.get("camera_move_time", 1.0))
            )

        if "camera_fov_point" in object:
            self.write_and_print(file, indent + "CameraFovPoint true")
            self.write_and_print(
                file,
                indent + "CameraFov %f" % float(object.get("camera_fov", 45.0))
            )
            self.write_and_print(
                file,
                indent + "CameraFovTime %f" % float(object.get("camera_fov_time", 1.0))
            )

        self.write_and_print(file, indent + "")

        for child in object.children:
            self.parse_scene_recursive(file, child, level + 1)

    def export(self):
        print("シーン情報出力開始... %r" % self.filepath)

        with open(self.filepath, "wt", encoding="utf-8") as file:
            self.write_and_print(file, "SCENE")

            for object in bpy.context.scene.objects:
                if object.parent:
                    continue

                self.parse_scene_recursive(file, object, 0)

    def execute(self, context):
        print("シーン情報をExportします")

        self.export()

        self.report({'INFO'}, "シーン情報をExportしました")
        print("シーン情報をExportしました")

        return {'FINISHED'}


class MYADDON_OT_export_scene_json(bpy.types.Operator, bpy_extras.io_utils.ExportHelper):
    bl_idname = "myaddon.myaddon_ot_export_scene_json"
    bl_label = "シーンJSON出力"
    bl_description = "シーン情報をJSONでExportします"

    filename_ext = ".json"

    def make_object_data(self, object):
        transform_data = VectorUtility.get_transform_data(object)

        object_data = {
            "name": object.name,
            "type": object.type,
            "transform": transform_data,
            "children": []
        }

        if "file_name" in object:
            object_data["file_name"] = object["file_name"]

        if "collider" in object:
            collider_center = VectorUtility.get_vector3(
                object.get("collider_center"),
                [0.0, 0.0, 0.0]
            )

            collider_size = VectorUtility.get_vector3(
                object.get("collider_size"),
                [2.0, 2.0, 2.0]
            )

            object_data["collider"] = {
                "type": object.get("collider", "BOX"),
                "center": collider_center,
                "size": collider_size,
                "rotation_mode": "object_rotation"
            }

        if "trigger" in object:
            trigger_center = VectorUtility.get_vector3(
                object.get("trigger_center"),
                [0.0, 0.0, 0.0]
            )

            trigger_size = VectorUtility.get_vector3(
                object.get("trigger_size"),
                [2.0, 2.0, 2.0]
            )

            object_data["trigger"] = {
                "type": object.get("trigger", "BOX"),
                "name": object.get("trigger_name", "Trigger"),
                "center": trigger_center,
                "size": trigger_size,
                "rotation_mode": "object_rotation"
            }

        if "enemy_spawn" in object:
            object_data["enemy_spawn"] = {
                "enable": bool(object.get("enemy_spawn", True)),
                "type": object.get("enemy_type", "NormalEnemy"),
                "id": object.get("enemy_spawn_id", "EnemySpawn"),
                "delay": float(object.get("enemy_spawn_delay", 0.0))
            }

        if "camera_point" in object:
            camera_target = VectorUtility.get_vector3(
                object.get("camera_target"),
                [0.0, 0.0, 0.0]
            )

            object_data["camera_point"] = {
                "enable": bool(object.get("camera_point", True)),
                "name": object.get("camera_point_name", "CameraPoint"),
                "target": camera_target,
                "move_time": float(object.get("camera_move_time", 1.0))
            }

        if "camera_fov_point" in object:
            object_data["camera_fov_point"] = {
                "enable": bool(object.get("camera_fov_point", True)),
                "fov": float(object.get("camera_fov", 45.0)),
                "time": float(object.get("camera_fov_time", 1.0))
            }

        for child in object.children:
            child_data = self.make_object_data(child)
            object_data["children"].append(child_data)

        return object_data

    def export(self):
        scene_data = {
            "scene": []
        }

        for object in bpy.context.scene.objects:
            if object.parent:
                continue

            object_data = self.make_object_data(object)
            scene_data["scene"].append(object_data)

        with open(self.filepath, "wt", encoding="utf-8") as file:
            json.dump(scene_data, file, ensure_ascii=False, indent=4)

    def execute(self, context):
        print("シーン情報をJSONでExportします")

        self.export()

        self.report({'INFO'}, "シーン情報をJSONでExportしました")
        print("シーン情報をJSONでExportしました")

        return {'FINISHED'}


class TOPBAR_MT_my_menu(bpy.types.Menu):
    bl_idname = "TOPBAR_MT_my_menu"
    bl_label = "MyMenu"
    bl_description = "拡張メニュー by " + bl_info["author"]

    def draw(self, context):
        self.layout.operator("wm.url_open_preset", text="Manual", icon='HELP')
        self.layout.operator("wm.url_open_preset", text="Tutorial", icon='URL')

        self.layout.separator()

        self.layout.operator("wm.save_as_mainfile", text="Save File", icon='FILE_TICK')
        self.layout.operator(
            MYADDON_OT_open_in_vscode.bl_idname,
            text=MYADDON_OT_open_in_vscode.bl_label,
            icon='CONSOLE'
        )

        self.layout.separator()

        self.layout.operator(
            MYADDON_OT_add_ico_sphere.bl_idname,
            text=MYADDON_OT_add_ico_sphere.bl_label,
            icon='MESH_ICOSPHERE'
        )

        self.layout.operator(
            MYADDON_OT_add_cube.bl_idname,
            text=MYADDON_OT_add_cube.bl_label,
            icon='CUBE'
        )

        self.layout.operator(
            MYADDON_OT_export_scene.bl_idname,
            text=MYADDON_OT_export_scene.bl_label,
            icon='EXPORT'
        )

        self.layout.operator(
            MYADDON_OT_export_scene_json.bl_idname,
            text=MYADDON_OT_export_scene_json.bl_label,
            icon='EXPORT'
        )

    @staticmethod
    def submenu(self, context):
        self.layout.menu(TOPBAR_MT_my_menu.bl_idname)


class OBJECT_PT_level_editor(bpy.types.Panel):
    bl_idname = "OBJECT_PT_level_editor"
    bl_label = "LevelEditor"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    def draw(self, context):
        layout = self.layout

        layout.label(text="Level Editor")

        layout.operator(
            MYADDON_OT_open_in_vscode.bl_idname,
            text=MYADDON_OT_open_in_vscode.bl_label,
            icon='CONSOLE'
        )

        layout.separator()

        layout.operator(
            MYADDON_OT_add_ico_sphere.bl_idname,
            text=MYADDON_OT_add_ico_sphere.bl_label,
            icon='MESH_ICOSPHERE'
        )

        layout.operator(
            MYADDON_OT_add_cube.bl_idname,
            text=MYADDON_OT_add_cube.bl_label,
            icon='CUBE'
        )

        layout.operator(
            MYADDON_OT_export_scene.bl_idname,
            text=MYADDON_OT_export_scene.bl_label,
            icon='EXPORT'
        )

        layout.operator(
            MYADDON_OT_export_scene_json.bl_idname,
            text=MYADDON_OT_export_scene_json.bl_label,
            icon='EXPORT'
        )

        layout.separator()

        if context.object is None:
            layout.label(text="オブジェクトが選択されていません")
            return

        if "file_name" in context.object:
            layout.prop(
                context.object,
                '["file_name"]',
                text="FileName"
            )
        else:
            layout.operator(
                MYADDON_OT_add_filename.bl_idname,
                text=MYADDON_OT_add_filename.bl_label
            )

        layout.separator()

        if "collider" in context.object:
            layout.label(text="Collider")

            layout.prop(
                context.object,
                '["collider"]',
                text="Type"
            )

            layout.prop(
                context.object,
                '["collider_center"]',
                text="Center"
            )

            layout.prop(
                context.object,
                '["collider_size"]',
                text="Size"
            )
        else:
            layout.operator(
                MYADDON_OT_add_collider.bl_idname,
                text=MYADDON_OT_add_collider.bl_label
            )

        layout.separator()

        if "trigger" in context.object:
            layout.label(text="TriggerBox")

            layout.prop(
                context.object,
                '["trigger"]',
                text="Type"
            )

            layout.prop(
                context.object,
                '["trigger_name"]',
                text="Name"
            )

            layout.prop(
                context.object,
                '["trigger_center"]',
                text="Center"
            )

            layout.prop(
                context.object,
                '["trigger_size"]',
                text="Size"
            )
        else:
            layout.operator(
                MYADDON_OT_add_trigger_box.bl_idname,
                text=MYADDON_OT_add_trigger_box.bl_label
            )

        layout.separator()

        if "enemy_spawn" in context.object:
            layout.label(text="EnemySpawnPoint")

            layout.prop(
                context.object,
                '["enemy_spawn"]',
                text="Enable"
            )

            layout.prop(
                context.object,
                '["enemy_type"]',
                text="EnemyType"
            )

            layout.prop(
                context.object,
                '["enemy_spawn_id"]',
                text="SpawnId"
            )

            layout.prop(
                context.object,
                '["enemy_spawn_delay"]',
                text="Delay"
            )
        else:
            layout.operator(
                MYADDON_OT_add_enemy_spawn_point.bl_idname,
                text=MYADDON_OT_add_enemy_spawn_point.bl_label
            )

        layout.separator()

        if "camera_point" in context.object:
            layout.label(text="CameraPoint")

            layout.prop(
                context.object,
                '["camera_point"]',
                text="Enable"
            )

            layout.prop(
                context.object,
                '["camera_point_name"]',
                text="Name"
            )

            layout.prop(
                context.object,
                '["camera_target"]',
                text="Target"
            )

            layout.prop(
                context.object,
                '["camera_move_time"]',
                text="MoveTime"
            )
        else:
            layout.operator(
                MYADDON_OT_add_camera_point.bl_idname,
                text=MYADDON_OT_add_camera_point.bl_label
            )

        layout.separator()

        if "camera_fov_point" in context.object:
            layout.label(text="CameraFovPoint")

            layout.prop(
                context.object,
                '["camera_fov_point"]',
                text="Enable"
            )

            layout.prop(
                context.object,
                '["camera_fov"]',
                text="Fov"
            )

            layout.prop(
                context.object,
                '["camera_fov_time"]',
                text="Time"
            )
        else:
            layout.operator(
                MYADDON_OT_add_camera_fov_point.bl_idname,
                text=MYADDON_OT_add_camera_fov_point.bl_label
            )


classes = (
    MYADDON_OT_open_in_vscode,
    MYADDON_OT_add_ico_sphere,
    MYADDON_OT_add_cube,
    MYADDON_OT_add_filename,
    MYADDON_OT_add_collider,
    MYADDON_OT_add_trigger_box,
    MYADDON_OT_add_enemy_spawn_point,
    MYADDON_OT_add_camera_point,
    MYADDON_OT_add_camera_fov_point,
    MYADDON_OT_export_scene,
    MYADDON_OT_export_scene_json,
    TOPBAR_MT_my_menu,
    OBJECT_PT_level_editor,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.TOPBAR_MT_editor_menus.append(TOPBAR_MT_my_menu.submenu)

    DrawCollider.handle = bpy.types.SpaceView3D.draw_handler_add(
        DrawCollider.draw_collider,
        (),
        "WINDOW",
        "POST_VIEW"
    )

    DrawTrigger.handle = bpy.types.SpaceView3D.draw_handler_add(
        DrawTrigger.draw_trigger,
        (),
        "WINDOW",
        "POST_VIEW"
    )

    print("レベルエディタが有効化されました。")


def unregister():
    bpy.types.TOPBAR_MT_editor_menus.remove(TOPBAR_MT_my_menu.submenu)

    if DrawCollider.handle is not None:
        bpy.types.SpaceView3D.draw_handler_remove(
            DrawCollider.handle,
            "WINDOW"
        )

        DrawCollider.handle = None

    if DrawTrigger.handle is not None:
        bpy.types.SpaceView3D.draw_handler_remove(
            DrawTrigger.handle,
            "WINDOW"
        )

        DrawTrigger.handle = None

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    print("レベルエディタが無効化されました。")


if __name__ == "__main__":
    register()
