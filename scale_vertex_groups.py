bl_info = {
    "name": "Scale Vertex Group",
    "author": "Samuel Bourland <samuel.bourland@gmail.co",
    "version": (1, 0),
    "blender": (4, 00, 0),
    "location": "Operator Search",
    "description": "Scales the selected vertex vroup on selected vertices",
    # "warning": "",
    # "doc_url": "",
    "category": "Rigging",
}

import bpy

class ScaleVertexGroup(bpy.types.Operator):
    bl_idname = "mesh.scale_vertex_group"
    bl_label = "Scale Vertex Group"

    def __init__(self):
        print("Start")

    def __del__(self):
        print("End")

    def execute(self, context):
        if self.shift:
            scale = 1 + self.value / 1000.0
        else:
            scale = 1 + self.value / 100.0

        for v in self.vertices:
            vw = self.active_vgroup.weight(v.index) * scale # Scale the active vertex group's weight by mouse_y
            if vw <= 1 - self.locked_weights[v.index]:

                self.active_vgroup.add([v.index], vw, 'REPLACE') # Replace weight with the newly scaled weight
                for vg in self.selected_vgroups:
                    if self.total_weight[v.index] - self.init_weights[self.active_vgroup.name + str(v.index)] - self.locked_weights[v.index] > 0:
                        if vg.index in [ vg.group for vg in v.groups ]:
                            normalize_vw = (self.init_weights[vg.name + str(v.index)] / (self.total_weight[v.index] - self.init_weights[self.active_vgroup.name + str(v.index)] - self.locked_weights[v.index])) * (self.total_weight[v.index] - vw - self.locked_weights[v.index])
                            vg.add([v.index], normalize_vw, 'REPLACE')


        return {'FINISHED'}


    def modal(self, context, event):
        if event.type == 'MOUSEMOVE':  # Apply
            self.value = event.mouse_y - event.mouse_prev_y
            self.shift = event.shift
            self.execute(context)
        elif event.type == 'LEFTMOUSE':  # Confirm
            bpy.ops.object.mode_set(mode='EDIT')
            return {'FINISHED'}
        elif event.type in {'RIGHTMOUSE', 'ESC'}:  # Cancel
            # Set all weights back to their original values
            for v in self.vertices:
                self.active_vgroup.add([v.index], self.init_weights[self.active_vgroup.name + str(v.index)], 'REPLACE')
                for vg in self.selected_vgroups:
                    if vg.index in [ vg.group for vg in v.groups ]:
                        vg.add([v.index], self.init_weights[vg.name + str(v.index)], 'REPLACE')
            bpy.ops.object.mode_set(mode='EDIT')
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        o = bpy.context.active_object

        bpy.ops.object.mode_set(mode='OBJECT')

        self.active_vgroup = o.vertex_groups.active # active vertex group

        self.vertices = [ v for v in bpy.context.active_object.data.vertices if self.active_vgroup.index in [ vg.group for vg in v.groups ] if v.select == True] # get all selected vertices in active vertex group

        self.selected_vgroups = set() #contains index of unlocked vertex groups assigned to selected vertices
        self.locked_vgroups = set() #contains index of locked vertex groups...

        for m in o.modifiers:
            if m.type == 'ARMATURE':
                armature = m.object # Get the armature modifiying the mesh

        for b in armature.pose.bones:
            if self.active_vgroup.name == b.name: # check if active vertex group is Deform
                for b in armature.pose.bones:
                    for v in self.vertices:
                        for vg in v.groups:
                            if o.vertex_groups[vg.group].name != self.active_vgroup.name: # don't add active_vgroup to the list
                                if o.vertex_groups[vg.group].name == b.name: # check if selected bones are Deform
                                    if o.vertex_groups[vg.group].lock_weight == False:
                                        self.selected_vgroups.add(o.vertex_groups[vg.group])
                                    else:
                                        self.locked_vgroups.add(o.vertex_groups[vg.group])

        self.init_weights = {}
        self.locked_weights = {}
        self.total_weight = {}

        for v in self.vertices:
            self.total_weight[v.index] = 0.0
            self.locked_weights[v.index] = 0.0

            self.init_weights[self.active_vgroup.name + str(v.index)] = self.active_vgroup.weight(v.index)
            self.total_weight[v.index] += self.active_vgroup.weight(v.index)

            for vg in self.selected_vgroups:
                if vg.index in [ vg.group for vg in v.groups ]:
                    self.init_weights[vg.name + str(v.index)] = vg.weight(v.index)
                    self.total_weight[v.index] += vg.weight(v.index)

            for vg in self.locked_vgroups:
                if vg.index in [ vg.group for vg in v.groups ]:
                    self.locked_weights[v.index] += vg.weight(v.index)
                    self.total_weight[v.index] += vg.weight(v.index)

        self.value = event.mouse_y - event.mouse_prev_y
        self.shift = event.shift
        self.execute(context)

        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


# Only needed if you want to add into a dynamic menu.
def menu_func(self, context):
    self.layout.operator(ScaleVertexGroup.bl_idname, text="Scale Vertex Group")


# Register and add to the object menu (required to also use F3 search "Modal Operator" for quick access).
def register():
    bpy.utils.register_class(ScaleVertexGroup)
    bpy.types.VIEW3D_MT_edit_mesh_weights.append(menu_func)

def unregister():
    bpy.utils.unregister_class(ScaleVertexGroup)
    bpy.types.VIEW3D_MT_edit_mesh_weights.remove(menu_func)
