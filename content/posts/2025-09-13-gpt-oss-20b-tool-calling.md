---
title: "gpt-oss-20b Tool Calling "
date: 2025-09-13T22:07:24+09:00
draft: false
categories: ["linuxer?"]
tags: ["ml", "gpt-oss", "tool", "funtion"]
slug: "gpt-oss-20b-tool-calling"
aliases:
  - /gpt-oss-20b-tool-calling/
  - /gpt-oss-20b-tool-calling/
---


```
System Specifications CPU: AMD Ryzen 9 9950X3D 16-Core (32 threads, up to 5.75 GHz) RAM: 60GB GPU: NVIDIA GeForce RTX 5090 (32GB VRAM, CUDA 12.9) Storage: 1.9TB (1.5TB available) OS: Fedora Linux 42 Server Edition Kernel: 6.15.10
```

이스펙으로 gpt-oss-20b 모델을 구동하고 테스트했다.
그냥 단순 부하 테스트로는 gpt-oss-20b 모델을 vllm 으로 실행했을때 90rps 까지 처리하고 초당 토큰을 생성하는 속도는 4000토큰 정도 생성했다.
4000 token/s 라는 이야기다.

생각보다 준수한 성능에 감탄하고 바로 도구를 사용할 수 있도록 작업을 했다.
홈랩의 구성을 여러번 갈아 엎게된 사연이 이과정에 있었다.

1. MSI X870 보드의 칩셋이 생각보다 최신이어서 WIFI 드라이버를 Linux 에서 애매하게 지원

   * 강제로 컴파일로 사용하도록 셋팅

* 커널업데이트이후 네트워크 안됨

* OS를 바꿔가며 잡아서 테스트

* 페도라에서 지원하는 버전과 드라이버를 확인하여 각자 OS에서 같은버전을 찾아서 설치

2. proxmox 셋팅해서 쿠버네티스 클러스터 구성

   * 데비안 계열로 WIFI 트슛이 쉽지 않았다..

* VM을 띄우고 사용하는 리소스가 생각보다 많이 들고 경합이 발생함을 인지

* 최적화 작업을 진행했으나, 홈랩환경에선 VM을 나눠 쓸필요가 없다고 판단 proxmox 탈락

3. 페도라로 셋팅하고 K3S를 채택

   * Argocd / harbor / gitops 구조
     <https://github.com/Cloud-Linuxer/argocd-apps>

* 앗! 집 인터넷이 배포만 하면 다운된다.

* 인터넷 문제라 생각하고 AS신청.

* ISP공유기를 사용하지 않으면 100MB 로 회선이 고정되어 공유기를 쓸수 밖에 없음.

* 공유기 하단에 MAC Addres 가 수십개가 동작하면 ISP공유기가 실시간으로 재부팅됨.
     + 확인하기 위해 스크립트로 DHCP로 IP할당 받는 인터페이스만 늘려봄 공유기 다운됨

+ 그럼 공유기 두대가 DHCP를 같이 뿌려서 발생하는 증상인지 확인하려고 하단의 공유기를 AP모드로 변경 증상 동일

+ 어떻게 해도 MAC사용량이 늘어나면 공유기가 다운됨

* 홈랩에서 너무 거창해짐을 판단 k3s 포기

4. Docker compose 로 변경

   * 간략하게 변경된 구조에서는 인터넷은 아주 안정적임

* vllm gpt-oss-20b 모델이 로딩하다 중단되는 증상이 발생
     + ollama 나 sglang 등은 정상

+ gpu 셋팅 옵션 문제라 생각하고 vllm 셋팅을 계속 변경함

+ 모델 로딩이 느려서 ./model 디렉토리를 마운트해서 pre-download 구조를 설정했는데 이 과정에서 모델의 일부가 깨져서 로딩이 진행되지 않음.ㅠㅠ 인터넷!!!!!!!!!!!!

+ 삭제후 다시 받아서 정상화됨

* Tool calling 을 구현하기 시작
     + 아무리 강하게 모델에게 프롬프트로 도구를 강제하여도 도구를 사용하지 않음 1+1은? 이런 질문도 도구를 사용하지 않고 그냥 모델이 응답함

+ native tool calling 을 지속적으로 테스트했으나, 모델이 응답하지 않음.

+ native tool calling 을 사용하기위한 조건이 복잡함.
       - harmony 포멧을 이용해야함

- harmony 를 사용하도록 만들어진 vllm 이미지는 어텐션3을 사용해야함
         * 블랙웰은 어텐션3을 사용할수 없음.

* 백엔드를 다른것으로 고정하면 하모니 포멧을 사용하는 vllm 버전을 사용불가

- harmony를 포기하고 다른방식으로 툴체인을 구성하기로 함

+ 툴사용에 대한 키워드가 프롬프트에 포함되면 강제로 프록시해서 툴 결과를 프롬프트에 끼워넣어서 출력하는 방식으로 설정

+ 이는 프록시 에뮬레이션 방식이라 보임

+ <https://github.com/Cloud-Linuxer/gpt-oss/blob/main/FINAL_IMPLEMENTATION_REPORT.md>

위의 정리와 같이 gpt-oss 모델에서 harmony를 사용하지 않는 펑션 에이전트를 제작.

![](/images/2025/09/image-1024x373.png)

이로서 3주차에 vllm 관련한 이슈들과 모델 사용관련 옵션 gpu관련한 부분들을 정리하여 사용가능하도록 수정하였다.

![](/images/2025/09/image-1.png)

이런 질문을 하는 사람이 있을거라 생각 못했는데..이후 재대로 구현후에는 재대로 대답을 했다.

![](/images/2025/09/image-2-1024x558.png)

아 재미있었다!!
