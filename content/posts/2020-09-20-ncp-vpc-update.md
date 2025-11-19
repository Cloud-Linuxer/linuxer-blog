---
title: "NCP-VPC-Update"
date: 2020-09-20T12:48:38+09:00
draft: false
categories: ["NCP"]
tags: ["vpc", "ncp", "ncp vpc"]
slug: "ncp-vpc-update"
aliases:
  - /ncp-vpc-update/
  - /ncp-vpc-update/
---


![](/images/2020/09/image-17.png)

드디어 NCP 에도 VPC가 업데이트 되었습니다.


![](/images/2020/09/image-18.png)

VPC 모드로 전환하면 파란색으로 인터페이스가 전환됩니다.


금융존은 주황색


![](/images/2020/09/image-19.png)

TMI는 여기 까지고 VPC를 생성해 보겠습니다.


![](/images/2020/09/image-20-1024x541.png)

![](/images/2020/09/image-21-1024x628.png)

https://linuxer.name/2020/05/aws-vpc/


아직 none-rfc-1918은 지원하지 않습니다. 다른 벤더에서도 rfc1918을 쓰는것을 권장하지만, none-rfc-1918의 필요성이 가끔 있으므로 차차 업데이트 되지 않을까 생각됩니다.


![](/images/2020/09/image-22-1024x391.png)

VPC 이름에는 대문자를 사용할 수 없습니다.


![](/images/2020/09/image-23-1024x693.png)

생성할떄 public / privite 으로 지정해서 만들게 됩니다. 인스턴스를 생성할때 public 으로 생성하면 인스턴스 용도로만 사용할수있고, private 으로 생성하면 로드벨런서 용도와 일반용도를 나누어서 생성할수 있습니다.


AWS 에서 계층화 된 서브넷의 구성에서 자유도를 빼놓은 구성같습니다.


사용자가 선택할수 있는 pub/pri 구분은 서브넷을 생성할 때 만 결정할 수 있는 것 입니다.


![](/images/2020/09/image-24.png)

라우팅 테이블의 메뉴가 있긴 하나, 이 라우팅 테이블은 서브넷간 통신과 VPN 통신등을 컨트롤하는거고 public / privite 은 한번 설정하면 수정할 수 없습니다.


일단 VPC 와 Subnet을 생성했으니, 한번 classic 모드와 VPC 모드 전환시도를 간단하게 진행해 보겠습니다.


classic 모드에서 인스턴스를 생성하고, 이생성한 인스턴스를 이미지로 만든후 vpc에서 이미지로 인스턴스를 생성해보겠습니다.


![](/images/2020/09/image-26-1024x549.png)

생성된 서버이미지를 이제 VPC 모드에서 보겠습니다.


![](/images/2020/09/image-27-1024x491.png)

안보입니다.


여긴어디 나는누구........그럼 어쩌지...vpc mode 로 전환 어쩌지..


![짤봇!](https://storage.googleapis.com/jjalbot-jjals/2018/12/rJHnhT4GlV/20171220_5a3a18c3c9eac.jpg)

아직 전환할수 있는 지원은 안나온거 같고..서로 풀을 공유하지 않는것으로 보입니다.


이후 3월 4일 패치내용입니다.


![](/images/2021/03/image-1024x472.png)

서버이미지 공유와 Classic 에서 VPC로 이미지 복제기능이 런칭되었습니다.


아주 칭찬해!


옮길수있는 이미지리스트는 정해져있지만 아주 수월하게 이동이 가능합니다.


<https://manvscloud.com/?p=516>


manvscloud 님의 블로그를 링크하며 글을 마칩니다.
