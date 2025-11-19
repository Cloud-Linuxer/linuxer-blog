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

\n

AWS LoadBalancer Controller 도 Fargate에 올려야 한다.

\n\n\n\n

비교적 간단한데, Controller Pod에 annotations 한줄만 추가하면된다.

\n\n\n\n

먼저 추가할때 Policy 를 생성한다.

\n\n\n\n

```
VPC_NAME=myeks-VPC // VPC NAME 으로 변경\nCLUSTER_NAME=myeks\nREGION=ap-northeast-2\ncurl -O https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.4.7/docs/install/iam_policy.json\n\naws iam create-policy \\\n    --policy-name AWSLoadBalancerControllerIAMPolicy \\\n    --policy-document file://iam_policy.json\n\nPOLICY_ARN=`aws iam list-policies | grep Arn | grep AWSLoadBalancerControllerIAMPolicy | awk -F\\" '{print $4}'`\nVPC_ID=$(aws ec2 describe-vpcs --query 'Vpcs[?contains(Tags[?Key==`Name`].Value[], `'$VPC_NAME'`) == `true`].[VpcId]' --output text)
```

\n\n\n\n

이 Policy를 이용하여 eksctl에서 사용할거다. POLICY\_ARN은 전체 Policy 에서 AWSLoadBalancerControllerIAMPolicy 의 arn을 추출한다.

\n\n\n\n

```
eksctl create iamserviceaccount \\\n  --cluster=myeks \\\n  --namespace=kube-system \\\n  --name=aws-load-balancer-controller \\\n  --role-name AmazonEKSLoadBalancerControllerRole \\\n  --attach-policy-arn=$POLICY_ARN \\\n  --approve
```

\n\n\n\n

```
  helm install aws-load-balancer-controller eks/aws-load-balancer-controller \\\n  -n kube-system \\\n  --set clusterName=$CLUSTER_NAME \\\n  --set serviceAccount.create=false \\\n  --set serviceAccount.name=aws-load-balancer-controller \\\n  --set region=$REGION \\\n  --set vpcId=$VPC_ID
```

\n\n\n\n

로 보통 AWS LoadBalancer Controller 를 설치해 줘야 하지만 우리는 Fargate annotations 추가 한단계를 더 거쳐야 한다.

\n\n\n\n

```
kubectl patch deployment aws-load-balancer-controller -n kube-system --type=json -p='[{"op": "add", "path": "/spec/template/metadata/annotations/eks.amazonaws.com~1fargate-profile", "value":"kube-system"}]'\nkubectl rollout restart deployment aws-load-balancer-controller -n kube-system
```

\n\n\n\n

다음과 같이 patch 를 하고 rollout restart 까지 하면 pod가 Fargate 로 생성된다.

\n\n\n\n

```
k get pod -o wide\nNAME                                            READY   STATUS    RESTARTS   AGE     IP               NODE                                                        NOMINATED NODE   READINESS GATES\naws-load-balancer-controller-76db948d9b-qzpsd   1/1     Running   0          46s     192.168.11.65    fargate-ip-192-168-11-65.ap-northeast-2.compute.internal    <none>           <none>\naws-load-balancer-controller-76db948d9b-t26qt   1/1     Running   0          88s     192.168.11.180   fargate-ip-192-168-11-180.ap-northeast-2.compute.internal   <none>           <none>
```

\n\n\n\n

시간날때마다 Fargate 로 추가되어야 하는 에드온들을 Fargate 로 생성하는 방법을 작성하겠다.

\n\n\n\n

읽어줘서 감사하다!

\n