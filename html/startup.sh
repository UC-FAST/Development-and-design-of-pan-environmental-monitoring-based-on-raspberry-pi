#!/bin/sh

sudo uwsgi --ini /usr/share/nginx/uwsgi.ini &
sudo nginx -c /usr/share/nginx/nginx.conf
sudo python3 /usr/share/nginx/html/run.py &
