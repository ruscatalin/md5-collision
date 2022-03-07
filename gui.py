from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QTextEdit, QDialog
import sys
import os
from md5 import MD5


class MD5cracker(QDialog):
    def __init__(self):
        super(MD5cracker, self).__init__()

    def closeEvent(self, event):
        QMainWindow.closeEvent(self, event)

app = QApplication(sys.argv)
window = MD5cracker()
uic.loadUi(os.path.join(sys.path[0], "gui.ui"), window)
window.setWindowIcon(QIcon(os.path.join(sys.path[0], "md5.png")))

input = window.findChild(QTextEdit, 'input')
button = window.findChild(QPushButton, 'pushButton')
output = window.findChild(QLabel, 'output')


def update_output(text):
    output.setText(text)

def click():
    print(MD5.hash(input.toPlainText()))
    update_output(MD5.hash(input.toPlainText()))
    # update_output("Clicked!")

button.clicked.connect(click)

window.show()
app.exec_()
