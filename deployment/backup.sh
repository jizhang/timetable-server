#!/bin/bash

cd /root/mysql-backup
DATE=`date +%Y%m%d`
mysqldump -uroot --databases timetable quark | gzip >$DATE.sql.gz
