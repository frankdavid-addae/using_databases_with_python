import sqlite3

dbCon = sqlite3.connect('emailDB.sqlite')
cursor = dbCon.cursor()

cursor.execute('DROP TABLE IF EXISTS Counts')

cursor.execute('CREATE TABLE Counts (email TEXT, count INTEGER)')

fileName = input('Enter file name: ')
if len(fileName) < 1:
    fileName = 'mbox-short.txt'
fileHandle = open(fileName)
for line in fileHandle:
    if not line.startswith('From: '):
        continue
    pieces = line.split()
    email = pieces[1]
    cursor.execute('SELECT count FROM Counts WHERE email = ? ', (email,))
    row = cursor.fetchone()
    if row is None:
        cursor.execute('INSERT INTO Counts (email, count) VALUES (?, 1)', (email,))
    else:
        cursor.execute('UPDATE Counts SET count = count + 1 WHERE email = ?', (email,))
    dbCon.commit()

sqlStr = 'SELECT email, count FROM Counts ORDER BY count DESC LIMIT 10'

for row in cursor.execute(sqlStr):
    print(str(row[0]), row[1])
cursor.close()
