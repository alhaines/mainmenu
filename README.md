# mainmenu a python3 database 
A menu system for media files in folders named Movies, TV Shows and Prograsmming. 
The media01.py will scan a folder for sub folders named Movies, TV Shows and Programming. 
All found media files will be entered into an Mysql Database. 
maindisplay.py will display a menu with the three tables listed for selection. 
After selecring a table you are presented with a display that contains a combo box filled from the table. 
Select a file and you can either view the file with VLC or rename the file. 
I use this as a launcher for my media files in the three folders. 
media.sql contains the sql description. 
config.py will hold credentials for the mysql database. 
