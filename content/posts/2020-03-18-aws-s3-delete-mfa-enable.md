---
title: "aws-s3-delete-mfa-enable"
date: 2020-03-18T10:28:19+09:00
draft: false
categories: ["AWS"]
tags: ["s3", "s3 delete mfa", "mfa", "delete"]
slug: "aws-s3-delete-mfa-enable"
aliases:
  - /aws-s3-delete-mfa-enable/
  - /aws-s3-delete-mfa-enable/
---


오늘은 s3 delete 를 mfa 로 제한하는 방법에 대해서 포스팅 해보겠다.


aws 에서 s3 버킷에 대한 삭제 제한을 해야 할때가 있다.


이경우에 root access key를 생성하여야 한다.


![](/images/2020/03/image-24-1024x372.png)

iam 대시보드에서 mfa 와 루트 엑세스키를 생성할수 있다.


![](/images/2020/03/image-25-1024x204.png)

보안자격증명 관리로 이동해서 진행한다. 과정은 간단하고 쉬우니 URL을 참고하자.


<https://docs.aws.amazon.com/ko_kr/IAM/latest/UserGuide/id_credentials_mfa.html> - MFA 활성화


<https://docs.aws.amazon.com/ko_kr/general/latest/gr/managing-aws-access-keys.html> -access key 생성


생성한 키로 aws cli 를 사용가능하도록 설정한다


/root/.aws/credentials 다음 위치다.


access key를 넣고 mfa 를 확인해보자


root@ip-10-0-0-12 ~]# aws iam list-virtual-mfa-devices
An error occurred (AccessDenied) when calling the ListVirtualMFADevices operation: User: arn:aws:sts:: usernumber :assumed-role/AmazonEC2RoleForSSM/i-052ebb4fb1eade551 is not authorized to perform: iam:ListVirtualMFADevices on resource: arn:aws:iam:: usernumber :mfa/


루트권한이 아닐경우 위와같은 에러가 난다 administrator 계정일경우 ListVirtualMFADevices 정책이 부여되어있어 에러가 발생하지 않을것이다. 하지만 mfa는 사용할수 없을것이라 root key여야 한다.


명령어가 정상적으로 작동하면 아래와 같이 반환된다.


{
 "VirtualMFADevices": [
 {
 "SerialNumber": "arn:aws:iam:: usernumber :mfa/root-account-mfa-device",
 "EnableDate": "2019-10-28T01:06:07Z",
 "User": {
 "PasswordLastUsed": "2020-03-18T00:27:36Z",
 "CreateDate": "2019-07-29T13:23:03Z",
 "UserId": "1",
 "Arn": "arn:aws:iam:: usernumber :root"
 }
 }
 ]
 }


나는 root 계정에만 mfa 를 활성화 하였기에 루트 계정에서 사용하는 mfa 만 뜬것이다.


root@ip-10-0-0-12 ~]# aws s3api put-bucket-versioning --bucket linuxer-data --versioning-configuration Status=Enabled,MFADelete=Enabled --mfa "arn:aws:iam::usernumber:mfa/root-account-mfa-device <016432>"
An error occurred (InvalidRequest) when calling the PutBucketVersioning operation: DevPay and Mfa are mutually exclusive authorization methods.


linuxer-data 라는 버킷을 versioning 을 켜고 MFADelete 를 활성화 한다는 명령어인데 에러가 발생한것이다. 이때 root 계정이 아니라서 발생한 에러이다.


root@ip-10-0-0-12 ~]# aws s3api put-bucket-versioning --bucket linuxer-data --versioning-configuration Status=Enabled,MFADelete=Enabled --mfa "arn:aws:iam:: usernumber:mfa/root-account-mfa-device 926220"


정상적으로 root access key일 경우에는 그냥 명령어가 떨어진다.


root@ip-10-0-0-12 ~]# aws s3api get-bucket-versioning --bucket linuxer-data
 {
 "Status": "Enabled",
 "MFADelete": "Enabled"
 }


이후에 다음과 같이 aws s3api get-bucket-versioning --bucket linuxer-data 명령어로 정상적으로 설정이 됬는지 확인이 가능하다.
