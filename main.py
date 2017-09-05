""" An introduction to sqlite3 database functions (for beginners)"""
# Source: Modified from https://docs.python.org/3/library/sqlite3.html
# Author: Lim Heng
# Contact: chhunlimheng@gmail.com

# Database Schema
#     table: person
#         fields: username, firstname, lastname, email, biography, occupation

# For example purposes
#     con = sqlite3.connect("database.db")
#     this will create a local database.db file in the same directory as this .py file.
# alternatively you can create a temperary database in memory with
#     con = sqlite3.connect(":memory:")

# To improve understanding and code execution:
#     no shorthand or context managers will be used in this example.

import sqlite3


def create_table():
    # Create table person with fields (id), username, email, firstname, lastname, biography, and occupation.
    """ Returns true if the table was created sucessfully and false if there was an error that occured. """
    try:
        con = sqlite3.connect("database.db")
        cur = con.cursor()
        cur.execute('''CREATE TABLE person
                       (username TEXT, email TEXT, firstname TEXT, lastname TEXT, biography TEXT, occupation TEXT)''')
        con.commit()
        con.close()
    except:
        return False
    return True

def drop_table():
    # Note: Cannot create tables with the same name
    #       Execute commands in sqlite are case insensitive.
    #       cur.execute('''drop table if exists person''') would also work.
    """ Checks if table exists and deletes it from database. """
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute('''DROP TABLE IF EXISTS person''')
    con.commit()
    con.close()

def insert_table(person):
    # Note: The amount of ? correspond to the number of fields in the table.
    """ Inserts a row to the database, variable person is a tuple. """
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute('INSERT INTO person VALUES (?,?,?,?,?,?)', person)
    con.commit()
    con.close()

def populate_table():
    # Note: There is a comma after the last item of the list people.
    #       Instead of cur.execute(), cur.executemany() is used.
    """ Populates mutiple rows in a table simultaneously. """
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    people = [('Janey', 'JaneDoe@gmail.com', 'Jane', 'Doe', 'Jane Doe is a Software Engineer.', 'Software Engineer'),
              ('Joey', 'JoeShmo@gmail.com', 'Joseph', 'Shmo', 'Joseph Shmo is a Data Scientist.', 'Data Scientist'),
              ('Jonny', 'JohnSmith@gmail.com', 'John', 'Smith', 'John Doe is a Database Administrator.', 'Database Administrator'),
             ]
    cur.executemany('INSERT INTO person VALUES (?,?,?,?,?,?)', people)
    con.commit()
    con.close()

def fetch_table():
    # Note: The ORDER BY was added to sort the returned list.
    #       con.commit() was not necessary when no modifications are made to the table.
    """ Print entire table by order of lastname. """
    values = []
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    for row in cur.execute('SELECT * FROM person ORDER BY lastname'):
        values.append(row)
    con.close()
    return values

def search_lastname_exact(lastname):
    # Note: Search is case sensitive.
    #       Variable is modified to a tuple before the execute command.
    #       The comma after the variable necessary in sqlite.
    """ Searches for the exact lastname and returns entire row. """
    value = []
    search = (lastname,)
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute('SELECT * FROM person WHERE lastname=?', search)
    value.append(cur.fetchone())
    con.close()
    return value

def search_biography_partial(bio):
    # Note: Search is case insensitive
    #       variable is modified to %variable% and instead of =, LIKE is used
    """ Search for a keyword in biography and returns the first match. """
    value = []
    search = ('%'+ bio +'%',)
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute('SELECT * FROM person WHERE biography LIKE ?', search)
    value = cur.fetchone()
    con.close()
    return value

def search_lastname_partial_fullname(find):
    # Note: The * is replaced with the fields to return, in this case firstname, lastname.
    #       Instead of cur.fetchone(), cur.fetchall() is used to return multiple match results.
    """ Seach of a keyword in lastname and returns all the matches ordered by firstname. """
    values = []
    search = ('%'+ find +'%',)
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute('SELECT firstname, lastname FROM person WHERE lastname LIKE ? ORDER BY firstname', search)
    values = cur.fetchall()
    con.close()
    return values

def main():
    # Note: It is more efficient to keep the connection open and execute each command,
    #       but in this tutorial connecting and closing was used to illustrate the processes needed for each function independently.
    """ How to use each function. """
    drop_table()
    if create_table():
        print('\ntable functions:')
        person = ('Neo', 'ThomasAnderson@gmail.com', 'Thomas', 'Anderson', 'Thomas Anderson is a Computer Programmer.', 'Computer Programmer')
        insert_table(person)
        populate_table()
        items = fetch_table()
        for i in items:
            print(i)

        print('\nsearch functions:')
        sle = search_lastname_exact('Shmo')
        print('lastname match:', sle)

        sbp = search_biography_partial('eng')
        print('biography match:', sbp)

        search = 's'
        print('matches for:', search)
        items = search_lastname_partial_fullname(search)
        for i in items:
            print('    name:', i)

if __name__ == '__main__':
    main()
