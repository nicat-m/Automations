#!/bin/bash
#Script to backup MYSQL databases
set -x
#Set MYSQL variables
MYSQL_USER=""
MYSQL_PASSWORD=""
MYSQL_HOST=""
PORT=30988

#Set the directory where the backups will be stored
BACKUP_DIR="/var/mysql-backup/"

#Set the date
DATE=$(date +"%d-%b-%Y_%H_%M_%S")

#Create backup directory if it does not exist
mkdir -p $BACKUP_DIR

#Delete files in the backup directory older than 5 days
find $BACKUP_DIR -name "*.gz" -mtime +5 -exec rm {} \;

#Backup all databases
databases=$(mysql -u $MYSQL_USER -h $MYSQL_HOST --port $PORT -p$MYSQL_PASSWORD -e 'SHOW DATABASES;' | grep -Ev "(Database|information_schema|performance_schema|testdb|my_database)")

for db in $databases; do
    mysqldump --events --ignore-table=mysql.event --routines --triggers --log-error="$BACKUP_DIR$db_$DATE.err" -u$MYSQL_USER -h $MYSQL_HOST --port $PORT -p$MYSQL_PASSWORD $db | gzip > "$BACKUP_DIR$db"_$DATE.sql.gz

    #Log the output
    if [ $? -eq 0 ]; then
        echo "Database backup success for $db on $DATE" >> "$BACKUP_DIR/backup_success.log"
    else
        echo "Database backup failed for $db on $DATE" >> "$BACKUP_DIR/backup_error.log"
fi

done
