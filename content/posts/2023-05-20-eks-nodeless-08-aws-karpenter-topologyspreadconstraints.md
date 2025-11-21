---
title: "EKS-NodeLess-08-AWS-Karpenter-topologySpreadConstraints"
date: 2023-05-20T20:45:29+09:00
draft: false
categories: ["AWS", "Kubernetes"]
tags: ["EKS", "karpenter", "topologySpreadConstraints"]
slug: "eks-nodeless-08-aws-karpenter-topologyspreadconstraints"
aliases:
  - /eks-nodeless-08-aws-karpenter-topologyspreadconstraints/
  - /eks-nodeless-08-aws-karpenter-topologyspreadconstraints/
---


topologySpreadConstraints 을 사용한 Karpenter 테스트를 진행하겠다.

topologySpreadConstraints 테스트는 Topology Aware Hint 를 예비한 테스트다.

<https://aws.amazon.com/ko/blogs/tech/amazon-eks-reduce-cross-az-traffic-costs-with-topology-aware-hints/>

참고할 부분이 있다면 이 글을 참고하길 바란다.

간략하게 설명하자면 Kubernetes 에서 Cross Zone Traffic 의 문제로 비용이 막대하게 발생할수 있다. 또한 Cross-AZ로 인하여 약간의 레이턴시가 발생할수도 있기때문에 Topology Aware Hint는 여러 문제점들을 줄여주는 역할을 한다.

조건은 몇가지가 있는데, Service 로 연결되 AZ가 수평적으로 동일하게 노드가 배포되어있고 서비스에

```yaml
apiVersion: v1
kind: Service
metadata:
  name: service
  annotations:
    service.kubernetes.io/topology-aware-hints: auto
```bash
다음과 같은 annotations 붙어있어야 한다.

그럼먼저 우리는 Provisioner가 자동으로 노드를 Deprovisioning 하도록 설정하자.

```yaml
apiVersion: karpenter.sh/v1alpha5 kind: Provisioner metadata:
  name: default spec:
  consolidation:
    enabled: true
  requirements:

    - key: karpenter.k8s.aws/instance-category
      operator: In
      values: [ t, m, c ]
  providerRef:
    name: default --- apiVersion: karpenter.k8s.aws/v1alpha1 kind: AWSNodeTemplate metadata:
  name: default spec:
  subnetSelector:
    karpenter.sh/discovery: "${CLUSTER_NAME}"
  securityGroupSelector:
    karpenter.sh/discovery: "${CLUSTER_NAME}"

```
consolidation enabled 옵션은 Pod 의 리소스 요구조건에 따라서 Karpenter 가 알아서 노드를 스케줄링한다.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: host-spread
spec:
  replicas: 20
  selector:
    matchLabels:
      app: host-spread
  template:
    metadata:
      labels:
        app: host-spread
    spec:
      containers:
      - image: public.ecr.aws/eks-distro/kubernetes/pause:3.2
        name: host-spread
        resources:
          requests:
            cpu: "1"
            memory: 256M
      topologySpreadConstraints:
      - labelSelector:
          matchLabels:
            app: host-spread
        maxSkew: 2
        topologyKey: kubernetes.io/hostname
        whenUnsatisfiable: DoNotSchedule
      - labelSelector:
          matchLabels:
            app: host-spread
        maxSkew: 5
        topologyKey: topology.kubernetes.io/zone
        whenUnsatisfiable: DoNotSchedule
