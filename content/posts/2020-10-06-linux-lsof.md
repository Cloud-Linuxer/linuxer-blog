---
title: "linux-lsof"
date: 2020-10-06T11:22:11+09:00
draft: false
categories: ["Linux"]
slug: "linux-lsof"
aliases:
  - /linux-lsof/
  - /linux-lsof/
---


사이트 확인중 이상 증상이 있는 고객이 있었다.


사용량이 많아지면 mysql.sock 에러가 발생하는 것이었다.


apache 에서 mysql 접속시 socket을 생성한다는건 일반적으로 접속을 Localhost 로 설정해야 하는데, local의 database를 사용하지 않는 상태였다.


socket을 사용하는 에러를 찾기위해 lsof 를 먼저 사용했다.


lsof | grep sock
httpd 15233 apache 5u sock 0,7 0t0 658393448 can't identify protocol
httpd 15250 apache 3u sock 0,7 0t0 658393444 can't identify protocol
httpd 15250 apache 5u sock 0,7 0t0 658393448 can't identify protocol
httpd 15258 apache 3u sock 0,7 0t0 658393444 can't identify protocol
httpd 15258 apache 5u sock 0,7 0t0 658393448 can't identify protocol
httpd 15312 apache 3u sock 0,7 0t0 658393444 can't identify protocol
httpd 15312 apache 5u sock 0,7 0t0 658393448 can't identify protocol
httpd 15314 apache 3u sock 0,7 0t0 658393444 can't identify protocol
httpd 15314 apache 5u sock 0,7 0t0 658393448 can't identify protocol


can't identify protocol mysql.sock 문제가 아니라 apache 의 sock 문제가 발생하고 있었다.


can't identify protocol 는 소켓이 완전히 닫히지 않거나 누수가 있다고 판단되는데, 확인이 필요했다. 요인은 openfile 갯수나 여러가지 요인이 있을거라 생각해서 먼저 openfile을 확인했다.


ulimit 로 확인한 openfile 갯수는 1024와 일단 수정해 줬다.


echo "\* soft nofile 65535" >> /etc/security/limits.conf
echo "\* hard nofile 65535" >> /etc/security/limits.conf
ulimit -Hn 65536
ulimit -Sn 65536


cat /proc/net/sockstat
sockets: used 261
TCP: inuse 17 orphan 0 tw 44811 alloc 54 mem 49
UDP: inuse 5 mem 15
UDPLITE: inuse 0
RAW: inuse 0
FRAG: inuse 0 memory 0


sockstat 를 확인시에 현재는 문제가 되는 상태는 아니었다.


이 조치 이후 추가적인 모니터링을 진행할 것이다.
