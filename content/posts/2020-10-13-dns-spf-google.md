---
title: "DNS-spf-google"
date: 2020-10-13T14:40:39+09:00
draft: false
categories: ["Linux"]
slug: "dns-spf-google"
aliases:
  - /dns-spf-google/
  - /dns-spf-google/
---


spf 레코드는 RFC 4408 의해서 255 characters으로 제한된다.


하나의 레코드가 255 characters 라는 이야기다.


그래서 255 characters 이상을 쓰려면 어떻게 해야할까? 그것을 구글의 사용 예를 들어서 설명하고자 한다.


google.com text = "v=spf1 include:_spf.google.com ~all"


_spf.google.com 도메인을 include 하고 _spf.google.com 도메인을 쿼리하면


_spf.google.com text = "v=spf1 include:_netblocks.google.com include:_netblocks2.google.com include:_netblocks3.google.com ~all"


_netblocks.google.com
_netblocks2.google.com
_netblocks3.google.com


세개의 도메인을 알려준다. 세개의 도메인은 각각의 역할에 따라 ipv4나 ipv6를 응답한다.


_netblocks.google.com text = "v=spf1 ip4:35.190.247.0/24 ip4:64.233.160.0/19 ip4:66.102.0.0/20 ip4:66.249.80.0/20 ip4:72.14.192.0/18 ip4:74.125.0.0/16 ip4:108.177.8.0/21 ip4:173.194.0.0/16 ip4:209.85.128.0/17 ip4:216.58.192.0/19 ip4:216.239.32.0/19 ~all"

_netblocks2.google.com text = "v=spf1 ip6:2001:4860:4000::/36 ip6:2404:6800:4000::/36 ip6:2607:f8b0:4000::/36 ip6:2800:3f0:4000::/36 ip6:2a00:1450:4000::/36 ip6:2c0f:fb50:4000::/36 ~all"

_netblocks3.google.com text = "v=spf1 ip4:172.217.0.0/19 ip4:172.217.32.0/20 ip4:172.217.128.0/19 ip4:172.217.160.0/20 ip4:172.217.192.0/19 ip4:172.253.56.0/21 ip4:172.253.112.0/20 ip4:108.177.96.0/19 ip4:35.191.0.0/16 ip4:130.211.0.0/22 ~all"


이렇게 2단계의 include를 거쳐서 255 characters 이상의 레코드를 구성한다.


그렇다면 A recode로 spf 를 관리하려면 어떻게해야 할까?


<https://spam.kisa.or.kr/filemanager/download.do?path=spam/customer/archive/&filename=SPF%EA%B8%B0%EC%88%A0%EB%AC%B8%EC%84%9C.pdf>


linuxer.name text = "v=spf1 a:_1.linuxer.name ~all"


바로 이런식이다 include: 부분을 a: 로 변경하는것이다.


그리고.. spf 레코드는 사용하는 대역이나 ip를 알려주는것 외에 정책을 정하는 역할을 하는데 다음과 같은 규칙이 적용된다.


Neutral (?) 출판된 데이터에 근거해 판단을 내릴 수 없음
Pass (+) 가 인가되어진 발송서버로 확인됨
Fail (-) 가 인가되어지지 않은 발송서버로 확인됨
Softfail (~) 는 인가되지 않은 발송서버이나 “Fail” 정책의 적용은 유보함.


linuxer.name text = "v=spf1 a:_1.linuxer.name +all"


이런식이면 _1.linuxer.name a 레코드로 등록된 IP는 인가된 발송서버로 확인된다는 의미다.


오랜만에 spf 레코드를 다시 복습하면서 정보진흥원의 문서를 보며 감탄 또 감탄했다.


위의 문서를 꼭 보시라!
