bl_info = {
    "name": "Add New Bendy Bone",
    "author": "Nico Zevallos",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Add > Armature > New BendyBone",
    "description": "Adds a new Bendy Bone object with handles",
    "warning": "",
    "wiki_url": "",
    "category": "Add Armature",
}


import bpy
from bpy.types import Operator
from bpy.props import FloatProperty, EnumProperty
from bpy_extras.object_utils import object_data_add, AddObjectHelper

def add_transform_driver(bone, armature_obj, variable, bone_target, type):
    driver = bone.driver_add(variable).driver
    driver.type = 'AVERAGE'
    var = driver.variables.new()
    var.type = 'TRANSFORMS'
    var.targets[0].id = armature_obj
    var.targets[0].bone_target = bone_target
    var.targets[0].transform_type = type
    var.targets[0].transform_space = 'LOCAL_SPACE'

def create_bbone(self, context, n_segments = 10, handle_length = 0.25):
    #Create armature and armature object
    armature = bpy.data.armatures.new('Armature')
    #Link armature object to our scene
    armature_obj = object_data_add(context, armature, operator=self)

    # must be in edit mode to add bones
    bpy.context.view_layer.objects.active = armature_obj
    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
    edit_bones = armature_obj.data.edit_bones

    # a new bone will have zero length and not be kept
    # move the head/tail to keep the bone
    head = edit_bones.new('head')
    head.head = (0, 0, 0)
    head.tail = (0, 0, handle_length)

    bone = edit_bones.new('bone')
    bone.head = (0, 0, 0)
    bone.tail = (0, 0, self.length)

    tail = edit_bones.new('tail')
    tail.head = (0, 0, self.length)
    tail.tail = (0, 0, self.length + handle_length)       
    tail.use_deform = False
    head.use_deform = False
    
    armature.display_type = 'BBONE'

    bone.bbone_segments = n_segments
    bone.bbone_custom_handle_end = tail
    bone.bbone_custom_handle_start = head
    bone.bbone_custom_handle_start = head
    bone.bbone_easein = 1.0
    bone.bbone_easeout = 1.0
    bone.bbone_handle_type_start = 'TANGENT'
    bone.bbone_handle_type_end = 'ABSOLUTE'
    bone.parent = head
    bone.use_inherit_scale=False

    # exit edit mode to save bones so they can be used in pose mode
    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
    
    bpy.ops.object.mode_set(mode='POSE', toggle=False)
    bone_pose = bpy.context.object.pose.bones["bone"]
    bone_pose.bone.select=True
    bpy.context.object.data.bones.active = bone_pose.bone
    
    bpy.ops.pose.constraint_add(type='STRETCH_TO')
    bone_pose.constraints["Stretch To"].target = armature_obj
    bone_pose.constraints["Stretch To"].subtarget = "tail"
    bone_pose.constraints["Stretch To"].head_tail = 0
    
    add_transform_driver(bone_pose, armature_obj, 'bbone_scaleinx',  'head', 'SCALE_X')
    add_transform_driver(bone_pose, armature_obj, 'bbone_scaleiny',  'head', 'SCALE_Z')
    add_transform_driver(bone_pose, armature_obj, 'bbone_scaleoutx', 'tail', 'SCALE_X')
    add_transform_driver(bone_pose, armature_obj, 'bbone_scaleouty', 'tail', 'SCALE_Z')
    add_transform_driver(bone_pose, armature_obj, 'bbone_easein',  'head', 'SCALE_Y')
    add_transform_driver(bone_pose, armature_obj, 'bbone_easeout', 'tail', 'SCALE_Y')
    
    try:
        display_obj = bpy.context.scene.objects[self.handle_display_obj]
    except KeyError:
        display_obj = None
    
    if display_obj:
        bpy.context.object.pose.bones["tail"].custom_shape = display_obj
        armature.bones["tail"].show_wire = True
        bpy.context.object.pose.bones["head"].custom_shape = display_obj
        armature.bones["head"].show_wire = True
    
    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
    return armature_obj
    
class OBJECT_OT_add_bbone(Operator, AddObjectHelper):
    """Create a new Bendy Bone Object"""
    bl_idname = "armature.add_bbone"
    bl_label = "Add Bendy Bone With Handles"
    bl_options = {'REGISTER', 'UNDO'}
        
    length: FloatProperty(
        default = 1.0,
        min = 1e-5, #If bone length is near zero it won't be created
        name = "Length",
        subtype = 'DISTANCE',
    )
    
    def item_cb(self, context):
        return [("", "", "")] + [(ob.name, ob.name, ob.type) for ob in bpy.context.scene.objects if ob.type == 'MESH']
    
    handle_display_obj: EnumProperty(
        name = "Handle Object",
        items = item_cb,
        description = "Choose object to display as handle here",
    )

    def execute(self, context):
        create_bbone(self, context)
        return {'FINISHED'}


# Registration
def add_bbone_button(self, context):
    self.layout.operator(
        OBJECT_OT_add_object.bl_idname,
        text="Bendy Bone",
        icon='BONE_DATA')

def register():
    bpy.utils.register_class(OBJECT_OT_add_bbone)
    bpy.types.VIEW3D_MT_armature_add.append(add_bbone_button)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_add_bbone)
    bpy.types.VIEW3D_MT_armature_add.remove(add_bbone_button)


if __name__ == "__main__":
    register()
