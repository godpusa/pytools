#!/usr/bin/env python3

###########################################################
#
# This python script is used for mysql like database backup
# using mysqldump and tar utility.
#
# Written by : Rahul Kumar
# modified by Adam Xu
# Last modified: Nov 20, 2018
# Tested with : Python 3.6
# Script Revision: 1.0
#
##########################################################

# Import required python libraries

import os
from time import strftime
#import datetime
from shlex import quote

# MySQL database details to which backup to be done. Make sure below user having enough privileges to take databases backup.
# you can create any file like /backup/dbnames.txt and put databases names one on each line and assigned to DB_NAME variable.
# or you can put all you dbnames seperated by space as chracters to DB_NAME variable.
DB_HOST = 'localhost'
DB_USER = 'root'
DB_USER_PASSWORD = '_mysql_user_password_'
#DB_NAME = '/backup/dbnameslist.txt'
DB_NAME = 'dbname1 dbname2 dbname3'
BACKUP_PATH = '/backup/dbbackup'

# Getting current DateTime to create the separate backup folder like "20180817-123433".
DATETIME = strftime('%Y%m%d-%H%M%S')
TODAYBACKUPPATH = BACKUP_PATH + '/' + DATETIME

# Checking if backup folder already exists or not. If not exists will create it.
try:
    os.stat(TODAYBACKUPPATH)
except:
    os.mkdir(TODAYBACKUPPATH)

# Code for checking if you want to take single database backup or assinged multiple backups in DB_NAME.
print ("checking for databases names file.")
if os.path.exists(DB_NAME):
    multi = 1
    print ("Databases file found...")
    print ("Starting backup of all dbs listed in file " + DB_NAME)
else:
    print ("Databases file not found...")
    print ("Starting backup of database " + DB_NAME)
    multi = 0

# Starting actual database backup process.
if multi:
    with open(DB_NAME) as dbfile:
        for db in dbfile:
            db = db.strip()
            dumpcmd = "mysqldump -h " + DB_HOST + " -u " + DB_USER + " -p" + DB_USER_PASSWORD + " " + db + " > " + quote(TODAYBACKUPPATH) + "/" + db + ".sql"
            os.system(dumpcmd)
            gzipcmd = "gzip " + quote(TODAYBACKUPPATH) + "/" + db + ".sql"
            os.system(gzipcmd)
else:
    for db in DB_NAME.split():
        dumpcmd = "mysqldump -h " + DB_HOST + " -u " + DB_USER + " -p" + DB_USER_PASSWORD + " " + db + " > " + quote(TODAYBACKUPPATH) + "/" + db + ".sql"
        os.system(dumpcmd)
        gzipcmd = "gzip " + quote(TODAYBACKUPPATH) + "/" + db + ".sql"
        os.system(gzipcmd)

print ("")
print ("Backup script completed")
print ("Your backups have been created in '" + TODAYBACKUPPATH + "' directory")
