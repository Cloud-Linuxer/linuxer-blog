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

\n

aws 관리형키를 사용할 경우 sns 암호화를 하면 cloudwatch 에서 호출이 안된다....

\n\n\n\n

작업 arn:aws:sns:ap-northeast-2:userid:sns\_topic을(를) 실행하지 못했습니다. 수신 오류: 'null (Service: AWSKMS; Status Code: 400; Error Code: AccessDeniedException; Request ID: 60c4ef-f3bb-4c89-98c8-67317fc18a)'

\n\n\n\n

이런 에러가 발생한다. 이경우 CMK 를 이용해서 SNS 암호화를 해야한다.

\n\n\n\n

<https://aws.amazon.com/ko/premiumsupport/knowledge-center/cloudwatch-receive-sns-for-alarm-trigger/>

\n\n\n\n

다음 링크를 참조했다.

\n\n\n\n
![](/images/2020/03/image-26-1024x106.png)
\n\n\n\n

위와 같은 구성으로 생성하고 정책을 적용한다.

\n\n\n\n{\n "Version": "2012-10-17",\n "Id": "EMR-System-KeyPolicy",\n "Statement": [\n {\n "Sid": "Allow access for Root User",\n "Effect": "Allow",\n "Principal": {\n "AWS": "arn:aws:iam::userid:root"\n },\n "Action": "kms:\*",\n "Resource": "\*"\n },\n {\n "Sid": "Allow access for Key Administrator",\n "Effect": "Allow",\n "Principal": {\n "AWS": "arn:aws:iam::userid:root"\n },\n "Action": [\n "kms:Create\*",\n "kms:Describe\*",\n "kms:Enable\*",\n "kms:List\*",\n "kms:Put\*",\n "kms:Update\*",\n "kms:Revoke\*",\n "kms:Disable\*",\n "kms:Get\*",\n "kms:Delete\*",\n "kms:TagResource",\n "kms:UntagResource",\n "kms:ScheduleKeyDeletion",\n "kms:CancelKeyDeletion"\n ],\n "Resource": "\*"\n },\n {\n "Sid": "Allow access for Key User (SNS IAM User)",\n "Effect": "Allow",\n "Principal": {\n "AWS": "arn:aws:iam::userid:root"\n },\n "Action": [\n "kms:GenerateDataKey\*",\n "kms:Decrypt"\n ],\n "Resource": "\*"\n },\n {\n "Sid": "Allow access for Key User (SNS Service Principal)",\n "Effect": "Allow",\n "Principal": {\n "Service": [\n "sns.amazonaws.com",\n "cloudwatch.amazonaws.com"\n ]\n },\n "Action": [\n "kms:GenerateDataKey\*",\n "kms:Decrypt"\n ],\n "Resource": "\*"\n }\n ]\n}\n\n\n\n

userid 부분만 수정해주면 잘작동한다.

\n\n\n\n\n