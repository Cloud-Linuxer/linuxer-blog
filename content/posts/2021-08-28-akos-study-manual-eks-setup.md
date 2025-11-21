---
title: "AKOS-Study-Manual-EKS-Setup"
date: 2021-08-28T14:24:25+09:00
draft: false
categories: ["AWS"]
tags: ["AKOS"]
slug: "akos-study-manual-eks-setup"
aliases:
  - /akos-study-manual-eks-setup/
  - /akos-study-manual-eks-setup/
---


두번째로 진행한 가시다님과의 스터디! AKOS다.

가시다님은 편한 스터디를 위해서 항상 CloudFromation 을 제공해주시지만 청개구리인 나는 사실 그대로 따라해본적은 없다. 이번에도 그렇다. 먼저 VPC와 bastion-hsot를 생성하는 cloudformation 템플릿을 주셨지만 어찌..엔지니어가 된자의 도리로 그대로 따라만 하겠는가..

라고 생각하여 일단 새로 생성하는것이 아닌..내가 사용하던 EC2에 셋팅을 했다.

미리 사용하던 VPC가 있었기에 VPC도 그대로 쓴다.

aws cli,eksctl,kubectl,
실습에서 사용하는 postgresql cmd docker 등 실습에 필요한 것들을 설치했다.
해당 부분은 cloudformation 템플릿에 user-data 로 셋팅하는 부분을 참고했다.

bastion-host를 셋팅후 bastion-host에 이미 ssm 을 사용하기 위해 추가했던 역할에 실습에 사용하기위한 권한을 을 부여했다.

![](/images/2021/08/image-6.png)

실습이 끝나면 administratoraccess 권한을 제거한다.

![](/images/2021/08/image-8.png)

EC2에 부여된 역할도 확인했다.

나는 SSM을 사용하기 때문에 SSH로 인스턴스를 접근하지 않는다. 실습중에 SSH에 접근하기 위해 보안그룹을 여는과정이 있었는데, 그부분은 스킵한다.

![](/images/2021/08/image-9.png)

이런식으로 웹에서 콘솔을 사용할수 있다. SSH 와는 다르다 SSH와는..

