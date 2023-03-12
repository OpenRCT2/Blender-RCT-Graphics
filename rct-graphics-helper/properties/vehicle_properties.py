'''
Copyright (c) 2023 RCT Graphics Helper developers

For a complete list of all authors, please refer to the addon's meta info.
Interested in contributing? Visit https://github.com/oli414/Blender-RCT-Graphics

RCT Graphics Helper is licensed under the GNU General Public License version 3.
'''

import bpy
import math
import os

from ..operators.render_operator import RCTRender
from ..angle_sections.track import sprite_group_metadata, legacy_group_names, legacy_group_metadata

class SpriteTrackFlag(object):
    name = ""
    description = ""
    default_value = False
    section_id = None

    def __init__(self, section_id, name, description, default_value):
        self.section_id = section_id
        self.name = name
        self.description = description
        self.default_value = default_value


def CreateSpriteEnum(defaultValue):
    return (
        ("0", "Disabled" + (defaultValue == 0 and " (Default)" or ""), "No sprites are rendered", 0),
        ("1", "1" + (defaultValue == 1 and " (Default)" or ""), "One sprite rendered", 1),
        ("2", "2" + (defaultValue == 2 and " (Default)" or ""), "Two sprites rendered", 2),
        ("4", "4" + (defaultValue == 4 and " (Default)" or ""), "Four sprites rendered", 4),
        ("8", "8" + (defaultValue == 8 and " (Default)" or ""), "Eight sprites rendered", 8),
        ("16", "16" + (defaultValue == 16 and " (Default)" or ""), "Sixteen sprites rendered", 16),
        ("32", "32" + (defaultValue == 32 and " (Default)" or ""), "Thirty-two sprites rendered", 32),
        ("64", "64" + (defaultValue == 64 and " (Default)" or ""), "Sixty-four sprites rendered", 64)
    )

class VehicleProperties(bpy.types.PropertyGroup):
    # Create legacy sprite groups
    legacy_defaults = []
    legacy_spritegroups = {}
    for legacy_group_name in legacy_group_names:
        config = legacy_group_metadata[legacy_group_name]
        legacy_spritegroups[legacy_group_name] = SpriteTrackFlag(legacy_group_name, *config)
        legacy_defaults.append(config[2])

    sprite_track_flags = bpy.props.BoolVectorProperty(
        name="Track Pieces",
        default=legacy_defaults,
        description="Which track pieces to render sprites for",
        size=len(legacy_spritegroups))

    # Create modern sprite groups
    for key, config in sprite_group_metadata.items():
        locals()[key] = bpy.props.EnumProperty(
            name = key,
            description = config[1],
            items = CreateSpriteEnum(config[0])
        )

    inverted_set = bpy.props.BoolProperty(
        name="Inverted Set",
        description="Used for rides which can invert for an extended amount of time like the flying and lay-down rollercoasters",
        default=False)

    sprite_group_mode = bpy.props.EnumProperty(
        name="Sprite group mode",
        items=(
            ("SIMPLE", "Simple sprite groups",
             "Combines several sprite groups and sets their sprite precisions automatically", 1),
            ("FULL", "Full sprite groups",
             "Set all sprite group precisions manually", 2),
        )
    )


def register_vehicles_properties():
    bpy.types.Scene.rct_graphics_helper_vehicle_properties = bpy.props.PointerProperty(
        type=VehicleProperties)


def unregister_vehicles_properties():
    del bpy.types.Scene.rct_graphics_helper_vehicle_properties
