---
title: "Certified Kubernetes Administrator-CKA-Review"
date: 2021-08-08T17:33:49+09:00
draft: false
categories: ["Certification", "Kubernetes"]
tags: ["k8s", "Kubernetes", "cka"]
slug: "certified-kubernetes-administrator-cka-review"
aliases:
  - /certified-kubernetes-administrator-cka-review/
  - /certified-kubernetes-administrator-cka-review/
---


![](/images/2021/08/image-1024x793.png)

CKA를 취득하기로 마음먹은지 어언 10개월.. 작년 7월부터 고민했던 종착점에 도착했다.

먼저 시험을 보기전의 나에 대해서 이야기해볼까 한다.

컨테이너는 그럭저럭 다루고, ECS기반의 아키텍처설계를 주로했다. EKS는 혼자서 사용하면서 대충~ 이야기할수있는 레벨이었다. 이직을 진행하면서 NKS에 대한 공부를 진행했고, 관리형 K8S는 어느정도 이해도가 높아졌다는 생각을 한 시점이었다.

그리고 DKOS-Docker Kubernetes online study를 진행하면서 나름의 공부를 한터라 자신이 있었다. 1차 시험에는 49점으로 탈락했다. 사실 다 풀었는데 왜이런 점수가 나왔는지 의아했다. 그래서 떨어지고나서 찾아보니..시험에서 원하는 답이 있다는 것을 알 수 있었다.

보통 나는 시험을 준비할 때 이런 프로세스를 따른다.

후기수집->언급빈도/공통키워드 분석-> 분석에 따른 시험공부->응시

그런데 이번엔 그렇지 않고 그냥 시험을 봤다. 평소와 다른 패턴으로 시험에서 원하는 답과 내가 생각하는 답의 거리. 그리고 K8S 클러스터에서 15번문제에서 작업한 것이 앞서 풀었던 문제에 영향을 끼쳤다. K8S context를 사용하는 문제들이 여러 문제였다.

명확하게 탈락 이유를 알게되고 본래 시험을 볼때 쓰던 방식을 따랐다.

경험자들의 후기를 수집했고 공통적으로 나오는 이야기가 있었다.

뭄샤드형. Mumshad Mannambeth 다. Udemy에 강의가 있다.

<https://www.udemy.com/course/certified-kubernetes-administrator-with-practice-tests>

원가는 좀 비싼데 유데미 특성상 시크릿모드로 여러번 반복해서 들어가면 할인된다. 나는 15000원에 구입했다.

먼저 스크립트를 보는 법을 알려준다.

![](/images/2021/08/image-1-1024x519.png)

CC에서 영어자막을 켜고, 그 옆에 Transcript 를 누르면 스크립트를 볼수있다.
축하한다. 이제 번역기를 쓸수있다. 강의 잘듣길 바란다.

![](/images/2021/08/image-2.png)

크롬 자체의 번역기 기능을 켜면 애매한 번역일지언정 대충 알아 볼수있게 번역해준다.

그리고 여기부터 중요하다.

Udemy 강의의 **24. Accessing the Labs** 를 보면 kodekloud의 쿠폰을 준다.

강의+실습쿠폰이라니 이 얼마나 혜자 구성인가. kodekloud에선 Lab을 진행할수 있고 쿠버네티스를 실습하고 문제를 풀 수 있도록 환경을 제공해준다. 쿠폰으로 가입까지 마무리했다면 udemy 강의와 실습은 별개임을 알아야한다. 이론적인 지식은 별개로 채우고 실습으로 맞아가며 공부하는게 빠르다.

<https://kodekloud.com/lessons/core-concepts-4/>

로그인이후에 이 URL로 가면 Lab 만 진행할수 있다. 뭄샤드형의 컴퓨팅파워를 마음껏 사용하도록하자. - 좀 느린게 흠이지만 나는 너무 만족했다-

이 실습을 다 풀어보면서 시험에서 요구하는 정확한 답이 뭔지 알았다.

7월 31일 탈락 8월 7일 합격이었다. 딱 일주일만의 재 시험을 봐서 합격했다.

일주일간 뭄샤드형 실습완료- killer.sh 1번 정주행. 그리고 참고서로 [쿠버네티스 완벽 가이드](https://book.naver.com/bookdb/book_detail.nhn?bid=20797710) 책을 이용해서 애매한 개념들을 이해했다.

이제 공부하는 과정을 설명했다면 시험본 과정을 설명할까한다.

시험 준비는 먼저 **구글번역/파파고번역/PSI /Innovative Exams Screensharing** 이렇게 네가지의 플러그인을 설치했다. LinuxFoundation 시험은 번역기를 무료로 쓸수 있게 해준다. 감사. 매우감사.

그리고 뭄샤드형 Lab을 하면서 내가 잘못하는 도메인의 **북마크**(즐겨찾기)를 마구 만들어 뒀다.

- 실제 시험 들어가니까 그건 안보이고 검색해서 모두 해결했다.-

그리고 시험 15분전에 시험에 참가전 신원검사와 장소검사 등등을 하고 시험을 봤다.

시험을 시작하면 제일먼저 해야할것은

```text
source <(kubectl completion bash) echo "source <(kubectl completion bash)" >> ~/.bashrc alias k=kubectl complete -F __start_kubectl k
```
이 네줄을 치트 시트에서 찾아서 입력하는것이다.

자동완성 없으면 진짜 손가락에 랙걸리는게 느껴진다.

내가 중점적으로 연습했던건 RBAC 였다. SA->Role->Rolebinding 과정이 번거로웠다.

그리고 나는 원래 VI를 사랑하는 유저지만 이번시험에선 VI를 봉인했다. VI로 들어가서 수정하는 과정이 매우 귀찮았다.

그래서

```bash
cat <<EOF | k apply -f - YAML EOF
```
cat <<EOF | k apply -f - enter! 다음에 원하는 YAML을 넣고 EOF하는 것이다. 메모장은 시험에서 제공된 메모장으로 모두 에디터했다.. VI로 열고 닫고 넘귀찮은것.. 물론 방법이야 있는데..

VIM 에서 :shell 혹은 :sh 혹은 Ctrl + z 를 누르면 쉘로 복귀한다. !w 하면 되는데 손이 바쁘니까 그냥 메모장서 복붙붙했다.

이런 과정을 거쳐서 시험은 2번째 시험에 합격했고, 후기를 적고있다.

대충 하고싶었던 말을 다썼고, 이제 감사할 일만 남았다.

첫번쨰로 DKOS 에 참여할수 있도록 허락해주신 [가시다](https://www.notion.so/gasidaseo/CloudNet-Blog-c9dfa44a27ff431dafdd2edacc8a1863)님.
두번째로 팁을 아낌없이 나눠주신 [라온클](https://lifeoncloud.kr/)님
세번째로 영원한 동료 [MVSC](https://manvscloud.com/?p=979)-manvscloud 님

글로 모두 적지는 못하지만 도움을 주신 모든 분들께 항상 감사를 드립니다.

맺음말은 같은방식으로 하겠습니다.

즐거운 저녁되시라!
