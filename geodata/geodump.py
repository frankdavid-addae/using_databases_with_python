import sqlite3
import json
import codecs

dbCon = sqlite3.connect('geodata.sqlite')
cursor = dbCon.cursor()

cursor.execute('SELECT * FROM Locations')
fileHandle = codecs.open('where.js', 'w', "utf-8")
fileHandle.write("myData = [\n")
count = 0
for row in cursor:
    data = str(row[1].decode())
    try:
        js = json.loads(str(data))
    except:
        continue

    if not ('status' in js and js['status'] == 'OK'):
        continue

    lat = js["results"][0]["geometry"]["location"]["lat"]
    lng = js["results"][0]["geometry"]["location"]["lng"]
    if lat == 0 or lng == 0:
        continue
    where = js['results'][0]['formatted_address']
    where = where.replace("'", "")
    try:
        print(where, lat, lng)

        count = count + 1
        if count > 1:
            fileHandle.write(",\n")
        output = "[" + str(lat) + "," + str(lng) + ", '" + where + "']"
        fileHandle.write(output)
    except:
        continue

fileHandle.write("\n];\n")
cursor.close()
fileHandle.close()
print(count, "records written to where.js")
print("Open where.html to view the data in a browser")
