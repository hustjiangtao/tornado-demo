#!/bin/bash
# deploy for tornado_demo include nginx conf & supervisor conf

cp /home/jiangtao/tornado-demo/deploy/nginx/tornado_demo.conf /etc/nginx/conf.d/tornado_demo.conf
cp /home/jiangtao/tornado-demo/deploy/supervisor/tornado_demo.ini /etc/supervisord.d/tornado_demo.ini
nginx -s reload
supervisorctl update
