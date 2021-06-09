#Authors:
#Franco Minutti Simoni - A01733927
#Alan Mondragón Rivas - A01734565
#Created 20 May, 2021
# This program functions as an mp3 player in a digital interface.


from PyQt5.QtWidgets import (QWidget, QSlider, QLineEdit, QLabel, QPushButton, QScrollArea,QApplication,
                             QHBoxLayout, QVBoxLayout, QMainWindow)
from PyQt5.QtCore import Qt, QSize
from PyQt5 import QtWidgets, uic
import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
import pygame, eyed3, time, threading, random, serial, math
from mutagen.mp3 import MP3

songs = []
f = open("X.txt","r")
for i in f:
    songs.append(i)


song_num = 0
state = False
ser =  serial.Serial('COM6',baudrate=9600, timeout=0.005)
tmp = ""
class Ui_MainWindow(object):
    song_num = 0
    state = True
#Reproduces the selected song, with te given conditions
    def Reproduce(self,play):
        global song_num
        pygame.mixer.init()
        cur_song = songs[song_num].rstrip()
        cur_song_file = "Songs/%s" % cur_song
        pygame.mixer.music.load(cur_song_file)
        audiofile = eyed3.load(cur_song_file)

        track = cur_song_file
        audio = MP3(track)
        m = int(audio.info.length // 60)
        s = int(audio.info.length % 60)

        if (play == 1):
            pygame.mixer.music.play()
            self.label.setText(str(audiofile.tag.title)+"\n"+str(audiofile.tag.artist)+"\n"+str(audiofile.tag.album)+"\n"+str(audiofile.tag.track_num)+"\n")
            self.time_s.setText(str(m)+':'+str(s))
        else:
            pygame.mixer.music.pause()
#Goes to the next song
    def Next(self):
        global song_num
        if (song_num>=(len(songs)-1)):
            song_num = 0
        else:
            song_num += 1
        self.Reproduce(1)
#Intercalates between Pause and Play the songs
    def PlayPause(self):
        global state
        if (state == True):
            state = False
            pygame.mixer.music.pause()

        else:
            state = True
            pygame.mixer.music.unpause()
#Goes to the Previous song
    def Previous(self):
        global song_num
        if (song_num<1):
            song_num = len(songs)-1 #9
        else:
            song_num -= 1
        self.Reproduce(1)
#Restarts the playlist
    def Stop(self):
        global song_num
        song_num = 0
        self.Reproduce(1)
#Plays a random song on playlist
    def random_song(self):
        global song_num
        song_num = random.randrange(0,len(songs))
        self.Reproduce(1)
#Detects what button was pressed

    ''''
    def increaseVolume(self):
		vol = self.player.volume()
		vol = min(vol+5,100)
		self.player.setVolume(vol)

	def decreaseVolume(self):
		vol = self.player.volume()
		vol = max(vol-5,0)
		self.player.setVolume(vol)'''
    #Setup the ui
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(810, 619)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.scroll = QScrollArea(self.centralwidget)
        self.scroll.setGeometry(QtCore.QRect(20, 20, 481, 431))
        self.scroll.setObjectName("scroll")            # Scroll Area which contains the widgets, set as the centralWidget
        self.widget = QWidget()                 # Widget that contains the collection of Vertical Box
        self.vbox = QVBoxLayout()
        global songs             # The Vertical Box that contains the Horizontal Boxes of  labels and buttons
        for i in range(0,len(songs)):
            object = QLabel(str(i+1)+": "+songs[i])
            self.vbox.addWidget(object)

        self.widget.setLayout(self.vbox)

        #Scroll Area Properties
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(520, 30, 271, 291))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label.setFont(font)
        self.label.setScaledContents(True)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setOpenExternalLinks(False)
        self.label.setObjectName("label")
        self.horizontalSlider = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSlider.setGeometry(QtCore.QRect(510, 370, 211, 20))
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.time_s = QtWidgets.QLabel(self.centralwidget)
        self.time_s.setGeometry(QtCore.QRect(720, 360, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.time_s.setFont(font)
        self.time_s.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.time_s.setObjectName("time_s")
        self.prev = QtWidgets.QPushButton(self.centralwidget)
        self.prev.setGeometry(QtCore.QRect(250, 470, 91, 91))
        self.prev.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("prev.jpeg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.prev.setIcon(icon)
        self.prev.setIconSize(QtCore.QSize(150, 150))
        self.prev.setCheckable(False)
        self.prev.setAutoRepeat(False)
        self.prev.setAutoExclusive(False)
        self.prev.setAutoDefault(True)
        self.prev.setDefault(True)
        self.prev.setObjectName("prev")
        self.stop = QtWidgets.QPushButton(self.centralwidget)
        self.stop.setGeometry(QtCore.QRect(470, 470, 91, 91))
        self.stop.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("stop.jpeg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.stop.setIcon(icon1)
        self.stop.setIconSize(QtCore.QSize(150, 150))
        self.stop.setAutoDefault(True)
        self.stop.setDefault(True)
        self.stop.setObjectName("stop")
        self.play_pause = QtWidgets.QPushButton(self.centralwidget)
        self.play_pause.setGeometry(QtCore.QRect(360, 470, 91, 91))
        self.play_pause.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("play_pause.jpeg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.play_pause.setIcon(icon2)
        self.play_pause.setIconSize(QtCore.QSize(150, 150))
        self.play_pause.setAutoDefault(True)
        self.play_pause.setDefault(True)
        self.play_pause.setObjectName("play_pause")
        self.next = QtWidgets.QPushButton(self.centralwidget)
        self.next.setGeometry(QtCore.QRect(580, 470, 91, 91))
        self.next.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("next.jpeg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.next.setIcon(icon3)
        self.next.setIconSize(QtCore.QSize(150, 150))
        self.next.setDefault(True)
        self.next.setObjectName("next")
        self.label_data = QtWidgets.QLabel(self.centralwidget)
        self.label_data.setGeometry(QtCore.QRect(100, 490, 121, 51))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setItalic(True)
        self.label_data.setFont(font)
        self.label_data.setAlignment(QtCore.Qt.AlignCenter)
        self.label_data.setObjectName("label_data")
        self.label_input = QtWidgets.QLabel(self.centralwidget)
        self.label_input.setGeometry(QtCore.QRect(10, 490, 91, 51))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_input.setFont(font)
        self.label_input.setAlignment(QtCore.Qt.AlignCenter)
        self.label_input.setObjectName("label_input")
        self.random = QtWidgets.QPushButton(self.centralwidget)
        self.random.setGeometry(QtCore.QRect(690, 470, 91, 91))
        self.random.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("random.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.random.setIcon(icon4)
        self.random.setIconSize(QtCore.QSize(100, 100))
        self.random.setCheckable(False)
        self.random.setAutoDefault(False)
        self.random.setDefault(True)
        self.random.setFlat(False)
        self.random.setObjectName("random")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 810, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.prev.clicked.connect(self.Previous)
        self.play_pause.clicked.connect(self.PlayPause)
        self.next.clicked.connect(self.Next)
        self.stop.clicked.connect(self.Stop)
        self.random.clicked.connect(self.random_song)

        # while (ser.in_waiting < 0):
        #     tmp = ""
        #     line = ser.readline().decode('utf-8').rstrip()
        #     if (line.isdigit()== True):
        #         line = ser.readline().decode('utf-8').rstrip()
        #         tmp += line
        #         print (tmp,"---")


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

        self.label.setText(_translate("MainWindow", " - "))
        self.time_s.setText(_translate("MainWindow", "0:00"))
        self.label_data.setText(_translate("MainWindow", "-"))
        self.label_input.setText(_translate("MainWindow", "Input:"))

        # User Code
        self.timeout = 0
        self.check_serial_event()

    def check_serial_event(self):
        global tmp, song_num
        self.timeout += 1
        # print (self.timeout)
        serial_thread = threading.Timer(1, self.check_serial_event)
        if ser.is_open == True:
            serial_thread.start()
            if ser.in_waiting:
                line = ser.readline().decode('utf-8').rstrip()
                if line.isdigit()== True:
                    tmp += line
                    self.label_data.setText(tmp)
                elif line == "*":
                    self.label_data.setText(tmp)
                    if (int(tmp)-1<len(songs)):
                        song_num = int(tmp)-1
                        self.Reproduce(1)
                    # llamado a funcion de canciones
                    tmp = ""
                else:
                    self.label_data.setText(line)
                    if line == "A":
                        self.Previous()
                    if line == "B":
                        self.PlayPause()
                    if line == "C":
                        self.Stop()
                    if line == "D":
                        self.Next()
                    if line == "#":
                        self.random_song()

                self.timeout = 0

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
    ser.flush()
    main()
