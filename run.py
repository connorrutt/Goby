#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
import hashlib
import tempfile
import shutil
import traceback
import requests


requests.packages.urllib3.disable_warnings()

# 获取文件md5


def file2md5(_file):
    with open(_file, 'rb') as f:
        md5obj = hashlib.md5()
        md5obj.update(f.read())
        return md5obj.hexdigest()

# 搜索代码


def searchcode(keyword, page=1, per_page=100):
    headers = {
        'Authorization': 'token {}'.format(os.getenv('GH_TOKEN')),
        'Connection': 'close',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36'
    }
    data = {'q': keyword, 'sort': 'indexed',
            'order': 'desc', 'page': page, 'per_page': per_page}
    try:
        rj = requests.get('https://api.github.com/search/code', params=data,
                          headers=headers, verify=False, allow_redirects=False, timeout=10).json()
        return rj
    except:
        return {}


if __name__ == '__main__':
    # 旧poc
    old_poc = {}
    for path in ['go', 'json']:
        for file in os.listdir(path):
            if not file.endswith('.json') and not file.endswith('.go'):
                continue
            old_poc[file2md5(os.path.join(path, file))] = 0

    root_path = os.path.dirname(os.path.abspath(__file__))
    print(root_path)
    # 搜索代码获取项目主页
    html_urls = ["https://github.com/helloexp/0day","https://github.com/Micr067/0day","https://github.com/fei9747/0day-1","https://github.com/merlinepedra/ODAY","https://github.com/takeboy/https-github.com-Lucifer1993-0day","https://github.com/wukong-bin/PeiQi-0day","https://github.com/jusk9527/GobyPoc","https://github.com/GGStudy-DDUp/0day","https://github.com/sunpeak/wiki","https://github.com/terry494/fengchenzxc.github.io","https://github.com/n0tfund404/nday","https://github.com/yuag/goby","https://github.com/york-cmd/CVE-2022-22947-goby","https://github.com/H4ckTh3W0r1d/Goby_POC","https://github.com/AnonymouID/POC","https://github.com/luck-ying/Library-POC","https://github.com/cckuailong/vulbase","https://github.com/xanszZZ/pocsuite3-poc","https://github.com/ChrR0m4n/Sword-Framework","https://github.com/aetkrad/goby_poc","https://github.com/k3vi-07/goby-exp","https://github.com/H4K6/Goby-POC","https://github.com/wgpsec/peiqi-wiki","https://github.com/XingHuoLiaoYuanBaby/goby_poc","https://github.com/shifeige/goby-poc","https://github.com/merlinepedra25/SCAN4ALL-1","https://github.com/zeroChen00/vulnerability_database"]
    for keyword in ['GobyQuery+language:Go', 'GobyQuery+language:Json']:
        for i in range(1, 6):
            try:
                rs = searchcode(keyword, page=i, per_page=100)
                html_urls += [item['repository']['html_url']
                              for item in rs.get('items', []) if item.get('repository', {}).get('html_url')]
            except:
                traceback.print_exc()
    html_urls = set(html_urls)
    for url in html_urls:
        print(url)
        try:
            temp_dir = tempfile.TemporaryDirectory().name
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir)
            os.chdir(temp_dir)
            # clone项目
            os.system('git clone {}'.format(url))
            author, repo = url[19:].split('/', 1)
            repo_path = os.path.join(temp_dir, repo)
            print(repo_path)
            # 复制poc
            if os.path.exists(repo_path):
                for root, _, files in os.walk(repo_path):
                    for file in files:
                        if not file.endswith('.json') and not file.endswith('.go'):
                            continue
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, 'r', encoding='utf8') as f:
                                content = f.read()
                            if 'GobyQuery' in content and 'ScanSteps' in content:
                                print(file_path)
                                md5 = file2md5(file_path)
                                if md5 not in old_poc:
                                    if file.endswith('.json'):
                                        shutil.copyfile(file_path, os.path.join(
                                            root_path, 'json', file))
                                    if file.endswith('.go'):
                                        shutil.copyfile(file_path, os.path.join(
                                            root_path, 'go', file))
                        except:
                            traceback.print_exc()
            os.chdir(root_path)
        except:
            traceback.print_exc()
    os.chdir(root_path)
    with open('README.md', 'w', encoding='utf8') as f:
        f.write('# Goby POC统计\n| 文件类型 | 数量 |\n| :----:| :----: |\n| .go | {} |\n| .json | {} |'.format(
            len([file for file in os.listdir('go') if file.endswith('.go')]), len([file for file in os.listdir('json') if file.endswith('.json')])))
