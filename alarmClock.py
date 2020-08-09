# importing modules

import sqlite3
import pyinputplus as pyip
from pytube import YouTube

def printMenu():
    print('---- MAIN MENU ----')
    print('1. DB')
    print('2. ALARM CLOCK')
    print('3. EXIT')
    action = ''
    choice = pyip.inputChoice(['1', '2', 'ALARM CLOCK', 'ALARM', 'CLOCK', '2. ALARM CLOCK', 'DB', '1. DB', '3', 'EXIT', '3. EXIT'], 'CHOOSE ACTION: ')
    choice = choice.upper()
    if choice == '1' or choice == 'DB' or choice == '1. DB':
        action = 'DB'
    elif choice == '2' or choice == 'ALARM' or choice == 'ALARM CLOCK' or choice == 'CLOCK' or choice == 'ALARM CLOCK':
        action = 'ALARM CLOCK'
    elif choice == '3' or choice == 'EXIT' or choice == '3. EXIT':
        action = 'EXIT'

    return action

def printMenuDB():
    print('---- DB MENU ----')
    print('1. List all links with titles.')
    print('2. Add new entry.')
    print('3. Delete some entry.')
    print('4. EXIT')
    actionDB = ''
    choice = pyip.inputChoice(['1', '2', '3', '4'], 'CHOOSE (1/2/3/4): ')
    if choice == '1':
        actionDB = 'LIST'
    elif choice == '2':
        actionDB = 'ADD'
    elif choice == '3':
        actionDB = 'DELETE'

    return actionDB


def addNewEntry():
    ytLink = pyip.inputURL('Provide YT Link: ')
    # Trying to create YT object
    try:
        # check if yt link is valid by creating YT object
        yt = YouTube(ytLink)
        cur.execute('INSERT INTO YTLINKS VALUES(NULL, ?, ?);', (ytLink, yt.title))
        # commit changes in the DB
        con.commit()

    except:
        print('Error occured. It could be connection error or check your URL validity')


def listAllEntries():
    # function get and list data from DB
    cur.execute('SELECT * FROM YTLINKS')
    records = cur.fetchall()
    for record in records:
        print(record['ID'], record['TITLE'], record['LINK'])

# creating connection with DB
con = sqlite3.connect('ytLinks.db')

# access to the columns by indexes and names
con.row_factory = sqlite3.Row

# creating cursor object
cur = con.cursor()

# creating table with YT Links
cur.execute('''
    CREATE TABLE IF NOT EXISTS YTLINKS (
        ID INTEGER PRIMARY KEY ASC,
        LINK VARCHAR(250) NOT NULL,
        TITLE VARCHAR(250) DEFAULT ''
        )''')

# create main loop , menu , and interface to adding new links, deleting and listing

program = True

# main loop
while program:
    action = printMenu() # possible results: DB, EXIT, ALARM CLOCK
    if action == 'EXIT':
        program = False
    elif action == 'DB':
        dbAction = printMenuDB() # possible results: LIST, ADD, DELETE
        if dbAction == 'ADD':
            addNewEntry()
        elif dbAction == 'LIST':
            listAllEntries()

