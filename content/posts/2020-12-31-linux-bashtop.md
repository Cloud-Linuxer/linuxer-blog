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

\n

bashtop&bpytop 이 핫해서 centos 7 에서 설치했습니다.

\n\n\n\n

bashtop 은 bash 4.4 이상 bpytop는 python3이상입니다.  
오늘 저는 bashtop를 사용해볼까 합니다.

\n\n\n\n

먼저 bash 5.0을 설치 하려 합니다.

\n\n\n\n

```
 cd /usr/local/src/\n wget http://ftp.gnu.org/gnu/bash/bash-5.0.tar.gz\n tar zxvf bash-5.0.tar.gz\n cd bash-5.0/\n ./configure && make && make install\n mv /bin/bash /bin/bash.bak\n ln -s /usr/local/bin/bash /bin/bash\n \n[root@linuxer src]# bash -version\nGNU bash, version 5.0.0(1)-release (x86_64-pc-linux-gnu)
```

\n\n\n\n

그래서 bash 를 다운받고 컴파일 해줬습니다. 기존 bash 는 4.2 버전이라 bash.bak 으로 변경해 문제가 생기면 언제든 사용할수 있도록 만들었습니다.

\n\n\n\n

```
yum install git\ngit clone https://github.com/aristocratos/bashtop.git\ncd bashtop/\nmake install
```

\n\n\n\n

이제 완성됬습니다.

\n\n\n\n

Bashtop 의 컴파일 까지 끝났으므로 실행만 하면 됩니다.

\n\n\n\n

```
./bashtop
```

\n\n\n\n
![](/images/2020/12/image-20.png)
\n\n\n\n
![](/images/2020/12/image-21.png)
\n\n\n\n

레트로 게임같은 비주얼에서 매우 만족스럽습니다.

\n\n\n\n

한번써보시는걸 추천해 드립니다.

\n\n\n\n

감사합니다.

\n