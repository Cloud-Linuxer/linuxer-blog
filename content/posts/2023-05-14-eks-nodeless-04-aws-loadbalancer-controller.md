---
title: "EKS-NodeLess-04-AWS-LoadBalancer-Controller"
date: 2023-05-14T18:56:27+09:00
draft: false
categories: ["AWS", "Kubernetes"]
tags: ["nodeless", "fargete", "awsingress", "ingress", "AWS LoadBalancer Controller"]
slug: "eks-nodeless-04-aws-loadbalancer-controller"
aliases:
  - /eks-nodeless-04-aws-loadbalancer-controller/
  - /eks-nodeless-04-aws-loadbalancer-controller/
---


AWS LoadBalancer Controller 도 Fargate에 올려야 한다.

비교적 간단한데, Controller Pod에 annotations 한줄만 추가하면된다.

먼저 추가할때 Policy 를 생성한다.

```bash
VPC_NAME=myeks-VPC // VPC NAME 으로 변경 CLUSTER_NAME=myeks REGION=ap-northeast-2 curl -O https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.4.7/docs/install/iam_policy.json
aws iam create-policy \\
    --policy-name AWSLoadBalancerControllerIAMPolicy \\
    --policy-document file://iam_policy.json
POLICY_ARN=`aws iam list-policies | grep Arn | grep AWSLoadBalancerControllerIAMPolicy | awk -F\\" '{print $4}'` VPC_ID=$(aws ec2 describe-vpcs --query 'Vpcs[?contains(Tags[?Key==`Name`].Value[], `'$VPC_NAME'`) == `true`].[VpcId]' --output text)
```bash
이 Policy를 이용하여 eksctl에서 사용할거다. POLICY_ARN은 전체 Policy 에서 AWSLoadBalancerControllerIAMPolicy 의 arn을 추출한다.

```text
eksctl create iamserviceaccount \\
  --cluster=myeks \\
  --namespace=kube-system \\
  --name=aws-load-balancer-controller \\
  --role-name AmazonEKSLoadBalancerControllerRole \\
  --attach-policy-arn=$POLICY_ARN \\
  --approve
```
```bash
  helm install aws-load-balancer-controller eks/aws-load-balancer-controller \\
  -n kube-system \\
  --set clusterName=$CLUSTER_NAME \\
  --set serviceAccount.create=false \\
  --set serviceAccount.name=aws-load-balancer-controller \\
  --set region=$REGION \\
  --set vpcId=$VPC_ID
```bash
로 보통 AWS LoadBalancer Controller 를 설치해 줘야 하지만 우리는 Fargate annotations 추가 한단계를 더 거쳐야 한다.

```bash
kubectl patch deployment aws-load-balancer-controller -n kube-system --type=json -p='[{"op": "add", "path": "/spec/template/metadata/annotations/eks.amazonaws.com~1fargate-profile", "value":"kube-system"}]' kubectl rollout restart deployment aws-load-balancer-controller -n kube-system
```
다음과 같이 patch 를 하고 rollout restart 까지 하면 pod가 Fargate 로 생성된다.

```text
k get pod -o wide NAME                                            READY   STATUS    RESTARTS   AGE     IP               NODE                                                        NOMINATED NODE   READINESS GATES aws-load-balancer-controller-76db948d9b-qzpsd   1/1     Running   0          46s     192.168.11.65    fargate-ip-192-168-11-65.ap-northeast-2.compute.internal    <none>           <none> aws-load-balancer-controller-76db948d9b-t26qt   1/1     Running   0          88s     192.168.11.180   fargate-ip-192-168-11-180.ap-northeast-2.compute.internal   <none>           <none>
```bash
시간날때마다 Fargate 로 추가되어야 하는 에드온들을 Fargate 로 생성하는 방법을 작성하겠다.

읽어줘서 감사하다!
