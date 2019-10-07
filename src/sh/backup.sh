#!/bin/bash
# cron 
# 0 2 * * * bash  /var/www/datasciencevault/current/src/sh/backup.sh

source /var/www/datasciencevault/current/env2/bin/activate
python /var/www/datasciencevault/current/src/manage.py dbbackup -s datasciencevalut --settings=project.settings.production
