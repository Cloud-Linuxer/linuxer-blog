---
title: "aws-cloudfront-s3-lambda cross-account access"
date: 2020-01-18T13:52:42+09:00
draft: false
categories: ["AWS"]
tags: ["cross", "교차계정", "람다엣지"]
slug: "aws-cloudfront-s3-lambda-cross-account-access"
aliases:
  - /aws-cloudfront-s3-lambda-cross-account-access/
  - /aws-cloudfront-s3-lambda-cross-account-access/
---

\n

cloudfront - s3 를 이용하게되면 결국 OAI를 이용한 Bucket policy를 사용하게 된다.

\n\n\n\n

단일 계정에서 사용할 경우엔 cloudfront 에서 자동으로 생성까지 해주므로 어려울것이 전혀없다.

\n\n\n\n

그런데 이제 이게 파트너사를 통해서 cloudfront 전용계정을 사용하게 된다던거 multi account 로 프로젝트를 진행할경우 자동으로 생성이 되지 않는다. 이 경우에 어떤방식으로 s3 Bucket policy 를 설정해야 하는지 포스팅하려 한다.

\n\n\n\n

먼저 Bucket policy 를보자

\n\n\n\n

{  
\n"Version": "2012-10-17",  
\n"Id": "PolicyForCloudFrontPrivateContent",  
\n"Statement": [  
\n {  
\n "Sid": " Grant a CloudFront Origin Identity access to support private content",  
\n "Effect": "Allow",  
\n "Principal": {  
\n "AWS": [  
\n "arn:aws:iam::cloudfront:user/CloudFront Origin Access Identity E39X8K28W3EQ"  
\n ]  
\n },  
\n "Action": "s3:GetObject",  
\n "Resource": "arn:aws:s3:::\*"  
\n }  
\n]  
\n}

\n\n\n\n

일반적으로 계정에서 버킷정책을 설정하면 위와같은 형태로 적용을 한다.  
가끔 정상적으로 적용이되지않는경우엔

\n\n\n\n

{  
 "Version": "2012-10-17",  
 "Id": "PolicyForCloudFrontPrivateContent",  
 "Statement": [  
 {  
 "Sid": " Grant a CloudFront Origin Identity access to support private content",  
 "Effect": "Allow",  
 "Principal": {  
 "AWS": [  
 "arn:aws:iam::cloudfront:user/CloudFront Origin Access Identity 49821f785cce6ee4f575de3f01c503dade8a7b15003aa337faa471d830d07493cbb195eec14f0d86d4a914622e1e42"  
 ]  
 },  
 "Action": "s3:GetObject",  
 "Resource": "arn:aws:s3:::\*"  
 }  
 ]  
 }

\n\n\n\n

이런식으로 caninucal user id 를 이용하여 정책을 설정하면 자동으로 OAI ID로 정책이 적용되게 된다.

\n\n\n\n

여기까진 아주 쉬웠다. 그런데

\n\n\n\n
![](/images/2020/01/image-55.png)
\n\n\n\n

람다 엣지를 이용한 리사이즈를 하는 프로세스에서 단일계정이 아니라 교차계정을 구성하게 되면 lambda가 A 계정에서 B 계정으로 접근하게 해줘야한다. 이부분에서 조금 헤멧는데 결국엔 굉장히 간단한 부분이었다.

\n\n\n\n

s3 Bucket policy 에서 계정의 role을 허용해주면 끝..

\n\n\n\n

{  
\n"Version": "2012-10-17",  
\n"Id": "PolicyForCloudFrontPrivateContent",  
\n"Statement": [  
\n {  
\n "Sid": " Grant a CloudFront Origin Identity access to support private content",  
\n "Effect": "Allow",  
\n "Principal": {  
\n "AWS": [  
\n "arn:aws:iam::cloudfront:user/CloudFront Origin Access Identity E39X8K58WRN3EQ",  
\n "arn:aws:iam::328341115633:role/lambda-resize-cloudfront"  
\n ]  
\n },  
\n "Action": "s3:GetObject",  
\n "Resource": "arn:aws:s3:::linuxer-resize/\*"  
\n }  
\n]  
\n}

\n\n\n\n

arn:aws:iam::328341115633:role/lambda-resize-cloudfront

\n\n\n\n

json 문법에 또 약해서 좀 해멧는데 금새 해결할수 있었다..

\n\n\n\n\n