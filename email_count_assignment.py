import sqlite3

dbCon = sqlite3.connect('orgDB.sqlite')
cursor = dbCon.cursor()

cursor.execute('DROP TABLE IF EXISTS Counts')

cursor.execute('CREATE TABLE Counts (org TEXT, count INTEGER)')

fileName = input('Enter file name: ')
if len(fileName) < 1:
    fileName = 'mbox.txt'
fileHandle = open(fileName)
for line in fileHandle:
    if not line.startswith('From: '):
        continue
    pieces = line.split()[1]
    org = pieces.split('@')[1]

    cursor.execute('SELECT count FROM Counts WHERE org = ? ', (org,))
    row = cursor.fetchone()
    if row is None:
        cursor.execute('INSERT INTO Counts (org, count) VALUES (?, 1)', (org,))
    else:
        cursor.execute('UPDATE Counts SET count = count + 1 WHERE org = ?', (org,))
dbCon.commit()

sqlStr = 'SELECT org, count FROM Counts ORDER BY count DESC LIMIT 10'

for row in cursor.execute(sqlStr):
    print(str(row[0]), row[1])
cursor.close()
