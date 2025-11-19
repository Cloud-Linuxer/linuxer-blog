---
title: "AWS-Linux-MariaDB-10.5-S3-Storage-Engine-install-실패"
date: 2020-05-23T16:43:39+09:00
draft: false
categories: ["Linux"]
tags: ["mariadb"]
slug: "aws-linux-mariadb-10-5-s3-storage-engine-install-실패"
aliases:
  - /aws-linux-mariadb-10-5-s3-storage-engine-install-실패/
  - /aws-linux-mariadb-10-5-s3-storage-engine-install-%ec%8b%a4%ed%8c%a8/
---

\n

mariadb 10.5 version 에서 S3 Storage Engine을 사용하기위해 먼저 repo를 설치하고 s3 engine 를 올리려고 해봤다. 원랜 바이너리 패키지로 지원해야 하는데....

\n\n\n\n

<https://mariadb.com/kb/en/using-the-s3-storage-engine/>

\n\n\n\n

아무리 찾아봐도 없어서...찾아보니까...

\n\n\n\n

<https://jira.mariadb.org/browse/MDEV-22606>

\n\n\n\n

The S3 storage engine is included in source code distributions of MariaDB Community Server 10.5. However, it is not currently built and distributed with any of our MariaDB Community Server 10.5 binary packages.

\n\n\n\n

이런내용이 있었다...제길..컴파일해야 하는구나.

\n\n\n\n

그래서 컴파일을 시작했다.

\n\n\n\n

mariadb 컴파일은 생각보다 엄청 오래걸린다. T2.micro 사이즈 기준으로 2시간정도.. 너무 느리다 생각되면 인스턴스 사이즈를 컴파일 할때만 잠깐 늘리거나 인스턴스가 터지지 않게 swap 을 늘려주자.

\n\n\n\n

\nhttps://linuxer.name/2019/09/file-swap-%eb%a7%8c%eb%93%a4%ea%b8%b0/\n

\n\n\n\n

이전에 포스팅한 swap 만들기가 있다. 참고하자.

\n\n\n\n

하면서 인스턴스용량 때문에 한번 메모리때문에 한번터져서 세번째엔 그냥 T3.large 유형으로 컴파일을 했다.

\n\n\n\n\n\n\n\n

설치 시작전에 먼저 필요한 패키지를 설치한다.

\n\n\n\n

cmake로 컴파일한다.

\n\n\n\n

# amazon-linuxer-extra install epel-release  
# yum install -y cmake gcc gcc-c++ ncurses-devel git curl-devel mhash-devel

\n\n\n\n

먼저 기본설정으로 두가지를 설치하자. epel은 mhash-devel 때문에 설치하는거다.

\n\n\n\n

# wget http://mirrors.supportex.net/mariadb//mariadb-10.5.3/source/mariadb-10.5.3.tar.gz

\n\n\n\n

다운받고

\n\n\n\n

tar zfxv mariadb-10.5.3.tar.gz

\n\n\n\n

압축풀고

\n\n\n\n

cd mariadb-10.5.3

\n\n\n\n

이동하고 컴파일 한다.

\n\n\n\n

# cmake \\  
-DWITH\_READLINE=1 \\  
-DWITH\_READLINE=1 \\  
-DWITH\_SSL=bundled \\  
-DWITH\_ZLIB=system \\  
-DDEFAULT\_CHARSET=utf8 \\  
-DDEFAULT\_COLLATION=utf8\_general\_ci \\  
-DENABLED\_LOCAL\_INFILE=1 \\  
-DWITH\_EXTRA\_CHARSETS=all \\  
-DWITH\_ARIA\_STORAGE\_ENGINE=1 \\  
-DWITH\_XTRADB\_STORAGE\_ENGINE=1 \\  
-DWITH\_ARCHIVE\_STORAGE\_ENGINE=1 \\  
-DWITH\_INNOBASE\_STORAGE\_ENGINE=1 \\  
-DWITH\_PARTITION\_STORAGE\_ENGINE=1 \\  
-DWITH\_BLACKHOLE\_STORAGE\_ENGINE=1 \\  
-DWITH\_FEDERATEDX\_STORAGE\_ENGINE=1 \\  
-DWITH\_PERFSCHEMA\_STORAGE\_ENGINE=1 \\  
-DPLUGIN\_S3=YES \\  
-DINSTALL\_SYSCONFDIR=/usr/local/mariadb/etc \\  
-DINSTALL\_SYSCONF2DIR=/usr/local/mariadb/etc/my.cnf.d \\  
-DMYSQL\_TCP\_PORT=3306 \\  
-DCMAKE\_INSTALL\_PREFIX=/usr/local/mariadb \\  
-DMYSQL\_DATADIR=/usr/local/mariadb/data \\  
-DMYSQL\_UNIX\_ADDR=/usr/local/mariadb/socket/mysql.socket

\n\n\n\n

CMake Error at cmake/plugin.cmake:296 (MESSAGE):  
Plugin S3 cannot be built  
Call Stack (most recent call first):  
CMakeLists.txt:427 (CONFIGURE\_PLUGINS)

