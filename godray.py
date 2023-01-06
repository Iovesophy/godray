# This is template of God Ray with Blender bpy
# License Copyright (c) 2023 Iovesophy
# This software is released under the MIT License, see LICENSE. https://opensource.org/licenses/mit-license.php

import bpy
import random

class GodRayShading:
    def __init__(self, object, material):
        self.object = object
        self.material = material

class ShadingParams:
    NAME = "GodRay"

def SetupMeshShading():
    Shading = GodRayShading(bpy.context.object, bpy.data.materials.new(name=ShadingParams.NAME))
    Shading.object.active_material = Shading.material
    Shading.material.use_nodes = True
    return Shading
    
def CreateEnvObject():
    bpy.ops.mesh.primitive_cube_add(size=30.0)
    
    GodRayEnv = SetupMeshShading()
    nodepbsdf = GodRayEnv.material.node_tree.nodes["Principled BSDF"]
    GodRayEnv.material.node_tree.nodes.remove(nodepbsdf)
        
    nodepvolume = GodRayEnv.material.node_tree.nodes.new(type="ShaderNodeVolumePrincipled")
    GodRayEnv.material.node_tree.nodes["Principled Volume"].inputs[2].default_value = 0.01
    
    nodematerialoutput = GodRayEnv.material.node_tree.nodes["Material Output"]
    GodRayEnv.material.node_tree.links.new(nodepvolume.outputs[0], nodematerialoutput.inputs[1])
    
def CreateSpotLight(angleX, angleY, angleZ):
    bpy.ops.object.light_add(type="SPOT", radius=0, rotation=(angleX, angleY, angleZ))
    lightobject = bpy.context.active_object
    light = lightobject.data
    light.energy = 1000
    light.color = (random.uniform(0, 1),random.uniform(0, 1),random.uniform(0, 1))
    
def CreateSphereWall():
    bpy.ops.mesh.primitive_uv_sphere_add(radius=30.0, segments=200)
    
def CreateGodRayEnvObject():
    CreateEnvObject()

def main():
    CreateGodRayEnvObject()
    for i in range(18):
        CreateSpotLight(0.0, i*20, 0.0)
    for i in range(18):
        CreateSpotLight(i*20, 0.0, 0.0)
    CreateSphereWall()

if __name__ == "__main__":
    main()

