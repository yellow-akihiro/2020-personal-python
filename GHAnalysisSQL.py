import os
import argparse
import json
import sqlite3


# getCount1 = 'SELECT * FROM GITHUB WHERE user_name=? AND event=?'
# getCount2 = 'SELECT * FROM GITHUB WHERE repo_name=? AND event=?'
# getCount3 = 'SELECT * FROM GITHUB WHERE user_name=? AND repo_name=? AND event=?'
# value = connector.execute(getCount1, ('waleko', 'PushEvent'))
# print(len(list(value)))
# value = connector.execute(getCount2, ('katzer/cordova-plugin-background-mode', 'PushEvent'))
# print(len(list(value)))
# value = connector.execute(getCount3, ('cdupuis', 'atomist/automation-client', 'PushEvent'))
# print(len(list(value)))
# connector.close()

def init(directory):
    # 初始化建表
    connector = sqlite3.connect("data.db")
    connector.execute('DROP TABLE IF EXISTS GITHUB;')
    connector.execute('''CREATE TABLE GITHUB (
                user_name   TEXT NOT NULL,
                repo_name   TEXT NOT NULL,
                event       TEXT NOT NULL
                );''')
    connector.commit()
    for fileName in os.listdir(directory):
        if fileName.endswith(".json"):
            fullPath = directory + '/' + fileName
            with open(fullPath, 'r', encoding='utf-8') as file:
                for line in file:
                    # 读取 json 文件中一行并暂存有效数据
                    data = json.loads(line)
                    insertData = (data['actor']['login'],
                                  data['repo']['name'], data['type'])
                    sqlInsert = 'INSERT INTO GITHUB(user_name, repo_name, event) VALUES(?, ?, ?)'
                    connector.execute(sqlInsert, insertData)
    # 实际写入文件
    connector.commit()
    pass


def query_user():
    pass


def query_repo():
    pass


def query_user_and_repo():
    pass


if __name__ == '__main__':
    # 设置接受的参数
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i', '--init', help='Initialize the database with files in the folder given.')
    parser.add_argument('-u', '--user', help='Provide a user name.')
    parser.add_argument('-r', '--repo', help='Provide a repository\'s name.')
    parser.add_argument('-e', '--event', help='Provide a type of events.')
    # 处理传入的参数
    args = parser.parse_args()
    if args.init:
        init(args.init)
    else:
        if not os.path.exists('data.db'):
            raise RuntimeError('Error: Please initialize first.')
        elif args.event:
            if args.user:
                if args.repo:
                    query_user_and_repo()
                else:
                    query_user()
            elif args.repo:
                query_repo()
            else:
                raise RuntimeError('Error: Argument -l or -c is required.')
        else:
            raise RuntimeError('Error: Argument -e is required.')