\n\n\n\n

-DPLUGIN\_S3=YES

\n\n\n\n

위 옵션이 먹지 않았다.

\n\n\n\n

<https://jira.mariadb.org/browse/MDEV-19416>

\n\n\n\n

이리저리 찾아봐도 안된다는 내용만.. source  에 있다해서 신나서 했는데..ㅠㅠ

\n\n\n\n

아직 10.5.3버전에서도 정상적으로 릴리즈되진 않은것으로 보인다.

\n\n\n\n

S3\_STORAGE\_ENGINE=1 이옵션으로 켜줘야 정상아닌가..그래서

\n\n\n\n

S3\_STORAGE\_ENGINE옵션을 주고 컴파일 해봤는데... 컴파일은 되는데 플러그인을 확인할수 없었다.

\n\n\n\n

-rwxr-xr-x 1 root root 30008 May 23 06:36 adt\_null.so  
-rwxr-xr-x 1 root root 22368 May 23 06:36 auth\_0x0100.so  
-rwxr-xr-x 1 root root 327904 May 23 06:36 auth\_ed25519.so  
-rwxr-xr-x 1 root root 33488 May 23 06:36 auth\_test\_plugin.so  
-rwxr-xr-x 1 root root 51160 May 23 06:35 caching\_sha2\_password.so  
-rwxr-xr-x 1 root root 343792 May 23 06:35 client\_ed25519.so  
-rw-r--r-- 1 root root 227 May 11 14:34 daemon\_example.ini  
-rwxr-xr-x 1 root root 31840 May 23 06:36 debug\_key\_management.so  
-rwxr-xr-x 1 root root 23608 May 23 06:36 dialog\_examples.so  
-rwxr-xr-x 1 root root 51848 May 23 06:35 dialog.so  
-rwxr-xr-x 1 root root 419984 May 23 06:36 disks.so  
-rwxr-xr-x 1 root root 59432 May 23 06:36 example\_key\_management.so  
-rwxr-xr-x 1 root root 184128 May 23 06:36 file\_key\_management.so  
-rwxr-xr-x 1 root root 1239672 May 23 06:36 func\_test.so  
-rwxr-xr-x 1 root root 718464 May 23 06:36 ha\_archive.so  
-rwxr-xr-x 1 root root 682112 May 23 06:36 ha\_blackhole.so  
-rwxr-xr-x 1 root root 8822896 May 23 06:36 ha\_connect.so  
-rwxr-xr-x 1 root root 532336 May 23 06:36 ha\_example.so  
-rwxr-xr-x 1 root root 874792 May 23 06:36 ha\_federated.so  
-rwxr-xr-x 1 root root 1526136 May 23 06:36 ha\_federatedx.so  
-rwxr-xr-x 1 root root 28310200 May 23 06:36 ha\_mroonga.so  
-rwxr-xr-x 1 root root 3250752 May 23 06:36 handlersocket.so  
-rwxr-xr-x 1 root root 126790184 May 23 06:35 ha\_rocksdb.so  
-rwxr-xr-x 1 root root 1806592 May 23 06:36 ha\_sphinx.so  
-rwxr-xr-x 1 root root 11633920 May 23 06:36 ha\_spider.so  
-rwxr-xr-x 1 root root 363776 May 23 06:36 ha\_test\_sql\_discovery.so  
-rwxr-xr-x 1 root root 84016 May 23 06:36 libdaemon\_example.so  
-rwxr-xr-x 1 root root 415792 May 23 06:36 locales.so  
-rwxr-xr-x 1 root root 592512 May 23 06:36 metadata\_lock\_info.so  
-rwxr-xr-x 1 root root 29352 May 23 06:36 mypluglib.so  
-rwxr-xr-x 1 root root 35656 May 23 06:35 mysql\_clear\_password.so  
-rwxr-xr-x 1 root root 29568 May 23 06:36 qa\_auth\_client.so  
-rwxr-xr-x 1 root root 39152 May 23 06:36 qa\_auth\_interface.so  
-rwxr-xr-x 1 root root 24592 May 23 06:36 qa\_auth\_server.so  
-rwxr-xr-x 1 root root 587624 May 23 06:36 query\_cache\_info.so  
-rwxr-xr-x 1 root root 731952 May 23 06:36 query\_response\_time.so  
-rwxr-xr-x 1 root root 234272 May 23 06:36 server\_audit.so  
-rwxr-xr-x 1 root root 28576 May 23 06:36 simple\_password\_check.so  
-rwxr-xr-x 1 root root 31152 May 23 06:36 sql\_errlog.so  
-rwxr-xr-x 1 root root 1281352 May 23 06:36 test\_versioning.so  
-rwxr-xr-x 1 root root 689104 May 23 06:36 type\_test.so  
-rwxr-xr-x 1 root root 720048 May 23 06:36 wsrep\_info.so

\n\n\n\n

플러그인 리스트를 첨부하는것으로 포스팅을 마친다...

\n\n\n\n\n\n\n\n

하....이번에도 역시 실패

\n