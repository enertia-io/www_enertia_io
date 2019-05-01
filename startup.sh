#!/bin/sh
cd /opt/www*
eval "$(ssh-agent -s)"
chmod 600 /root/.ssh/id_rsa
ssh-add /root/.ssh/id_rsa
caddy --conf Caddyfile
