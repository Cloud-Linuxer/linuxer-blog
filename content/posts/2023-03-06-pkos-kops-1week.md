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

\n

이번에 스터디에 참가하게 되었다.

\n\n\n\n

가시다님의 PKOS!

\n\n\n\n

스터디할시에 사용하는 책은 [24단계 실습으로 정복하는 쿠버네티스](http://www.yes24.com/Product/Goods/115187666) 이다.

\n\n\n\n\n\n\n\n

kOps를 프로비저닝하는데 오타가 발생해서 심심해서 스크립트를 만들었다.  
그덕에 한번 다시 만들었다.

\n\n\n\n

```
#!/bin/bash\n\necho "클러스터명-도메인을 입력해주세요 : "\nread KOPS_CLUSTER_NAME\necho "버킷명을 입력해 주세요 s3:// 는 입력하지 않아도 됩니다. : "\nread  KOPS_STATE_STORE\n# Access Key를 입력 받음\nread -p "엑세스키를 입력해주세요 : " ACCESS_KEY\n\n# Secret Access Key를 입력 받음\nread -p "시크릿키를 입력해주세요 : " SECRET_KEY\n\n# AWS 계정 구성\naws configure set aws_access_key_id $ACCESS_KEY\naws configure set aws_secret_access_key $SECRET_KEY\necho 'export AWS_PAGER=""' >>~/.bashrc\necho "export REGION=ap-northeast-2" >>~/.bashrc\necho "export KOPS_CLUSTER_NAME=$KOPS_CLUSTER_NAME" >>~/.bashrc\necho "export KOPS_STATE_STORE=s3://$KOPS_STATE_STORE" >>~/.bashrc\n\nkops create cluster --zones="$REGION"a,"$REGION"c --networking amazonvpc --cloud aws \\\n--master-size t3.medium --node-size t3.medium --node-count=2 --network-cidr 172.30.0.0/16 \\\n--ssh-public-key ~/.ssh/id_rsa.pub --name=$KOPS_CLUSTER_NAME --kubernetes-version "1.24.10" --dry-run -o yaml > mykops.yaml\n\n\nkops create cluster --zones="$REGION"a,"$REGION"c --networking amazonvpc --cloud aws \\\n--master-size t3.medium --node-size t3.medium --node-count=2 --network-cidr 172.30.0.0/16 \\\n--ssh-public-key ~/.ssh/id_rsa.pub --name=$KOPS_CLUSTER_NAME --kubernetes-version "1.24.10" -y\n\nsource <(kubectl completion bash)\necho 'source <(kubectl completion bash)' >> ~/.bashrc\necho 'alias k=kubectl' >> ~/.bashrc\necho 'complete -F __start_kubectl k' >> ~/.bashrc
```

\n\n\n\n

read 명령어를 이용하여 스크립트에 변수를 부여하고 입력받은 변수를 이용하여 aws configure 를 설정하고, kops 명령어로 k8s 클러스터를 프로비저닝한다.

\n\n\n\n

이거다음에는 사실 initscript 에 내가원하는 값을 넣는게 제일 편하나 그건..좀 공개하기 애매하니 스크립트라도 공개한다.

\n