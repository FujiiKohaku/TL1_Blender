import bpy
from .op_system import MYADDON_OT_open_in_vscode
from .op_add import (
    MYADDON_OT_add_ico_sphere,
    MYADDON_OT_add_cube,
    MYADDON_OT_add_filename,
    MYADDON_OT_add_collider,
    MYADDON_OT_add_trigger_box,
    MYADDON_OT_add_enemy_spawn_point,
    MYADDON_OT_add_camera_point,
    MYADDON_OT_add_camera_fov_point,
    MYADDON_OT_add_gimmick,
    MYADDON_OT_add_patrol_route,
    MYADDON_OT_add_patrol_waypoint,
    MYADDON_OT_add_terrain,
    MYADDON_OT_add_mesh_sync,
    MYADDON_OT_create_terrain_mesh,
    MYADDON_OT_add_uv_sphere,
    MYADDON_OT_start_grass_paint,
    MYADDON_OT_generate_grass_preview,
    MYADDON_OT_clear_grass_preview,
    MYADDON_OT_create_animated_character,
    MYADDON_OT_control_character,
    MYADDON_OT_create_robot_character,
)
from .op_export import (
    MYADDON_OT_export_scene,
    MYADDON_OT_export_scene_json,
)
from .spawn import MYADDON_OT_spawn_create_player, MYADDON_OT_spawn_create_enemy


class TOPBAR_MT_my_level_menu(bpy.types.Menu):
    bl_idname = "TOPBAR_MT_my_level_menu"
    bl_label = "MyMenu"
    bl_description = "拡張メニュー by Taro Kamata"

    def draw(self, context):
        import traceback
        import os
        log_path = r"C:\Projects\TL1\addons\level_editor\menu_error.txt"
        
        try:
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
                MYADDON_OT_add_uv_sphere.bl_idname,
                text=MYADDON_OT_add_uv_sphere.bl_label,
                icon='SPHERE'
            )

            self.layout.operator(
                MYADDON_OT_add_cube.bl_idname,
                text=MYADDON_OT_add_cube.bl_label,
                icon='CUBE'
            )

            self.layout.operator(
                MYADDON_OT_spawn_create_player.bl_idname,
                text="プレイヤー出現ポイントの作成",
                icon='OUTLINER_OB_EMPTY'
            )

            self.layout.operator(
                MYADDON_OT_spawn_create_enemy.bl_idname,
                text="敵出現ポイントの作成",
                icon='OUTLINER_OB_EMPTY'
            )

            self.layout.operator(
                MYADDON_OT_create_animated_character.bl_idname,
                text="走るキャラクターの追加",
                icon='USER'
            )

            self.layout.operator(
                MYADDON_OT_create_robot_character.bl_idname,
                text="走るメカロボットの追加",
                icon='GHOST_ENABLED'
            )

            self.layout.operator(
                MYADDON_OT_control_character.bl_idname,
                text="キャラクターをキーボードで動かす",
                icon='GAMEPAD'
            )

            self.layout.operator(
                MYADDON_OT_create_terrain_mesh.bl_idname,
                text="地形（Terrain）オブジェクトの作成",
                icon='GRID'
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

            if os.path.exists(log_path):
                try:
                    os.remove(log_path)
                except Exception:
                    pass
        except Exception as e:
            try:
                with open(log_path, "w", encoding="utf-8") as f:
                    f.write("GEMINI MENU DRAW ERROR DETECTED:\n")
                    traceback.print_exc(file=f)
            except Exception:
                pass

    @staticmethod
    def submenu(self, context):
        self.layout.menu(TOPBAR_MT_my_level_menu.bl_idname)


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
            layout.operator(
                MYADDON_OT_add_camera_fov_point.bl_idname,
                text=MYADDON_OT_add_camera_fov_point.bl_label
            )

        layout.separator()

        if "gimmick" in context.object:
            layout.label(text="Gimmick")
            layout.prop(context.object, '["gimmick"]', text="Type")
            layout.prop(context.object, '["gimmick_speed"]', text="Speed")
            layout.prop(context.object, '["gimmick_range"]', text="Range")
        else:
            layout.operator(MYADDON_OT_add_gimmick.bl_idname, text=MYADDON_OT_add_gimmick.bl_label)

        layout.separator()

        if "patrol_route" in context.object:
            layout.label(text="PatrolRoute")
            layout.operator(MYADDON_OT_add_patrol_waypoint.bl_idname, text="巡回ポイントの追加")
            waypoint_count = 0
            for child in context.object.children:
                if "waypoint" in child or child.name.startswith("Waypoint"):
                    waypoint_count += 1
            layout.label(text=f"ウェイポイント数: {waypoint_count}")
        else:
            layout.operator(MYADDON_OT_add_patrol_route.bl_idname, text=MYADDON_OT_add_patrol_route.bl_label)

        layout.separator()

        if "terrain" in context.object:
            layout.label(text="Terrain")
            layout.prop(context.object, '["terrain_file"]', text="Heightmap File")
            layout.prop(context.object, '["terrain_width"]', text="Width")
            layout.prop(context.object, '["terrain_height"]', text="Height")
            layout.separator()
            layout.operator(
                MYADDON_OT_start_grass_paint.bl_idname,
                text="草をマウスで植える (ペイント開始)",
                icon='BRUSH_DATA'
            )
            
            row = layout.row(align=True)
            row.operator(
                MYADDON_OT_generate_grass_preview.bl_idname,
                text="草のプレビューを表示",
                icon='OUTLINER_OB_MESH'
            )
            row.operator(
                MYADDON_OT_clear_grass_preview.bl_idname,
                text="消去",
                icon='TRASH'
            )
        else:
            layout.operator(MYADDON_OT_add_terrain.bl_idname, text=MYADDON_OT_add_terrain.bl_label)

        layout.separator()

        if "mesh_sync" in context.object:
            layout.label(text="MeshSync: 有効")
        else:
            layout.operator(MYADDON_OT_add_mesh_sync.bl_idname, text=MYADDON_OT_add_mesh_sync.bl_label)
