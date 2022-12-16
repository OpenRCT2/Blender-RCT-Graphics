'''
Copyright (c) 2022 RCT Graphics Helper developers

For a complete list of all authors, please refer to the addon's meta info.
Interested in contributing? Visit https://github.com/oli414/Blender-RCT-Graphics

RCT Graphics Helper is licensed under the GNU General Public License version 3.
'''

import bpy

def draw(self, context):
    self.layout.operator("render.rct_switch")

def register_button():
    bpy.types.INFO_MT_render.append(draw)


def unregister_button():
    bpy.types.INFO_MT_render.remove(draw)


def try_register_button(context):
    if "Rig" in context.scene.objects:
        register_button()
    else:
        unregister_button()
