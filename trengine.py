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
    engine = dict()
    page = requests.get(link)
    d = pq(page.content)
    # get description
    tbs = d(".tdArticleGroup>.tdArticleItem").eq(2)
    engine['Description'] = ""
    for title in tbs('td[colspan]').filter(lambda i: i > 0).items():
        engine['Description'] += "%s " % (title.text())
    engine['Description'] = engine['Description'].strip()
    # get rest data
    index = 0
    key = ""
    for d in tbs('td:not([colspan])').items():
        if is_odd(index):
            key = str(d.text()).strip().rstrip(":").replace("/", " ")
        else:
            engine[key] = str(d.text()).strip().replace("/", " ").replace("\n", " | ")
            key = ""
        index += 1
    return engine

def get_engine_link(link):
    engine_link = ""
    page = requests.get(link)
    d = pq(page.content)
    links = d(".tractornav li>a")
    for a in links:
        if a.text.strip().lower() == 'engine':
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
m_json_append_sql = "INSERT INTO `model_engine_json` VALUES(?,?) ON DUPLICATE KEY UPDATE `EngineJSON`=?"

cur = conn.cursor(dictionary=True)

cur.execute(model_sql)

rows = cur.fetchall()
for col in rows:
    engine_link = get_engine_link(col['Link'])
    engine = parse_page(engine_link)
    # save engine data
    e_dump = json.dumps(engine)
    cur.execute(m_json_append_sql, (col['ID'], e_dump, e_dump))
    conn.commit()
    time.sleep(0.5)
conn.close()
