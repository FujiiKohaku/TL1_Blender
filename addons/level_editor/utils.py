import math
import mathutils
import gpu
import gpu_extras.batch


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
