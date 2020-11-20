#!/usr/bin/python3
# coding: utf-8

whites = ['100']

with open('ip.txt', 'w+') as f:
    for x in range(130, 0, -1):
        if str(x) not in whites:
            ip = f'172.16.{x}.240'
            f.write(f'{ip}\n')