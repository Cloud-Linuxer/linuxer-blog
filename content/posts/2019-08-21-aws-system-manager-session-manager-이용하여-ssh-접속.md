---
title: "aws system manager session manager 이용하여 ssh 접속"
date: 2019-08-21T21:59:07+09:00
draft: false
categories: ["AWS", "Linux"]
tags: ["aws ssm", "session manager", "aws", "system manager"]
slug: "aws-system-manager-session-manager-이용하여-ssh-접속"
aliases:
  - /aws-system-manager-session-manager-이용하여-ssh-접속/
  - /aws-system-manager-session-manager-%ec%9d%b4%ec%9a%a9%ed%95%98%ec%97%ac-ssh-%ec%a0%91%ec%86%8d/
---

\n

간단하게 설명하면 필요한것은 AmazonEC2RoleforSSM policy 로 만든 역할, s3 bucket, cloudwatch group 다.

\n\n\n\n

미리 로그 쌓을 버킷, 워치 그룹, ssm 역할 생성까지 마친후에 역할을 인스턴스에 부여해주자.

\n\n\n\n

session manager 같은경우엔 신기하게 aws -> ec2 로 연결하는것이 아니다.  
ec2 -> session manager로 접근하는거다.

\n\n\n\n

그리고 ec2에 ssm user 를 생성해 주자 계정명은 상관 없다.

\n\n\n\n

그다음에 기본설정을 넣어준다

\n\n\n\n
![](/images/2019/08/image-1-1024x915.png)
\n\n\n\n

적절히 잘넣어주자.

\n\n\n\n

그리고 세션을 시작하면 된다.

\n\n\n\n
![](/images/2019/08/Screenshot-2019-08-21-at-21.54.41-1024x360.jpg)
\n\n\n\n

그럼 잘된다

\n\n\n\n

장점은 인스턴스에 퍼블릭IP가 없는 상태에서도 사용이 가능하다.  
key pair 나 패스워드가 없는 상태에서도 로그인이 가능하다.

\n\n\n\n

단점은 쁘띠느낌이 없다는걸까...

\n