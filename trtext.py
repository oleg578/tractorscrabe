import requests
from pyquery import PyQuery as pq
import mariadb
import sys
import json
import time

def parse_page(link):
    page = requests.get(link)
    d = pq(page.content)
    page_text = d(".tdArticleGroup").text()
    rows = str(page_text).split("\n")
    tractor = dict()
    data = []
    for row in rows:
        r = row.strip()
        if len(r)>0:
            data.append(row.strip())
    index = 0
    if len(data)<2:
        return tractor
    tractor['Description'] = "%s %s" % (data[0], data[1])
    for row in data:
        row = row.strip(":")
        if row[-6:] == 'Series':
            tractor['Series'] = data[index+1]
        if row[-12:] == 'Manufacturer':
            tractor['Manufacturer'] = data[index+1]
        if row[-4:] == 'Type':
            tractor['Type'] = data[index+1]
        if row[-7:] == 'Factory':
            tractor['Factory'] = data[index+1]
        if row[-6:] == 'Engine' and len(row)<7:
            if (index+2) < (len(data)-1):
                tractor['Engine'] = "%s %s" % (data[index+1], data[index+2])
            else:
                tractor['Engine'] = data[index+1]
        if row[-6:] == 'Engine' and len(row)>=7:
                tractor['Engine'] = data[index+1]
        if row[-7:] == 'Chassis':
            tractor['Chassis'] = data[index+1]
        if row[-8:] == 'Steering':
            tractor['Steering'] = data[index+1]
        if row[-6:] == 'Brakes':
            tractor['Brakes'] = data[index+1]
        if row[-3:] == 'Cab':
            tractor['Cab'] = data[index+1]
        if row[-12:] == 'Transmission':
            tractor['Transmission'] = data[index+1]
        if row[-6:] == 'Weight':
            if (index+2) < (len(data)-1):
                tractor['Weight'] = "%s %s" % (data[index+1], data[index+2])
            else:
                tractor['Weight'] = data[index+1]
        index +=1
    return tractor

# Connect to MariaDB Platform
try:
    conn = mariadb.connect(
            user="root",
            database="tractors",
            unix_socket="/tmp/mysql.sock"
            #unix_socket="/run/mysqld/mysqld.sock"
            )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB: {e}")
    sys.exit(1)

# check conn
if not conn:
    print("connecting to MariaDB is null")
    sys.exit(1)

# Get Cursor
cur = conn.cursor()
model_sql = "SELECT `ID`,`Link` from `model`"
m_json_append_sql = "INSERT INTO `model_json` VALUES(?,?) ON DUPLICATE KEY UPDATE `ModelJSON`=?"

cur = conn.cursor(dictionary=True)

cur.execute(model_sql)

rows = cur.fetchall()
for col in rows:
    tractor = parse_page(col['Link'])
    t_dump = json.dumps(tractor)
    cur.execute(m_json_append_sql, (col['ID'], t_dump, t_dump))
    conn.commit()
    time.sleep(0.5)

conn.close()
