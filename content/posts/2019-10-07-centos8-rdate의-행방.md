---
title: "centos8 rdate의 행방"
date: 2019-10-07T10:31:19+09:00
draft: false
categories: ["Linux"]
tags: ["ntp", "rdate", "chrony"]
slug: "centos8-rdate의-행방"
aliases:
  - /centos8-rdate의-행방/
  - /centos8-rdate%ec%9d%98-%ed%96%89%eb%b0%a9/
---

\n

지금까지 rdate로 시간동기화를 강제로 맞췄다.

\n\n\n\n

ntp를 써도 됬지만 centos5에서 적응한 방식이라 레거시에서 벗어날수 없었다.

\n\n\n\n

ansible 테스트중에 알게됬다.

\n\n\n\n

rdate 가 설치되지 않았다.

\n\n\n\n

TASK [rdate] \*  
 fatal: [13.125.94.121]: FAILED! => {"changed": false, "failures": ["rdate 일치하는 패키지 없음"], "msg": "Failed to install some of the specified packages", "rc": 1, "results": []}  
 …ignoring

\n\n\n\n

centos8 은 4점대 커널이다. centos7은 3점대고.

\n\n\n\n

이커널 차이에서 오는 가장 큰차이점은 ntp 가 기본이냐, chronyd가 기본이냐다.

\n\n\n\n

centos8 부턴 chronyd 기본지원이므로 이전과 같이 불편하게 설정하지 않아도 될것같다.

\n\n\n\n

[root@ip-172-31-45-50] ~# uname -a  
 Linux ip-172-31-45-50.ap-northeast-2.compute.internal 4.18.0-80.7.1.el8\_0.x86\_64 #1 SMP Sat Aug 3 15:14:00 UTC 2019 x86\_64 x86\_64 x86\_64 GNU/Linux  
 [root@ip-172-31-45-50] ~# rpm -qa | grep chronyd  
 [root@ip-172-31-45-50] ~# rpm -qa | grep chrony  
 chrony-3.3-3.el8.x86\_64

\n\n\n\n\n\n\n\n\n