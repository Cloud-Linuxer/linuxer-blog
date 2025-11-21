---
title: "EKS-NodeLess-07-AWS-Karpenter-CRD"
date: 2023-05-20T18:25:40+09:00
draft: false
categories: ["AWS", "Kubernetes"]
slug: "eks-nodeless-07-aws-karpenter-crd"
aliases:
  - /eks-nodeless-07-aws-karpenter-crd/
  - /eks-nodeless-07-aws-karpenter-crd/
---


이제 카펜터의 CRD를 정리하고 어떻게 사용해야 하는지 이야기를 해보려고 한다. 거의 끝에 다왔다.

https://linuxer.name/2023/05/eks-nodeless-05-aws-karpenter-component/

Karpenter Component 를 설명할때 CRD를 설명했었다.

다시 이야기 하자면 **provisioners.karpenter.sh** - **`provisioners`** - / **awsnodetemplates.karpenter.k8s.aws** -**`awsnodetemplates`** - 두가지를 셋팅해야 한다.

먼저 **`provisioners`** 를 이야기 해볼까 한다.

```yaml
apiVersion: karpenter.sh/v1alpha5 kind: Provisioner metadata:
  name: default spec:
  requirements:

    - key: karpenter.k8s.aws/instance-category
      operator: In
      values: [c, m, r]

    - key: karpenter.k8s.aws/instance-generation
      operator: Gt
      values: ["2"]
  providerRef:
    name: default
```bash
<https://karpenter.sh/v0.27.3/concepts/provisioners/>

<https://github.com/aws/karpenter/tree/main/examples>

**`provisioners`** 의 사용은 이 두가지 링크를 참고하면 대부분 할수있는데, 간단하게 **`provisioners`**를 설명하자면 노드를 만들기 위한 조건을 정의하는거다.

예를 들자면 인스턴스 페밀리 / 인스턴스 CPU 갯수 / 하이퍼바이저 유형 / AZ / kubeletConfiguration 등을 설정할수 있다. 프로비저너는 노드를 생성하고 관리하는데 사용되는 CRD다

<https://karpenter.sh/v0.27.5/concepts/node-templates/>

```yaml
apiVersion: karpenter.k8s.aws/v1alpha1 kind: AWSNodeTemplate metadata:
  name: default spec:
  subnetSelector:
    karpenter.sh/discovery: "${CLUSTER_NAME}"
  securityGroupSelector:
    karpenter.sh/discovery: "${CLUSTER_NAME}"
```
**`awsnodetemplates`** 은 필수 요소들이 있다. 그것이 Subnet / SecurityGroup 다.
서브넷 셀렉터는 subnet-id 혹은 서브넷에 연결된 특정 태그로 동작한다.
보안그룹또한 ID혹은 특정 태그다.

**`awsnodetemplates`**은 ami / userdata ebs 등들을 컨트롤하려 원하는 노드의 OS를 선택할수도 있다.
