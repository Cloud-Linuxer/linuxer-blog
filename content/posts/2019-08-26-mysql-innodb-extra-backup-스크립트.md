---
title: "mysql innodb extra backup 스크립트"
date: 2019-08-26T21:42:45+09:00
draft: false
categories: ["Linux"]
tags: ["mysql", "backup", "extra", "script"]
slug: "mysql-innodb-extra-backup-스크립트"
aliases:
  - /mysql-innodb-extra-backup-스크립트/
  - /mysql-innodb-extra-backup-%ec%8a%a4%ed%81%ac%eb%a6%bd%ed%8a%b8/
---

\n

#엑스트라 백업 설치  
rpm -Uhv <https://www.percona.com/redir/downloads/percona-release/redhat/percona-release-0.1-4.noarch.rpm>

\n\n\n\n

#yum 으로 설치  
yum install xtrabackup

\n\n\n\n

#디렉토리 확인  
ll /backup  
ll /backup/full\_backup  
ll /backup/incre\_backup

\n\n\n\n

#디렉토리 생성  
mkdir /backup  
mkdir /backup/full\_backup  
mkdir /backup/incre\_backup

\n\n\n\n

#crontab 에 설정   
\* \*/1 \* \* \* root /root/bin/mysql\_innodb\_backup.sh

\n\n\n\n

crontab 와 db\_full\_backup\_time 은 중요합니다.스크립스트는 crontab 실행될때 백업이 되며, db\_full\_backup\_time이 아닐경우 차등백업을 실행합니다.

\n\n\n\n

따라서 1시간마다 백업을하며 db\_full\_backup\_time이 있을경우에 full 백업을 합니다.

\n\n\n\n

아래의 스크립트에서 03 15을 변수로 줄경우 배열로 받아서 참일경우 full 백업 거짓일경우 차등백업을 진행합니다.따라서 새벽 3시 오후3시에 백업을 진행 합니다.

\n\n\n\n

# !/bin/bash

\n\n\n\n

# DB Backup

\n\n\n\n

BAK\_DIR=/backup;  
\nTODAY=$(date +%Y%m%d --date '12 hours ago')

\n\n\n\n

# TODAY=$(date +%Y%m%d)

\n\n\n\n

RMTODAY=$(date +%Y%m%d --date '10 days ago')

\n\n\n\n

# Delete DB File

\n\n\n\n

rm -rf $BAK\_DIR/full\_backup/$RMTODAY\*  
\nrm -rf $BAK\_DIR/incre\_backup/$RMTODAY\*

\n\n\n\n

## Backup Time

\n\n\n\n

db\_full\_backup\_time=("03 15")

\n\n\n\n

## Now Time & Time Check

\n\n\n\n

TOTIME=$(date +%H)

\n\n\n\n

# TOTIME=$(date +%H)

\n\n\n\n

echo $TOTIME  
\nin\_array() {  
\n local needle array value  
\n needle="${1}"; shift; array=("${@}")  
\n for value in ${array[@]}; do [ "${value}" == "${needle}" ] && echo "true" && return; done  
\n echo "false"  
\n}

\n\n\n\n

db\_full\_backup\_check=`in_array $TOTIME ${db_full_backup_time[@]}`

\n\n\n\n

if [ "$db\_full\_backup\_check" == "true" ]; then  
 # full backup  
 /bin/nice -n 10 /usr/bin/ionice -c2 -n 7 /usr/bin/innobackupex --defaults-file=/etc/my.cnf \\  
 --user=root --password='1234' --slave-info --no-timestamp \\  
 --compress $BAK\_DIR/full\_backup/$TODAY  
 else  
 # hot backup  
 /bin/nice -n 10 /usr/bin/ionice -c2 -n 7 /usr/bin/innobackupex --defaults-file=/etc/my.cnf \\  
 --user=root --password='1234' --no-timestamp --compress --incremental \\  
 --incremental-basedir=$BAK\_DIR/full\_backup/$TODAY $BAK\_DIR/incre\_backup/$TODAY/$TOTIME  
 fi

\n