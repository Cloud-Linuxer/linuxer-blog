---
title: "AWS-auto-assign IP settings"
date: 2020-05-08T09:39:04+09:00
draft: false
categories: ["AWS"]
tags: ["aws", "public ip"]
slug: "aws-auto-assign-ip-settings"
aliases:
  - /aws-auto-assign-ip-settings/
  - /aws-auto-assign-ip-settings/
---


기본 VPC의 경우에는 EC2를 생성할때 자동으로 인스턴스에 Public IP가 자동으로 붙는다.

이퍼블릭 IP는 생성되면 뗄수도없고 인스턴스를 종료후 재생성 해야지만 된다.
 Private subnet 에서도 Public IP가 생성되는것이므로 보안상의 취약점을 초래한다.

따라서 인스턴스를 생성할때는

![](/images/2020/05/image-12.png)

이렇게 퍼블릭 IP가 비활성화로 생성해야하는데 매번 일일이 신경써서 하기엔 불편하다.

![](/images/2020/05/image-14.png)

VPC-서브넷 에서 자동 할당 IP 설정 수정 옵션을 해제해주면 된다.

![](/images/2020/05/image-15.png)

해제하고 저장후 인스턴스를 생성해보면 아래와 같이 확인된다.

![](/images/2020/05/image-13.png)

스샷에서 보이듯 서브넷의 기본설정을 수정하여 자동으로 비활성화 할수있다.

이미붙은 Public IP는 뗄수 없다.

명심하자. 모든 EC2는 Public IP 없이 생성해야한다.

읽어주셔서 감사하다!

좋은하루 되시라!
