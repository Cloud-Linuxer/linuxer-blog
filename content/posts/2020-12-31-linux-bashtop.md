---
title: "Linux-bashtop"
date: 2020-12-31T16:23:38+09:00
draft: false
categories: ["Linux"]
slug: "linux-bashtop"
aliases:
  - /linux-bashtop/
  - /linux-bashtop/
---


bashtop&bpytop 이 핫해서 centos 7 에서 설치했습니다.

bashtop 은 bash 4.4 이상 bpytop는 python3이상입니다.
오늘 저는 bashtop를 사용해볼까 합니다.

먼저 bash 5.0을 설치 하려 합니다.

```bash
 cd /usr/local/src/
 wget http://ftp.gnu.org/gnu/bash/bash-5.0.tar.gz
 tar zxvf bash-5.0.tar.gz
 cd bash-5.0/
 ./configure && make && make install
 mv /bin/bash /bin/bash.bak
 ln -s /usr/local/bin/bash /bin/bash

[root@linuxer src]# bash -version GNU bash, version 5.0.0(1)-release (x86_64-pc-linux-gnu)
```bash
그래서 bash 를 다운받고 컴파일 해줬습니다. 기존 bash 는 4.2 버전이라 bash.bak 으로 변경해 문제가 생기면 언제든 사용할수 있도록 만들었습니다.

```bash
yum install git git clone https://github.com/aristocratos/bashtop.git cd bashtop/ make install
```bash
이제 완성됬습니다.

Bashtop 의 컴파일 까지 끝났으므로 실행만 하면 됩니다.

```bash
./bashtop
```bash
![](/images/2020/12/image-20.png)

![](/images/2020/12/image-21.png)

레트로 게임같은 비주얼에서 매우 만족스럽습니다.

한번써보시는걸 추천해 드립니다.

감사합니다.
