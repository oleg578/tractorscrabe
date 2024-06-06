import requests
from time import sleep
from pyquery import PyQuery as pq
import mariadb
import sys

def load_tractors(category_link):
    page = requests.get(category_link)
    d = pq(page.content)
    links = d("table.tdMenu1 td:not([align]):not([class])>a")
    t = dict()
    for link in links:
        t[link.text] = link.attrib['href']
    sleep(0.5)
    return t

def load_models(mfu_link):
    page = requests.get(mfu_link)
    d = pq(page.content)
    links = d("#tddbTable a")
    t = dict()
    for link in links:
        t[link.text] = link.attrib['href'] 
    sleep(0.5)
    return t

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
tractor_query = "INSERT INTO `model` VALUES(?,?,?,?,?) ON DUPLICATE KEY UPDATE `Category`=?,`Manufacturer`=?,`Model`=?,`Link`=?"
# main

node_num = 0

categories = {
        'farm': "https://www.tractordata.com/farm-tractors/index.html", 
        'lawn': "https://www.tractordata.com/lawn-tractors/index.html"
        }
for category, cat_link in categories.items():
    manufacturers = load_tractors(cat_link)
    for manufacturer, mfu_link in manufacturers.items():
        models = load_models(mfu_link)
        for model, mod_link in models.items():
            #print("%s: %s: %s => %s" %(category,manufacturer, model, mod_link))
            try:
                node_num +=1
                cur.execute(tractor_query,
                            (node_num,category,manufacturer,model,mod_link,category,manufacturer,model,mod_link))
            except mariadb.Error as e:
                print(f"Error: {e}")
                sys.exit(1)
            conn.commit()

conn.close()
