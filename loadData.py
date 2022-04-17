import os
os.system("sqlite3 db.sqlite3 < data/courses.sql")
os.system("sqlite3 db.sqlite3 < data/majorMinor.sql")
os.system("sqlite3 db.sqlite3 < data/departments.sql")