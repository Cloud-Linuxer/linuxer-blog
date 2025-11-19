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


#엑스트라 백업 설치
rpm -Uhv <https://www.percona.com/redir/downloads/percona-release/redhat/percona-release-0.1-4.noarch.rpm>


#yum 으로 설치
yum install xtrabackup


#디렉토리 확인
ll /backup
ll /backup/full_backup
ll /backup/incre_backup


#디렉토리 생성
mkdir /backup
mkdir /backup/full_backup
mkdir /backup/incre_backup


#crontab 에 설정
\* \*/1 \* \* \* root /root/bin/mysql_innodb_backup.sh


crontab 와 db_full_backup_time 은 중요합니다.스크립스트는 crontab 실행될때 백업이 되며, db_full_backup_time이 아닐경우 차등백업을 실행합니다.


따라서 1시간마다 백업을하며 db_full_backup_time이 있을경우에 full 백업을 합니다.


아래의 스크립트에서 03 15을 변수로 줄경우 배열로 받아서 참일경우 full 백업 거짓일경우 차등백업을 진행합니다.따라서 새벽 3시 오후3시에 백업을 진행 합니다.


# !/bin/bash


# DB Backup


BAK_DIR=/backup;
TODAY=$(date +%Y%m%d --date '12 hours ago')


# TODAY=$(date +%Y%m%d)


RMTODAY=$(date +%Y%m%d --date '10 days ago')


# Delete DB File


rm -rf $BAK_DIR/full_backup/$RMTODAY\*
rm -rf $BAK_DIR/incre_backup/$RMTODAY\*


## Backup Time


db_full_backup_time=("03 15")


## Now Time & Time Check


TOTIME=$(date +%H)


# TOTIME=$(date +%H)


echo $TOTIME
in_array() {
 local needle array value
 needle="${1}"; shift; array=("${@}")
 for value in ${array[@]}; do [ "${value}" == "${needle}" ] && echo "true" && return; done
 echo "false"
}


db_full_backup_check=`in_array $TOTIME ${db_full_backup_time[@]}`


if [ "$db_full_backup_check" == "true" ]; then
 # full backup
 /bin/nice -n 10 /usr/bin/ionice -c2 -n 7 /usr/bin/innobackupex --defaults-file=/etc/my.cnf \\
 --user=root --password='1234' --slave-info --no-timestamp \\
 --compress $BAK_DIR/full_backup/$TODAY
 else
 # hot backup
 /bin/nice -n 10 /usr/bin/ionice -c2 -n 7 /usr/bin/innobackupex --defaults-file=/etc/my.cnf \\
 --user=root --password='1234' --no-timestamp --compress --incremental \\
 --incremental-basedir=$BAK_DIR/full_backup/$TODAY $BAK_DIR/incre_backup/$TODAY/$TOTIME
 fi
