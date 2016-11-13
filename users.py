import sqlite3 as lite
import sys

sales = {
    ('John', 2200),
    ('John', 2200),
    ('John', 2200),
    ('John', 2200),
    ('John', 2200),
    ('John', 2200),
    ('John', 2200),
    ('John', 2200),
    ('John', 2200),
    ('John', 2200)
}


con = lite.connect('sales.db')

with con:

    cur = con.cursor()

    cur.execute("DROP TABLE IF EXISTS reps")
    cur.execute("CREATE TABLE reps(rep_name TEXT, amount INT)")
    cur.executemany("INSERT INTO reps VALUES(?, ?)",sales)