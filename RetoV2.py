#Authors:
#Franco Minutti Simoni - A01733927
#Alan Mondragón Rivas - A01734565
#Created 20 May, 2021
# This program functions as an mp3 player in a digital interface.

#Import the python libraries
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
#Create a vector to manage the songs
songs = []
f = open("X.txt","r")
for i in f:
    songs.append(i)
#Declare global variables
song_num = 0
state = False
#Declare the serial port
ser =  serial.Serial('COM6',baudrate=9600, timeout=0.005)
tmp = "" #tmp striing for serial data
tpass = 0 #
maxsong = 0 #max time of the songs
ispaused = False
first = 0 # flag to now if it the first time pausing the music
#Class to create the User interface
class Ui_MainWindow(object):
    song_num = 0
    state = True
#Reproduces the selected song, with te given conditions
    def Reproduce(self,play):
        global song_num, tpass, maxsong
        f2=open('test1.txt','w')#Opens the txt to write the data of the song for the OLED
        pygame.mixer.init() #Starts the mixer
        cur_song = songs[song_num].rstrip() #Takes the song selected
        cur_song_file = "Songs/%s" % cur_song
        pygame.mixer.music.load(cur_song_file)
        audiofile = eyed3.load(cur_song_file)
#writes the info of current song on file
        title= str(audiofile.tag.title)
        artist = str(audiofile.tag.artist)
        album = str(audiofile.tag.album)
        f2.write(title+"\n")
        f2.write(artist+"\n")
        f2.write(album +"\n")
        f2.write("Track: " + str(song_num+1))
        f2.close()
