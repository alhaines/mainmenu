#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#  Copyright 2023 AL Haines <alfredhaines@gmail.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#

# Import necessary modules
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget, QDialog
from display_page import DisplayPage

# MainMenu class for handling the main menu
class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 400, 300)
        self.setWindowTitle('Database Viewer - Main Menu')

        layout = QVBoxLayout()

        # Buttons for each table
        movies_button = QPushButton('Movies Table', self)
        movies_button.clicked.connect(lambda: self.show_display_page('movies'))
        layout.addWidget(movies_button)

        tv_shows_button = QPushButton('TV Shows Table', self)
        tv_shows_button.clicked.connect(lambda: self.show_display_page('tv_shows'))
        layout.addWidget(tv_shows_button)

        programming_button = QPushButton('Programming Table', self)
        programming_button.clicked.connect(lambda: self.show_display_page('programming'))
        layout.addWidget(programming_button)

        # Quit button
        quit_button = QPushButton('Quit', self)
        quit_button.clicked.connect(self.close)
        layout.addWidget(quit_button)

        # Create a central widget and set the layout
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def show_display_page(self, table_name):
        display_page = DisplayPage(table_name, self)
        display_page.exec()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_menu = MainMenu()
    main_menu.show()
    sys.exit(app.exec())