![자쿠와는 다르다! 자쿠와는!"은 무슨 뜻일까?](https://t1.daumcdn.net/cfile/tistory/999157475E0552C128)

![](/images/2021/08/image-10.png)

키페어를 생성하는 중에 추가된게 보였다 pem 말고 이젠 ppk 방식의 키도 제공한다..
이전까지는 puttygen으로 제너레이터 하던부분이 개선된거 같다. 개꿀팁...와...

이제 EKS 구성!!

클러스터 구성은 다음과 같은 명령어를 사용한다.

```bash
eksctl create cluster --vpc-public-subnets $WKSubnets --name $CLUSTER_NAME --region $AWS_REGION --version 1.21 \\
 --nodegroup-name $CLUSTER_NAME-nodegroup --node-type t3.medium --nodes 3 --nodes-min 3 --nodes-max 6 \\
 --with-oidc --node-volume-size=20 --ssh-access --ssh-public-key $MySSHKeypair --dry-run
```bash
근데 또 이대로 생성은 못한다. 이유는 나는..수동으로 하기때문.......가자 매뉴얼의 길!!

```bash
echo "export WKVPC=`aws ec2 describe-vpcs --filters Name=tag:Name,Values=Linuxer-Blog-VPC | jq -r '.Vpcs[].VpcId'`" >> ~/.bashrc echo $WKVPC vpc-094808933b68add7c echo "export AWS_REGION=$AWS_REGION" >> ~/.bashrc echo "export CLUSTER_NAME=first-eks" >> ~/.bashrc echo "export WKSubnets=subnet-0a603a222db0cce10,subnet-007964ce4a003361a,subnet-007813cf58631ef3b" >> ~/.bashrc echo "export MySSHKeypair=eks-test-key" >> ~/.bashrc source ~/.bashrc
```bash
그리고 클러스터 생성을 dry-run 으로 하면

```yaml
ksctl create cluster --vpc-public-subnets $WKSubnets --name $CLUSTER_NAME --region $AWS_REGION --version 1.21 \\ >  --nodegroup-name $CLUSTER_NAME-nodegroup --node-type t3.medium --nodes 3 --nodes-min 3 --nodes-max 6 \\ >  --with-oidc --node-volume-size=20 --ssh-access --ssh-public-key $MySSHKeypair --dry-run apiVersion: eksctl.io/v1alpha5 availabilityZones: - ap-northeast-2c - ap-northeast-2b - ap-northeast-2a cloudWatch:
  clusterLogging: {} iam:
  vpcResourceControllerPolicy: true
  withOIDC: true kind: ClusterConfig managedNodeGroups: - amiFamily: AmazonLinux2
  desiredCapacity: 3
  disableIMDSv1: false
  disablePodIMDS: false
  iam:
    withAddonPolicies:
      albIngress: false
      appMesh: false
      appMeshPreview: false
      autoScaler: false
      certManager: false
      cloudWatch: false
      ebs: false
      efs: false
      externalDNS: false
      fsx: false
      imageBuilder: false
      xRay: false
  instanceSelector: {}
  instanceType: t3.medium
  labels:
    alpha.eksctl.io/cluster-name: first-eks
    alpha.eksctl.io/nodegroup-name: first-eks-nodegroup
  maxSize: 6
  minSize: 3
  name: first-eks-nodegroup
  privateNetworking: false
  releaseVersion: ""
  securityGroups:
    withLocal: null
    withShared: null
  ssh:
    allow: true
    publicKeyPath: eks-test-key
  tags:
    alpha.eksctl.io/nodegroup-name: first-eks-nodegroup
    alpha.eksctl.io/nodegroup-type: managed
  volumeIOPS: 3000
  volumeSize: 20
  volumeThroughput: 125
  volumeType: gp3 metadata:
  name: first-eks
  region: ap-northeast-2
  version: "1.21" privateCluster:
  enabled: false vpc:
  autoAllocateIPv6: false
  cidr: 10.0.0.0/16
  clusterEndpoints:
    privateAccess: false
    publicAccess: true
  id: vpc-094808933b68add7c
  manageSharedNodeSecurityGroupRules: true
  nat:
    gateway: Disable
  subnets:
    public:
      ap-northeast-2a:
        az: ap-northeast-2a
        cidr: 10.0.11.0/24
        id: subnet-0a603a222db0cce10
      ap-northeast-2b:
        az: ap-northeast-2b
        cidr: 10.0.12.0/24
        id: subnet-007964ce4a003361a
      ap-northeast-2c:
        az: ap-northeast-2c
        cidr: 10.0.13.0/24
        id: subnet-007813cf58631ef3b
```bash
잘 동작한다.

```bash
eksctl create cluster --vpc-public-subnets $WKSubnets --name $CLUSTER_NAME --region $AWS_REGION --version 1.21 \\ >  --nodegroup-name $CLUSTER_NAME-nodegroup --node-type t3.medium --nodes 3 --nodes-min 3 --nodes-max 6 \\ >  --with-oidc --node-volume-size=20 --ssh-access --ssh-public-key $MySSHKeypair 2021-08-28 12:09:47 [ℹ]  eksctl version 0.63.0 2021-08-28 12:09:47 [ℹ]  using region ap-northeast-2 2021-08-28 12:09:47 [✔]  using existing VPC (vpc-094808933b68add7c) and subnets (private:map[] public:map[ap-northeast-2a:{subnet-0a603a222db0cce10 ap-northeast-2a 10.0.11.0/24} ap-northeast-2b:{subnet-007964ce4a003361a ap-northeast-2b 10.0.12.0/24} ap-northeast-2c:{subnet-007813cf58631ef3b ap-northeast-2c 10.0.13.0/24}]) 2021-08-28 12:09:47 [!]  custom VPC/subnets will be used; if resulting cluster doesn't function as expected, make sure to review the configuration of VPC/subnets 2021-08-28 12:09:47 [ℹ]  nodegroup "first-eks-nodegroup" will use "" [AmazonLinux2/1.21] 2021-08-28 12:09:47 [ℹ]  using EC2 key pair %!q(*string=<nil>) 2021-08-28 12:09:47 [ℹ]  using Kubernetes version 1.21 2021-08-28 12:09:47 [ℹ]  creating EKS cluster "first-eks" in "ap-northeast-2" region with managed nodes 2021-08-28 12:09:47 [ℹ]  will create 2 separate CloudFormation stacks for cluster itself and the initial managed nodegroup 2021-08-28 12:09:47 [ℹ]  if you encounter any issues, check CloudFormation console or try 'eksctl utils describe-stacks --region=ap-northeast-2 --cluster=first-eks' 2021-08-28 12:09:47 [ℹ]  CloudWatch logging will not be enabled for cluster "first-eks" in "ap-northeast-2" 2021-08-28 12:09:47 [ℹ]  you can enable it with 'eksctl utils update-cluster-logging --enable-types={SPECIFY-YOUR-LOG-TYPES-HERE (e.g. all)} --region=ap-northeast-2 --cluster=first-eks' 2021-08-28 12:09:47 [ℹ]  Kubernetes API endpoint access will use default of {publicAccess=true, privateAccess=false} for cluster "first-eks" in "ap-northeast-2" 2021-08-28 12:09:47 [ℹ]  2 sequential tasks: { create cluster control plane "first-eks", 3 sequential sub-tasks: { 4 sequential sub-tasks: { wait for control plane to become ready, associate IAM OIDC provider, 2 sequential sub-tasks: { create IAM role for serviceaccount "kube-system/aws-node", create serviceaccount "kube-system/aws-node" }, restart daemonset "kube-system/aws-node" }, 1 task: { create addons }, create managed nodegroup "first-eks-nodegroup" } } 2021-08-28 12:09:47 [ℹ]  building cluster stack "eksctl-first-eks-cluster" 2021-08-28 12:09:48 [ℹ]  deploying stack "eksctl-first-eks-cluster" 2021-08-28 12:10:18 [ℹ]  waiting for CloudFormation stack "eksctl-first-eks-cluster"
```bash
eksctl 도 내부적으론 cloudformation 으로 동작하는것을 알수있다.
eksctl 을 안쓰고 수동으로 node 만들고 EKS-master 에 연결하고 했다면 아마 좀힘들지 않았을까..? 하고 생각하는 중에 에러가 발생했다.

```bash
021-08-28 12:30:36 [✖]  unexpected status "ROLLBACK_IN_PROGRESS" while waiting for CloudFormation stack "eksctl-first-eks-nodegroup-first-eks-nodegroup" 2021-08-28 12:30:36 [ℹ]  fetching stack events in attempt to troubleshoot the root cause of the failure 2021-08-28 12:30:36 [!]  AWS::IAM::Role/NodeInstanceRole: DELETE_IN_PROGRESS 2021-08-28 12:30:36 [!]  AWS::EC2::LaunchTemplate/LaunchTemplate: DELETE_IN_PROGRESS 2021-08-28 12:30:36 [!]  AWS::EKS::Nodegroup/ManagedNodeGroup: DELETE_IN_PROGRESS 2021-08-28 12:30:36 [✖]  AWS::EKS::Nodegroup/ManagedNodeGroup: CREATE_FAILED – "Nodegroup first-eks-nodegroup failed to stabilize: [{Code: Ec2SubnetInvalidConfiguration,Message: One or more Amazon EC2 Subnets of [subnet-007964ce4a003361a, subnet-0a603a222db0cce10, subnet-007813cf58631ef3b] for node group first-eks-nodegroup does not automatically assign public IPaddresses to instances launched into it. If you want your instances to be assigned a public IP address, then you need to enable auto-assign public IP address for the subnet. See IP addressing in VPC guide: https://docs.aws.amazon.com/vpc/latest/userguide/vpc-ip-addressing.html#subnet-public-ip,ResourceIds: [subnet-007964ce4a003361a, subnet-0a603a222db0cce10, subnet-007813cf58631ef3b]}]" 2021-08-28 12:30:36 [!]  1 error(s) occurred and cluster hasn't been created properly, you may wish to check CloudFormation console 2021-08-28 12:30:36 [ℹ]  to cleanup resources, run 'eksctl delete cluster --region=ap-northeast-2 --name=first-eks' 2021-08-28 12:30:36 [✖]  waiting for CloudFormation stack "eksctl-first-eks-nodegroup-first-eks-nodegroup": ResourceNotReady: failed waiting for successful resource state Error: failed to create cluster "first-eks"
```bash
으아니.....서브넷에서 Public IP를 자동으로 붙이도록 해야한다니ㅠㅠ AWS양반 이게 무슨말이요....

![](/images/2021/08/image-11.png)

나는 기본으로 끄도록 설정한다. 켜주고..

또 보니까 eks 를 생성명령어 치고 에러가 발생하면

```bash
eksctl delete cluster --region=ap-northeast-2 --name=first-eks 2021-08-28 12:35:42 [ℹ]  eksctl version 0.63.0 2021-08-28 12:35:42 [ℹ]  using region ap-northeast-2 2021-08-28 12:35:42 [ℹ]  deleting EKS cluster "first-eks" 2021-08-28 12:35:42 [ℹ]  deleted 0 Fargate profile(s) 2021-08-28 12:35:42 [✔]  kubeconfig has been updated 2021-08-28 12:35:42 [ℹ]  cleaning up AWS load balancers created by Kubernetes objects of Kind Service or Ingress 2021-08-28 12:35:43 [!]  retryable error (Throttling: Rate exceeded
        status code: 400, request id: 3c52ae23-c941-435c-82ef-4df78b0f706e) from cloudformation/DescribeStacks - will retry after delay of 5.632676043s 2021-08-28 12:35:50 [ℹ]  3 sequential tasks: { delete nodegroup "first-eks-nodegroup", 2 sequential sub-tasks: { 2 sequential sub-tasks: { delete IAM role for serviceaccount "kube-system/aws-node", delete serviceaccount "kube-system/aws-node" }, delete IAM OIDC provider }, delete cluster control plane "first-eks" [async] } 2021-08-28 12:35:50 [ℹ]  will delete stack "eksctl-first-eks-nodegroup-first-eks-nodegroup" 2021-08-28 12:35:50 [ℹ]  waiting for stack "eksctl-first-eks-nodegroup-first-eks-nodegroup" to get deleted 2021-08-28 12:35:50 [ℹ]  waiting for CloudFormation stack "eksctl-first-eks-nodegroup-first-eks-nodegroup" 2021-08-28 12:36:06 [ℹ]  waiting for CloudFormation stack "eksctl-first-eks-nodegroup-first-eks-nodegroup" 2021-08-28 12:36:06 [ℹ]  will delete stack "eksctl-first-eks-addon-iamserviceaccount-kube-system-aws-node" 2021-08-28 12:36:06 [ℹ]  waiting for stack "eksctl-first-eks-addon-iamserviceaccount-kube-system-aws-node" to get deleted 2021-08-28 12:36:06 [ℹ]  waiting for CloudFormation stack "eksctl-first-eks-addon-iamserviceaccount-kube-system-aws-node" 2021-08-28 12:36:24 [ℹ]  waiting for CloudFormation stack "eksctl-first-eks-addon-iamserviceaccount-kube-system-aws-node" 2021-08-28 12:36:24 [ℹ]  deleted serviceaccount "kube-system/aws-node" 2021-08-28 12:36:25 [ℹ]  will delete stack "eksctl-first-eks-cluster" 2021-08-28 12:36:25 [✔]  all cluster resources were deleted
```bash
자동으로 삭제하진 않고 내가 수동으로 삭제해야한다. 삭제를 하면 다시 설치!! 설치가 완료됬다.

이제 pgsql rds와 secretmanager 셋팅을 할거다.

![](/images/2021/08/image-12.png)

t2.micro로 생성하고

![](/images/2021/08/image-13.png)

Secrets Manager 도 생성했다.

rds endpoint 도 변수로 추가하고 보안그룹 열어주고 pgsql 유저 패스워드를 지정한다

```bash
RDSEP=eksworkdb.cnnbttekipxl.ap-northeast-2.rds.amazonaws.com createuser -d -U eksdbadmin -P -h $RDSEP mywork Enter password for new role: Enter it again: Password: #디비 생성 PGPASSWORD=$AppDbPw createdb -U mywork -h $RDSEP -E UTF8 myworkdb
```bash
이후로는 책의 진행을 따라서 backend-app 까지 배포했다.

```
ubectl logs -l app=backend-app -f --max-log-requests 8 2021-08-28 14:00:12.504 [http-nio-8080-exec-7] INFO  k.s.presentation.api.HealthApi - Health GET API called. 2021-08-28 14:00:12.507 [http-nio-8080-exec-8] INFO  k.s.presentation.api.HealthApi - Health GET API called. 2021-08-28 14:00:42.503 [http-nio-8080-exec-3] INFO  k.s.presentation.api.HealthApi - Health GET API called. 2021-08-28 14:00:42.505 [http-nio-8080-exec-5] INFO  k.s.presentation.api.HealthApi - Health GET API called. 2021-08-28 14:01:12.503 [http-nio-8080-exec-5] INFO  k.s.presentation.api.HealthApi - Health GET API called. 2021-08-28 14:01:12.503 [http-nio-8080-exec-4] INFO  k.s.presentation.api.HealthApi - Health GET API called. 2021-08-28 14:01:42.503 [http-nio-8080-exec-1] INFO  k.s.presentation.api.HealthApi - Health GET API called. 2021-08-28 14:01:42.505 [http-nio-8080-exec-2] INFO  k.s.presentation.api.HealthApi - Health GET API called. 2021-08-28 14:02:12.508 [http-nio-8080-exec-8] INFO  k.s.presentation.api.HealthApi - Health GET API called. 2021-08-28 14:02:12.513 [http-nio-8080-exec-9] INFO  k.s.presentation.api.HealthApi - Health GET API called.
```bash
정상적으로 들어오는거 확인하고~ 프론트를 빌드했다.

이후에 빌드한 것을 s3 로 정적호스팅 설정하고,

![](/images/2021/08/image-14-1024x254.png)

OAI 설정 및 연결해주고..대부분 기본설정이다.

![](/images/2021/08/image-15-1024x591.png)

이전에 만든 CF를 썼는데 원본이름이 이상하다...

![](/images/2021/08/image-16.png)

일단 정적페이지 까지 띄웠다.

생각보다 긴 실습이었다.

```bash
eksctl delete cluster --region=ap-northeast-2 --name=first-eks 2021-08-28 14:28:19 [ℹ]  eksctl version 0.63.0 2021-08-28 14:28:19 [ℹ]  using region ap-northeast-2 2021-08-28 14:28:19 [ℹ]  deleting EKS cluster "first-eks" 2021-08-28 14:28:20 [ℹ]  deleted 0 Fargate profile(s) 2021-08-28 14:28:20 [✔]  kubeconfig has been updated 2021-08-28 14:28:20 [ℹ]  cleaning up AWS load balancers created by Kubernetes objects of Kind Service or Ingress 2021-08-28 14:29:57 [!]  retryable error (Throttling: Rate exceeded
        status code: 400, request id: 79716aac-f9df-40d9-871c-e473113fe5c1) from cloudformation/DescribeStacks - will retry after delay of 9.550890926s 2021-08-28 14:30:06 [ℹ]  3 sequential tasks: { delete nodegroup "first-eks-nodegroup", 2 sequential sub-tasks: { 2 sequential sub-tasks: { delete IAM role for serviceaccount "kube-system/aws-node", delete serviceaccount "kube-system/aws-node" }, delete IAM OIDC provider }, delete cluster control plane "first-eks" [async] } 2021-08-28 14:30:06 [ℹ]  will delete stack "eksctl-first-eks-nodegroup-first-eks-nodegroup" 2021-08-28 14:30:06 [ℹ]  waiting for stack "eksctl-first-eks-nodegroup-first-eks-nodegroup" to get deleted 2021-08-28 14:30:06 [ℹ]  waiting for CloudFormation stack "eksctl-first-eks-nodegroup-first-eks-nodegroup" 2021-08-28 14:30:23 [ℹ]  waiting for CloudFormation stack "eksctl-first-eks-nodegroup-first-eks-nodegroup" 2021-08-28 14:30:40 [ℹ]  waiting for CloudFormation stack "eksctl-first-eks-nodegroup-first-eks-nodegroup" 2021-08-28 14:30:59 [ℹ]  waiting for CloudFormation stack "eksctl-first-eks-nodegroup-first-eks-nodegroup" 2021-08-28 14:31:16 [ℹ]  waiting for CloudFormation stack "eksctl-first-eks-nodegroup-first-eks-nodegroup" 2021-08-28 14:31:36 [ℹ]  waiting for CloudFormation stack "eksctl-first-eks-nodegroup-first-eks-nodegroup" 2021-08-28 14:31:55 [ℹ]  waiting for CloudFormation stack "eksctl-first-eks-nodegroup-first-eks-nodegroup" 2021-08-28 14:32:14 [ℹ]  waiting for CloudFormation stack "eksctl-first-eks-nodegroup-first-eks-nodegroup" 2021-08-28 14:32:31 [ℹ]  waiting for CloudFormation stack "eksctl-first-eks-nodegroup-first-eks-nodegroup" 2021-08-28 14:32:49 [ℹ]  waiting for CloudFormation stack "eksctl-first-eks-nodegroup-first-eks-nodegroup" 2021-08-28 14:33:05 [ℹ]  waiting for CloudFormation stack "eksctl-first-eks-nodegroup-first-eks-nodegroup" 2021-08-28 14:33:21 [ℹ]  waiting for CloudFormation stack "eksctl-first-eks-nodegroup-first-eks-nodegroup" 2021-08-28 14:33:40 [ℹ]  waiting for CloudFormation stack "eksctl-first-eks-nodegroup-first-eks-nodegroup" 2021-08-28 14:33:56 [ℹ]  waiting for CloudFormation stack "eksctl-first-eks-nodegroup-first-eks-nodegroup" 2021-08-28 14:33:56 [ℹ]  will delete stack "eksctl-first-eks-addon-iamserviceaccount-kube-system-aws-node" 2021-08-28 14:33:56 [ℹ]  waiting for stack "eksctl-first-eks-addon-iamserviceaccount-kube-system-aws-node" to get deleted 2021-08-28 14:33:56 [ℹ]  waiting for CloudFormation stack "eksctl-first-eks-addon-iamserviceaccount-kube-system-aws-node" 2021-08-28 14:34:13 [ℹ]  waiting for CloudFormation stack "eksctl-first-eks-addon-iamserviceaccount-kube-system-aws-node" 2021-08-28 14:34:13 [ℹ]  deleted serviceaccount "kube-system/aws-node" 2021-08-28 14:34:14 [ℹ]  will delete stack "eksctl-first-eks-cluster" 2021-08-28 14:34:14 [✔]  all cluster resources were deleted
```bash
클러스터를 삭제하며 포스팅을 마친다.
