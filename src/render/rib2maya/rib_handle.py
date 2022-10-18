#!/usr/bin/python
# -*- coding: utf-8 -*-

import os,sys
import maya.cmds as cmds
import maya.utils as utils
import rfm2.api.nodes

#=================== install function

def onMayaDroppedPythonFile(obj):

    sys_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')) 
    sys.path.append(sys_path) #install this mod to maya
    


class rib_handle():

    def __init__(self):
        pass

    def export_rib(self,file_name):        
        cmds.file ( file_name ,force=True, options =   "rmanExportRIBFormat=1;rmanExportMultipleFrames=0;rmanExportStartFrame=1;rmanExportEndFrame=10;rmanExportByFrame=1;rmanExportRIBArchive=1;rmanExportRIBOmitDefaultedAttributes=0;rmanExportRIBCamera=persp" ,
                    typ = "RIB" ,pr = True, es = True )

    def import_rib(self,file_name):
        rfm2.api.nodes.import_archive(file_name)


if (__name__ == "__main__"):

    
    r_h = rib_handle()

    filepath = "V:\\Quasar\\approved\\caches\\Rib\\Grass"

    objs = cmds.ls(sl=True)

    for obj in objs:
        
        cmds.select(cl=True)
        cmds.select(obj)
        
        file_name = os.path.join(filepath,obj)
        
        print(file_name)        
        r_h.export_rib(file_name)

        #t = threading.Thread(target = export_to_rib,args = [filename])    
        #t.start()


    file_path = "V:\\Quasar\\approved\\caches\\Rib\\Grass"
    
    file_list = os.listdir(file_path)
        
    for rib_file in file_list:      
        if(os.path.splitext(rib_file)[1]==".rib"):
            file_name = os.path.join(file_path,rib_file)
            r_h.import_rib(file_name)



