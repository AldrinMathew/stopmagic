import bpy
from ..functions.update_stopmagic import *


class PurgeUnusedData(bpy.types.Operator):
    """Deletes all unushed Mesh data created by the addon"""

    bl_idname = "object.purge_unused_data"
    bl_label = "Purge Unused Data"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        used_sm_mesh = {}

        for item in bpy.data.objects:
            ob: bpy.types.Object = item
            if ob.get("sm_id") is None:
                continue

            sm_id = ob.get("sm_id")
            used_sm_mesh[sm_id] = []

            fcurves = ob.animation_data.action.fcurves
            for item in fcurves:
                fcurve: bpy.types.FCurve = item
                if fcurve.data_path != '["sm_datablock"]':
                    continue
                #
                keyframe_points = fcurve.keyframe_points
                for item in keyframe_points:
                    keyframe: bpy.types.Keyframe = item
                    used_sm_mesh[sm_id].append(keyframe.co.y)

        delete_mesh = []

        for mesh in bpy.data.meshes:
            if mesh.get("sm_id") is None:
                continue

            mesh_sm_id = mesh.get("sm_id")

            if mesh_sm_id not in used_sm_mesh:
                delete_mesh.append(mesh)
                continue

            mesh_sm_datablock = mesh.get("sm_datablock")

            if mesh_sm_datablock not in used_sm_mesh[mesh_sm_id]:
                delete_mesh.append(mesh)
                continue

        if len(delete_mesh) == 0:
            self.report({'INFO'}, 'No meshes were removed by Stopmagic')
        else:
            self.report({'INFO'}, str(len(delete_mesh)) + ' meshes were removed by Stopmagic')
        for mesh in delete_mesh:
            mesh.use_fake_user = False

        update_stopmagic(bpy.context.scene)

        for mesh in delete_mesh:
            if mesh.users == 0:
                bpy.data.meshes.remove(mesh)

        return {"FINISHED"}


def register():
    bpy.utils.register_class(PurgeUnusedData)


def unregister():
    bpy.utils.unregister_class(PurgeUnusedData)
