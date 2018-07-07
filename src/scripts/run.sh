#! /bin/bash

# script for a cron job to run hourly parser

# put proper directories before deployment
source /var/www/datasciencevault/current/env2/bin/activate
python /var/www/datasciencevault/current/src/manage.py runscript parser --settings=project.settings.production



# cron job - temp
# 0 * * * *	bash /var/www/datasciencehub/current/src/scripts/run.sh
