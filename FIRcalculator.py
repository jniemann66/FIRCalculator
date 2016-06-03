# -*- coding: utf-8 -*-
"""
Created on Mon May 30 00:47:42 2016

@author: Judd Niemann
"""

import sys
import numpy as np

# import the signal processing library:
from scipy import signal
from PyQt4 import QtGui
#from PyQt4 import QtCore
#from PyQt4 import Qt  

from FIRDesigner import Ui_MainWindow as mw 

class MainWindow(QtGui.QMainWindow, mw): 
    def __init__(self): 
        QtGui.QMainWindow.__init__(self)
        self.setupUi(self)
        self.setupSignals()
        self.onBandsSpinBoxChanged() #show/hide bands
        self.setupPlots()
        
        #start with a lowpass filter:
        self.onActionLowpassTriggered()
    
    def setupPlots(self):
        self.fig1 = self.impulseMatplotlibwidget.figure
        self.impulseAx = self.fig1.add_subplot(111)
        self.impulseAx.hold(False)
        self.fig2 = self.freqResponseMatplotlibwidget.figure
        self.freqAx = self.fig2.add_subplot(111)
        
    def setupSignals(self):
        self.calculatePushButton.clicked.connect(self.onCalculateButtonClicked)
        self.bandsSpinBox.valueChanged.connect(self.onBandsSpinBoxChanged)
        
        # signals for Menu actions:
        self.actionLowpass.triggered.connect(self.onActionLowpassTriggered)
        self.actionHighpass.triggered.connect(self.onActionHighpassTriggered)
        self.actionBandpass.triggered.connect(self.onActionBandpassTriggered)
        self.actionBandreject.triggered.connect(self.onActionBandrejectTriggered)
        self.action4_band.triggered.connect(self.onAction4bandTriggered)
        
        # signals for band1:
        self.bandStartHorizontalSlider.sliderMoved.connect(self.onBandStartHorizontalSliderMoved)
        self.bandEndHorizontalSlider.sliderMoved.connect(self.onBandEndHorizontalSliderMoved)
        self.bandLevelVerticalSlider.sliderMoved.connect(self.onBandLevelVerticalSliderMoved)
        self.bandStart.valueChanged.connect(self.onBandStartValueChanged)
        self.bandEnd.valueChanged.connect(self.onBandEndValueChanged)
        self.bandLevel.valueChanged.connect(self.onBandLevelValueChanged)
        
        # signals for band2:
        self.bandStartHorizontalSlider_2.sliderMoved.connect(self.onBandStartHorizontalSlider_2Moved)
        self.bandEndHorizontalSlider_2.sliderMoved.connect(self.onBandEndHorizontalSlider_2Moved)
        self.bandLevelVerticalSlider_2.sliderMoved.connect(self.onBandLevelVerticalSlider_2Moved)
        self.bandStart_2.valueChanged.connect(self.onBandStartValue_2Changed)
        self.bandEnd_2.valueChanged.connect(self.onBandEndValue_2Changed)
        self.bandLevel_2.valueChanged.connect(self.onBandLevelValue_2Changed)
        
        # signals for band3:
        self.bandStartHorizontalSlider_3.sliderMoved.connect(self.onBandStartHorizontalSlider_3Moved)
        self.bandEndHorizontalSlider_3.sliderMoved.connect(self.onBandEndHorizontalSlider_3Moved)
        self.bandLevelVerticalSlider_3.sliderMoved.connect(self.onBandLevelVerticalSlider_3Moved)
        self.bandStart_3.valueChanged.connect(self.onBandStartValue_3Changed)
        self.bandEnd_3.valueChanged.connect(self.onBandEndValue_3Changed)
        self.bandLevel_3.valueChanged.connect(self.onBandLevelValue_3Changed)
	
         # signals for band4:
        self.bandStartHorizontalSlider_4.sliderMoved.connect(self.onBandStartHorizontalSlider_4Moved)
        self.bandEndHorizontalSlider_4.sliderMoved.connect(self.onBandEndHorizontalSlider_4Moved)
        self.bandLevelVerticalSlider_4.sliderMoved.connect(self.onBandLevelVerticalSlider_4Moved)
        self.bandStart_4.valueChanged.connect(self.onBandStartValue_4Changed)
        self.bandEnd_4.valueChanged.connect(self.onBandEndValue_4Changed)
        self.bandLevel_4.valueChanged.connect(self.onBandLevelValue_4Changed)                                 
        
    def onCalculateButtonClicked(self):
        
        #prepare parameters for remez() ... using short variable names
        taps=self.tapsSpinBox.value()
        s1=self.bandStart.value()
        e1=self.bandEnd.value()
        s2=self.bandStart_2.value()
        e2=self.bandEnd_2.value()
        s3=self.bandStart_3.value()
        e3=self.bandEnd_3.value()
        s4=self.bandStart_4.value()
        e4=self.bandEnd_4.value()
        v1=self.bandLevel.value()
        v2=self.bandLevel_2.value()
        v3=self.bandLevel_3.value()
        v4=self.bandLevel_4.value()
        bands=self.bandsSpinBox.value()
        i=self.iterationsSpinBox.value()
        
        try:
            if bands==2:
                filt = signal.remez(taps,[s1,e1,s2,e2],[v1,v2],[1,1],1,'bandpass',i)
            if bands==3:
                filt = signal.remez(taps,[s1,e1,s2,e2,s3,e3],[v1,v2,v3],[1,1,1],1,'bandpass',i)
            if bands==4:
                filt = signal.remez(taps,[s1,e1,s2,e2,s3,e3,s4,e4],[v1,v2,v3,v4],[1,1,1,1],1,'bandpass',i)   
        
        except ValueError:
            self.coeffsTextBrowser.setText('Failed to converge')
            self.coeffsTextBrowser.update()
            return
        
        if self.minPhaseRadioButton.isChecked():
            fftsize = 8192 # needs to be fairly generous for good results !
            maxphaseFilter=np.real(np.fft.ifft(np.exp(signal.hilbert(np.real(np.log(np.fft.fft(filt,fftsize)))))))
            minphaseFilter=maxphaseFilter[::-1] # reverse
            finalFilt=minphaseFilter[0:self.tapsSpinBox.value()-1]
        else:
            finalFilt=filt
            
        #print filter coefficients:
        txt =""" // FIR coefficients:\n"""
        for x in finalFilt:
            txt += '\n{:.15f},'.format(x)
        txt=txt[0:len(txt)-1] #chop off last comma
        self.coeffsTextBrowser.setText(txt)
        
        #plot impulse response:        
        self.impulseMatplotlibwidget.get_renderer().clear()
        self.impulseAx.plot(finalFilt,'g-')
        self.impulseAx.grid()
        self.impulseAx.draw(self.impulseMatplotlibwidget.get_renderer())
        self.impulseMatplotlibwidget.update()
      
        #calculate frequency response:
        freq, response = signal.freqz(finalFilt)
        ampl = np.abs(response)
        
        #plot frequency response:
        fs=self.sampleRateDoubleSpinBox.value() if self.sampleRateDoubleSpinBox.value() > 0 else 1.0 
        self.freqResponseMatplotlibwidget.get_renderer().clear()    
        self.freqAx.plot(fs*freq/(2*np.pi), 20*np.log10(ampl), 'b-')
        self.freqAx.set_xlabel('Frequency Response')
        self.freqAx.set_ylabel('dB')
        self.freqAx.grid()
        self.freqAx.draw(self.freqResponseMatplotlibwidget.get_renderer())
        self.freqResponseMatplotlibwidget.update()
        
    def onBandsSpinBoxChanged(self):
        self.setEnabledBand1(False)
        self.setEnabledBand2(False)
        self.setEnabledBand3(False)
        self.setEnabledBand4(False)
        if self.bandsSpinBox.value() > 0:
            self.setEnabledBand1(True)
        if self.bandsSpinBox.value() > 1:
            self.setEnabledBand2(True) 
        if self.bandsSpinBox.value() > 2:
            self.setEnabledBand3(True)
        if self.bandsSpinBox.value() > 3:
            self.setEnabledBand4(True)
    
    def setEnabledBand1(self,enabled):
        self.bandStartHorizontalSlider.setVisible(enabled)
        self.bandEndHorizontalSlider.setVisible(enabled)
        self.bandLevelVerticalSlider.setVisible(enabled)
        self.bandStart.setVisible(enabled)
        self.bandEnd.setVisible(enabled)
        self.bandLevel.setVisible(enabled)
        self.band1Label.setVisible(enabled)
        
    def setEnabledBand2(self,enabled):
        self.bandStartHorizontalSlider_2.setVisible(enabled)
        self.bandEndHorizontalSlider_2.setVisible(enabled)
        self.bandLevelVerticalSlider_2.setVisible(enabled)
        self.bandStart_2.setVisible(enabled)
        self.bandEnd_2.setVisible(enabled)
        self.bandLevel_2.setVisible(enabled)
        self.band2Label.setVisible(enabled)
        
    def setEnabledBand3(self,enabled):
        self.bandStartHorizontalSlider_3.setVisible(enabled)
        self.bandEndHorizontalSlider_3.setVisible(enabled)
        self.bandLevelVerticalSlider_3.setVisible(enabled)
        self.bandStart_3.setVisible(enabled)
        self.bandEnd_3.setVisible(enabled)
        self.bandLevel_3.setVisible(enabled)
        self.band3Label.setVisible(enabled)
        
    def setEnabledBand4(self,enabled):
        self.bandStartHorizontalSlider_4.setVisible(enabled)
        self.bandEndHorizontalSlider_4.setVisible(enabled)
        self.bandLevelVerticalSlider_4.setVisible(enabled)
        self.bandStart_4.setVisible(enabled)
        self.bandEnd_4.setVisible(enabled)
        self.bandLevel_4.setVisible(enabled)
        self.band4Label.setVisible(enabled)
    
    def onActionLowpassTriggered(self):
        self.bandStart.setValue(0.0)
        self.bandEnd.setValue(0.3)
        self.bandLevel.setValue(1.0)
        
        self.bandStart_2.setValue(0.4)
        self.bandEnd_2.setValue(0.5)
        self.bandLevel_2.setValue(0.0)
        
        if self.bandsSpinBox.value() != 2:
            self.bandsSpinBox.setValue(2)
            self.onBandsSpinBoxChanged()
        self.makeBlackAll()
    
    def onActionHighpassTriggered(self):
        self.bandStart.setValue(0.0)
        self.bandEnd.setValue(0.1)
        self.bandLevel.setValue(0.0)
        
        self.bandStart_2.setValue(0.2)
        self.bandEnd_2.setValue(0.5)
        self.bandLevel_2.setValue(1.0)
        
        if self.bandsSpinBox.value() != 2:
            self.bandsSpinBox.setValue(2)
            self.onBandsSpinBoxChanged()
        self.makeBlackAll()
            
    def onActionBandpassTriggered(self):
        self.bandStart.setValue(0.0)
        self.bandEnd.setValue(0.1)
        self.bandLevel.setValue(0.0)
        
        self.bandStart_2.setValue(0.2)
        self.bandEnd_2.setValue(0.3)
        self.bandLevel_2.setValue(1.0)
        
        self.bandStart_3.setValue(0.4)
        self.bandEnd_3.setValue(0.5)
        self.bandLevel_3.setValue(0.0)
        
        if self.bandsSpinBox.value() != 3:
            self.bandsSpinBox.setValue(3)
            self.onBandsSpinBoxChanged()
        self.makeBlackAll()
    
    def onActionBandrejectTriggered(self):
        self.bandStart.setValue(0.0)
        self.bandEnd.setValue(0.1)
        self.bandLevel.setValue(1.0)
        
        self.bandStart_2.setValue(0.2)
        self.bandEnd_2.setValue(0.3)
        self.bandLevel_2.setValue(0.0)
        
        self.bandStart_3.setValue(0.4)
        self.bandEnd_3.setValue(0.5)
        self.bandLevel_3.setValue(1.0)
        
        if self.bandsSpinBox.value() != 3:
            self.bandsSpinBox.setValue(3)
            self.onBandsSpinBoxChanged()
        self.makeBlackAll()
            
    def onAction4bandTriggered(self):
        self.bandStart.setValue(0.0)
        self.bandEnd.setValue(0.1)
        self.bandLevel.setValue(1.0)
        
        self.bandStart_2.setValue(0.15)
        self.bandEnd_2.setValue(0.25)
        self.bandLevel_2.setValue(0.0)
        
        self.bandStart_3.setValue(0.3)
        self.bandEnd_3.setValue(0.35)
        self.bandLevel_3.setValue(1.0)
        
        self.bandStart_4.setValue(0.4)
        self.bandEnd_4.setValue(0.5)
        self.bandLevel_4.setValue(0.0)
        
        if self.bandsSpinBox.value() != 4:
            self.bandsSpinBox.setValue(4)
            self.onBandsSpinBoxChanged()
        self.makeBlackAll()
    
    def makeRed(self,qdsb):
        qdsb.setStyleSheet("QDoubleSpinBox {color:red}")
    
    def makeBlack(self,qdsb):
        qdsb.setStyleSheet("QDoubleSpinBox {color:black}")
    
    def makeBlackAll(self):
        self.makeBlack(self.bandStart)
        self.makeBlack(self.bandEnd)
        self.makeBlack(self.bandStart_2)
        self.makeBlack(self.bandEnd_2)
        self.makeBlack(self.bandStart_3)
        self.makeBlack(self.bandEnd_3)
        self.makeBlack(self.bandStart_4)
        self.makeBlack(self.bandEnd_4)
        
    # handlers for band 1:
    def onBandStartHorizontalSliderMoved(self):
        self.bandStart.setValue(self.bandStartHorizontalSlider.value()/100.0)
    
    def onBandEndHorizontalSliderMoved(self):
        self.bandEnd.setValue(self.bandEndHorizontalSlider.value()/100.0)
        
    def onBandLevelVerticalSliderMoved(self):
        self.bandLevel.setValue(self.bandLevelVerticalSlider.value()/100.0)
    
    def onBandStartValueChanged(self):
        self.bandStartHorizontalSlider.setValue(self.bandStart.value()*100.0)
        low = 0
        val = self.bandStart.value()
        high = self.bandEnd.value()
        if (val < low) or (val > high):
            self.makeRed(self.bandStart)
        else:
            self.makeBlack(self.bandStart)
            
    def onBandEndValueChanged(self):
        self.bandEndHorizontalSlider.setValue(self.bandEnd.value()*100.0)
        low = self.bandStart.value()
        val = self.bandEnd.value()
        high = self.bandStart_2.value()
        if (val < low) or (val > high):
            self.makeRed(self.bandEnd)
        else:
            self.makeBlack(self.bandEnd)
    
    def onBandLevelValueChanged(self):
        self.bandLevelVerticalSlider.setValue(self.bandLevel.value()*100.0)
        
     # handlers for band 2:
    def onBandStartHorizontalSlider_2Moved(self):
        self.bandStart_2.setValue(self.bandStartHorizontalSlider_2.value()/100.0)
    
    def onBandEndHorizontalSlider_2Moved(self):
        self.bandEnd_2.setValue(self.bandEndHorizontalSlider_2.value()/100.0)
        
    def onBandLevelVerticalSlider_2Moved(self):
        self.bandLevel_2.setValue(self.bandLevelVerticalSlider_2.value()/100.0)
    
    def onBandStartValue_2Changed(self):
        self.bandStartHorizontalSlider_2.setValue(self.bandStart_2.value()*100.0)
        low = self.bandEnd.value()
        val = self.bandStart_2.value()
        high = self.bandEnd_2.value()
        if (val < low) or (val > high):
            self.makeRed(self.bandStart_2)
        else:
            self.makeBlack(self.bandStart_2)
    
    def onBandEndValue_2Changed(self):
        self.bandEndHorizontalSlider_2.setValue(self.bandEnd_2.value()*100.0)
        low = self.bandStart_2.value()
        val = self.bandEnd_2.value()
        high = self.bandStart_3.value() if self.bandsSpinBox.value() > 2 else 0.5
        if (val < low) or (val > high):
            self.makeRed(self.bandEnd_2)
        else:
            self.makeBlack(self.bandEnd_2)
    
    def onBandLevelValue_2Changed(self):
        self.bandLevelVerticalSlider_2.setValue(self.bandLevel_2.value()*100.0)
     
     # handlers for band 3:
    def onBandStartHorizontalSlider_3Moved(self):
        self.bandStart_3.setValue(self.bandStartHorizontalSlider_3.value()/100.0)
    
    def onBandEndHorizontalSlider_3Moved(self):
        self.bandEnd_3.setValue(self.bandEndHorizontalSlider_3.value()/100.0)
        
    def onBandLevelVerticalSlider_3Moved(self):
        self.bandLevel_3.setValue(self.bandLevelVerticalSlider_3.value()/100.0)
    
    def onBandStartValue_3Changed(self):
        self.bandStartHorizontalSlider_3.setValue(self.bandStart_3.value()*100.0)
        low = self.bandEnd_2.value()
        val = self.bandStart_3.value()
        high = self.bandEnd_3.value()
        if (val < low) or (val > high):
            self.makeRed(self.bandStart_3)
        else:    
            self.makeBlack(self.bandStart_3)

    def onBandEndValue_3Changed(self):
        self.bandEndHorizontalSlider_3.setValue(self.bandEnd_3.value()*100.0)
        low = self.bandStart_3.value()
        val = self.bandEnd_3.value()
        high = self.bandStart_4.value() if self.bandsSpinBox.value() > 3 else 0.5
        if (val < low) or (val > high):
            self.makeRed(self.bandEnd_3)
        else:
            self.makeBlack(self.bandEnd_3)
    
    def onBandLevelValue_3Changed(self):
        self.bandLevelVerticalSlider_3.setValue(self.bandLevel_3.value()*100.0)
        
    # handlers for band 4:
    def onBandStartHorizontalSlider_4Moved(self):
        self.bandStart_4.setValue(self.bandStartHorizontalSlider_4.value()/100.0)
    
    def onBandEndHorizontalSlider_4Moved(self):
        self.bandEnd_4.setValue(self.bandEndHorizontalSlider_4.value()/100.0)
        
    def onBandLevelVerticalSlider_4Moved(self):
        self.bandLevel_4.setValue(self.bandLevelVerticalSlider_4.value()/100.0)
    
    def onBandStartValue_4Changed(self):
        self.bandStartHorizontalSlider_4.setValue(self.bandStart_4.value()*100.0)
        low = self.bandEnd_3.value()
        val = self.bandStart_4.value()
        high = self.bandEnd_4.value()
        if (val < low) or (val > high):
            self.makeRed(self.bandStart_4)
        else:    
            self.makeBlack(self.bandStart_4)
    
    def onBandEndValue_4Changed(self):
        self.bandEndHorizontalSlider_4.setValue(self.bandEnd_4.value()*100.0)
        low = self.bandStart_4.value()
        val = self.bandEnd_4.value()
        high = 0.5
        if (val < low) or (val > high):
            self.makeRed(self.bandEnd_4)
        else:
            self.makeBlack(self.bandEnd_4)
    
    def onBandLevelValue_4Changed(self):
        self.bandLevelVerticalSlider_4.setValue(self.bandLevel_4.value()*100.0) 
         
         
app = QtGui.QApplication(sys.argv) 
main = MainWindow()
main.show()
sys.exit(app.exec_())
