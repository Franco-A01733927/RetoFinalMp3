# RetoFinalMp3

Video: [Reto TE2003B](https://youtu.be/vWmVSsLhZlg)

Authors:
Franco Minutti Simoni - A01733927
Alan Mondragón Rivas - A01734565

Created 20 May, 2021

This program functions as an mp3 player with a digital interface running on a
raspberry pi with a keypad and a potentiometer connected to an Arduino Uno, that 
at the same time sends the data with UART protocol to the raspberry

For this program to run properly the user needs to install the keypad.h library 
(zip included in the repository), also needs to install the following libraries:
- [ ] pygame (pip install pygame) pygame (pip install pygame)
* pyqt5 (pip install pyqt5)
* eyed3 (pip install eyed3)
* mutagen (pip install mutagen)
* threading (pip install threading)

## How to Run it with a desktop file:

1. To create the desktop file you need to create a file like the "prueba_8" where you only specify the path of the main file and the command on terminal to run the python file(s).
2. Ones you have the path on that file, you need to create the desktop file just like the "Reto.desktop" file and change the path where the previous file was located ("pyfiles"), and the path to the icon you want to watch on your shortcut (optional).
3. Double click the icon of the program created and click on the button "Execute in terminal" to run the program.