#variables to set duration song labels
        track = cur_song_file
        audio = MP3(track)
        maxsong = audio.info.length
        mx = maxsong
        m = int(mx// 60)
        s = int(mx % 60)
        if s < 10 :
            segs = "0"+ str(s)
        else:
            segs = str(s)
        maxsong = int(maxsong)
#Plays the selected song
        if (play == 1):
            pygame.mixer.music.play()
            self.label.setText(str(audiofile.tag.title)+"\n"+str(audiofile.tag.artist)+"\n"+str(audiofile.tag.album)+"\n"+str(audiofile.tag.track_num)+"\n"+str(song_num+1))
            self.time_s_end.setText(str(m)+':'+segs)
            tpass = 0
            self.horizontalSlider.setMinimum(0)
            self.horizontalSlider.setMaximum(maxsong)
            self.horizontalSlider.setValue(0)
#Pauses the selected song
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
        global ispaused, state, first
        if (first != 0):
            if (state == True):
                state = False
                pygame.mixer.music.pause()
                ispaused = True

            else:
                state = True
                pygame.mixer.music.unpause()
                ispaused = False
        else:
            first = 1
            pygame.mixer.music.pause()
            ispaused = True
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
#Setup the user interface
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
#Code generated with QT designer for the interface
#///////////////////////////////////////////////////////////////////////////////
        #Scroll Area Properties
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)

        font = QtGui.QFont()
        font.setPointSize(10)
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
        self.horizontalSlider.setGeometry(QtCore.QRect(530, 410, 241, 20))
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.time_s_end = QtWidgets.QLabel(self.centralwidget)
        self.time_s_end.setGeometry(QtCore.QRect(720, 360, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.time_s_end.setFont(font)
        self.time_s_end.setAlignment(QtCore.Qt.AlignCenter)
        self.time_s_end.setObjectName("time_s_end")
        self.prev = QtWidgets.QPushButton(self.centralwidget)
        self.prev.setGeometry(QtCore.QRect(250, 470, 91, 91))
        self.prev.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("prev.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
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
        icon1.addPixmap(QtGui.QPixmap("stop.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.stop.setIcon(icon1)
        self.stop.setIconSize(QtCore.QSize(150, 150))
        self.stop.setAutoDefault(True)
        self.stop.setDefault(True)
        self.stop.setObjectName("stop")
        self.play_pause = QtWidgets.QPushButton(self.centralwidget)
        self.play_pause.setGeometry(QtCore.QRect(360, 470, 91, 91))
        self.play_pause.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("play_pause.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.play_pause.setIcon(icon2)
        self.play_pause.setIconSize(QtCore.QSize(150, 150))
        self.play_pause.setAutoDefault(True)
        self.play_pause.setDefault(True)
        self.play_pause.setObjectName("play_pause")
        self.next = QtWidgets.QPushButton(self.centralwidget)
        self.next.setGeometry(QtCore.QRect(580, 470, 91, 91))
        self.next.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("next.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.next.setIcon(icon3)
        self.next.setIconSize(QtCore.QSize(150, 150))
        self.next.setDefault(True)
        self.next.setObjectName("next")
        self.label_data_input = QtWidgets.QLabel(self.centralwidget)
        self.label_data_input.setGeometry(QtCore.QRect(130, 460, 100s, 51))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setItalic(True)
        self.label_data_input.setFont(font)
        self.label_data_input.setAlignment(QtCore.Qt.AlignCenter)
        self.label_data_input.setObjectName("label_data_input")
        self.label_input = QtWidgets.QLabel(self.centralwidget)
        self.label_input.setGeometry(QtCore.QRect(10, 460, 91, 51))
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
        self.label_data_vol = QtWidgets.QLabel(self.centralwidget)
        self.label_data_vol.setGeometry(QtCore.QRect(130, 500, 81, 51))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setItalic(True)
        self.label_data_vol.setFont(font)
        self.label_data_vol.setAlignment(QtCore.Qt.AlignCenter)
        self.label_data_vol.setObjectName("label_data_vol")
        self.label_volume = QtWidgets.QLabel(self.centralwidget)
        self.label_volume.setGeometry(QtCore.QRect(0, 500, 131, 51))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_volume.setFont(font)
        self.label_volume.setAlignment(QtCore.Qt.AlignCenter)
        self.label_volume.setObjectName("label_volume")
        self.time_s_begin = QtWidgets.QLabel(self.centralwidget)
        self.time_s_begin.setGeometry(QtCore.QRect(510, 360, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.time_s_begin.setFont(font)
        self.time_s_begin.setAlignment(QtCore.Qt.AlignCenter)
        self.time_s_begin.setObjectName("time_s_begin")
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
#pushbuttons of interface actions connected
        self.prev.clicked.connect(self.Previous)
        self.play_pause.clicked.connect(self.PlayPause)
        self.next.clicked.connect(self.Next)
        self.stop.clicked.connect(self.Stop)
        self.random.clicked.connect(self.random_song)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "-"))
        self.time_s_end.setText(_translate("MainWindow", "0:00"))
        self.label_data_input.setText(_translate("MainWindow", "-"))
        self.label_input.setText(_translate("MainWindow", "Input:"))
        self.label_data_vol.setText(_translate("MainWindow", "-"))
        self.label_volume.setText(_translate("MainWindow", "Volume:"))
        self.time_s_begin.setText(_translate("MainWindow", "0:00"))
#///////////////////////////////////////////////////////////////////////////////
        self.timeout = 0
        self.random_song()
        self.check_serial_event()
#Controls the time labels of the interface and change to next song after one ends
    def song_time(self,tpass):
        global maxsong, ispaused
        tp2 = tpass // 60
        if ispaused == True:
            return
        else:
            if tpass > maxsong:
                self.Next()
                return
            else:
                if (tpass // 60 < 0):
                    if tpass < 10:
                        self.time_s_begin.setText("0:0"+str(tpass))
                    else:
                        self.time_s_begin.setText("0:"+str(tpass))
                else:
                    if (tpass%60) < 10:
                        self.time_s_begin.setText(str(tp2)+":0"+str(tpass%60))
                    else:
                        self.time_s_begin.setText(str(tp2)+":"+str(tpass%60))
                self.horizontalSlider.setValue(tpass)
#This function controls the data recived form arduino to set volume and do the pushbutton functions
    def check_serial_event(self):
        global tmp,tpass, song_num, maxsong, ispaused
        if ispaused == False:
            tpass+=1
        self.timeout += 1
        serial_thread = threading.Timer(1, self.check_serial_event)
        serial_thread.setDaemon(True)
        if ser.is_open == True:
            serial_thread.start()
            self.song_time(tpass)
            if ser.in_waiting:
                line = ser.readline().decode('utf-8').rstrip()
                key = line[1:2]#Defines if the action is for the volume or the pad
                value = line[4:]#Gets the value
                if (key == "1"): #data from potentiometer
                    volume_level = int(value)/1023
                    pygame.mixer.music.set_volume(volume_level)
                    volume_porc = int(volume_level*100)
                    self.label_data_vol.setText(str(volume_porc)+"%")
                if (key == "2"): #data from keypad
                    if value.isdigit()== True:
                        tmp += value
                        self.label_data_input.setText(tmp)
                    elif value == "*":#Enter for the numerical inputs
                        self.label_data_input.setText(tmp)
                        if (int(tmp)-1<len(songs)):
                            song_num = int(tmp)-1 #if the song number is valid
                            self.Reproduce(1) #reproduces the selected song
                        tmp = ""
                    else:
                        if value == "A":
                            self.label_data_input.setText("Previous")
                            self.Previous()
                        if value == "B":
                            if (ispaused == True):
                                self.label_data_input.setText("Play")
                            else:
                                self.label_data_input.setText("Pause")
                            self.PlayPause()
                        if value == "C":
                            self.label_data_input.setText("Restart")
                            self.Stop()
                        if value == "D":
                            self.label_data_input.setText("Next")
                            self.Next()
                        if value == "#":
                            self.label_data_input.setText("Random")
                            self.random_song()
                    self.timeout = 0

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
