# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'File_LIster.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

# ==========================================================================================================================
# Program ma ułatwić życie osobom, które nie znają poleceń DOSa lub tych, które nie chcą 'babrać' sie w linię poleceń.
# Dokładnie chodzi o komendę DIR *.* /w >lista.txt,
# które zapisuje do pliku 'lista.txt' nazwy wszystkich plików z folderu, w którym aktualnie się znajdujemy. 
# W przypadku tworzenia programów do wycięcia detali na laserze ułatwia to wykonanie spisu elementów do wycięcia.
# Spis powstaje z plików zawierających rysunki poszczególnych detali.
# 
# Najczęściej używanymi formatami plików są (poza *.geo): *.dxf, *.dwg, *.pdf.
# Dodatkowo można wybrać dowolny, inny format pliku, poprzez wpisanie jego roszerzenia.
# Listę można wydrukować.
#
# Wersja 1.0 - tworzenie listy pików
# Wersja 1.1 - dodano drukowanie listy
# Wersja 1.2 - dodano automatyczne zapisywanie pliku lista.txt w listowanym katalogu 
# ==========================================================================================================================
# The program is to make life easier for people who don't know DOS commands or those who don't want to mess with the command line.
# Exactly the DIR command *. * / W> list.txt,
# which saves to the file 'list.txt' the names of all files from the current folder.
# In the case of creating programs for cutting details on the laser, it facilitates the preparation of a list of elements to be cut.
# The list is created from files containing drawings of individual details.
#
# The most commonly used file formats are (except *.geo): * .dxf, * .dwg, * .pdf.
# Additionally, you can choose any other file format by entering its extension.
# The list can be printed.
#
# Version 1.0 - creating a list of peaks
# Version 1.1 - added list printing
# Version 1.2 - added automatic saving of the list.txt file in the directory listed
# ==========================================================================================================================

import sys
import os
import fnmatch
from pathlib import Path
from PyQt5 import QtCore, QtGui, QtWidgets, QtPrintSupport
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog, QRadioButton, QGroupBox

