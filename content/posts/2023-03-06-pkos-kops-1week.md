---
title: "PKOS-kOps-1Week"
date: 2023-03-06T21:11:35+09:00
draft: false
categories: ["Linux", "Kubernetes"]
tags: ["bash", "kops", "cli"]
slug: "pkos-kops-1week"
aliases:
  - /pkos-kops-1week/
  - /pkos-kops-1week/
---


이번에 스터디에 참가하게 되었다.

가시다님의 PKOS!

스터디할시에 사용하는 책은 [24단계 실습으로 정복하는 쿠버네티스](http://www.yes24.com/Product/Goods/115187666) 이다.

kOps를 프로비저닝하는데 오타가 발생해서 심심해서 스크립트를 만들었다.
그덕에 한번 다시 만들었다.

```
#!/bin/bash
echo "클러스터명-도메인을 입력해주세요 : " read KOPS_CLUSTER_NAME echo "버킷명을 입력해 주세요 s3:// 는 입력하지 않아도 됩니다. : " read  KOPS_STATE_STORE # Access Key를 입력 받음 read -p "엑세스키를 입력해주세요 : " ACCESS_KEY
# Secret Access Key를 입력 받음 read -p "시크릿키를 입력해주세요 : " SECRET_KEY
# AWS 계정 구성 aws configure set aws_access_key_id $ACCESS_KEY aws configure set aws_secret_access_key $SECRET_KEY echo 'export AWS_PAGER=""' >>~/.bashrc echo "export REGION=ap-northeast-2" >>~/.bashrc echo "export KOPS_CLUSTER_NAME=$KOPS_CLUSTER_NAME" >>~/.bashrc echo "export KOPS_STATE_STORE=s3://$KOPS_STATE_STORE" >>~/.bashrc
kops create cluster --zones="$REGION"a,"$REGION"c --networking amazonvpc --cloud aws \\ --master-size t3.medium --node-size t3.medium --node-count=2 --network-cidr 172.30.0.0/16 \\ --ssh-public-key ~/.ssh/id_rsa.pub --name=$KOPS_CLUSTER_NAME --kubernetes-version "1.24.10" --dry-run -o yaml > mykops.yaml
 kops create cluster --zones="$REGION"a,"$REGION"c --networking amazonvpc --cloud aws \\ --master-size t3.medium --node-size t3.medium --node-count=2 --network-cidr 172.30.0.0/16 \\ --ssh-public-key ~/.ssh/id_rsa.pub --name=$KOPS_CLUSTER_NAME --kubernetes-version "1.24.10" -y
source <(kubectl completion bash) echo 'source <(kubectl completion bash)' >> ~/.bashrc echo 'alias k=kubectl' >> ~/.bashrc echo 'complete -F __start_kubectl k' >> ~/.bashrc
```

read 명령어를 이용하여 스크립트에 변수를 부여하고 입력받은 변수를 이용하여 aws configure 를 설정하고, kops 명령어로 k8s 클러스터를 프로비저닝한다.

이거다음에는 사실 initscript 에 내가원하는 값을 넣는게 제일 편하나 그건..좀 공개하기 애매하니 스크립트라도 공개한다.
