import os
import argparse
import json
import sqlite3

con = sqlite3.connect("data.db")
cursor = con.cursor()
con.execute('DROP TABLE IF EXISTS GITHUB;')
con.execute('''CREATE TABLE GITHUB (
            user_name   TEXT NOT NULL,
            repo_name   TEXT NOT NULL,
            event       TEXT NOT NULL
            );''')
con.commit()
for fileName in os.listdir('./'):
    if fileName.endswith(".json"):
        with open(fileName, 'r', encoding='utf-8') as file:
            for line in file:
                data = json.loads(line)
                insertData = (data['actor']['login'], data['repo']['name'], data['type'])
                sqlInsert = 'INSERT INTO GITHUB(user_name, repo_name, event) VALUES(?, ?, ?)'
                con.execute(sqlInsert, insertData)
con.commit()
getCount1 = 'SELECT * FROM GITHUB WHERE user_name=? AND event=?'
getCount2 = 'SELECT * FROM GITHUB WHERE repo_name=? AND event=?'
getCount3 = 'SELECT * FROM GITHUB WHERE user_name=? AND repo_name=? AND event=?'
# value = con.execute(getCount1, ('waleko', 'PushEvent'))
# print(len(list(value)))
# value = con.execute(getCount2, ('katzer/cordova-plugin-background-mode', 'PushEvent'))
# print(len(list(value)))
# value = con.execute(getCount3, ('cdupuis', 'atomist/automation-client', 'PushEvent'))
# print(len(list(value)))
con.close()