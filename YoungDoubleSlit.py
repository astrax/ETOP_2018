# -*- coding: utf-8 -*-
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog

import sys
from Ui_DoubleSlit1D import Ui_MainWindow
from ImDiffract import ImDiffract
        
from numpy import pi, linspace, sin, exp, real, imag, load

class DoubleSlit1D(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.imtool= ImDiffract(self)

    def fig1(self):
        lamda = self.slider_lambda.value() * 1.E-9
        k = (2 * pi)/lamda  # Wavelength
        # Slits width, b is along (Ox)
        b = self.SpinBox_b.value() * 1.E-6
        db = self.slider_db.value() * 1.E-6
        b1 = b
        b2 = b + db
        b_moy = (b1 + b2) / 2
        a = self.SpinBox_a.value() * 1.E-2    # Edge-Slits distance
        # f2=D Lens focal-length(m)
        D = self.slider_D.value()/10
        # Square-shaped screen (m)
        sx = 2 * 1.E-2
#        sx =10.E-3
        # Central maximum width (Ox)
        dx = 1.E+2 * (2 * lamda * D) / b
        self.Central_Spot.setText(str("%.4f" % dx))
        # Central maximum width (Oy)
        dy = 1.E+2 * (lamda * D) / (a + b_moy)
        self.Internal_Spot.setText(str("%.4f" % dy))
        self.X_Mmax = sx / 2
        self.X_Mmin = -sx / 2
        N = 600
        # Coordinates of screen
        X = linspace(self.X_Mmin, self.X_Mmax, N)
        v1 = (k * (a + b1) * X) / (2 * D)
        v2 = (k * b1 * X ) / (2 * D)
        v3 = (k * (a + b2) * X ) / (2 * D)
        v4 = (k * b2 * X) / (2 * D)
        
        Amplitude = exp(1j * v1) * sin(v2)/v2
                       
        Amplitude1 = real(Amplitude)*real(Amplitude)
        Amplitude2 = imag(Amplitude)*imag(Amplitude)
        
        envelop = Amplitude1 + Amplitude2
        
        AmplitudeI = b1 * exp(1j * v1) * sin(v2)/v2 + b2 * exp(-1j * v3) * sin(v4)/v4
        Amplitude1I = real(AmplitudeI)*real(AmplitudeI)
        Amplitude2I = imag(AmplitudeI)*imag(AmplitudeI)
        # b_moy Fctor of normalisation
        I = (Amplitude1I + Amplitude2I)/4/ (b_moy*b_moy)
        #-- Figure 1 D ------------------
        mpl1d = self.mplwidget1D.canvas
        mpl1d.ax.clear()
        mpl1d.ax.plot(X, I, '--y', linewidth=2, label="Callculated Intensity",
                      alpha=.8)
        mpl1d.ax.plot(X, envelop, ":w", linewidth=1, alpha=.8)
        mpl1d.ax.set_xlim(self.X_Mmin, self.X_Mmax)
        mpl1d.ax.set_xlabel(r'$X (m)$', fontsize=12, fontweight='bold')
        mpl1d.ax.set_ylabel(r'$I(X,Y)/I_0$', fontsize=12, fontweight='bold')
        mpl1d.figure.suptitle(
            'Fraunhofer Double Slits Diffraction', fontsize=14, fontweight='bold')
        mpl1d.ax.set_title(r"$\lambda = %.3e \ m, \ b1 = %.2e \ m, \ b2 = %.2e \ m, \ a = %.2e \ m, \ D = %.1f \ m$" % (
            lamda, b1, b2, a, D), fontsize=10)
        
        # Profile
        P_I=load(self.filename_p[0])
        xs=linspace(self.X_Mmin,self.X_Mmax, len(P_I))
        for ix,ip in zip(xs,P_I):
            if ip==max(P_I):
#                print(ix,ip)
                xp_max = ix
            
        mpl1d.ax.plot(xs-xp_max, P_I/max(P_I), '-r', lw=2,label="Measured Intensity")
        
        mpl1d.ax.legend()
        mpl1d.draw()

    @pyqtSlot("int")
    def on_slider_lambda_valueChanged(self, value):
        self.SpinBox_lambda.setValue(value)
        self.fig1()

    @pyqtSlot("int")
    def on_slider_b_valueChanged(self, value):
        self.SpinBox_b.setValue(value)
        self.fig1()

    @pyqtSlot("int")
    def on_slider_db_valueChanged(self, value):
        self.SpinBox_db.setValue(value)
        self.fig1()

    @pyqtSlot("int")
    def on_slider_a_valueChanged(self, value):
        self.SpinBox_a.setValue(value/1000)
        self.fig1()

    @pyqtSlot("int")
    def on_slider_D_valueChanged(self, value):
        self.SpinBox_D.setValue(value/10)
        self.fig1()

    @pyqtSlot("int")
    def on_SpinBox_lambda_valueChanged(self, value):
        self.slider_lambda.setValue(value)

    @pyqtSlot("double")
    def on_SpinBox_b_valueChanged(self, value):
        self.slider_b.setValue(value)
        self.fig1()

    @pyqtSlot("double")
    def on_SpinBox_db_valueChanged(self, value):
        self.slider_db.setValue(value)

    @pyqtSlot("double")
    def on_SpinBox_a_valueChanged(self, value):
        self.slider_a.setValue(value*1000)
        self.fig1()


    @pyqtSlot("double")
    def on_SpinBox_D_valueChanged(self, value):
        self.slider_D.setValue(value*10)
        self.fig1()
    @pyqtSlot()
    def on_button_data_clicked(self):
        try:
            self.filename_p = QFileDialog.getOpenFileName(
                self,
                self.tr("Charger le profile d'intensité"),
                "profiles/",
                "")
            self.gb_sim.setEnabled(True)
            self.fig1()
            
        except:
            pass
        
    @pyqtSlot()
    def on_bt_imtool_clicked(self):
        try:
            self.imtool.show()
            self.imtool.activateWindow()
            
        except:
            pass
        
            
if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    MyApplication = DoubleSlit1D()
    MyApplication.show()

    sys.exit(app.exec_())
