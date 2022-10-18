#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import maya.cmds as cmds
import maya.utils as utils
import threading

def export_file(filename):
    
     cmds.file ( filename ,force=True, options =   "rmanExportRIBFormat=1;rmanExportMultipleFrames=0;rmanExportStartFrame=1;rmanExportEndFrame=10;rmanExportByFrame=1;rmanExportRIBArchive=1;rmanExportRIBOmitDefaultedAttributes=0;rmanExportRIBCamera=persp" ,
                                      typ = "RIB" ,pr = True, es = True )

def export_to_rib(filename):
    
    utils.executeDeferred(  export_file  , filename)


filepath = "E:/temp"
objs = cmds.ls(sl=True)

for obj in objs:
    
    cmds.select(cl=True)
    cmds.select(obj)
    
    filename = os.path.join(filepath,obj)
    
    print(filename)
    
    t = threading.Thread(target = export_to_rib,args = [filename])
    
    t.start()