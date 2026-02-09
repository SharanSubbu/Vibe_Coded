bl_info = {
    "name": "Custom Cube Addon",
    "author": "Author Name",
    "version": (1, 0),
    "blender": (5, 0, 0),
    "location": "View3D > Sidebar > Cube Tools",
    "description": "Generates and merges cube arrays",
    "category": "Mesh",
}

import bpy
import math
from bpy.props import IntProperty
from mathutils import Vector

# --- Utility Functions ---

def cleanup_default_scene():
    """Removes the default cube to ensure a clean start."""
    if "Cube" in bpy.data.objects:
        obj = bpy.data.objects["Cube"]
        bpy.data.objects.remove(obj, do_unlink=True)

def get_cube_collection():
    """Creates a specific collection for managed objects."""
    col_name = "Cube_Objects"
    if col_name not in bpy.data.collections:
        new_col = bpy.data.collections.new(col_name)
        bpy.context.scene.collection.children.link(new_col)
        return new_col
    return bpy.data.collections[col_name]

# --- Operators ---

class MESH_OT_DistributeCubes(bpy.types.Operator):
    bl_idname = "mesh.distribute_cubes"
    bl_label = "Distribute Cubes"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        n = context.scene.cube_count_n
        if n > 20:
            self.report({'ERROR'}, "The number is out of range")
            return {'CANCELLED'}

        cleanup_default_scene()
        col = get_cube_collection()
        m = math.ceil(math.sqrt(n))
        
        count = 0
        for i in range(m):
            for j in range(m):
                if count >= n: break
                pos = Vector((i * 1.0, j * 1.0, 0))
                if not any((obj.location - pos).length < 0.1 for obj in bpy.data.objects):
                    bpy.ops.mesh.primitive_cube_add(size=1, location=pos)
                    obj = context.active_object
                    obj.name = "Managed_Cube"
                    for c in obj.users_collection:
                        c.objects.unlink(obj)
                    col.objects.link(obj)
                count += 1
        return {'FINISHED'}

class MESH_OT_DeleteCubes(bpy.types.Operator):
    bl_idname = "mesh.delete_cubes"
    bl_label = "Delete Cubes"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        selected = context.selected_objects
        if not selected: return {'CANCELLED'}
        for obj in selected:
            if obj.type != 'MESH':
                self.report({'ERROR'}, "Selected object is not a cube!")
                return {'CANCELLED'}
        bpy.ops.object.delete(use_global=False)
        return {'FINISHED'}

class MESH_OT_ComposeMesh(bpy.types.Operator):
    bl_idname = "mesh.compose_mesh"
    bl_label = "Compose Mesh"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        selected = [obj for obj in context.selected_objects if obj.type == 'MESH']
        if len(selected) < 2:
            self.report({'WARNING'}, "Select at least 2 cubes")
            return {'CANCELLED'}

        active = context.active_object
        others = [o for o in selected if o != active]
        if not any((active.location - o.location).length <= 1.01 for o in others):
            self.report({'ERROR'}, "Meshes must share at least 1 common face")
            return {'CANCELLED'}

        bpy.ops.object.join()
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.remove_doubles(threshold=0.001)
        bpy.ops.mesh.dissolve_limited(angle_limit=0.001)
        bpy.ops.object.mode_set(mode='OBJECT')
        return {'FINISHED'}

# --- UI Panel ---

class VIEW3D_PT_CustomCubeAddon(bpy.types.Panel):
    bl_label = "Custom Cube Addon"
    bl_idname = "VIEW3D_PT_custom_cube"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Cube Tools'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        row = layout.row(align=True)
        row.prop(scene, "cube_count_n", text="Number of Cubes")
        row.operator("mesh.distribute_cubes", text="Distribute")
        layout.separator()
        layout.operator("mesh.delete_cubes", text="Delete Selected Cubes", icon='TRASH')
        layout.operator("mesh.compose_mesh", text="Merge Shared Faces", icon='AUTOMERGE_ON')

# --- Registration ---

classes = (MESH_OT_DistributeCubes, MESH_OT_DeleteCubes, MESH_OT_ComposeMesh, VIEW3D_PT_CustomCubeAddon)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.cube_count_n = IntProperty(name="N", default=4, min=1, max=25) # Max 25 to test error

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.cube_count_n

if __name__ == "__main__":
    register()