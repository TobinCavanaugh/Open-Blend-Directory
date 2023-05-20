import bpy
import os
import subprocess
import platform

bl_info = {
    "name": "Open Blend Directory",
    "description": "Opens the directory where the currently opened .blend file is stored similarly to how JetBrains handles it. Cross Platform!",
    "author": "Tobin Cavanaugh",
    "version": (1, 0),
    "blender": (3, 3, 1),
    "location": "View3D > Tool Shelf > My Addon",
    "category": "System",
}

addon_keymaps = []

# Thanks to
# https://blender.stackexchange.com/questions/717/is-it-possible-to-print-to-the-report-window-in-the-info-view
# Manu Järvinen & brockmann for this solution
def ErrorMessageUnsaved(self, context):
    self.layout.label(text="You haven't saved your blender file yet! That's bad! Save it!")

def ErrorMessageOS(self, context):
    self.layout.label(text="I don't know this operating system! It should be easy to add support for though")


#Actual function for opening the blend directory
def open_blend_directory():

    #Get the save data path
    blend_file_path = bpy.data.filepath

    #Choose the correct OS, if its a valid save path
    #No guarantees that these work on non windows platforms
    #According to Lous Brandy & Boris Verkhoviskiy this should be correct
    # https://stackoverflow.com/questions/1854/how-to-identify-which-os-python-is-running-on
    if blend_file_path:
        if platform.system() == 'Windows':
            subprocess.Popen(f'explorer /select, "{bpy.data.filepath}"')
        elif platform.system() == 'Linux':
            subprocess.Popen(['xdg-open', os.path.dirname(blend_file_path)])
        elif platform.system() == 'Darwin':
            subprocess.Popen(['open', '-R', blend_file_path])
        else:
            bpy.context.window_manager.popup_menu(ErrorMessageOS, title="Error", icon='ERROR')
    else:
        bpy.context.window_manager.popup_menu(ErrorMessageUnsaved, title="Error", icon='ERROR')


def register():

    #Register our class
    bpy.utils.register_class(OpenBlendDirectoryOperator)
    wm = bpy.context.window_manager

    #I dont really understand whats going on here tbh

    #Get our new keymap
    km = wm.keyconfigs.addon.keymaps.new(name='Window', space_type='EMPTY')
    
    #Create the keymap? if you want to change the keybinds for alt + shift + r, do it here!!
    kmi = km.keymap_items.new('wm.open_blend_directory', 'R', 'PRESS', alt=True, shift=True)
    
    #Append to the keymaps
    addon_keymaps.append((km, kmi))


def unregister():

    #Unregister our class
    bpy.utils.unregister_class(OpenBlendDirectoryOperator)
    wm = bpy.context.window_manager

    #Remove all keymaps
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)

    #Clear our locally saved keymaps
    addon_keymaps.clear()


#Define our operator class
class OpenBlendDirectoryOperator(bpy.types.Operator):

    bl_idname = "wm.open_blend_directory"
    bl_label = "Open Blend Directory"
    bl_options = {'REGISTER'}

    #On execution, open the directory
    def execute(self, context):
        open_blend_directory()
        return {'FINISHED'}

classes = [
    OpenBlendDirectoryOperator,
]

if __name__ == "__main__":
    register()