from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QTextEdit, QDialog, QSlider
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtCore import QUrl
import sys
import os
from md5 import MD5
import binascii

# binascii.hexlify(bytearray(array_alpha)) #might possibly help
# def x(strColl1, strColl2):
#     var byteColl1 = bytes(strColl1,'UTF-8');
#     var byteColl2 = bytes(strColl2,'UTF-8');
#     for i in range(0, strColl1.length()) #bytes in byte:
#         if byteColl1[i] != byteColl2[i]:
#           print(byteColl1[i], end=' ') #highlited
#         else:
#           print(byteColl1[i], end=' ') #simple
#
#     for i in range(0, strColl2.length()) #bytes in byte:
#         if byteColl2[i] != byteColl1[i]:
#           print(byteColl2[i], end=' ') #highlited
#         else:
#           print(byteColl2[i], end=' ') #simple
#
#     necessitates further integration with the gui

VOLUME = 3


class MD5cracker(QDialog):
    def __init__(self):
        super(MD5cracker, self).__init__()

    def closeEvent(self, event):
        QMainWindow.closeEvent(self, event)

app = QApplication(sys.argv)
window = MD5cracker()
uic.loadUi(os.path.join(sys.path[0], "gui.ui"), window)
window.setWindowIcon(QIcon(os.path.join(sys.path[0], "media/md5.png")))
player = QMediaPlayer()

input = window.findChild(QTextEdit, 'input')
button = window.findChild(QPushButton, 'pushButton')
output = window.findChild(QLabel, 'output')

volume_icon = window.findChild(QLabel, 'volumeIcon')
volume_slider = window.findChild(QSlider, 'volumeSlider')


def update_output(text):
    output.setText(text)

def click():
    print(MD5.hash(input.toPlainText()))
    update_output(MD5.hash(input.toPlainText()))
    # update_output("Clicked!")

def update_volume(value):
    VOLUME = value
    player.setVolume(VOLUME)
    if value == 0:
        volume_icon.setPixmap(QPixmap(os.path.join(sys.path[0], "media/volume_0.png")))
    elif value <= 33:
        volume_icon.setPixmap(QPixmap(os.path.join(sys.path[0], "media/volume_low.png")))
    else:
        volume_icon.setPixmap(QPixmap(os.path.join(sys.path[0], "media/volume_medium.png")))

def slide():
    update_volume(int(volume_slider.value()))

def play_audio():
    url = QUrl.fromLocalFile(os.path.join(sys.path[0], "media/Jester-Elysium.mp3"))
    song = QMediaContent(url)
    player.setMedia(song)
    update_volume(VOLUME)
    player.play()

button.clicked.connect(click)
volume_slider.valueChanged.connect(slide)

window.show()
play_audio()
app.exec_()

# str = 'muie';
# x(str)