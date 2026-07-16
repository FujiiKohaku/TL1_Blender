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


def get_or_create_grass_mesh():
    mesh_name = "GrassPreviewMesh"
    mesh = bpy.data.meshes.get(mesh_name)
    if mesh is not None:
        return mesh

    # 十字に交差した2枚の細長い板（ゲーム用草モデルの定番）
    verts = [
        (-0.2, 0.0, 0.0), (0.2, 0.0, 0.0), (-0.2, 0.0, 1.2), (0.2, 0.0, 1.2),
        (0.0, -0.2, 0.0), (0.0, 0.2, 0.0), (0.0, -0.2, 1.2), (0.0, 0.2, 1.2)
    ]
    faces = [
        (0, 1, 3, 2),
        (4, 5, 7, 6)
    ]

    mesh = bpy.data.meshes.new(mesh_name)
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    return mesh


class MYADDON_OT_generate_grass_preview(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_generate_grass_preview"
    bl_label = "草のプレビューを表示"
    bl_description = "塗られたウェイト位置に十字クロスの簡易草オブジェクトを生成して配置します"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.active_object
        if obj is None or obj.type != 'MESH':
            self.report({'WARNING'}, "地形オブジェクトが選択されていません")
            return {'CANCELLED'}

        vg = obj.vertex_groups.get("GrassGroup")
        if vg is None:
            self.report({'WARNING'}, "草のペイントデータ（GrassGroup）が見つかりません。まずペイントしてください。")
            return {'CANCELLED'}

        original_mode = obj.mode
        if original_mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')

        col_name = "GrassPreview"
        preview_col = context.scene.collection.children.get(col_name)
        
        if preview_col is not None:
            for p_obj in list(preview_col.objects):
                bpy.data.objects.remove(p_obj, do_unlink=True)
        else:
            preview_col = bpy.data.collections.new(col_name)
            context.scene.collection.children.link(preview_col)

        mat_name = "GrassPreviewMaterial"
        mat = bpy.data.materials.get(mat_name)
        if mat is None:
            mat = bpy.data.materials.new(name=mat_name)
            mat.use_nodes = True
            bsdf = mat.node_tree.nodes.get("Principled BSDF")
            if bsdf is not None:
                bsdf.inputs['Base Color'].default_value = (0.1, 0.8, 0.1, 1.0)

        # 草メッシュを取得
        grass_mesh = get_or_create_grass_mesh()

        matrix_world = obj.matrix_world
        mesh = obj.data
        step = 3
        import random
        random.seed(42)
        
        created_count = 0
        for i in range(0, len(mesh.vertices), step):
            v = mesh.vertices[i]
            
            in_group = False
            weight = 0.0
            for g in v.groups:
                if g.group == vg.index:
                    in_group = True
                    weight = g.weight
            
            if in_group:
                if weight >= 0.1:
                    if random.random() < weight:
                        world_pos = matrix_world @ v.co
                        
                        # 十字草オブジェクトを作成
                        grass_obj = bpy.data.objects.new("GrassCone", grass_mesh)
                        grass_obj.location = world_pos
                        
                        # ランダムにZ軸（上向き軸）まわりを回転させてばらつきを表現
                        grass_obj.rotation_euler.z = random.uniform(0.0, 6.28)
                        
                        # ランダムにスケール（高さ）をばらつかせる
                        scale_factor = random.uniform(0.8, 1.3)
                        grass_obj.scale = (scale_factor, scale_factor, scale_factor)
                        
                        # マテリアル適用
                        grass_obj.data.materials.append(mat)
                        
                        # 簡易変形モディファイア（曲げ）を追加して風揺れを表現
                        try:
                            mod = grass_obj.modifiers.new(name="WindSway", type='SIMPLE_DEFORM')
                            mod.deform_method = 'BEND'
                            mod.deform_axis = 'X'
                            
                            # 角度（angle）にサイン波ドライバを追加
                            driver_fcurve = mod.driver_add("angle")
                            driver = driver_fcurve.driver
                            driver.type = 'SCRIPTED'
                            
                            # 各々の草にランダムな揺れの速さ、揺れのズレ（位相）、揺れの強さを適用
                            speed = random.uniform(0.05, 0.08)
                            offset = random.uniform(0.0, 6.28)
                            amplitude = random.uniform(0.1, 0.18)
                            
                            driver.expression = f"sin(frame * {speed:.4f} + {offset:.4f}) * {amplitude:.4f}"
                        except Exception as e:
                            pass

                        # コレクションに追加（マスターコレクションへは自動追加されないためunlink不要）
                        preview_col.objects.link(grass_obj)
                        created_count += 1

        context.view_layer.objects.active = obj
        if original_mode != 'OBJECT':
            bpy.ops.object.mode_set(mode=original_mode)

        self.report({'INFO'}, f"草プレビューを {created_count} 本生成しました")
        return {'FINISHED'}


class MYADDON_OT_clear_grass_preview(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_clear_grass_preview"
    bl_label = "プレビュー消去"
    bl_description = "草のプレビューオブジェクトとコレクションを一括削除します"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        col_name = "GrassPreview"
        preview_col = context.scene.collection.children.get(col_name)
        
        if preview_col is None:
            self.report({'INFO'}, "消去するプレビューが見つかりません")
            return {'FINISHED'}

        original_obj = context.active_object
        original_mode = None
        if original_obj is not None:
            original_mode = original_obj.mode
            if original_mode != 'OBJECT':
                bpy.ops.object.mode_set(mode='OBJECT')

        for p_obj in list(preview_col.objects):
            bpy.data.objects.remove(p_obj, do_unlink=True)

        bpy.data.collections.remove(preview_col)

        if original_obj is not None and original_mode is not None:
            context.view_layer.objects.active = original_obj
            if original_mode != 'OBJECT':
                bpy.ops.object.mode_set(mode=original_mode)

        self.report({'INFO'}, "草プレビューを消去しました")
        return {'FINISHED'}
