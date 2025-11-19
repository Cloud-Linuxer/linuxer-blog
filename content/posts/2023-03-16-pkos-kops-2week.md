---
title: "PKOS-kOps-2Week"
date: 2023-03-16T20:47:35+09:00
draft: false
categories: ["Kubernetes"]
tags: ["k8s", "CNI", "kops", "eni"]
slug: "pkos-kops-2week"
aliases:
  - /pkos-kops-2week/
  - /pkos-kops-2week/
---

\n

ㅠㅠ 울고 시작하려한다. 스터디에 집중을 하려고 한다.  
가시다님 그동안 숙제 너무 조금해서 죄송했어요...ㅠㅠ엉엉흑흑

\n\n\n\n

일단 사과를 드리고 시작하며, 이제 살짝 각잡고 kOps 부터 설명하겠다.

\n\n\n\n

**kOps는 Kubernetes Operations의 약자로, Kubernetes 클러스터를 AWS (Amazon Web Services)에서 손쉽게 설치, 업그레이드 및 관리할 수 있도록 해주는 오픈 소스 도구이다. Kops를 사용하면 CLI(Command Line Interface)를 통해 클러스터를 구성할 수 있으며, YAML 파일을 사용하여 쉽게 클러스터를 정의할 수 있다**

\n\n\n\n

Kops는 여러 가지 기능을 제공한다

\n\n\n\n

\n1. 클러스터 구성: Kops를 사용하여 Kubernetes 클러스터를 쉽게 구성할 수 있다. YAML 파일을 사용하여 클러스터 구성을 정의하고, AWS 리소스를 프로비저닝하고 구성을 배포한다.
\n\n\n\n2. 노드 그룹: Kops는 노드 그룹을 사용하여 클러스터 내에서 다양한 유형의 노드를 정의할 수 있다. 예를 들어, CPU 또는 메모리 요구 사항이 높은 애플리케이션을 실행하는 데 필요한 노드 그룹을 만들 수 있다.
\n\n\n\n3. 클러스터 업그레이드: Kops를 사용하여 클러스터를 업그레이드하면, 기존 클러스터의 구성 및 애플리케이션 상태가 유지된다. 이는 클러스터 업그레이드가 더욱 안정적이며 안전하게 진행될 수 있도록 도와준다.
\n\n\n\n4. 롤링 업데이트: Kops는 클러스터의 노드 그룹을 업데이트할 때 롤링 업데이트를 수행할 수 있다. 이를 통해 클러스터에 대한 서비스 중단 없이 노드 그룹의 업데이트를 진행할 수 있다.
\n
\n\n\n\n

Kops는 쉽게 시작할 수 있는 Kubernetes 설치 및 관리 도구 중 하나이다, AWS에서 Kubernetes 클러스터를 운영하는 데 매우 유용하다.

\n\n\n\n

PKOS에서는 [24단계 실습으로 정복하는 쿠버네티스](http://www.yes24.com/Product/Goods/115187666) 로 실습을 진행하면서 kOps를 사용한다.

\n\n\n\n

나는 EKS 를 근래에 주로 다루고 있다.

\n\n\n\n

kOps 와 EKS를 간략하게 비교해봤다.

\n\n\n\n

| 기능 / 속성 | kOps | EKS |
| --- | --- | --- |
| 관리 형태 | 오픈 소스 도구 | 완전 관리형 서비스 |
| 클라우드 플랫폼 | AWS, GCP 등 다양한 플랫폼 | AWS 전용 |
| 클러스터 구축 | 사용자 정의 구성 가능 | 표준화된 구성 사용 |
| 클러스터 업그레이드 | 사용자가 직접 관리 | AWS가 제공하는 관리형 업그레이드 |
| 클러스터 유효성 검사 | kOps 도구를 사용하여 제공 | AWS 콘솔 및 API를 통해 제공 |
| 비용 | 인프라 리소스 비용만 발생 | 인프라 리소스 및 EKS 서비스 비용 |
| 운영의 편의성 | 사용자가 더 많은 관리를 수행함 | AWS가 더 많은 관리를 처리함 |

\n\n\n\n

역시 관리형이 편하다.

\n\n\n\n

이번주에는 K8S의 네트워킹에 대해서 공부를 했는데 다른점이 많은 kOps 와 EKS지만 kOps 를 사용하면 EKS를 배우기 편한 부분이 있다. 이유는 에드온이나, CNI를 같은것을 사용할수 있다.

\n\n\n\n

**awsLoadBalancerController** / CNI로는 amazonvpc 를 사용한다.

\n\n\n\n

내가 이야기할 것은 CNI다.

\n\n\n\n

amazonvpc CNI 같은 경우에는 한가지 특징이 있는데 AWS ENI를 컨테이너에 연결하여 일반적으로 우리가 사용하는 kube-proxy의 동작이 현저하게 줄어들게 된다.

\n\n\n\n

kube-proxy의 동작이 줄어드는 아키텍처는 노드에서의 네트워크 처리횟수가 줄어들어 CPU의 사용량이 줄어든다. 기본적으로 리눅스 네트워크 스택은 자원의 사용량이 적지만 네트워크의 미학을 가진 K8S는 적극적으로 리눅스네트워크 스택을 사용한다. 그러므로 노드의 부하는 커진다. 이런 문제를 amazonvpc CNI는 회피할수 있는 방법을 제시한것이다.

\n\n\n\n

POD가 클러스터를 통하지 않고 통신하는 방식은 Network Hop을 줄이기 때문에 일반적인 오버레이 네트워크의 Network Hop보다 현저하게 줄어들고 빠른 방식이 가능한것이다.

\n\n\n\n

이때문에 kube-proxy를 쓰는 nodeport 같은 형태의 Sevice는 EKS에 어울리지 않는다.

\n\n\n\n

반드시 **awsLoadBalancerController** 를 사용할떈 target option을 IP로 사용하길 추천한다.

\n\n\n\n\n\n\n\n\n\n\n\n\n