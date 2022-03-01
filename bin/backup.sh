#!/bin/bash

DATE=`date +%Y%m%d`

cd /home/jizhang/timetable/backup
cp ../timetable.db timetable.db.$DATE
gzip timetable.db.$DATE
