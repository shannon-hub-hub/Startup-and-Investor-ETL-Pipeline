import sqlite3

conn = sqlite3.connect('scraper_data.db')
cursor = conn.cursor()

cursor.execute("SELECT * FROM investors")
for row in cursor.fetchall():
    print(row)

conn.close()