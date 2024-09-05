import csv
import sqlite3

conn = sqlite3.connect("jarvis.db")
cursor = conn.cursor()

# query = "CREATE TABLE IF NOT EXISTS sys_command(id integer primary key, name VARCHAR(100), path VARCHAR(1000))"
# cursor.execute(query)

# query = "INSERT INTO sys_command VALUES (null, 'photo booth', '/System/Applications/Photo Booth.app')"
# cursor.execute(query)
# conn.commit()

# query = "CREATE TABLE IF NOT EXISTS web_command(id integer primary key, name VARCHAR(100), url VARCHAR(1000))"
# cursor.execute(query)

# query = "INSERT INTO web_command VALUES (null, 'swiggy', 'https://www.swiggy.com')"
# cursor.execute(query)
# conn.commit()

# create a table with the desired columns
cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (id integer primary key, name VARCHAR(200), mobile_no VARCHAR(200), email VARCHAR(255) NULL)''')

# specify the column indices you want to import
desired_columns_indices = [0, 18]

# read data from csv and insert into SQLite table for desired columns
with open ('contacts.csv', 'r', encoding='utf-8') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        selected_data = [row[i] for i in desired_columns_indices]
        cursor.execute(''' INSERT INTO contacts('id', 'name', 'mobile_no') VALUES (null, ?, ?);''', tuple(selected_data))

# commit changes and close connection
conn.commit()
conn.close()