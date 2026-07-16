import bpy
import bpy_extras
import math
import json
from .utils import VectorUtility


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

        disabled = False
        if "disabled" in object:
            disabled = bool(object["disabled"])

        obj_type = object.type
        if "type" in object:
            try:
                obj_type = str(object["type"])
            except Exception:
                pass

        object_data = {
            "name": object.name,
            "type": obj_type,
            "disabled": disabled,
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
