#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#  Copyright 2023 AL Haines <alfredhaines@gmail.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
import os
import sys
import pymysql
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QTextEdit, QWidget
from config import mysql_config

class DatabaseViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.connect_to_db()

    def initUI(self):
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Database Viewer')

        # Create layout
        layout = QVBoxLayout()

        # Create text boxes for each table
        self.movies_textbox = QTextEdit(self)
        self.movies_textbox.setReadOnly(True)
        self.movies_textbox.setPlaceholderText('Movies Table')
        layout.addWidget(self.movies_textbox)

        self.tv_shows_textbox = QTextEdit(self)
        self.tv_shows_textbox.setReadOnly(True)
        self.tv_shows_textbox.setPlaceholderText('TV Shows Table')
        layout.addWidget(self.tv_shows_textbox)

        self.programming_textbox = QTextEdit(self)
        self.programming_textbox.setReadOnly(True)
        self.programming_textbox.setPlaceholderText('Programming Table')
        layout.addWidget(self.programming_textbox)

        # Create a central widget and set the layout
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def connect_to_db(self):
        try:
            # Use credentials from config.py
            self.connection = pymysql.connect(**mysql_config)
            self.cursor = self.connection.cursor()
            self.display_tables()
        except pymysql.Error as e:
            print(f"Error: Unable to connect to the database. {e}")

    def display_tables(self):
        self.display_table('movies', self.movies_textbox)
        self.display_table('tv_shows', self.tv_shows_textbox)
        self.display_table('programming', self.programming_textbox)

    def display_table(self, table_name, textbox):
        try:
            self.cursor.execute(f"SELECT * FROM {table_name} ORDER by title")
            rows = self.cursor.fetchall()
            textbox.clear()
            for row in rows:
                textbox.append(str(row))
        except pymysql.Error as e:
            print(f"Error: Unable to fetch data from {table_name}. {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = DatabaseViewer()
    viewer.show()
    sys.exit(app.exec())
