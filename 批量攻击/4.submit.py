#!/usr/bin/python3
# coding: utf-8

import requests

url = 'http://192.168.100.80/index.php'

def submit(flag):
    flag = flag.split('@')

    back_data = {'token': 'xxx', 'flag': flag[0], 'ip': flag[1]}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.74 Safari/537.36 Edg/79.0.309.43',
        'Cookie': 'PHPSESSID=al9fueke3j06ggu128kjl3aoti; _csrf=27ecbf8e6853320037636898dfbe775a15fa2d7417bcf7167638ae6deccc18b9a:2:{i:0;s:5:"_csrf";i:1;s:32:"NqtD-77fniA4YW6nrQgovtlPWU0XbMyC";}'
    }
    try:
        req = requests.post(url=url, data=back_data, timeout=3)
    except:
        print('[-] 平台连接失败')
    if req.status_code == 200:
        if '成功' in req.text:
            print(f'[+] {flag[1]} 提交成功')
        else:
            print(f'[-] {flag[1]} 提交失败')
    else:
        print('[-] 平台响应失败')

def main():
    with open('flag.txt', 'r') as f:
        for flag in f.readlines():
            submit(flag.strip())

main()