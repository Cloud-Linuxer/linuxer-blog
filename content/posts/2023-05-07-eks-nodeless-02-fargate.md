---
title: "EKS-NodeLess-02-Fargate"
date: 2023-05-07T19:54:14+09:00
draft: false
categories: ["AWS", "Kubernetes"]
tags: ["EKS", "nodeless", "fargate"]
slug: "eks-nodeless-02-fargate"
aliases:
  - /eks-nodeless-02-fargate/
  - /eks-nodeless-02-fargate/
---


![](/images/2023/05/image-1-1024x725.png)

```
# k get pod -A -o wide NAMESPACE     NAME                         READY   STATUS    RESTARTS   AGE    IP               NODE                                                        NOMINATED NODE   READINESS GATES default       nginx-pod                    1/1     Running   0          11m    192.168.12.217   ip-192-168-12-150.ap-northeast-2.compute.internal           <none>           <none> karpenter     karpenter-5bffc6f5d8-6f779   1/1     Running   0          125m   192.168.12.99    fargate-ip-192-168-12-99.ap-northeast-2.compute.internal    <none>           <none> karpenter     karpenter-5bffc6f5d8-84mjn   1/1     Running   0          130m   192.168.11.201   fargate-ip-192-168-11-201.ap-northeast-2.compute.internal   <none>           <none> kube-system   aws-node-h5z8d               1/1     Running   0          11m    192.168.12.150   ip-192-168-12-150.ap-northeast-2.compute.internal           <none>           <none> kube-system   coredns-fd69467b9-4nk6x      1/1     Running   0          127m   192.168.12.52    fargate-ip-192-168-12-52.ap-northeast-2.compute.internal    <none>           <none> kube-system   coredns-fd69467b9-cqqpq      1/1     Running   0          125m   192.168.11.122   fargate-ip-192-168-11-122.ap-northeast-2.compute.internal   <none>           <none> kube-system   kube-proxy-z8qlj             1/1     Running   0          11m    192.168.12.150   ip-192-168-12-150.ap-northeast-2.compute.internal           <none>           <none>

```
먼저 예제를 보여준다.
NodeLess EKS 컨셉의 기반이다. nginx-pod / aws-node-h5z8d / kube-proxy-z8qlj 는 카펜터가 만든 노드위에 올라가 있다.

NodeLess 의 컨셉은 두가지를 기반으로 한다.

쿠버네티스 컴포넌트 kube-system namespace Pod들은 Fargate에 올린다.
여기에 에드온이나 관리가 필요한 Pod도 포함된다. karpenter controller라던가..AWS ELB Controller 라던가 그런 에드온들이 그런 역할을 한다.

Node가 필요한 Pod는 NodeGroup을 사용하지 않고 Karpenter를 사용한다.

그럼 NodeGroup이 없는 클러스터부터 만드는 방법이다.

<https://eksctl.io/usage/fargate-support/>

```
eksctl create cluster --fargate
```
간단하다 옵션으로 --fargate를 주면된다.

Fargate profile 같은경우에는 사실 콘솔에서 손으로 만들면 편하다. subnet이나 iam role 넣어주는게....그렇지 않다면 먼저 aws cli 부터 학습해야 한다. eksctl이 자동으로 해주는 부분도 있지만 필수요소는 알아야 하기 때문이다.

<https://awscli.amazonaws.com/v2/documentation/api/latest/reference/eks/create-fargate-profile.html>

```
aws eks create-fargate-profile --fargate-profile-name kube-system --cluster-name myeks --pod-execution-role-arn arn:aws:iam::123456789:role/AmazonEKSFargatePodExecutionRole --subnets "subnet-1" "subnet-2" "subnet-3"
```
<https://docs.aws.amazon.com/ko_kr/eks/latest/userguide/pod-execution-role.html> 역할생성은 이링크를 참고한다.

이런식으로 만들고 파게이트는 네임스페이스로 지정하면 네임스페이스에 만들어지는 톨레이션이나 다른 노드 어피니티등을 가지지 않은 Pod를 Fargate로 프로비저닝 한다. 이때 일반적인 쿠버네티스와 다른 부분은 Fargate 스케줄러(fargate-scheduler)가 별도로 동작하여 Fargate를 프로비저닝한다. 일반적인 경우엔 (default-scheduler)가 Pod를 프로비저닝 한다.

이 차이를 알아두면 어떤 노드를 물고있는지 확인하기 편하다.
