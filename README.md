# RetoFinalMp3

Video: [Reto TE2003B](https://youtu.be/vWmVSsLhZlg)

Authors:
Franco Minutti Simoni - A01733927
Alan Mondragón Rivas - A01734565

Created 20 May, 2021

This program functions as an mp3 player with a digital interface running on a
Raspberry Pi with a keypad and a potentiometer connected to an Arduino Uno, that
at the same time sends the data with UART protocol to the RPI which it going to communicate with the OLED display by I2C.

![image](https://user-images.githubusercontent.com/67660198/121632620-eb5a0980-ca46-11eb-9699-6699006d0592.png)

For this program to run properly the user needs to install the keypad.h library in the arduino IDE
, also needs to install the following libraries on python:
###### Arduino:
* install Keypad-master.zip (zip included in the repository)
* install FreeRtos (Use the library manager un Arduino IDE and search for FreeRtos)

![image](https://user-images.githubusercontent.com/67660198/121632165-1f80fa80-ca46-11eb-97c5-239db9f03633.png)
###### RPI:
* pygame (pip install pygame)
* pyqt5 (pip install pyqt5)
* eyed3 (pip install eyed3)
* mutagen (pip install mutagen)
* threading (pip install threading)
###### OLED:
* Adafruit_SSD1306 (pip install Adafruit_SSD1306)
* PIL (pip install PIL)

## Keypad and potentiometer functionalities:
- Number Keys (0-9): Enter song number of playlist
- Select Key (\*): Select the song enter by the number keys
- Previous key (A): Reproduces previous song
- Play/Pause key (B): Pauses or play a song
- Stop key (C): Reproduces the first song of the playlist
- Next key (D): Reproduces next song
- Random key (\#): Reproduces a random song on playlist
- Potentiometer: sets volume of music player

## How to Run it with a desktop file:
1. To create the desktop file you need to create a file like the "prueba_8" where you only specify the path of the main file and the command on terminal to run the python files at the same time ("RetoV2.py" & "oledt1.py").
2. Ones you have the path on that file, you need to create the desktop file just like the "Reto.desktop" file and change the path where the previous file was located ("prueba_8"), and the path to the icon you want to watch on your desktop file (optional).
3. Double click the icon of the program created and click on the button "Execute in terminal" to run the program.

## Adding a new song
1. Copy the mp3 file of the song to the Songs folder.
2. Copy the full name of the song file (without the path) to the SongNames.txt.

## Circuit Diagrams

![image](https://user-images.githubusercontent.com/67660198/121631735-44c13900-ca45-11eb-81fe-93c8ae44d123.png)
![image](https://user-images.githubusercontent.com/67660198/121631766-530f5500-ca45-11eb-976f-3f13e3c17fda.png)
