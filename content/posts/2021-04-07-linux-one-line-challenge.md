---
title: "Linux-one-line-Challenge"
date: 2021-04-07T22:05:59+09:00
draft: false
categories: ["Linux"]
tags: ["shell", "linux", "bash"]
slug: "linux-one-line-challenge"
aliases:
  - /linux-one-line-challenge/
  - /linux-one-line-challenge/
---

\n

리눅서들은 이상한 것에 집착하곤 한다.

\n\n\n\n

한줄 명령어가 그 중 하나이다.

\n\n\n\n
![](/images/2021/04/image-1.png)
\n\n\n\n

보통 그렇다. 이런 아무렇지 않은 질문으로 시작한다.

\n\n\n\n

질문은 곧 챌린지가 되고 도전이 시작된다.

\n\n\n\n
![](/images/2021/04/image-2.png)
\n\n\n\n

적당히 조언했던것이..

\n\n\n\n
![](/images/2021/04/image-3.png)
\n\n\n\n

다른 분의 참전으로 새로운 측면을 맞이한다.

\n\n\n\n

ls -lt 는 시간순 정렬이다.

\n\n\n\n
![](/images/2021/04/image-4.png)
\n\n\n\n

대충이라고 하셨지만 골자는 이렇다. ls -ptl 은 파일의 최신순서대로 정렬해서 보여준다. 거기에 / 디렉토리를 빼고 토탈을 빼는 방식이다.

\n\n\n\n

물론 이런것들이 한방에 되진 않는다.

\n\n\n\n
![](/images/2021/04/image-5-741x1024.png)
\n\n\n\n

여러 가지 조언을했지만 사실 말처럼 쉽게 되지 않는다. 그저 제한사항 들을 확인하는 것이다.

\n\n\n\n

위에 내가 쓴 명령어는 안됬다.

\n\n\n\n
![](/images/2021/04/image-6.png)
\n\n\n\n

하얀색 프로필을쓰시는 분은 초굇수다.

\n\n\n\n
![](/images/2021/04/image-7.png)
\n\n\n\n

이제 거의 정답이 나왔다. 여기서 디렉토리만 제외하면 정답이다.

\n\n\n\n
![](/images/2021/04/image-8.png)
\n\n\n\n

맞다 나눠서 하는것도 정답이다. 하지만, 챌린지는 그렇게 쉽지 않다. 한줄로 해야한다.

\n\n\n\n
![](/images/2021/04/image-10.png)
\n\n\n\n

```
find . -type d -exec bash -c 'echo "next dir: ${1}" ; ls -lt "$1" |\n    grep ^- |\n    head -n 5' bash {} \\;
```

\n\n\n\n

정답이다. 그러나 더깔끔하게 하고싶었다 나는...ㅠㅠ

\n\n\n\n
![](/images/2021/04/image-11.png)
\n\n\n\n

```
find /root -type d -exec sh -c "ls -lpt {} | egrep -v '^d|합계' | head -n 1" \\;
```

\n\n\n\n

나는 grep -v 로 ^d 옵션을 줘서 첫글자가 d 그러니까 디렉토리 속성일경우 제외하여 결과를 만들었다.

\n\n\n\n
![](/images/2021/04/image-13.png)
\n\n\n\n

```
sh -c "find /root -type d -exec bash -c \\"ls -lpt {} | egrep -v '/|total' | head -n 1 \\" \\;" | awk '{print $9}'
```

\n\n\n\n

리눅스는 각자의 방법이 있다.

\n\n\n\n

그런 방법들이 너무 사랑스럽다.

\n\n\n\n

오랜만에 즐거운 one line Challenge 였다.

\n\n\n\n\n\n\n\n

좋은하루되시라!

\n\n\n\n\n