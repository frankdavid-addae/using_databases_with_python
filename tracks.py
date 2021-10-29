import sqlite3
import xml.etree.ElementTree as ET

dbCon = sqlite3.connect('trackdb.sqlite')
cursor = dbCon.cursor()

# Create database tables using executescript
cursor.executescript('''
DROP TABLE IF EXISTS artist;
DROP TABLE IF EXISTS album;
DROP TABLE IF EXISTS track;

CREATE TABLE artist (
    artistId  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    artistName    TEXT UNIQUE
);

CREATE TABLE album (
    albumId  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    artistId  INTEGER,
    albumTitle   TEXT UNIQUE
);

CREATE TABLE track (
    id  INTEGER NOT NULL PRIMARY KEY 
        AUTOINCREMENT UNIQUE,
    trackTitle TEXT  UNIQUE,
    albumId  INTEGER,
    trackLength INTEGER, 
    trackRating INTEGER, 
    trackPlayCount INTEGER
);
''')

fileName = input('Enter file name: ')
if len(fileName) < 1:
    fileName = 'library.xml'


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
    if lookup(track, 'Track ID') is None:
        continue

    name = lookup(track, 'Name')
    artist = lookup(track, 'Artist')
    album = lookup(track, 'Album')
    count = lookup(track, 'Play Count')
    rating = lookup(track, 'Rating')
    length = lookup(track, 'Total Time')

    if name is None or artist is None or album is None:
        continue

    print(name, artist, album, count, rating, length)

    cursor.execute('''INSERT OR IGNORE INTO artist (artistName) 
        VALUES ( ? )''', (artist,))
    cursor.execute('SELECT artistId FROM artist WHERE artistName = ? ', (artist,))
    artistId = cursor.fetchone()[0]

    cursor.execute('''INSERT OR IGNORE INTO album (albumTitle, artistId) 
        VALUES ( ?, ? )''', (album, artistId))
    cursor.execute('SELECT albumId FROM album WHERE albumTitle = ? ', (album,))
    albumId = cursor.fetchone()[0]

    cursor.execute('''INSERT OR REPLACE INTO track
        (trackTitle, albumId, trackLength, trackRating, trackPlayCount) 
        VALUES ( ?, ?, ?, ?, ? )''', (name, albumId, length, rating, count))

    dbCon.commit()
