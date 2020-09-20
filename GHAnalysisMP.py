import os
import argparse
import json
import multiprocessing
import shutil


def init(directory):
    if os.path.exists('tempdata'):
        shutil.rmtree('tempdata')
    os.mkdir('tempdata')
    pool = multiprocessing.Pool()
    for fileName in os.listdir(directory):
        if fileName.endswith(".json"):
            pool.apply_async(read, (directory, fileName,))
    pool.close()
    pool.join()
    userData = {}
    repoData = {}
    userRepoData = {}
    for fileName in os.listdir('tempdata'):
        if fileName.endswith(".json"):
            with open('tempdata/' + fileName, 'r', encoding='utf-8') as file:
                for line in file:
                    data = json.loads(line)
                    if not userData.get(data['actor_login']):
                        userData[data['actor_login']] = {}
                        userRepoData[data['actor_login']] = {}
                    userData[data['actor_login']][data['type']] = userData[data['actor_login']].get(
                        data['type'], 0) + 1
                    if not repoData.get(data['repo_name']):
                        repoData[data['repo_name']] = {}
                    repoData[data['repo_name']][data['type']] = repoData[data['repo_name']].get(
                        data['type'], 0) + 1
                    if not userRepoData[data['actor_login']].get(data['repo_name']):
                        userRepoData[data['actor_login']
                                     ][data['repo_name']] = {}
                    userRepoData[data['actor_login']][data['repo_name']][data['type']
                                                                         ] = userRepoData[data['actor_login']][data['repo_name']].get(data['type'], 0)+1
    with open('1.json', 'w', encoding='utf-8') as file:
        json.dump(userData, file)
    with open('2.json', 'w', encoding='utf-8') as file:
        json.dump(repoData, file)
    with open('3.json', 'w', encoding='utf-8') as file:
        json.dump(userRepoData, file)
    shutil.rmtree('tempdata')
    print(0)


def read(directory, fileName):
    with open(directory + '/' + fileName, 'r', encoding='utf-8') as file1, open('tempdata/' + fileName, 'a', encoding='utf-8') as file2:
        for line in file1:
            data = json.loads(line)
            temp = {}
            temp['actor_login'] = data['actor']['login']
            temp['repo_name'] = data['repo']['name']
            temp['type'] = data['type']
            json.dump(temp, file2)
            file2.write("\n")


def query(query_type, user="", repo="", event=""):
    if query_type == 0:
        # 查用户事件数
        with open('1.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            result = data[user].get(event, 0)
    elif query_type == 1:
        # 查仓库事件数
        with open('2.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            result = data[repo].get(event, 0)
    elif query_type == 2:
        # 查用户在仓库的事件数
        with open('3.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            if data[user].get(repo, 0):
                result = data[user][repo].get(event, 0)
            else:
                result = 0
    print(result)
    return result


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
        # 未初始化
        if not os.path.exists('1.json'):
            raise RuntimeError('Error: Initialization is required.')
        elif args.event:
            if args.user:
                if args.repo:
                    # 三个参数都提供即为第 3 种查询
                    query(2, user=args.user, repo=args.repo, event=args.event)
                else:
                    query(0, user=args.user, event=args.event)
            elif args.repo:
                query(1, repo=args.repo, event=args.event)
            else:
                raise RuntimeError('Error: Argument -l or -c is required.')
        else:
            raise RuntimeError('Error: Argument -e is required.')
