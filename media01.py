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
import pymysql
import re
from config import mysql_config, external_hard_drive_path

# Modify the patterns to capture more file names
movie_pattern = re.compile(r'.*(\.mp4|\.mkv|\.avi)$', re.IGNORECASE)
tv_show_pattern = re.compile(r'.*?[Ss](\d{1,3})[Ee](\d{1,3}).*(\.mp4|\.mkv|\.avi)$', re.IGNORECASE)

# Function to connect to MySQL database
def connect_to_db():
    try:
        connection = pymysql.connect(**mysql_config)
        return connection
    except pymysql.Error as e:
        print(f"Error: Unable to connect to the database. {e}")
        return None

# Add a function to truncate tables
def truncate_table(connection, table_name):
    cursor = connection.cursor()
    cursor.execute(f"TRUNCATE TABLE {table_name}")
    print(f"Table {table_name} truncated.")

# Modify the insertion function to capture all files, handling None pattern
def insert_files(connection, folder_path, table_name, pattern):
    cursor = connection.cursor()
    file_count = 0
    unmatched_files = []
    
    print(f"Scanning files in: {folder_path}")
    
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if pattern is None or pattern.match(file):
                title = os.path.splitext(file)[0]
                file_path = os.path.join(root, file)
                cursor.execute(f"INSERT INTO {table_name} (title, file_path) VALUES (%s, %s)", (title, file_path))
                file_count += 1
            else:
                unmatched_files.append(os.path.join(root, file))
    
    connection.commit()
    print(f"{table_name.capitalize()} cataloging completed. Total files processed: {file_count}")
    if unmatched_files:
        print(f"Unmatched files for {table_name}:")
        for file in unmatched_files:
            print(file)

# Recursive function to scan and catalog TV show files
def scan_and_catalog_tv_shows_recursive(connection, folder_path):
    print("Scanning and cataloging TV show files...")
    truncate_table(connection, 'tv_shows')
    scan_and_catalog_tv_shows_recursive_helper(connection, folder_path)

def scan_and_catalog_tv_shows_recursive_helper(connection, folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if tv_show_pattern.match(file):
                title = os.path.splitext(file)[0]
                file_path = os.path.join(root, file)
                cursor = connection.cursor()
                cursor.execute(f"INSERT INTO tv_shows (title, file_path) VALUES (%s, %s)", (title, file_path))

    for dir in dirs:
        new_path = os.path.join(folder_path, dir)
        scan_and_catalog_tv_shows_recursive_helper(connection, new_path)

# Function to display the cataloged files
def display_catalog(connection, table_name):
    cursor = connection.cursor()
    cursor.execute(f"SELECT title, file_path FROM {table_name}")
    print(f"\nCatalog for {table_name}:")
    for row in cursor.fetchall():
        print(f"Title: {row[0]}\nFile Path: {row[1]}\n")

if __name__ == "__main__":
    # Connect to MySQL database
    db_connection = connect_to_db()
    if db_connection:
        # Scan and catalog movie files
        movies_folder = os.path.join(external_hard_drive_path, 'Movies')
        if os.path.exists(movies_folder):
            insert_files(db_connection, movies_folder, 'movies', movie_pattern)
        else:
            print("Movies folder not found.")
        
        # Scan and catalog TV show files using the recursive approach
        tv_shows_folder = os.path.join(external_hard_drive_path, 'TV Shows')
        if os.path.exists(tv_shows_folder):
            scan_and_catalog_tv_shows_recursive(db_connection, tv_shows_folder)
        else:
            print("TV Shows folder not found.")
        
        # Scan and catalog programming files
        programming_folder = os.path.join(external_hard_drive_path, 'Programming')
        if os.path.exists(programming_folder):
            insert_files(db_connection, programming_folder, 'programming', None)
        else:
            print("Programming folder not found.")
        
        # Display the cataloged movies, TV shows, and programming
        display_catalog(db_connection, 'movies')
        display_catalog(db_connection, 'tv_shows')
        display_catalog(db_connection, 'programming')
        
        # Close the database connection
        db_connection.close()
