import requests
from pyquery import PyQuery as pq
import mariadb
import sys
import json
import time

def is_odd(i):
    if  i % 2 == 0:
        return True
    else:
        return False

def parse_page(link):
    dimension = dict()
    if link == '':
        return dimension
    page = requests.get(link)
    d = pq(page.content)
    tbs = d(".tdArticleGroup>.tdArticleItem").eq(2)
    index = 0
    key = ""
    for d in tbs('td:not([colspan])').items():
        if is_odd(index):
            key = str(d.text()).strip().rstrip(":").replace("/", " ").replace("\u00b0", ' "')
        else:
            dimension[key] = str(d.text()).strip().replace("/", " ").replace("\n", " | ").replace("\u00b0", ' "')
            key = ""
        index += 1
    return dimension

def get_m_link(link):
    engine_link = ""
    page = requests.get(link)
    d = pq(page.content)
    links = d(".tractornav li>a")
    for a in links:
        if a.text.strip().lower() == 'attachments':
            engine_link = a.attrib['href']
            return engine_link
    return engine_link
    

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
m_json_append_sql = "INSERT INTO `model_attachments_json` VALUES(?,?) ON DUPLICATE KEY UPDATE `AttachmentsJSON`=?"

cur = conn.cursor(dictionary=True)

cur.execute(model_sql)

rows = cur.fetchall()
for col in rows:
    m_link = get_m_link(col['Link'])
    m = parse_page(m_link)
    # save data
    e_dump = json.dumps(m)
    cur.execute(m_json_append_sql, (col['ID'], e_dump, e_dump))
    conn.commit()
    break
    time.sleep(0.5)
conn.close()
