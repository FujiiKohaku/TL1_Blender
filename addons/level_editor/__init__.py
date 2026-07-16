import sys
import importlib

# サブモジュールの強制リロード（Blenderの登録キャッシュを破壊する）
prefix = __package__ + "."
for mod_name in list(sys.modules.keys()):
    if mod_name.startswith(prefix):
        try:
            importlib.reload(sys.modules[mod_name])
        except Exception as e:
            print(f"Failed to reload sub-module {mod_name}: {str(e)}")

import bpy
from . import op_system
from . import utils
from . import draw
from . import op_add
from . import op_export
from . import ui
from . import disabled
from . import spawn

from .op_system import MYADDON_OT_open_in_vscode
from .utils import VectorUtility, DrawUtility
from .draw import DrawCollider, DrawTrigger
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
from .op_export import MYADDON_OT_export_scene, MYADDON_OT_export_scene_json
from .ui import TOPBAR_MT_my_level_menu, OBJECT_PT_level_editor
from .disabled import MYADDON_OT_add_disabled, OBJECT_PT_disabled
from .spawn import (
    MYADDON_OT_spawn_import_symbol,
    MYADDON_OT_spawn_create_symbol,
    MYADDON_OT_spawn_create_player,
    MYADDON_OT_spawn_create_enemy,
)



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


classes = (
    MYADDON_OT_open_in_vscode,
    MYADDON_OT_add_disabled,
    MYADDON_OT_spawn_import_symbol,
    MYADDON_OT_spawn_create_symbol,
    MYADDON_OT_spawn_create_player,
    MYADDON_OT_spawn_create_enemy,
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
    MYADDON_OT_export_scene,
    MYADDON_OT_export_scene_json,
    TOPBAR_MT_my_level_menu,
    OBJECT_PT_level_editor,
    OBJECT_PT_disabled,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.TOPBAR_MT_editor_menus.append(TOPBAR_MT_my_level_menu.submenu)

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
    bpy.types.TOPBAR_MT_editor_menus.remove(TOPBAR_MT_my_level_menu.submenu)

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
