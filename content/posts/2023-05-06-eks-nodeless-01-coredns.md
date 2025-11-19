---
title: "EKS-NodeLess-01-CoreDNS"
date: 2023-05-06T16:10:45+09:00
draft: false
categories: ["AWS", "Kubernetes"]
tags: ["EKS", "fargeate", "coredns"]
slug: "eks-nodeless-01-coredns"
aliases:
  - /eks-nodeless-01-coredns/
  - /eks-nodeless-01-coredns/
---


EKS의 관리영역중 Addon 이나 필수 컴포넌트중에 Node에서 동작해야하는 것들이 있다. 이 경우에 NodeGroup을 운영해야한다. NodeGroup에 여러 파드들이 스케줄링되고 관리형 Pod들은 다른 서비스에 운영되는 NodeGroup과 섞여서 스케줄리되어야 하는데, 이것의 가장큰 문제는 Node의 사망이 기능의 장애로 이어진다는 점이다. 따라서 Node를 전용 Node로 사용하면 좋은데 아주작은 노드를 스케줄링한다고 해도 관리되어야 하는 대상이 됨은 틀림없고, 노드를 정해서 사용해야 하는 문제점들이 생기게된다.


이러한 문제를 해결하기에 EKS에서는 Fargate가 있다. 1Node - 1Pod 라는게 아주 중요한 포인트다.


CoreDNS는 클러스터에 최저 2개의 Pod가 스케줄링되어야 한다.


<https://docs.aws.amazon.com/ko_kr/eks/latest/userguide/fargate-profile.html>


eksctl를 사용하여 Fargate 프로파일을 생성하려면 다음 eksctl 명령으로 Fargate 프로파일을 생성하고 모든 example value를 고유한 값으로 바꿉니다. 네임스페이스를 지정해야 합니다. 그러나 --labels 옵션은 필요하지 않습니다.


```
eksctl create fargateprofile \\\n    --cluster my-cluster \\\n    --name kube-system \\\n    --namespace kube-system
```


다음과 같이 생성해 주면된다. 그럼 kube-system namespace로 스케줄링되는 Pod는 Fargate로 생성되게 된다.


그다음은 CoreDNS를 패치하고 재시작하면된다.


<https://docs.aws.amazon.com/ko_kr/prescriptive-guidance/latest/patterns/deploy-coredns-on-amazon-eks-with-fargate-automatically-using-terraform-and-python.html>


```
kubectl patch deployment coredns -n kube-system --type=json -p='[{"op": "remove", "path": "/spec/template/metadata/annotations", "value": "eks.amazonaws.com/compute-type"}]' kubectl rollout restart -n kube-system deployment coredns
```


이렇게 진행하면 CoreDNS를 Fargate로 실행하게 된다.


```
 k get pod -o wide NAME                      READY   STATUS    RESTARTS   AGE     IP              NODE                                                       NOMINATED NODE   READINESS GATES coredns-fd69467b9-bsh88   1/1     Running   0          5h18m   192.168.13.23   fargate-ip-192-168-13-23.ap-northeast-2.compute.internal   <none>           <none> coredns-fd69467b9-gn24k   1/1     Running   0          5h18m   192.168.12.34   fargate-ip-192-168-12-34.ap-northeast-2.compute.internal   <none>           <none>\n
```


다음과 같이 스케줄링되면 정상적으로 배포 된것이다.
