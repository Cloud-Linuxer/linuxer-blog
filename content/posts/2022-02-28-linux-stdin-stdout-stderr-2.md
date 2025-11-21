---
title: "Linux-stdin-stdout-stderr-2"
date: 2022-02-28T20:52:17+09:00
draft: false
categories: ["Linux"]
tags: ["grep", "linux", "buffer", "stderr", "stdin", "stdout"]
slug: "linux-stdin-stdout-stderr-2"
aliases:
  - /linux-stdin-stdout-stderr-2/
  - /linux-stdin-stdout-stderr-2/
---


**stderr 는 버퍼를 사용하지 않지만 그것과 별개로 그대로 출력하기 때문에 grep 이 되지 않는것입니다.**

<https://www.facebook.com/groups/korelnxuser/permalink/2060620130779393/>

소용환님께서 답변해주셔서 알 수 있었습니다.

![](/images/2022/02/image.png)

그래서 테스트를 진행하였습니다.

stdbuf 명령어를 이용하여 buffer 를 제거하고 grep 해보았습니다. stdbuf -o0 는 stdout 를 unbuffered 로 출력하는 명력어 입니다.

```
# cat test.txt
1 2
3 4
5 6
# stdbuf -o0 cat test.txt | grep 2 2

```

그런데 문득 버퍼사이즈가 0인것과 버퍼가 아주없는 unbuffered 는 차이가 있다는것을 알게되었습니다. 그래서 stderr 에 buffer 를 주었습니다.

```
# cat test.txt 1>&2 | stdbuf -eL grep 2 1
2 3
4 5
6
# stdbuf -eL cat test.txt 1>&2 | grep 2 1
2 3
4 5
6

```

grep 이 되지 않는것을 확인할수 있었습니다.

이 테스트를 결과로 stderr가 grep 되지 않는것은 buffer의 사용유무와 상관없이 그대로 출력하기 때문임을 알게되었습니다.

![](/images/2022/02/pipe_stdio_example.png)

https://www.pixelbeat.org/programming/stdio_buffering/

이해를 돕기위해 pixelbeat.org 의 이미지를 첨부합니다.
