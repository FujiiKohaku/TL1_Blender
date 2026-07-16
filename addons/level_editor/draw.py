import bpy
from .utils import VectorUtility, DrawUtility


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
