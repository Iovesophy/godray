# This is template of God Ray with Blender bpy
# License Copyright (c) 2023 Iovesophy
# This software is released under the MIT License, see LICENSE. https://opensource.org/licenses/mit-license.php

import bpy

class StainedGlassShading:
    def __init__(self, object, material):
        self.object = object
        self.material = material

class ShadingParams:
    NAME = "StainedGlass"

def CreateMesh(type):
    if type == "context"
        return 0
    elif type == "cone":
        bpy.ops.mesh.primitive_cone_add()
    elif type == "cube":
        bpy.ops.mesh.primitive_cube_add()
    elif type == "cylinder":
        bpy.ops.mesh.primitive_cylinder_add()
    elif type == "ico_sphere":
        bpy.ops.mesh.primitive_ico_sphere_add()
    elif type == "monkey":
        bpy.ops.mesh.primitive_monkey_add()
    elif type == "torus":
        bpy.ops.mesh.primitive_torus_add()
    elif type == "uv_sphere":
        bpy.ops.mesh.primitive_uv_sphere_add()
    else:
        bpy.ops.mesh.primitive_ico_sphere_add()

def SetupMeshShading():
    Shading = StainedGlassShading(bpy.context.object, bpy.data.materials.new(name=ShadingParams.NAME))
    Shading.object.active_material = Shading.material
    Shading.material.use_nodes = True
    return Shading
    
def CreateWireframeObject(type):
    status = CreateMesh(type)
    if status == 0:
        print(status, "wireframe: CreateMesh is context mode")

    bpy.ops.object.modifier_add(type="WIREFRAME")
    
    StainedGlass = SetupMeshShading()
    nodepbsdf = StainedGlass.material.node_tree.nodes["Principled BSDF"]
    nodepbsdf.inputs[0].default_value = (0, 0, 0, 1)
    
def CreateSurfaceObject(type):
    CreateMesh(type)
    StainedGlass = SetupMeshShading()
    
    nodepbsdf = StainedGlass.material.node_tree.nodes["Principled BSDF"]
    StainedGlass.material.node_tree.nodes.remove(nodepbsdf)
    
    nodematerialoutput = StainedGlass.material.node_tree.nodes["Material Output"]
    nodegbsdf = StainedGlass.material.node_tree.nodes.new(type="ShaderNodeBsdfGlass")
    nodegbsdf.inputs[2].default_value = 20.0
    
    nodeinfo = StainedGlass.material.node_tree.nodes.new("ShaderNodeObjectInfo")
    nodeinfo.location = -500, -110
    
    nodecolor = StainedGlass.material.node_tree.nodes.new("ShaderNodeValToRGB")
    nodecolor.location = -300, -110
    nodecolor.color_ramp.color_mode = "HSV"
    nodecolor.color_ramp.hue_interpolation = "CW"
    nodecolor.color_ramp.elements[0].color = (1, 0, 0, 1)
    nodecolor.color_ramp.elements[1].color = (1, 0, 0.01, 1)
    
    StainedGlass.material.node_tree.links.new(nodeinfo.outputs[5], nodecolor.inputs[0])
    StainedGlass.material.node_tree.links.new(nodecolor.outputs[0], nodegbsdf.inputs[0])
    StainedGlass.material.node_tree.links.new(nodegbsdf.outputs[0], nodematerialoutput.inputs[0])
    
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.edge_split(type="EDGE")
    bpy.ops.mesh.separate(type="LOOSE")
    bpy.ops.object.editmode_toggle()
    
def CreatePointLight():
    bpy.ops.object.light_add(type="POINT", radius=10)
    lightobject = bpy.context.active_object
    light = lightobject.data
    light.energy = 500
    
def CreateFloor():
    bpy.ops.mesh.primitive_plane_add(size=30.0, align="WORLD", location=(0.0, 0.0, -1.0))
    
def CreateStainedGlassObject(type):
    CreateWireframeObject(type)
    CreateSurfaceObject(type)

def main():
    CreateStainedGlassObject("uv_sphere")
    #CreatePointLight()
    #CreateFloor()

if __name__ == "__main__":
    main()

# todo: enable god ray mode
# todo: enable blender ui
# todo: enable blender addon
# todo: enable shader mix for glass, because need pass light beam.

