# -*- coding: utf-8 -*-

import os,sys
import maya.cmds as cmds
import maya.utils as utils

import re


#=================== install function

def onMayaDroppedPythonFile(obj):

    sys_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')) 
    sys.path.append(sys_path) #install this mod to maya


class CommonTools(QWidget):

    def __init__(self):
        
        super(CommonTools,self).__init__()
        self.mayaMainWindowPtr = omui.MQtUtil.mainWindow()
        self.mayaMainWindow = wrapInstance(long(self.mayaMainWindowPtr), QWidget) 

        #Set the object name     
        self.setObjectName('CommonTools')
        self.setWindowTitle('CommonTools')

        #Parent widget under Maya main window        
        self.setParent(self.mayaMainWindow) 
        self.setWindowFlags(Qt.Window)


    def initUI(self,root_path):
        loader = QUiLoader()
        file = QFile(root_path+"/common_tools_ui.ui")
        file.open(QFile.ReadOnly) 
        self.ui = loader.load(file, parentWidget=self)
        file.close()

        # Call rename_dup if user click button
        self.ui.pushButton.clicked.connect( self.rename_dup)       


        self.show()

    
    @Slot()
    def rename_dup(self):
        #Find all objects that have the same shortname as another
        #We can indentify them because they have | in the name
        duplicates = [f for f in cmds.ls() if '|' in f]
        #Sort them by hierarchy so that we don't rename a parent before a child.
        duplicates.sort(key=lambda obj: obj.count('|'), reverse=True)
        
        #if we have duplicates, rename them
        if duplicates:
            for name in duplicates:
                # extract the base name
                m = re.compile("[^|]*$").search(name) 
                shortname = m.group(0)
    
                # extract the numeric suffix
                m2 = re.compile(".*[^0-9]").match(shortname) 
                if m2:
                    stripSuffix = m2.group(0)
                else:
                    stripSuffix = shortname
                
                #rename, adding '#' as the suffix, which tells maya to find the next available number
                newname = cmds.rename(name, (stripSuffix + "#")) 
                print("renamed %s to %s" % (name, newname))
                
            return "Renamed %s objects with duplicated name." % len(duplicates)
        else:
            return "No Duplicates"
            

# ====================================
import common_tools

root_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ))) #after install we can get the current file's path
ct = CommonTools()
ct.initUI(root_path)
    
