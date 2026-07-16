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


class MYADDON_OT_add_gimmick(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_add_gimmick"
    bl_label = "Gimmick追加"
    bl_description = "選択中のオブジェクトにGimmickを追加します"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.object is None:
            self.report({'WARNING'}, "オブジェクトが選択されていません")
            return {'CANCELLED'}

        context.object["gimmick"] = "ROTATION"
        context.object["gimmick_speed"] = 1.0
        context.object["gimmick_range"] = mathutils.Vector((0.0, 0.0, 0.0))

        return {'FINISHED'}


class MYADDON_OT_add_patrol_route(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_add_patrol_route"
    bl_label = "PatrolRoute追加"
    bl_description = "選択中のオブジェクトに巡回ルートを追加します"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.object is None:
            self.report({'WARNING'}, "オブジェクトが選択されていません")
            return {'CANCELLED'}

        context.object["patrol_route"] = True

        return {'FINISHED'}


class MYADDON_OT_add_patrol_waypoint(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_add_patrol_waypoint"
    bl_label = "巡回ポイントの作成"
    bl_description = "選択中のオブジェクトの子として巡回用のEmptyを追加します"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        parent_obj = context.object
        if parent_obj is None:
            self.report({'WARNING'}, "親となるオブジェクトが選択されていません")
            return {'CANCELLED'}

        # 新しいEmptyオブジェクトを作成
        waypoint = bpy.data.objects.new("Waypoint", None)
        context.collection.objects.link(waypoint)
        waypoint.parent = parent_obj
        
        # 3Dカーソル位置に配置
        waypoint.location = context.scene.cursor.location
        waypoint["waypoint"] = True

        # 作成したEmptyを選択・アクティブにする
        bpy.ops.object.select_all(action='DESELECT')
        waypoint.select_set(True)
        context.view_layer.objects.active = waypoint

        return {'FINISHED'}


class MYADDON_OT_add_terrain(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_add_terrain"
    bl_label = "Terrain追加"
    bl_description = "選択中のオブジェクトにTerrainを追加します"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.object is None:
            self.report({'WARNING'}, "オブジェクトが選択されていません")
            return {'CANCELLED'}

        context.object["terrain"] = True
        context.object["terrain_file"] = "heightmap.png"
        context.object["terrain_width"] = 100.0
        context.object["terrain_height"] = 10.0

        return {'FINISHED'}


class MYADDON_OT_add_mesh_sync(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_add_mesh_sync"
    bl_label = "MeshSync追加"
    bl_description = "選択中のオブジェクトにMeshSyncを追加します"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.object is None:
            self.report({'WARNING'}, "オブジェクトが選択されていません")
            return {'CANCELLED'}

        context.object["mesh_sync"] = True

        return {'FINISHED'}


class MYADDON_OT_create_terrain_mesh(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_create_terrain_mesh"
    bl_label = "地形（Terrain）オブジェクトの作成"
    bl_description = "スカルプト可能な細分化グリッドを作成し、Terrainプロパティを設定します"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        cursor_loc = context.scene.cursor.location

        try:
            bpy.ops.mesh.primitive_grid_add(
                x_subdivisions=100,
                y_subdivisions=100,
                size=100.0,
                location=cursor_loc
            )
        except Exception as e:
            self.report({'ERROR'}, f"グリッド生成に失敗しました: {str(e)}")
            return {'CANCELLED'}

        grid_obj = context.view_layer.objects.active
        if grid_obj is None:
            self.report({'ERROR'}, "生成されたオブジェクトのアクティブ化に失敗しました")
            return {'CANCELLED'}

        grid_obj.name = "Terrain"

        grid_obj["terrain"] = True
        grid_obj["terrain_file"] = "Terrain_Stage.obj"
        grid_obj["terrain_width"] = 100.0
        grid_obj["terrain_height"] = 10.0

        try:
            grid_obj.vertex_groups.new(name="GrassGroup")
        except Exception as e:
            self.report({'WARNING'}, f"頂点グループの作成に失敗しました: {str(e)}")

        try:
            bpy.ops.object.mode_set(mode='SCULPT')
            self.report({'INFO'}, "Terrainオブジェクトを作成しました。スカルプトモードを開始します。")
        except Exception as e:
            self.report({'WARNING'}, f"スカルプトモードへの切り替えに失敗しました: {str(e)}")

        return {'FINISHED'}


class MYADDON_OT_add_uv_sphere(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_add_uv_sphere"
    bl_label = "UV球追加"
    bl_description = "UV球（Sphere）を追加します"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        try:
            bpy.ops.mesh.primitive_uv_sphere_add()
            self.report({'INFO'}, "UV球を追加しました。")
        except Exception as e:
            self.report({'ERROR'}, f"UV球の追加に失敗しました: {str(e)}")
            return {'CANCELLED'}
        return {'FINISHED'}


class MYADDON_OT_start_grass_paint(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_start_grass_paint"
    bl_label = "草をマウスで植える（ペイント開始）"
    bl_description = "ウェイトペイントモードを開始し、草を植えたい場所をマウスで塗ります"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.active_object
        if obj is None or obj.type != 'MESH':
            self.report({'WARNING'}, "メッシュオブジェクトが選択されていません")
            return {'CANCELLED'}

        group_name = "GrassGroup"
        vg = obj.vertex_groups.get(group_name)
        if vg is None:
            vg = obj.vertex_groups.new(name=group_name)

        obj.vertex_groups.active = vg

        try:
            bpy.ops.object.mode_set(mode='WEIGHT_PAINT')
            self.report({'INFO'}, "草ペイントを開始します。マウスで草を生やす場所を塗ってください（赤＝草が密になる）")
        except Exception as e:
            self.report({'ERROR'}, f"ウェイトペイントモードへの切り替えに失敗しました: {str(e)}")
            return {'CANCELLED'}

        return {'FINISHED'}
