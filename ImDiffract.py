# -*- coding: utf-8 -*-
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
import sys
from Ui_ImDiffract import Ui_MainWindow

import matplotlib.image as mpimg
from scipy import ndimage
import numpy as np

class ImDiffract(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        
    def Image(self):
        
        self.img=mpimg.imread(self.filename1[0])
        self.yc=self.slider_yc.value()
        self.label_ycVal.setText(str(self.slider_yc.value()))
        
        plt1=self.gv1.canvas
        plt1.ax.clear()
        # Rotate image
        rot_angle = self.angle.value()/10   
        ## Dial label
        self.label_angle.setText(str(rot_angle)+"°")
        self.im_rot = ndimage.rotate(self.img,rot_angle,mode='constant',cval=100)
#        plt1.ax.imshow(self.img)
        plt1.ax.imshow(self.im_rot, interpolation='gaussian')
        plt1.ax.axhline(y=self.yc, color='y',lw=2, ls='--')
        plt1.ax.set_title("Figure de diffraction", fontsize=14, weight="bold")
        plt1.ax.set_xlabel("Pixels", weight="bold")
        plt1.ax.set_ylabel("Pixels", weight="bold")
        plt1.draw()
    def Profile(self):
        
        red = self.im_rot[:,:,0]
        green = self.im_rot[:,:,1]
        blue = self.im_rot[:,:,2]
        
        # Define Red and RGB profiles
        self.red_line=blue[self.yc,:]
        self.rgb_lines = self.im_rot[self.yc,:]
        # Check Box
        if self.cb_RGB.isChecked() == True:
            line= self.rgb_lines
        else:
            line= self.red_line
            
        # Figure
        plt2=self.gv2.canvas
        plt2.ax.clear()
        
        plt2.ax.plot(line)
        plt2.ax.set_title("Profile", fontsize=14, weight="bold")
        plt2.ax.set_xlabel("Pixels", weight="bold")
        plt2.ax.set_ylabel("Inetensité (ua)", weight="bold")
        plt2.draw()
   
    @pyqtSlot("int")
    def on_slider_yc_valueChanged(self, value):
        self.Image()
        self.Profile()
    
    @pyqtSlot("int")
    def on_angle_valueChanged(self, value):
        self.Image()
        self.Profile()
    
    @pyqtSlot()
    def on_bt_load_clicked(self):
        try:
            self.filename1 = QFileDialog.getOpenFileName(
                self,
                self.tr("Charger une image de diffraction"),
                "images/",
                "")
            self.Image()
            self.Profile()
            self.groupBox.setEnabled(True)
            self.bt_save.setEnabled(True)
        except:
            pass

    @pyqtSlot()
    def on_bt_save_clicked(self):
        try:
            self.filename2 = QFileDialog.getSaveFileName(
                self,
                self.tr("Save Profile"),
                "profiles/",
                "")
            np.save(self.filename2[0], self.red_line)
            
        except:
            pass
#        a=np.load("profiles/data_test.npy")
#        print(a)

    @pyqtSlot()
    def on_cb_RGB_clicked(self):
        try:
            self.Profile()
        except:
            pass
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    MyApplication = ImDiffract()
    MyApplication.show()
    sys.exit(app.exec_())
