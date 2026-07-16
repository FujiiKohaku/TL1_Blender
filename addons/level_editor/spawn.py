import os
import bpy

# シンボル種別ごとのデータテーブル
SPAWN_TABLE = {
    "Player": {
        "prototype": "PrototypePlayerSpawn",
        "instance": "PlayerSpawn",
        "path": os.path.join("player", "player.obj")
    },
    "Enemy": {
        "prototype": "PrototypeEnemySpawn",
        "instance": "EnemySpawn",
        "path": os.path.join("enemy", "enemy.obj")
    }
}


class MYADDON_OT_spawn_import_symbol(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_spawn_import_symbol"
    bl_label = "シンボルモデル読み込み"
    bl_description = "出現地点モデルをデータベースへ読み込みます"
    bl_options = {'REGISTER', 'UNDO'}

    def load_obj(self, spawn_type):
        if spawn_type not in SPAWN_TABLE:
            self.report({'ERROR'}, f"無効なシンボル種別です: {spawn_type}")
            return {'CANCELLED'}

        data = SPAWN_TABLE[spawn_type]
        prototype_name = data["prototype"]
        relative_path = data["path"]

        # 既にデータベース上に複製元が存在すれば何もしない（正常終了）
        spawn_object = bpy.data.objects.get(prototype_name)
        if spawn_object is not None:
            return {'FINISHED'}

        addon_directory = os.path.dirname(__file__)
        full_path = os.path.join(addon_directory, relative_path)

        if not os.path.exists(full_path):
            self.report({'ERROR'}, f"モデルファイルが見つかりません ({spawn_type}): {full_path}")
            return {'CANCELLED'}

        old_objects = set(bpy.context.scene.objects)

        try:
            bpy.ops.wm.obj_import(
                "EXEC_DEFAULT",
                filepath=full_path,
                forward_axis="Z",
                up_axis="Y"
            )
        except Exception as e:
            self.report({'ERROR'}, f"インポートに失敗しました ({spawn_type}): {str(e)}")
            return {'CANCELLED'}

        new_objects = []
        for obj in bpy.context.scene.objects:
            if obj not in old_objects:
                new_objects.append(obj)

        if len(new_objects) == 0:
            self.report({'WARNING'}, f"オブジェクトがインポートされませんでした: {spawn_type}")
            return {'CANCELLED'}

        # 既存の選択状態を解除し、インポートしたオブジェクトのみを選択
        bpy.ops.object.select_all(action='DESELECT')
        for obj in new_objects:
            obj.select_set(True)

        # 代表オブジェクトをアクティブにする
        bpy.context.view_layer.objects.active = new_objects[0]

        # 回転を適用
        try:
            bpy.ops.object.transform_apply(
                location=False,
                rotation=True,
                scale=False,
                properties=False,
                isolate_users=False
            )
        except Exception as e:
            self.report({'WARNING'}, f"回転の適用に失敗しました ({spawn_type}): {str(e)}")

        # 名前とカスタムプロパティを設定
        root_obj = bpy.context.view_layer.objects.active
        if root_obj is not None:
            root_obj.name = prototype_name
            root_obj["type"] = prototype_name

        # シーン（コレクション）からアンリンクして非表示にする
        for obj in new_objects:
            for col in obj.users_collection:
                col.objects.unlink(obj)

        return {'FINISHED'}

    def execute(self, context):
        # データテーブルのすべての種別を順次読み込む
        for spawn_type in SPAWN_TABLE.keys():
            result = self.load_obj(spawn_type)
            if 'CANCELLED' in result:
                return {'CANCELLED'}

        self.report({'INFO'}, "すべての複製元モデルを読み込みました")
        return {'FINISHED'}


class MYADDON_OT_spawn_create_symbol(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_spawn_create_symbol"
    bl_label = "出現ポイントシンボルの作成"
    bl_description = "指定した出現地点シンボルをシーンに配置します"
    bl_options = {'REGISTER', 'UNDO'}

    spawn_type: bpy.props.StringProperty(
        name="Type",
        default="Player"
    )

    def execute(self, context):
        if self.spawn_type not in SPAWN_TABLE:
            self.report({'ERROR'}, f"指定された種別はデータテーブルに存在しません: {self.spawn_type}")
            return {'CANCELLED'}

        data = SPAWN_TABLE[self.spawn_type]
        prototype_name = data["prototype"]
        instance_name = data["instance"]

        # データベースから複製元オブジェクトを検索
        spawn_object = bpy.data.objects.get(prototype_name)

        # 未読み込みの場合は、読み込みオペレーターを実行
        if spawn_object is None:
            try:
                # 読み込みオペレーターを呼び出すと、すべてのモデルがロードされます
                bpy.ops.myaddon.myaddon_ot_spawn_import_symbol("EXEC_DEFAULT")
            except Exception as e:
                self.report({'ERROR'}, f"複製元モデルのロード呼び出しに失敗しました: {str(e)}")
                return {'CANCELLED'}

            spawn_object = bpy.data.objects.get(prototype_name)
            if spawn_object is None:
                self.report({'ERROR'}, f"複製元モデルが見つかりません: {prototype_name}")
                return {'CANCELLED'}

        # 選択オブジェクトをすべて解除
        bpy.ops.object.select_all(action='DESELECT')

        # 複製元オブジェクトとその子供を再帰的にコピーしてリンクするヘルパー関数
        def copy_object_recursive(src_obj, parent_copy=None):
            obj_copy = src_obj.copy()
            
            if parent_copy is not None:
                obj_copy.parent = parent_copy
            
            # 現在のコレクションにリンク
            context.collection.objects.link(obj_copy)
            
            # 子オブジェクトも再帰的にコピー
            for child in src_obj.children:
                copy_object_recursive(child, obj_copy)
                
            return obj_copy

        # 複製を実行
        new_root = copy_object_recursive(spawn_object)

        # 名前とカスタムプロパティを上書き
        new_root.name = instance_name
        new_root["type"] = instance_name # "PlayerSpawn" または "EnemySpawn"
        
        # 3Dカーソル位置へ配置
        new_root.location = context.scene.cursor.location

        # 複製したオブジェクトを選択してアクティブにする
        new_root.select_set(True)
        context.view_layer.objects.active = new_root

        self.report({'INFO'}, f"{self.spawn_type}出現地点シンボルを配置しました")
        return {'FINISHED'}


class MYADDON_OT_spawn_create_player(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_spawn_create_player"
    bl_label = "プレイヤー出現ポイントの作成"
    bl_description = "プレイヤーの出現地点シンボルをシーンに配置します"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        try:
            result = bpy.ops.myaddon.myaddon_ot_spawn_create_symbol(
                "EXEC_DEFAULT",
                spawn_type="Player"
            )
            if 'CANCELLED' in result:
                return {'CANCELLED'}
        except Exception as e:
            self.report({'ERROR'}, f"プレイヤー配置に失敗しました: {str(e)}")
            return {'CANCELLED'}

        return {'FINISHED'}


class MYADDON_OT_spawn_create_enemy(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_spawn_create_enemy"
    bl_label = "敵出現ポイントの作成"
    bl_description = "敵の出現地点シンボルをシーンに配置します"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        try:
            result = bpy.ops.myaddon.myaddon_ot_spawn_create_symbol(
                "EXEC_DEFAULT",
                spawn_type="Enemy"
            )
            if 'CANCELLED' in result:
                return {'CANCELLED'}
        except Exception as e:
            self.report({'ERROR'}, f"敵配置に失敗しました: {str(e)}")
            return {'CANCELLED'}

        return {'FINISHED'}
