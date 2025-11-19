---
title: "AWS-IAM-Identity-Center"
date: 2022-08-13T21:26:23+09:00
draft: false
categories: ["AWS"]
slug: "aws-iam-identity-center"
aliases:
  - /aws-iam-identity-center/
  - /aws-iam-identity-center/
---


가시다 님과 함께하는 CASS 스터디를 시작했다.


첫시간은 OU / IAM과 함께하는 즐거운 시간.
MSP에서 OU는 열심히 익힌터라 좀 자신이 있었다. 그래서 나는 IAM Center를 써봤다.


검증할것은 이것이다. 지금까지는 각 계정에 역할을 생성하고, STS를 통해서 계정에 접근했다면 IAM Center에선 통합계정을 생성하여 OU에 연결된 루트계정들에 접근할수 있도록한다.


먼저 OU에 계정을 연결한다.


![](/images/2022/08/image.png)

3개의 계정이 연결된것을 확인할수있다.


linxuer 계정이 Root OU를 관리한다.


linuxer 계정에서 IAM Identity Center서비스 로 이동한다. 그리고 사용자를 생성한다.


![](/images/2022/08/image-1.png)

사용자를 생성할때 권한세트를 참조한다. 나는 AdministratorAccess 권한을 미리 생성해서 넣어줬다.


IAM Identity Center 에서는 이계정으로 OU의 하위 모든 계정을 관리한다 이과정에서 IAM Role Change가 필요하지 않다. 테스트하면서 정말 놀랐다.


계정을 생성하면 아래와 같은 메일주소가 온다.


![](/images/2022/08/image-3.png)

내 포탈이라는 페이지로 이동하면 계정의 패스워드와 MFA를 설정할수 있는 페이지로 이동한다. MFA 잊지말고 설정하자


이포탈의 역할은 딱하나다.


로그인-MFA-다른계정의 콘솔접근-억세스키생성
편리하지만 위험하다. 단순 1회발급되고 휘발성을 가지던 억세스키가 페이지 안에선 변경되지 않고 여러차례 확인이 가능하다


![](/images/2022/08/image-5.png)

보안에 특별히 유의가 필요하다!!!!!!!!


![](/images/2022/08/image-7.png)

이서비스는 다음과 같은 메뉴만 제공한다. 미리 OU에서 SCP로 Linuxer2 계정의 S3를 제한해 놨다. linuxer2 계정에서 S3로 이동해 볼거다.


![](/images/2022/08/image-4.png)

![](/images/2022/08/image-10-1024x174.png)

IAM Identity Center 계정도 정상적으로 제어된다. 그럼 Trail 에는 어떻게 표시될까?


![](/images/2022/08/image-11-1024x65.png)

signin.amazonaws.com 을통해 로그인한 계정을 추적할수 있다.


앞으로 OU를 사용하는 사용자는 IAM Identity Center를 이용해 다량의 작업을 편하게 할수 있음을 알았고 불편하게 역할 전환을 하게되는 경우가 없이 IAM Identity Center Console을 사용할수 있음 을 알수있었다.


새로운 보안의 공백이 될 수 있음을 염두에 두도록 하자.


읽어 주셔서 감사하다!