# zdefiniowanie domyśłnych wartości
global file_type                # deklaracje zmiennej globalnej, aby była widoczna we wszystkich metodach
file_type = 'jpg'                 # definicja zmennej domyśłnej, która jest u zywana, gdy nie wybrano żadnej z opcji przy pomocy przycisków typu radio


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(860, 550)
        font = QtGui.QFont()
        font.setPointSize(10)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        path = os.path.dirname(__file__)
        MainWindow.setWindowIcon(QtGui.QIcon(path+"\QF_bold.bmp"))
     
    #===================================================================================
    #======================= widżety GUI ===============================================
    #===================================================================================
        self.btn_Open_Folder = QtWidgets.QPushButton(self.centralwidget)
        self.btn_Open_Folder.setGeometry(QtCore.QRect(20, 20, 151, 28))
        self.btn_Open_Folder.setObjectName("btn_Open_Folder")

        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 50, 171, 171))
        self.groupBox.setObjectName("groupBox")
        #======================= RADIO BUTTONS =========================================
        self.radio_btn_DXF = QtWidgets.QRadioButton(self.groupBox)
        self.radio_btn_DXF.setGeometry(QtCore.QRect(10, 30, 95, 21))
        self.radio_btn_DXF.setObjectName("radio_btn_DXF")
        #self.radio_btn_DXF.setChecked(True)
        self.radio_btn_DXF.toggled.connect(self.onClicked)
        #-------------------------------------------------------------
        self.radio_btn_DWG = QtWidgets.QRadioButton(self.groupBox)
        self.radio_btn_DWG.setGeometry(QtCore.QRect(10, 60, 95, 21))
        self.radio_btn_DWG.setObjectName("radio_btn_DWG")
        self.radio_btn_DWG.toggled.connect(self.onClicked)
        #-------------------------------------------------------------
        self.radio_btn_PDF = QtWidgets.QRadioButton(self.groupBox)
        self.radio_btn_PDF.setGeometry(QtCore.QRect(10, 90, 95, 21))
        self.radio_btn_PDF.setObjectName("radio_btn_PDF")
        self.radio_btn_PDF.toggled.connect(self.onClicked)
        #-------------------------------------------------------------
        self.radio_btn_Inne = QtWidgets.QRadioButton(self.groupBox)
        self.radio_btn_Inne.setGeometry(QtCore.QRect(10, 120, 95, 21))
        self.radio_btn_Inne.setObjectName("radio_btn_Inne")
        self.radio_btn_Inne.toggled.connect(self.onClicked)
        #-------------------------------------------------------------
        self.lineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit.setGeometry(QtCore.QRect(80, 120, 81, 21))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.textChanged[str].connect(self.onClicked)
        #====================================================================
        self.lbl_List_of_File = QtWidgets.QLabel(self.centralwidget)
        self.lbl_List_of_File.setGeometry(QtCore.QRect(200, 10, 131, 41))
        self.lbl_Name_Of_Folder = QtWidgets.QLabel(self.centralwidget)
        self.lbl_Name_Of_Folder.setGeometry(QtCore.QRect(10, 220, 171, 41))
        self.lbl_Name_Of_Folder_Value = QtWidgets.QLabel(self.centralwidget)
        self.lbl_Name_Of_Folder_Value.setGeometry(QtCore.QRect(10, 240, 171, 41))
        self.lbl_Name_Of_Folder_Value.setVisible(False)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lbl_List_of_File.setFont(font)
        self.lbl_List_of_File.setObjectName("lbl_List_of_File")
        self.lbl_Name_Of_Folder.setFont(font)
        self.lbl_Name_Of_Folder.setObjectName("lbl_Name_of_Folder")
        self.lbl_Name_Of_Folder_Value.setFont(font)
        self.lbl_Name_Of_Folder_Value.setObjectName("lbl_Name_of_Folder_Value")
        self.lbl_Name_Of_Folder_Value.setVisible(False) 
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(200, 50, 620, 431))
        self.textEdit.setObjectName("listView")
        self.btn_Print = QtWidgets.QPushButton(self.centralwidget)
        self.btn_Print.setGeometry(QtCore.QRect(200, 490, 93, 28))
        self.btn_Print.setObjectName("btn_Print")
        self.btn_Print.clicked.connect(self.handle_print)

        # wyświetlenie logo w oknie aplikacji przy pomocą label i QPixmap
        self.logo = QtWidgets.QLabel(self.centralwidget)
        self.logo.setGeometry(QtCore.QRect(10, 320, 120, 120))
        self.logo.setText("")
        self.logo.setPixmap(QtGui.QPixmap(path+"\QF_bold_gr.bmp"))
        self.logo.setScaledContents(True)

        # sprawdzić
        #self.file_type = file_type
        
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # dot. sygnałów przycisku do otwierania okna dialogowego  z wyborem pliku
        self.btn_Open_Folder.clicked.connect(self.OpenFileDialog)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    # dot. wyboru przycisku radio_button z wyborem typu pliku
    def onClicked(self):
        # radioButton = self.sender()                       ## !!!!! czemu to nie działa????
        global file_type                                    # ponowne ustawienie dla zmiennej file_type parametru global - zmienna jest globalana i widoczna w innych funkcjach/metodach programu
                                                            # ustawienie to jest wymagane, aby wybór typu pliku był widoczny w innych metodach
        if self.radio_btn_Inne.isChecked():                 # jeżeli zaznaczony jest przycisk wyboru 'Inne" i 
            if len(self.lineEdit.text()) != 0:              # jeżeli pole edycyjne jest wypełnione, to
              file_type = (self.lineEdit.text().lower())    # ustaw zmienną file_type na jego zawartość pisana małymi literami
            else:
              file_type = 'html'                            # w przeciwnym wypadku ustaw na html(to też jest często używane w programach na laser)
              #self.lineEdit.setText('html')                 # wypełnij pole edycji wartością 'html'
        elif self.radio_btn_DXF.isChecked():                # w przypadku wybrania przycisku typu radio DXF  
            file_type = 'dxf'                               # zdefiniuj zmienna file_type na dxf i 
            self.lineEdit.clear()                           # wyczyść pole edycji
        elif self.radio_btn_DWG.isChecked():                # w przypadku wybrania przycisku typu radio DWG 
            file_type = 'dwg'                               # zdefiniuj zmienna file_type na dwg i
            self.lineEdit.clear()                           # wyczyść pole edycji
        elif self.radio_btn_PDF.isChecked():                # w przypadku wybrania przycisku typu radio PDF
            file_type = 'pdf'                               # zdefiniuj zmienna file_type na pdf i
            self.lineEdit.clear()                           # wyczyść pole edycji
             
    def OpenFileDialog(self):
        self.textEdit.clear()                                # przy otwarciu okna dialogowego (wyboruy folderu), czyść zawartość okna textEdit
        folderpath = QtWidgets.QFileDialog.getExistingDirectory(None, 'Wybierz Folder') #czemu tutaj działa None , a nie działa self

        dlugosc_folder_path_name = min(len(folderpath),60)   # (max 65 znaków)
        self.textEdit.append("*"*(dlugosc_folder_path_name+5))
        self.textEdit.append(folderpath.replace('/','\\'))   # wyświetl ścieżkę dostępu i jednocześnie zamienia w niej znak '/' na '\' zgodnie z systemem Winodws
        self.textEdit.append("*"*(dlugosc_folder_path_name+5))

        
        #print (file_type)
        for file_name in os.listdir(folderpath):                # pętla w celu odczytania wszystkich plików w folderze
            if fnmatch.fnmatch(file_name, '*.' + file_type):    # ale warunek powoduje, że będą to tylko pliki o wskazanym rozszerzeniu -> file_type
                self.textEdit.append(file_name)                 # dodaj do pola textEdit kolejno odczytane z folderu nazwy pików
                self.textEdit.append("-"*60)                    # oraz linie rozdzielające pomiędzy nazwami
       
        self.lbl_Name_Of_Folder_Value.setVisible(True)          # pokaż etykietę, która wyświetla nazwę wybranego folderu
        self.lbl_Name_Of_Folder_Value.setText(os.path.basename(folderpath)) # za pomocą metody basename wyświetla nazwę folderu, która jest na końcu ścieżki dostępu

        # automatyczne zapisywanie pliku lista.txt w sprawdanym katalogu
        file = open(folderpath+'\lista.txt','w')
        text = self.textEdit.toPlainText()
        file.write(text)
        file.close()

        
    def handle_print(self):                                     # metoda drukująca zawartość okna textEdit po naciśnięciu przycisku 'Drukuj'
        dialog = QtPrintSupport.QPrintDialog()
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.textEdit.print_(dialog.printer())
            
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Files Lister by Quiet Falcon    v1.2"))
        self.btn_Open_Folder.setText(_translate("MainWindow", "Otwórz katalog"))
        self.groupBox.setTitle(_translate("MainWindow", "Rozszerzenie"))
        self.radio_btn_DXF.setText(_translate("MainWindow", "DXF"))
        self.radio_btn_DWG.setText(_translate("MainWindow", "DWG"))
        self.radio_btn_PDF.setText(_translate("MainWindow", "PDF"))
        self.radio_btn_Inne.setText(_translate("MainWindow", "INNE:"))
        self.lbl_List_of_File.setText(_translate("MainWindow", "Lista plików:"))
        self.btn_Print.setText(_translate("MainWindow", "Drukuj"))
        self.lbl_Name_Of_Folder.setText(_translate("MainWindow", "Nazwa folderu:"))
       # self.lbl_Name_Of_Folder_Value.setText(_translate("MainWindow", "Nazwa folderu:"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
