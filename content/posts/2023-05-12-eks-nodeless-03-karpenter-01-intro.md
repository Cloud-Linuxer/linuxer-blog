---
title: "EKS-NodeLess-03-Karpenter-01-intro"
date: 2023-05-12T10:10:00+09:00
draft: false
categories: ["AWS", "Kubernetes"]
tags: ["EKS", "nodeless", "karpenter"]
slug: "eks-nodeless-03-karpenter-01-intro"
aliases:
  - /eks-nodeless-03-karpenter-01-intro/
  - /eks-nodeless-03-karpenter-01-intro/
---


NodeLess 컨셉에서 제일 중요한 역할을 맡고 있는 Karpenter 다.


Karpenter 의 기본적인 아키텍처 부터 리뷰해볼까 한다. 그렇다면 그전에 Cluster Autoscaler 부터 설명해야 한다.


Cluster Autoscaler 는 보통 CA라 부른다. 간략하게 플로우를 설명하겠다.


1. Kubernetes에 새로운 Pod 가 프로비저닝 되었을때 Pod는 노드그룹에 스케줄링 된다.


2. 노드그룹에 자원이 부족하면 CA가 트리거 된다.


3. CA는 AWS 의 ASG에 새로운 로드를 요청한다.


4. ASG는 새로운노드를 생성하고 노드그룹에 추가한다.


5. 새로 스케줄링된 노드에 Pod가 생성된다.


생략된 단계가 있지만 실제로 이 단계를 모두 거쳐야 인스턴스가 EKS에 연결되고 노드그룹에 인스턴스가 노출된다. 그렇다면 단순히 ASG에서 노드를 제거해본 경험이 있는가? 있다면 알것이다. 이건 가끔 커피한잔하고 와도 제거안된 인스턴스가 있는 경우도 있다.


ASG가 나쁜건 아니다. 반응성이 좀 떨어질 뿐이다.
하지만, Kubernetes 에 어울리는 솔루션은 아니라 생각했다.


그렇다면 Kerpenter 의 간략한 플로우는 어떨까?


1. default-scheduler 는 Karpenter API에 새 파드를 요청한다.


2. Karpenter 컨트롤러는 Pod를 프로비저닝 할수 있는 노드를 찾는다.


3. 노드가 없으면 Karpenter는 AWS SDK를 이용하여 AWS에 새 노드를 요청한다.


4. AWS는 새노드를 생성하고 새노드가 프로비저닝 되면 클러스터에 Join 하게 된다


5. 노드가 추가되면 Karpenter는 Node를 감지하여 Kubernetes scheduler에 Node 준비를 알린다.


6. Kubernetes scheduler 는 Pod를 프로비저닝 한다


조금더 상세한 내용을 추가해서 설명했는데, 실제로는 노드그룹이나 CA ASG같은게 빠지고 노드에 대한 부분은 카펜터가 모두 AWS SDK로 컨트롤 한다. 여러 단계들을 제거함으로 빨라진것이다.
