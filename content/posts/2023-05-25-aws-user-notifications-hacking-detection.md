---
title: "AWS-User-Notifications-Hacking-Detection"
date: 2023-05-25T08:51:48+09:00
draft: false
categories: ["AWS"]
tags: ["ec2", "noti", "user-noti", "state"]
slug: "aws-user-notifications-hacking-detection"
aliases:
  - /aws-user-notifications-hacking-detection/
  - /aws-user-notifications-hacking-detection/
---


**아직 이걸 설정 안했다면 반드시 하길 바란다.**

우리는 AWS를 다루면 항상 해킹의 위험에 당면한다.
미리 막는다면 너무좋은 일이겠으나, 그렇지 못한경우가 많다.

해킹을 당한다 하여도 문제들을 간단하게 캐치할수 있는 방법이 있다.

보통 AWS계정이 해킹당하면 해커의 니즈는 컴퓨팅 리소스를 사용하여 채굴을 돌리려고 한다. 이 과정에서 EC2를 만들게 되고, EC2의 생성을 모니터링 할수 있는 방법이 있다면, 조기에 해킹을 진압할수 있을 것이다.

이번에 나온AWS User Notifications 서비스가 그 니즈에 완벽하게 부합하다.

![](/images/2023/05/image-6.png)

이미지 대로 생성하자, 활성화되지 않은 계정의 리전들은 서비스노티도 안되거나 서비스가 런칭되지 않아서 리전에서 제외해야한다. 초기 한국계정으로 선택되지 않은 리전이다.

케이프타운 / 홍콩 / 멜버른 / 자카르타 / 하이데라바드 / 뭄바이 / 밀라노 / 바레인 / 프랑크푸르트 / 바레인 / UAE / 취리히

```bash
[af-south-1, ap-east-1, ap-southeast-4, ap-southeast-3, ap-south-2, eu-south-1, eu-south-2, eu-central-2, me-south-1, me-central-1]
```bash
리전선택하고 이메일 넣고 생성해 주자

![](/images/2023/05/image-7.png)

태그기반으로 예외할 인스턴스의 정책이 있다면 좋겠는데 그런정책은 아직없다.
하지만 간단히 활성화된 모든리전의 EC2의 상태변경 노티를 받아볼수 있다는 장점은 어마어마하다.

개인계정이라면 반드시 활성화해서 사용하길 바란다!

좋은하루 되시라!
