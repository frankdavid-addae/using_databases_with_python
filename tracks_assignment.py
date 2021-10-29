import xml.etree.ElementTree as ET
import sqlite3

dbCon = sqlite3.connect('track_db.sqlite')
cursor = dbCon.cursor()

# Make some fresh tables using executescript()
cursor.executescript('''
DROP TABLE IF EXISTS Artist;
DROP TABLE IF EXISTS Album;
DROP TABLE IF EXISTS Track;
DROP TABLE IF EXISTS Genre;

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
);
''')

fileName = input('Enter file name: ')
if len(fileName) < 1:
    fileName = 'assignment_library.xml'


# <key>Track ID</key><integer>369</integer>
# <key>Name</key><string>Another One Bites The Dust</string>
# <key>Artist</key><string>Queen</string>
def lookup(d, key):
    found = False
    for child in d:
        if found:
            return child.text
        if child.tag == 'key' and child.text == key:
            found = True
    return None


stuff = ET.parse(fileName)
tracks = stuff.findall('dict/dict/dict')
print('Dict count:', len(tracks))
for track in tracks:
    if lookup(track, 'Track ID') is None: continue

    name = lookup(track, 'Name')
    artist = lookup(track, 'Artist')
    genre = lookup(track, 'Genre')
    album = lookup(track, 'Album')
    count = lookup(track, 'Play Count')
    rating = lookup(track, 'Rating')
    length = lookup(track, 'Total Time')

    if name is None or artist is None or album is None or genre is None:
        continue

    print(name, artist, genre, album, count, rating, length)

    cursor.execute('''INSERT OR IGNORE INTO Artist (name) 
        VALUES ( ? )''', (artist,))
    cursor.execute('SELECT id FROM Artist WHERE name = ? ', (artist,))
    artist_id = cursor.fetchone()[0]

    cursor.execute('''INSERT OR IGNORE INTO Genre (name) 
            VALUES ( ? )''', (genre,))
    cursor.execute('SELECT id FROM Genre WHERE name = ? ', (genre,))
    genre_id = cursor.fetchone()[0]

    cursor.execute('''INSERT OR IGNORE INTO Album (title, artist_id) 
        VALUES ( ?, ? )''', (album, artist_id))
    cursor.execute('SELECT id FROM Album WHERE title = ? ', (album,))
    album_id = cursor.fetchone()[0]

    cursor.execute('''INSERT OR REPLACE INTO Track
        (title, album_id, genre_id, len, rating, count) 
        VALUES ( ?, ?, ?, ?, ?, ? )''', (name, album_id, genre_id, length, rating, count))

    dbCon.commit()
