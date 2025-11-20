---
title: "aws-sns-kms-cmk"
date: 2020-03-20T11:18:57+09:00
draft: false
categories: ["AWS"]
tags: ["cmk", "kms", "sns"]
slug: "aws-sns-kms-cmk"
aliases:
  - /aws-sns-kms-cmk/
  - /aws-sns-kms-cmk/
---


aws 관리형키를 사용할 경우 sns 암호화를 하면 cloudwatch 에서 호출이 안된다....

작업 arn:aws:sns:ap-northeast-2:userid:sns_topic을(를) 실행하지 못했습니다. 수신 오류: 'null (Service: AWSKMS; Status Code: 400; Error Code: AccessDeniedException; Request ID: 60c4ef-f3bb-4c89-98c8-67317fc18a)'

이런 에러가 발생한다. 이경우 CMK 를 이용해서 SNS 암호화를 해야한다.

<https://aws.amazon.com/ko/premiumsupport/knowledge-center/cloudwatch-receive-sns-for-alarm-trigger/>

다음 링크를 참조했다.

![](/images/2020/03/image-26-1024x106.png)

위와 같은 구성으로 생성하고 정책을 적용한다.

{ "Version": "2012-10-17", "Id": "EMR-System-KeyPolicy", "Statement": [ { "Sid": "Allow access for Root User", "Effect": "Allow", "Principal": { "AWS": "arn:aws:iam::userid:root" }, "Action": "kms:\*", "Resource": "\*" }, { "Sid": "Allow access for Key Administrator", "Effect": "Allow", "Principal": { "AWS": "arn:aws:iam::userid:root" }, "Action": [ "kms:Create\*", "kms:Describe\*", "kms:Enable\*", "kms:List\*", "kms:Put\*", "kms:Update\*", "kms:Revoke\*", "kms:Disable\*", "kms:Get\*", "kms:Delete\*", "kms:TagResource", "kms:UntagResource", "kms:ScheduleKeyDeletion", "kms:CancelKeyDeletion" ], "Resource": "\*" }, { "Sid": "Allow access for Key User (SNS IAM User)", "Effect": "Allow", "Principal": { "AWS": "arn:aws:iam::userid:root" }, "Action": [ "kms:GenerateDataKey\*", "kms:Decrypt" ], "Resource": "\*" }, { "Sid": "Allow access for Key User (SNS Service Principal)", "Effect": "Allow", "Principal": { "Service": [ "sns.amazonaws.com", "cloudwatch.amazonaws.com" ] }, "Action": [ "kms:GenerateDataKey\*", "kms:Decrypt" ], "Resource": "\*" } ] }

userid 부분만 수정해주면 잘작동한다.
