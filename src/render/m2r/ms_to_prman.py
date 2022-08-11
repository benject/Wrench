#!/usr/bin/python
# -*- coding: utf-8 -*-


import os
import maya.cmds as cmds


# for ui
from maya import OpenMayaUI as omui 
from PySide2.QtCore import * 
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtUiTools import QUiLoader

from shiboken2 import wrapInstance 

import rfm2


class M2R_UI(QWidget): 
    
    def __init__(self, *args, **kwargs):        
        super(M2R_UI, self).__init__(*args, **kwargs)

        self.mayaMainWindowPtr = omui.MQtUtil.mainWindow()
        self.mayaMainWindow = wrapInstance(long(self.mayaMainWindowPtr), QWidget) 

        #Set the object name     
        self.setObjectName('M2R_UI')        
        self.setWindowTitle('M2R_UI')

        #Parent widget under Maya main window        
        self.setParent(self.mayaMainWindow) 
        self.setWindowFlags(Qt.Window)

        self.folder = r''

        self.initUI()

        self.show()




    def initUI(self):
        loader = QUiLoader()        
        #currentDir = os.path.dirname(__file__)
        currentDir = r"D:\Personal_works\python\maya_scripts"
        file = QFile(currentDir+"/ms_to_prman.py.ui")        
        file.open(QFile.ReadOnly) 
        self.ui = loader.load(file, parentWidget=self)        
        file.close()
        
        # Call doOK if user clicks OK button
        self.ui.pushButton.clicked.connect( self.doOK )
    
    @Slot()
    def doOK(self):

        self.folder = self.ui.textEdit.toPlainText()
        self.connectTextures()



    def createPxrNetwork(self):
        
        sgNode = rfm2.api.nodes.create_and_assign_bxdf('PxrSurface')
        dispNode = rfm2.api.nodes.create_node( '' , 'PxrDisplace')[8:-1]
        surfNode = rfm2.api.nodes.get_bxdf(sgNode)

        cmds.setAttr('%s.diffuseDoubleSided'%surfNode,1)
        cmds.setAttr('%s.specularDoubleSided'%surfNode,1)
        
        print("%s,created!"%surfNode)
        nodes = []
        
        #color
        
        pxrBlend = rfm2.api.nodes.create_node('','PxrBlend')[8:-1]
        cmds.setAttr("%s.operation"%pxrBlend ,18) #set blend mode to multiply
    

        aoTex = rfm2.api.nodes.create_node( '', 'PxrTexture' )[8:-1]
        cmds.setAttr('%s.missingColor'%aoTex,1,1,1,type='double3')
        cmds.connectAttr('%s.resultRGB'%aoTex,'%s.topRGB'%pxrBlend)
            
        
        albedoTex = rfm2.api.nodes.create_node( '', 'PxrTexture' )[8:-1]
        cmds.setAttr('%s.missingColor'%albedoTex,1,1,1,type='double3')
        cmds.setAttr('%s.linearize'%albedoTex, 1)
        
        cmds.connectAttr('%s.resultRGB'%albedoTex,'%s.bottomRGB'%pxrBlend)    

        nodes.append(aoTex)
        nodes.append(albedoTex)
        

        
        #normal map
        
        normalTex = rfm2.api.nodes.create_node( '', 'PxrNormalMap' )[8:-1]
        
        cmds.setAttr('%s.orientation'%normalTex , 0)
        cmds.connectAttr('%s.resultN'%normalTex , '%s.bumpNormal'%surfNode)
        
        nodes.append(normalTex) 
        
        #metalness

        mtlTex = rfm2.api.nodes.create_node( '', 'PxrTexture' )[8:-1]
        cmds.setAttr('%s.missingColor'%mtlTex,0,0,0,type='double3')

        nodes.append(mtlTex)
        

        pxrMtl = rfm2.api.nodes.create_node( '', 'PxrMetallicWorkflow' )[8:-1]
        #connect base color to metalness as we are on metalness workflow
        
        cmds.connectAttr('%s.resultRGB'%pxrBlend,'%s.baseColor'%pxrMtl)
        cmds.connectAttr('%s.resultRGB.resultRGBR'%mtlTex,'%s.metallic'%pxrMtl)


        cmds.connectAttr('%s.resultDiffuseRGB'%pxrMtl,'%s.diffuseColor'%surfNode)  
        cmds.connectAttr('%s.resultSpecularEdgeRGB'%pxrMtl, '%s.specularEdgeColor'%surfNode)
        cmds.connectAttr('%s.resultSpecularFaceRGB'%pxrMtl, '%s.specularFaceColor'%surfNode)
        
        #roughness
        
        roufTex = rfm2.api.nodes.create_node( '', 'PxrTexture' )[8:-1]
        cmds.setAttr('%s.missingColor'%roufTex,1,1,1,type='double3')
        cmds.connectAttr('%s.resultRGB.resultRGBR'%roufTex,'%s.specularRoughness'%surfNode)

        nodes.append(roufTex)



        #displacement
    
        dispTex = rfm2.api.nodes.create_node( '', 'PxrTexture' )[8:-1]
        cmds.setAttr('%s.missingColor'%dispTex,0,0,0,type='double3')

        nodes.append(dispTex)

        dispTransform = rfm2.api.nodes.create_node('','PxrDispTransform')[8:-1]
        cmds.setAttr('%s.dispHeight'%dispTransform ,1)
        cmds.setAttr('%s.dispDepth'%dispTransform ,1)
        cmds.setAttr('%s.dispRemapMode'%dispTransform ,2)        


        cmds.connectAttr('%s.resultRGB.resultRGBR'%dispTex,'%s.dispScalar'%dispTransform)
        cmds.connectAttr('%s.resultF'%dispTransform,'%s.dispScalar'%dispNode)


        #opacity
        opTex = rfm2.api.nodes.create_node( '', 'PxrTexture' )[8:-1]
        cmds.setAttr('%s.missingColor'%opTex,1,1,1,type='double3')
        cmds.connectAttr('%s.resultRGB.resultRGBR'%opTex,'%s.presence'%surfNode)
        nodes.append(opTex)
        '''
        #translucency
        transTex = rfm2.api.nodes.create_node( '', 'PxrTexture' )[8:-1]
        cmds.setAttr('%s.missingColor'%opTex,0,0,0,type='double3')
        cmds.connectAttr('%s.resultRGB.resultRGB'%transTex,'%s.specularRoughness'%surfNode)
        nodes.append(transTex)
        '''

        #connect manifold
        manifold = rfm2.api.nodes.create_node('','PxrManifold2D')[8:-1]

        cmds.connectAttr('%s.result'%manifold,'%s.manifold'%aoTex)
        cmds.connectAttr('%s.result'%manifold,'%s.manifold'%albedoTex)
        cmds.connectAttr('%s.result'%manifold,'%s.manifold'%normalTex)
        cmds.connectAttr('%s.result'%manifold,'%s.manifold'%mtlTex)
        cmds.connectAttr('%s.result'%manifold,'%s.manifold'%roufTex)
        cmds.connectAttr('%s.result'%manifold,'%s.manifold'%dispTex)
        cmds.connectAttr('%s.result'%manifold,'%s.manifold'%opTex)


        return nodes


    def connectTextures(self):

        #create shading network

        folder = self.folder

        if(len(folder)>0):

            nodes = self.createPxrNetwork()
            #print(nodes)

            #folder = r"R:\Megascan\Downloaded\surface\fabric_leather_tlooadar"

            
            textures = os.listdir(folder)

            for texture in textures:

                texName = os.path.splitext(texture)
            
                
                if(texName[0].endswith("AO")==True):

                    pxrTex = (os.path.join(folder,texture))
                    cmds.setAttr("%s.filename"%nodes[0],pxrTex,type="string")

                if(texName[0].endswith("Albedo")==True):

                    pxrTex = (os.path.join(folder,texture))
                    cmds.setAttr("%s.filename"%nodes[1],pxrTex,type="string")
                
                
                if(texName[0].endswith("Normal")==True  or texName[0].endswith("Normal_LOD0")== True ):

                    pxrTex = (os.path.join(folder,texture))
                    cmds.setAttr("%s.filename"%nodes[2],pxrTex,type="string")

                if(texName[0].endswith("Metalness")==True):
                
                    pxrTex = (os.path.join(folder,texture))
                    cmds.setAttr("%s.filename"%nodes[3],pxrTex,type="string")

                if(texName[0].endswith("Roughness")==True):

                    pxrTex = (os.path.join(folder,texture))
                    cmds.setAttr("%s.filename"%nodes[4],pxrTex,type="string")
                
                if(texName[0].endswith("Displacement")==True):

                    pxrTex = (os.path.join(folder,texture))
                    cmds.setAttr("%s.filename"%nodes[5],pxrTex,type="string")
                
                if(texName[0].endswith("Opacity")==True):

                    pxrTex = (os.path.join(folder,texture))
                    cmds.setAttr("%s.filename"%nodes[6],pxrTex,type="string")
                '''
                if(texName[0].endswith("Translucency")==True):

                    pxrTex = (os.path.join(folder,texture))
                    cmds.setAttr("%s.filename"%nodes[7],pxrTex,type="string")
                '''
                                        

m2r_ui = M2R_UI()
    