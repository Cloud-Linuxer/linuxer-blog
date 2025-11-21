---
title: "Linux-stdin-stdout-stderr-1"
date: 2022-02-26T19:07:57+09:00
draft: false
categories: ["Linux"]
tags: ["grep", "linux", "buffer"]
slug: "linux-stdin-stdout-stderr"
aliases:
  - /linux-stdin-stdout-stderr/
  - /linux-stdin-stdout-stderr/
---


**잘못된 정보를 공유하였습니다.**
**그부분을 수정하고자 게시물을 다시 올립니다.**

바로잡은 내용은 아래의 글입니다.

https://linuxer.name/2022/02/linux-stdin-stdout-stderr-2/

리눅스에서 stderr 으로 받는 문자열은 grep이 되지 않는다.

이유는 stderr는 Unbufferd 로 출력만 하기때문이다.

```bash
# httpd -T | grep http AH00558: httpd: Could not reliably determine the server's fully qualified domain name, using 10.0.10.6. Set the 'ServerName' directive globally to suppress this message (98)Address already in use: AH00072: make_sock: could not bind to address 0.0.0.0:80 no listening sockets available, shutting down AH00015: Unable to open logs

```

위의 경우가 그 예이다.

우리가 사용하는 grep, awk 같은 명령어는 buffer를 이용한다. 그런데 stderr는 buffer 를 거치지 않고 출력하기때문에 grep 나 awk를 사용할수 없는 것이다.

이것을 이해하기 위해선 Buffering을 이해해야 한다.

이런 경우 우리는 2>&1 같은 리디렉션을 이용하여 처리를 한다.

2(stderr)>(리디렉션)&(실행한 다음)1(stdout) 이것은 표준에러를 표준출력으로 변경해준다는 의미로 받아들이면 접근이 굉장히 어렵다. 더 풀어써보겠다.

stderr 는 unbuffer 고 이것을 pipe buffer 를 거쳐 stdin 으로 들어가 grep 은 버퍼내의 데이터를 읽어들여서 stdout로 출력하게 되는것이다.

그냥 버퍼까지 올리지 않던 데이터를 리디렉션으로 버퍼에 넣어준다고 생각하자.

```bash
# httpd -T 2>&1 | grep http AH00558: httpd: Could not reliably determine the server's fully qualified domain name, using 10.0.10.6. Set the 'ServerName' directive globally to suppress this message
```

다음과 같이 grep 가 동작한다.

grep 는 버퍼를 사용하는 명령어다. 버퍼를 사용하지 않는 출력(stderr)은 grep 할수없다.

버퍼를 사용하는 출력(stdout)는 grep 할수있다.