```bash
topologyKey: kubernetes.io/zone maxSkew: 2는 하나의 호스트 즉 노드간 파드의 차이는 maxSkew: 2 를 초과할수 없다. topologyKey: topology.kubernetes.io/zone maxSkew: 5 zone 간 pod의 갯수는 maxSkew: 5 초과 할수 없으므로 하나의 zone에서만 pod가 스케줄링된다면 20개의 replicas 를 요청한다 해도 5개의 pod 만 스케줄링 된다.

AZ별로 제공하는 유형의 인스턴스 페일리가 달라서 특정 유형만 사용하려고 하면 프로비저닝 조건에 걸려서 스케줄링이 쉽지 않다.

karpenter 의 강력함은 테스트중에 확인할수 있는데, 42s 만에 Pod 가 Running 된다. 42초안에 Node도 프로비저닝 된다는 말이다.

```text
2023-05-20T11:03:34.806Z\tERROR\tcontroller.provisioner\tCould not schedule pod, incompatible with provisioner "default", no instance type satisfied resources {"cpu":"1","memory":"256M","pods":"1"} and requirements karpenter.k8s.aws/instance-category In [c m t], kubernetes.io/os In [linux], kubernetes.io/arch In [amd64], karpenter.sh/provisioner-name In [default], karpenter.sh/capacity-type In [on-demand], topology.kubernetes.io/zone In [ap-northeast-2a]\t{"commit": "d7e22b1-dirty", "pod": "default/host-spread-fbbf7c9d9-x4lfd"}
```
topologySpreadConstraints 옵션을 테스트하면서 느꼈는데, 여러 요인들로 잘 스케줄링하지 못한다.

두가지 조건에 의해서 pod는 모두다 스케줄링 되지 못하는데, 노드를 스케줄링하지 못해서 걸리기도 한다. 조건은 확실히 걸리긴한다.

```text
k get node --show-labels | grep -v fargate | awk -F"topology.kubernetes.io/" '{print $3}' | sort
zone=ap-northeast-2a
zone=ap-northeast-2a
zone=ap-northeast-2a
zone=ap-northeast-2b
zone=ap-northeast-2b
zone=ap-northeast-2b
zone=ap-northeast-2c
```bash
다음과같이 노드가 a 3대 b 3대 c 1대 스케줄링 되면 모두 14개의 pod가 스케줄링된다. C zone때문에 두번째 조건에 걸리기 때문이다. 다양한 조건을 사용하면 이와 같이 균등하게 zone 에 스케줄링 하긴 어려운점이 있다. 적당히 조건을 걸어주면 잘 작동한다.

```yaml
      - labelSelector:
          matchLabels:
            app: host-spread
        maxSkew: 2
        topologyKey: kubernetes.io/hostname
        whenUnsatisfiable: DoNotSchedule
```
이 조건을 삭제하면 topology.kubernetes.io/zone maxSkew 5 만 남겨서 프로비저닝 해보면 비대칭으로 az 에 node가 프로비저닝 되지만 조건에만 맞는다면 pod를 모두 생성한다.

```bash
k get pod
NAME                          READY   STATUS    RESTARTS   AGE
host-spread-dd5f6c569-49ps7   1/1     Running   0          115s
host-spread-dd5f6c569-8772p   1/1     Running   0          115s
host-spread-dd5f6c569-9q2hn   1/1     Running   0          115s
host-spread-dd5f6c569-b68k2   1/1     Running   0          115s
host-spread-dd5f6c569-bfhv5   1/1     Running   0          115s
host-spread-dd5f6c569-bqqz2   1/1     Running   0          116s
host-spread-dd5f6c569-bsp8m   1/1     Running   0          115s
host-spread-dd5f6c569-dh8wx   1/1     Running   0          115s
host-spread-dd5f6c569-ffjdg   1/1     Running   0          115s
host-spread-dd5f6c569-jghmr   1/1     Running   0          115s
host-spread-dd5f6c569-jhbxg   1/1     Running   0          116s
host-spread-dd5f6c569-kf69q   1/1     Running   0          115s
host-spread-dd5f6c569-ksktv   1/1     Running   0          115s
host-spread-dd5f6c569-lbqmv   1/1     Running   0          115s
host-spread-dd5f6c569-mbf2g   1/1     Running   0          116s
host-spread-dd5f6c569-pd92p   1/1     Running   0          115s
host-spread-dd5f6c569-pgphc   1/1     Running   0          115s
host-spread-dd5f6c569-ph59g   1/1     Running   0          115s
host-spread-dd5f6c569-sdp7d   1/1     Running   0          115s
host-spread-dd5f6c569-tf8v9   1/1     Running   0          115s

(user-linuxer@myeks:default) [root@myeks-bastion-EC2 EKS]# k get node --show-labels | grep -v fargate | awk -F"topology.kubernetes.io/" '{print $3}' | sort
zone=ap-northeast-2a
zone=ap-northeast-2a
zone=ap-northeast-2a
zone=ap-northeast-2b
zone=ap-northeast-2b
zone=ap-northeast-2c
```bash
AZ 별로 균등하게 node를 프로비저닝 해야하는 방법이 필요하다.

<https://github.com/aws/karpenter/issues/2572>

일단 테스트한 결과와 git issues 를 보면 karpenter 가 topologySpreadConstraints 에 적절히 대응되지 않는것을 느낄수 있었다. 따라서 minDomains 옵션으로 3개의 zone을 지정도 해보았으나 썩 좋은 결과는 없었다.

따라서 다이나믹하게 Node를 프로비저닝하면서 사용할수는 없을것같고, 미리 Node를 프로비저닝 하는 구성에선 될법한데, 그건 Karpenter 의 패턴은 아니라고 느꼈다.
