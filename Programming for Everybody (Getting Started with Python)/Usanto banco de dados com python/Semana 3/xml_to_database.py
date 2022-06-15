import xml.etree.cElementTree as ET

import sqlite3

conn = sqlite3.connect('trackdb.sqlite')
cur = conn.cursor()

cur.executescript('''
CREATE TABLE Artist (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);

CREATE TABLE Genre (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);

CREATE TABLE Album (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    artist_id  INTEGER,
    title   TEXT UNIQUE
);

CREATE TABLE Track (
    id  INTEGER NOT NULL PRIMARY KEY 
        AUTOINCREMENT UNIQUE,
    title TEXT  UNIQUE,
    album_id  INTEGER,
    genre_id  INTEGER,
    len INTEGER, rating INTEGER, count INTEGER
);''')


def lookup(node, key):
    found = False
    for child in node:
        if found: return child.text
        if child.tag == 'key' and child.text == key:
            found = True
    return None

file_name = 'Library.xml'
stuff = ET.parse(file_name)
all = stuff.findall('dict/dict/dict')

# print('Dict count.: ', len(all))
for entry in all:
    if(lookup(entry, 'Track ID') is None): continue
    artist = lookup(entry, 'Artist')
    genre = lookup(entry, 'Genre')
    album = lookup(entry, 'Album')
    track = lookup(entry, 'Name')
    size = lookup(entry, 'Size')
    rating = lookup(entry, 'Rating')
    count = lookup(entry, 'Play Count')


    if (artist is None) or (genre is None) or (album is None) or (track is None):
        continue

    print(artist, genre, album, track)

    cur.execute('''INSERT OR IGNORE INTO Artist (name) VALUES (?)''', (artist,))
    cur.execute('SELECT id FROM Artist WHERE name = ?', (artist,))
    artist_id = cur.fetchone()[0]

    cur.execute('''INSERT OR IGNORE INTO Genre (name) VALUES(?)''', (genre,))
    cur.execute('''SELECT id FROM Genre WHERE name = ?''', (genre,))
    genre_id = cur.fetchone()[0]

    cur.execute('''INSERT OR IGNORE INTO Album (title, artist_id) VALUES (?, ?)''',(album, artist_id))
    cur.execute('''SELECT id FROM Album WHERE title = ?''', (album,))
    album_id = cur.fetchone()[0]

    cur.execute('''INSERT OR REPLACE INTO Track (title, album_id, genre_id, len, rating, count) VALUES (?, ?, ?, ?, ?, ?)''', 
        (track, album_id, genre_id, size, rating, count))

    conn.commit()

conn.close()