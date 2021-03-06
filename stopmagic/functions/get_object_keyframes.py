from typing import List
import bpy


def get_object_keyframes(obj: bpy.types.Object) -> List[int]:
    """Get all keyframes that has mesh keyframes, associated with the active object"""
    keyframes: List[int] = []
    if obj is None:
        obj = bpy.context.view_layer.objects.active
    if obj.get("sm_id") is not None:
        for action in bpy.data.actions:
            if obj.user_of_id(action.id_data):
                fcurves = action.fcurves
                if fcurves is not None:
                    for item in fcurves:
                        fcurve: bpy.types.FCurve = item
                        if fcurve.data_path != '["sm_datablock"]':
                            continue
                        #
                        keyframe_points = fcurve.keyframe_points
                        for item in keyframe_points:
                            i = 0
                            while i < len(item.co):
                                keyframes.append(int(item.co[i]))
                                i += 2
                        return keyframes
    return keyframes
