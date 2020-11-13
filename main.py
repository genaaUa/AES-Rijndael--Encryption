import sys
import os
import time
import rijndael
from PySide2.QtWidgets import QMainWindow, QWidget, QApplication, QPushButton, QTextEdit, QLineEdit, QRadioButton
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader
from ui_mainwindow import Ui_MainWindow


class UI(QMainWindow):

    def __init__(self):
        super(UI, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.lineEdit = self.findChild(QLineEdit, "lineEdit")
        self.lineEdit2 = self.findChild(QLineEdit, "lineEdit_2")
        self.lineEdit2.setMaxLength(16)
        
        self.textEdit = self.findChild(QTextEdit, "textEdit")
        self.textEdit.setReadOnly(True)
        
        self.radioButton = self.findChild(QRadioButton, "radioButton")
        self.radioButton.setChecked(True)
        
        self.button = self.findChild(QPushButton, "pushButton")
        self.button2 = self.findChild(QPushButton, "pushButton_2")
        
        self.button.clicked.connect(self.clickedBtn)
        self.button2.clicked.connect(self.clickedBtn2)

        self.show()

    def clickedBtn2(self):
        sys.exit()

    def clickedBtn(self):
        if self.radioButton.isChecked():
            way = '1'
        else:
            way = '2'

        input_path = self.lineEdit.text()
            
        if os.path.isfile(input_path):
            pass
        else:
            self.textEdit.setPlainText("This is not a file! Check a path!\n")
            return

        key = self.lineEdit2.text()

        
        time_before = time.time()

        # Input data
        with open(input_path, 'rb') as f:
            data = f.read()
        if way == '1':
            crypted_data = []
            temp = []
            for byte in data:
                 temp.append(byte)
                 if len(temp) == 16:
                    print("123")
                    crypted_part = rijndael.encrypt(temp, key)
                    crypted_data.extend(crypted_part)
                    del temp[:]
            else:
                #padding v1
                # crypted_data.extend(temp)

                # padding v2
                if 0 < len(temp) < 16:
                    empty_spaces = 16 - len(temp)
                    for i in range(empty_spaces - 1):
                        temp.append(0)
                    temp.append(1)
                    crypted_part = rijndael.encrypt(temp, key)
                    crypted_data.extend(crypted_part)

            out_path = os.path.join(os.path.dirname(input_path) , 'crypted_' + os.path.basename(input_path))

            if os.path.exists(out_path):
                os.remove(out_path)

            # Ounput data
            with open(out_path, 'xb') as ff:
                ff.write(bytes(crypted_data))

            self.textEdit.setPlainText("Encryption is successful! Check the file with name crypted_" + os.path.basename(input_path)+"\n")   

        else: # if way == '2'
            decrypted_data = []
            temp = []
            for byte in data:
                temp.append(byte)
                if len(temp) == 16:
                    decrypted_part = rijndael.decrypt(temp, key)
                    decrypted_data.extend(decrypted_part)
                    del temp[:] 
            else:
                #padding v1
                # decrypted_data.extend(temp)
                    
                # padding v2
                if 0 < len(temp) < 16:
                    empty_spaces = 16 - len(temp)
                    for i in range(empty_spaces - 1):
                        temp.append(0)
                    temp.append(1)
                    decrypted_part = rijndael.encrypt(temp, key)
                    decrypted_data.extend(crypted_part) 

            out_path = os.path.join(os.path.dirname(input_path) , 'decrypted_' + os.path.basename(input_path))

            if os.path.exists(out_path):
                os.remove(out_path)
                
            # Ounput data
            with open(out_path, 'xb') as ff:
                ff.write(bytes(decrypted_data))

            self.textEdit.setPlainText("Decryption is successful! Check the file with name decrypted_" + os.path.basename(input_path)+ "\n")   


        time_after = time.time()

        return

app = QApplication(sys.argv)
window = UI()
app.exec_()
