# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Flood_tab.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import pandas as pd
import os
import arcpy
import data_process as dp
import predictCl as pc
from tqdm import *
import time
from dialog_signature import Ui_Dialog_Signature as Form
from dialog_progress import Transparent as Pgrs

import logging
class Ui_Dialog(QtWidgets.QWidget):
    def __init__(self):

        QtWidgets.QWidget.__init__(self)
        #self._dialog = None
        self.run = False;
        self._dialog = None
        self.roiGroupsPass = []
        self.setupUi(self)

        self.workerThread = WorkerThread()
        self.workerThread.log.connect(self.toLog)
        self.workerThread.started.connect(lambda: self.toLog('start'))
        self.workerThread.finished.connect(lambda: self.toLog('finished'))


    def toLog(self, txt):
        logging.info(txt)
        print(txt)
        if(txt == 'start'):
            self.run = True;
        else:
            self.run = False;

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(946, 823)
        self.tabWidget = QtWidgets.QTabWidget(Form)
        self.tabWidget.setGeometry(QtCore.QRect(40, 20, 871, 681))
        self.tabWidget.setObjectName("tabWidget")
        self.tab_1 = QtWidgets.QWidget()
        self.tab_1.setObjectName("tab_1")
        self.groupBox_3 = QtWidgets.QGroupBox(self.tab_1)
        self.groupBox_3.setGeometry(QtCore.QRect(30, 20, 771, 341))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.groupBox_3.setFont(font)
        self.groupBox_3.setObjectName("groupBox_3")
        self.pushButton_preFlood = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton_preFlood.setGeometry(QtCore.QRect(420, 50, 93, 28))
        self.pushButton_preFlood.setObjectName("pushButton_preFlood")
        self.pushButton_postFlood = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton_postFlood.setGeometry(QtCore.QRect(420, 120, 93, 28))
        self.pushButton_postFlood.setObjectName("pushButton_postFlood")
        self.textEdit_3 = QtWidgets.QTextEdit(self.groupBox_3)
        self.textEdit_3.setGeometry(QtCore.QRect(-200, 230, 104, 87))
        self.textEdit_3.setObjectName("textEdit_3")
        self.textEdit_preFlood = QtWidgets.QTextEdit(self.groupBox_3)
        self.textEdit_preFlood.setGeometry(QtCore.QRect(10, 50, 401, 41))
        self.textEdit_preFlood.setObjectName("textEdit_preFlood")
        self.textEdit_postFlood = QtWidgets.QTextEdit(self.groupBox_3)
        self.textEdit_postFlood.setGeometry(QtCore.QRect(10, 120, 401, 41))
        self.textEdit_postFlood.setObjectName("textEdit_postFlood")
        self.textEdit_outputProcess = QtWidgets.QTextEdit(self.groupBox_3)
        self.textEdit_outputProcess.setGeometry(QtCore.QRect(10, 260, 401, 41))
        self.textEdit_outputProcess.setObjectName("textEdit_outputProcess")
        self.comboBox_landsatType = QtWidgets.QComboBox(self.groupBox_3)
        self.comboBox_landsatType.setGeometry(QtCore.QRect(560, 50, 111, 41))
        self.comboBox_landsatType.setObjectName("comboBox_landsatType")
        self.comboBox_landsatType.addItem("")
        self.comboBox_landsatType.addItem("")
        self.label_landsatType = QtWidgets.QLabel(self.groupBox_3)
        self.label_landsatType.setGeometry(QtCore.QRect(560, 30, 111, 16))
        self.label_landsatType.setObjectName("label_landsatType")
        self.textEdit_shapefile = QtWidgets.QTextEdit(self.groupBox_3)
        self.textEdit_shapefile.setGeometry(QtCore.QRect(10, 190, 401, 41))
        self.textEdit_shapefile.setObjectName("textEdit_shapefile")
        self.pushButton_shapefile = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton_shapefile.setGeometry(QtCore.QRect(420, 190, 93, 28))
        self.pushButton_shapefile.setObjectName("pushButton_shapefile")
        self.label_3 = QtWidgets.QLabel(self.groupBox_3)
        self.label_3.setGeometry(QtCore.QRect(10, 30, 401, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.groupBox_3)
        self.label_4.setGeometry(QtCore.QRect(10, 96, 401, 20))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.groupBox_3)
        self.label_5.setGeometry(QtCore.QRect(10, 165, 401, 21))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.groupBox_3)
        self.label_6.setGeometry(QtCore.QRect(10, 240, 401, 16))
        self.label_6.setObjectName("label_6")
        self.pushButton_awal = QtWidgets.QPushButton(self.tab_1)
        self.pushButton_awal.setGeometry(QtCore.QRect(612, 557, 101, 41))
        self.pushButton_awal.setObjectName("pushButton_awal")
        self.groupBox_5 = QtWidgets.QGroupBox(self.tab_1)
        self.groupBox_5.setGeometry(QtCore.QRect(40, 380, 311, 251))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.groupBox_5.setFont(font)
        self.groupBox_5.setObjectName("groupBox_5")
        self.label_maskType = QtWidgets.QLabel(self.groupBox_5)
        self.label_maskType.setGeometry(QtCore.QRect(30, 50, 201, 21))
        self.label_maskType.setObjectName("label_maskType")
        self.comboBox_maskType = QtWidgets.QComboBox(self.groupBox_5)
        self.comboBox_maskType.setGeometry(QtCore.QRect(30, 80, 191, 31))
        self.comboBox_maskType.setObjectName("comboBox_maskType")
        self.comboBox_maskType.addItem("")
        self.comboBox_maskType.addItem("")
        self.comboBox_maskType.addItem("")
        self.comboBox_maskType.addItem("")
        self.comboBox_maskType.addItem("")
        self.label_confidence = QtWidgets.QLabel(self.groupBox_5)
        self.label_confidence.setGeometry(QtCore.QRect(30, 150, 201, 21))
        self.label_confidence.setObjectName("label_confidence")
        self.comboBox_confidence = QtWidgets.QComboBox(self.groupBox_5)
        self.comboBox_confidence.setGeometry(QtCore.QRect(30, 180, 191, 31))
        self.comboBox_confidence.setObjectName("comboBox_confidence")
        self.comboBox_confidence.addItem("")
        self.comboBox_confidence.addItem("")
        self.comboBox_confidence.addItem("")
        self.comboBox_confidence.addItem("")
        self.tabWidget.addTab(self.tab_1, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.groupBox = QtWidgets.QGroupBox(self.tab_2)
        self.groupBox.setGeometry(QtCore.QRect(60, 40, 751, 551))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")
        self.comboBox_defaultThreshold = QtWidgets.QComboBox(self.groupBox)
        self.comboBox_defaultThreshold.setGeometry(QtCore.QRect(30, 170, 201, 31))
        self.comboBox_defaultThreshold.setObjectName("comboBox_defaultThreshold")
        self.comboBox_defaultThreshold.addItem("")
        self.comboBox_defaultThreshold.addItem("")
        self.checkBox_defaultThreshold = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_defaultThreshold.setGeometry(QtCore.QRect(30, 130, 381, 31))
        self.checkBox_defaultThreshold.setObjectName("checkBox_defaultThreshold")
        self.checkBox_defineThreshold = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_defineThreshold.setGeometry(QtCore.QRect(30, 260, 381, 31))
        self.checkBox_defineThreshold.setObjectName("checkBox_defineThreshold")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(30, 340, 101, 20))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(30, 390, 131, 20))
        self.label_2.setObjectName("label_2")
        self.textEdit_defineDeltaNDWI = QtWidgets.QTextEdit(self.groupBox)
        self.textEdit_defineDeltaNDWI.setGeometry(QtCore.QRect(190, 340, 111, 31))
        self.textEdit_defineDeltaNDWI.setObjectName("textEdit_defineDeltaNDWI")
        self.textEdit_definePostNDWI = QtWidgets.QTextEdit(self.groupBox)
        self.textEdit_definePostNDWI.setGeometry(QtCore.QRect(190, 380, 111, 31))
        self.textEdit_definePostNDWI.setObjectName("textEdit_definePostNDWI")
        self.checkBox_trainingSample = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_trainingSample.setGeometry(QtCore.QRect(30, 460, 401, 20))
        self.checkBox_trainingSample.setObjectName("checkBox_trainingSample")
        self.label_detailDefault = QtWidgets.QLabel(self.groupBox)
        self.label_detailDefault.setGeometry(QtCore.QRect(30, 200, 631, 51))
        self.label_detailDefault.setObjectName("label_detailDefault")
        self.textEdit_folderPreprocess = QtWidgets.QTextEdit(self.groupBox)
        self.textEdit_folderPreprocess.setGeometry(QtCore.QRect(30, 60, 401, 51))
        self.textEdit_folderPreprocess.setObjectName("textEdit_folderPreprocess")
        self.pushButton_folderPreprocess = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_folderPreprocess.setGeometry(QtCore.QRect(450, 60, 93, 41))
        self.pushButton_folderPreprocess.setObjectName("pushButton_folderPreprocess")
        self.label_folderPreprocess = QtWidgets.QLabel(self.groupBox)
        self.label_folderPreprocess.setGeometry(QtCore.QRect(30, 25, 401, 31))
        self.label_folderPreprocess.setObjectName("label_folderPreprocess")
        self.label_14 = QtWidgets.QLabel(self.groupBox)
        self.label_14.setGeometry(QtCore.QRect(310, 350, 151, 16))
        self.label_14.setObjectName("label_14")
        self.label_15 = QtWidgets.QLabel(self.groupBox)
        self.label_15.setGeometry(QtCore.QRect(310, 390, 151, 16))
        self.label_15.setObjectName("label_15")
        self.pushButton_lanjut = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_lanjut.setGeometry(QtCore.QRect(350, 590, 111, 41))
        self.pushButton_lanjut.setObjectName("pushButton_lanjut")
        self.tabWidget.addTab(self.tab_2, "")

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(Form)


        self.checkBox_defaultThreshold.setChecked (True)
        self.checkBox_defineThreshold.setEnabled (False)
        self.checkBox_trainingSample.setEnabled (False)
        self.comboBox_defaultThreshold.setDisabled (False)

        self.label.setEnabled (False)
        self.label_2.setEnabled (False)
        self.textEdit_defineDeltaNDWI.setEnabled (False)
        self.textEdit_definePostNDWI.setEnabled (False)

        self.checkBox_defaultThreshold.toggled.connect(self.checkbox_toggled_default)
        self.checkBox_defineThreshold.toggled.connect(self.checkbox_toggled_define)
        self.checkBox_trainingSample.toggled.connect(self.checkbox_toggled_training)
        
    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Deteksi Banjir"))
        self.tab_1.setToolTip(_translate("Form", "<html><head/><body><p>Pengolahan awal</p></body></html>"))
        self.groupBox_3.setTitle(_translate("Form", "Data directory"))
        self.pushButton_preFlood.setText(_translate("Form", "Browse"))
        self.pushButton_postFlood.setText(_translate("Form", "Browse"))
        self.textEdit_preFlood.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:7.8pt; color:#838383;\">directoryPreFlood</span></p></body></html>"))
        self.textEdit_postFlood.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:7.8pt; color:#838383;\">directoryPostFlood</span></p></body></html>"))
        self.textEdit_outputProcess.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:7.8pt; color:#838383;\">outputDirectory</span></p></body></html>"))
        self.comboBox_landsatType.setItemText(0, _translate("Form", "Landsat8"))
        self.comboBox_landsatType.setItemText(1, _translate("Form", "Landsat7"))
        self.label_landsatType.setText(_translate("Form", "Jenis Data"))
        self.textEdit_shapefile.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:7.8pt; color:#838383;\">projectedShapefile</span></p></body></html>"))
        self.pushButton_shapefile.setText(_translate("Form", "Browse"))
        self.label_3.setText(_translate("Form", "Folder data sebelum banjir (Scene code)"))
        self.label_4.setText(_translate("Form", "Folder data saat banjir (Scene code) "))
        self.label_5.setText(_translate("Form", "Shapefile yang terprojeksi (.shp)"))
        self.label_6.setText(_translate("Form", "Folder keluaran hasil praproses"))
        self.pushButton_awal.setText(_translate("Form", "Proses Data"))
        self.groupBox_5.setTitle(_translate("Form", "Cloud Mask"))
        self.label_maskType.setText(_translate("Form", "Tipe masking"))
        self.comboBox_maskType.setItemText(0, _translate("Form", "Cloud"))
        self.comboBox_maskType.setItemText(1, _translate("Form", "Cirrus"))
        self.comboBox_maskType.setItemText(2, _translate("Form", "Snow"))
        self.comboBox_maskType.setItemText(3, _translate("Form", "Vegetation"))
        self.comboBox_maskType.setItemText(4, _translate("Form", "Water"))
        self.label_confidence.setText(_translate("Form", "Nilai Confidence"))
        self.comboBox_confidence.setItemText(0, _translate("Form", "High"))
        self.comboBox_confidence.setItemText(1, _translate("Form", "Medium"))
        self.comboBox_confidence.setItemText(2, _translate("Form", "Low"))
        self.comboBox_confidence.setItemText(3, _translate("Form", "None"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_1), _translate("Form", "Pengolahan awal"))
        self.tab_2.setToolTip(_translate("Form", "<html><head/><body><p>Pengolahan lanjut</p></body></html>"))
        self.groupBox.setTitle(_translate("Form", "Threshold"))
        self.comboBox_defaultThreshold.setItemText(0, _translate("Form", "Gao (1996)"))
        self.comboBox_defaultThreshold.setItemText(1, _translate("Form", "McFeeters (1996)"))
        self.checkBox_defaultThreshold.setText(_translate("Form", "Default dari referensi jurnal"))
        self.checkBox_defineThreshold.setText(_translate("Form", "Tentukan sendiri nilai threshold"))
        self.label.setText(_translate("Form", "Delta NDWI"))
        self.label_2.setText(_translate("Form", "NDWI during flood"))
        self.textEdit_defineDeltaNDWI.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#7a7a7a;\">&gt;=value</span></p></body></html>"))
        self.textEdit_definePostNDWI.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#7a7a7a;\">&gt;=value</span></p></body></html>"))
        self.checkBox_trainingSample.setText(_translate("Form", "Buat training sampel dari ArcMap"))
        self.label_detailDefault.setText(_translate("Form", "Keterangan: deltaNDWI >= 0.094 ; duringNDWI >= 0.161"))
        self.textEdit_folderPreprocess.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#7a7a7a;\">preprocessFolder</span></p></body></html>"))
        self.pushButton_folderPreprocess.setText(_translate("Form", "Browse"))
        self.label_folderPreprocess.setText(_translate("Form", "Folder hasil praproses ([sceneCode]_OutputTools)"))
        self.label_14.setText(_translate("Form", "(.) decimal separated"))
        self.label_15.setText(_translate("Form", "(.) decimal separated"))
        self.pushButton_lanjut.setText(_translate("Form", "Proses data"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Form", "Pengolahan lanjut"))

        self.pushButton_preFlood.clicked.connect(self.openPreFlood)
        self.pushButton_postFlood.clicked.connect(self.openPostFlood)
        self.pushButton_shapefile.clicked.connect(self.openShapeFile)
        self.pushButton_folderPreprocess.clicked.connect(self.openFolderPreprocess)
        self.pushButton_awal.clicked.connect(self.executeCodeAwal)
        self.pushButton_lanjut.clicked.connect(self.executeCodeLanjut)
        self.comboBox_defaultThreshold.currentIndexChanged.connect(self.comboBox_toggled)

    def comboBox_toggled(self):
        if (self.comboBox_defaultThreshold.currentText() == "Gao (1996)"):
            self.label_detailDefault.setText("Keterangan : deltaNDWI >= 0.228 ; duringNDWI >= 0.548")

        else:
            self.label_detailDefault.setText("Keterangan : deltaNDWI >= 0.094 ; duringNDWI >= 0.161")
    def checkbox_toggled_default(self):
        if (self.checkBox_defaultThreshold.isChecked() == True):
            self.checkBox_defineThreshold.setEnabled (False)
            self.label.setEnabled (False)
            self.label_2.setEnabled (False)
            self.label_detailDefault.setEnabled (True)
            self.checkBox_trainingSample.setEnabled (False)
            self.comboBox_defaultThreshold.setEnabled (True)

        else:
            self.checkBox_defineThreshold.setEnabled (True)
            self.checkBox_trainingSample.setEnabled (True)
            self.checkBox_trainingSample.setEnabled (True)
            self.label.setEnabled (False)
            self.label_2.setEnabled (False)
            self.label_detailDefault.setEnabled (False)
            self.comboBox_defaultThreshold.setEnabled (False)

    def checkbox_toggled_define(self):
        if (self.checkBox_defineThreshold.isChecked() == True):
            self.checkBox_defaultThreshold.setEnabled (False)
            self.checkBox_trainingSample.setEnabled (False)
            self.textEdit_defineDeltaNDWI.setEnabled (True)
            self.textEdit_definePostNDWI.setEnabled (True)
            self.label.setEnabled (True)
            self.label_2.setEnabled (True)
            self.label_detailDefault.setEnabled (False)

        else:
            self.checkBox_defaultThreshold.setEnabled (True)
            self.checkBox_trainingSample.setEnabled (True)
            self.textEdit_defineDeltaNDWI.setEnabled (False)
            self.textEdit_definePostNDWI.setEnabled (False)

            self.label.setEnabled (False)
            self.label_2.setEnabled (False)
            self.label_detailDefault.setEnabled (False)


    def checkbox_toggled_training(self):
        if (self.checkBox_trainingSample.isChecked() == True):
            self.checkBox_defaultThreshold.setEnabled (False)
            self.checkBox_defineThreshold.setEnabled (False)
            self.textEdit_defineDeltaNDWI.setEnabled (False)
            self.textEdit_definePostNDWI.setEnabled (False)
            self.comboBox_defaultThreshold.setEnabled (False)

            self.label.setEnabled (False)
            self.label_2.setEnabled (False)
            self.label_detailDefault.setEnabled (False)
        else:
            self.checkBox_defaultThreshold.setEnabled (True)
            self.checkBox_defineThreshold.setEnabled (True)

            self.label.setEnabled (False)
            self.label_2.setEnabled (False)
            self.label_detailDefault.setEnabled (False)



    def openPreFlood(self):
        fileName = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select directory')
        self.textEdit_preFlood.setText(fileName)

        if(os.path.isdir(fileName+'_OutputTools')):
            print "exists"
            #os.chdir
            #os.system('rmdir /s /q pic')
            self.showBox("Error", "Folder keluaran sudah ada, silahkan ganti nama folder yang akan digunakan", "")
            self.textEdit_outputProcess.setText(fileName+'_OutputTools')
        else:
            self.textEdit_outputProcess.setText(fileName+'_OutputTools')
        #print(fileName)

    def openPostFlood(self):
        fileName = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select directory')
        self.textEdit_postFlood.setText(fileName)
        #print(fileName)

    def openShapeFile(self):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file')
        self.textEdit_shapefile.setText(fileName)
        #print(fileName)

    def openFolderPreprocess(self):
        fileName = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select directory')
        self.textEdit_folderPreprocess.setText(fileName)

    def msgbtn(self):
        print "Button pressed is:"

    def showCircleProgress(self):
        dialogProgress = Pgrs()
        dialogProgress.exec_()

    def handleOpenDialog(self):
        if self._dialog is None:
            self._dialog = QDialog(self)
            button = QPushButton('PyQt5', self._dialog)
            self._dialog.resize(200, 100)
            self._dialog.setModal(False)
        self._dialog.show()
        self._dialog.exec_()

    def showBox(self, text, info, title):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)

        msg.setText(text)
        msg.setInformativeText(info)
        msg.setWindowTitle(title)
        msg.setDetailedText("The details are as follows:")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.buttonClicked.connect(self.msgbtn)

        retval = msg.exec_()
        print "value of pressed message box button:", retval

    def showChooseSignature(self):

        #dialog = QtWidgets.QDialog()
        dialog = Form()
        #dialog.ui.setupUi(dialog)
        dialog.exec_()
        #dialog.show()

        print(dialog.roiGroups)
        self.roiGroupsPass.append(dialog.roiGroups[0])

    def executeCodeLanjut(self):
        if (self.checkBox_defaultThreshold.isChecked() == False and self.checkBox_defineThreshold.isChecked() == False and 
            self.checkBox_trainingSample.isChecked() == False):
            self.showBox("Something wrong", "Silahkan pilih salah satu threshold yang digunakan", "Error")
        else:
            self.showBox("Processing data", "Silahkan tunggu sampai semua proses selesai, program akan berjalan setelah kamu menekan tombol Ok",
            "Mulai...")

            #self.handleOpenDialog()
            out_process = self.textEdit_folderPreprocess.toPlainText()
            msgRun = QMessageBox(self)

            msgRun.setAttribute(Qt.WA_DeleteOnClose)
            msgRun.setWindowFlags(QtCore.Qt.FramelessWindowHint)
            msgRun.setIcon(QMessageBox.Warning)
            msgRun.setBaseSize(QSize(1000, 500))

            msgRun.setText("Please wait, Its better to keep this dialog open")
            msgRun.setWindowTitle("Running")
            msgRun.setStandardButtons(QMessageBox.Ignore)
            msgRun.setWindowModality(Qt.NonModal);
            QCoreApplication.processEvents()
            msgRun.show()
            QCoreApplication.processEvents()
            dat = pd.read_csv(out_process+"/list.csv")
            pre_flood = dat["colummn"][0]
            post_flood = dat["colummn"][1]

            if(self.checkBox_defaultThreshold.isChecked() == True):

                print("Default Threshold")
                if(self.comboBox_defaultThreshold.currentText() == "Gao (1996)"):
                    print("Gao")
                    deltaNDWI = "0.094"
                    NDWIduring = "0.161"
                else:
                    print("McFeeter")
                    deltaNDWI = "0.228"
                    NDWIduring = "0.548"
            else:

                print("Define Threshold")
                deltaNDWI = self.textEdit_defineDeltaNDWI.toPlainText()
                NDWIduring = self.textEdit_definePostNDWI.toPlainText()
                print(deltaNDWI)
                print(NDWIduring)


            if(self.checkBox_trainingSample.isChecked() == True):
                for i in tqdm(range(1000)):
                    for j in tqdm(range(100)):
                        count = 0
                        count = count+1
                
                self.showChooseSignature()
                print "yuk hitung dengan"
                print self.roiGroupsPass[0]

                dp.sampleClassification(out_process, os.path.basename(post_flood), os.path.normpath(self.roiGroupsPass[0]))
                dp.maskOutFinal(out_process, pre_flood)
                dp.final_spatial_filter(out_process, pre_flood)
                for i in tqdm(range(1000)):
                    for j in tqdm(range(100)):
                        count = 0
                        count = count+1

                msgRun.close()
                self.showBox("finished", "Kamu dapat menutup program ini sekarang", "Selesai...")
            else:

                dp.diffNDWI(out_process, os.path.basename(pre_flood), os.path.basename(post_flood))
                dp.pixelExtraction(out_process, os.path.basename(pre_flood), os.path.basename(post_flood), deltaNDWI, NDWIduring)
                dp.maskOutFinal(out_process, pre_flood)
                dp.final_spatial_filter(out_process, pre_flood)
                dp.rasterToVector(out_process)
                dp.layerToKml(out_process)
                #pc.predictClass(post_flood, r"C:\Prog\EditInterface_thread\DataTest_decisionTree.pkl", out_process)

                for i in tqdm(range(1000)):
                    for j in tqdm(range(100)):
                        count = 0
                        count = count+1

                msgRun.close()
                self.showBox("finished", "Kamu dapat menutup program ini sekarang", "Selesai...")

        return

    def executeCodeAwal(self):
        if (os.path.exists(self.textEdit_preFlood.toPlainText()) == False):
            self.showBox("Something wrong", "PreFlood(Data Sebelum Banjir) masih belum diisi atau path salah", "Error")
        elif (os.path.exists(self.textEdit_postFlood.toPlainText()) == False):
            self.showBox("Something wrong", "PostFlood(Data Setelah Banjir) masih belum diisi atau path salah", "Error")
        elif (os.path.exists(self.textEdit_shapefile.toPlainText()) == False):
            self.showBox("Something wrong", "Shapefile yang terprojeksi masih belum diisi atau path salah", "Error")

        else:
            self.showBox("Processing data", "Silahkan tunggu sampai semua proses selesai, program akan berjalan setelah kamu menekan tombol Ok",
            "Mulai...")

            #self.handleOpenDialog()

            msgRun = QMessageBox(self)

            msgRun.setAttribute(Qt.WA_DeleteOnClose)
            msgRun.setWindowFlags(QtCore.Qt.FramelessWindowHint)
            msgRun.setIcon(QMessageBox.Warning)
            msgRun.setBaseSize(QSize(1000, 500))

            msgRun.setText("Please wait, Its better to keep this dialog open")
            msgRun.setWindowTitle("Running")
            msgRun.setStandardButtons(QMessageBox.Ignore)
            msgRun.setWindowModality(Qt.NonModal);
            QCoreApplication.processEvents()
            msgRun.show()
            QCoreApplication.processEvents()


            ####################################################################################
            data_type = self.comboBox_landsatType.currentText()

            pre_flood = self.textEdit_preFlood.toPlainText()
            post_flood = self.textEdit_postFlood.toPlainText()
            out_process = self.textEdit_outputProcess.toPlainText()
            
            inFC = self.textEdit_shapefile.toPlainText()

            # pre_flood = os.path.normpath(pre_flood)
            # post_flood = os.path.normpath(post_flood)
            # out_process = os.path.normpath(out_process)
            # inFC = os.path.normpath(inFC)

            SR = arcpy.Describe(inFC).spatialReference
            print(data_type)
            print(pre_flood)
            print(post_flood)
            print(out_process)

            masktype = self.comboBox_maskType.currentText()
            confidence = self.comboBox_confidence.currentText()
            cummulative = 'false'

            print(masktype)
            print(confidence)

            deltaNDWI = '0.11'
            NDWIduring = '0.11'
            items = [data_type, pre_flood, post_flood, out_process, SR, deltaNDWI, NDWIduring, masktype, confidence, cummulative]

            # self.workerThread.setItems(items)
            # self.workerThread.start()

            os.mkdir(out_process)
            some_list = [pre_flood, post_flood]
            df = pd.DataFrame(some_list, columns=["colummn"])
            df.to_csv(out_process+'/list.csv', index=False)
            dp.mask_cloud(pre_flood, masktype, confidence, cummulative, out_process)
            dp.mask_cloud(post_flood, masktype, confidence, cummulative, out_process)
            dp.process_landsat(pre_flood, SR, out_process, "_PreFlood", data_type, "")
            dp.process_landsat(post_flood, SR, out_process, "_PostFlood", data_type, "")
            #self.showCircleProgress()
            msgRun.close()
            self.showBox("finished", "Kamu dapat menutup program ini sekarang", "Selesai...")
        return

class WorkerThread(QThread):
    log = pyqtSignal(str)
    def __init__(self, parent=None):
        super(WorkerThread, self).__init__(parent)
        self._items = []

    def setItems(self, items):
        if not self.isRunning():
            self._items[:] = items

    def run(self):
        # dialog = Pgrs()
        # dialog.exec_()
        for i in tqdm(range(1000)):
            for j in tqdm(range(100)):
                count = 0
                count = count+1

        #dialog.close()
        data_type= self._items[0]
        pre_flood= self._items[1]
        post_flood= self._items[2]
        out_process= self._items[3]

        pre_flood = os.path.normpath(pre_flood)
        post_flood = os.path.normpath(post_flood)
        out_process = os.path.normpath(out_process)
        #inFC = os.path.normpath(inFC)
        SR = self._items[4]

        deltaNDWI = self._items[5] 
        NDWIduring = self._items[6]
        masktype = self._items[7] 
        confidence = self._items[8] 
        cummulative = self._items[9] 

        print data_type
        print pre_flood
        print post_flood
        print out_process
        print SR
        print deltaNDWI
        print NDWIduring
        print masktype
        print confidence
        print cummulative

        os.mkdir(out_process)
        some_list = [pre_flood, post_flood]
        df = pd.DataFrame(some_list, columns=["colummn"])
        df.to_csv(out_process+'/list.csv', index=False)
        dp.mask_cloud(pre_flood, masktype, confidence, cummulative, out_process)
        # dp.mask_cloud(post_flood, masktype, confidence, cummulative, out_process)
        # dp.process_landsat(pre_flood, SR, out_process, "_PreFlood", data_type, "")
        # dp.process_landsat(post_flood, SR, out_process, "_PostFlood", data_type, "")

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = Ui_Dialog()
    ex.show()
    sys.exit(app.exec_())