---
title: "AWS-instance-Attach to Auto Scaling Group"
date: 2020-05-20T11:59:08+09:00
draft: false
categories: ["AWS"]
tags: ["aws", "asg", "autoscaling"]
slug: "aws-instance-attach-to-auto-scaling-group"
aliases:
  - /aws-instance-attach-to-auto-scaling-group/
  - /aws-instance-attach-to-auto-scaling-group/
---

\n

나는 몹쓸 고정관념이 있었다.

\n\n\n\n

auto scaling group 에서 인스턴스를 분리 하게되면 재연결할수 없다고 생각했다.

\n\n\n\n

아니었다..그저 연결하는 메뉴가 Auto Scaling Group에 존재하지 않았을 뿐이다.

\n\n\n\n\n\n\n\n

하..멍청멍청.

\n\n\n\n
![](/images/2020/05/image-25.png)
\n\n\n\n

ASG에서 인스턴스를 분리한다.

\n\n\n\n
![](/images/2020/05/image-26.png)
\n\n\n\n

하나의 인스턴스만 남는다. 내 ASG는

\n\n\n\n
![](/images/2020/05/image-27.png)
\n\n\n\n

이렇게 설정되어있고 축소정책이 없는 상태라 분리하여도 문제가 없다.

\n\n\n\n

정상적으로 분리된게 확인되면 인스턴스 탭으로 이동하자.

\n\n\n\n
![](/images/2020/05/image-28.png)
\n\n\n\n

분리된인스턴스에서 인스턴스셋팅을 보면 Attach 메뉴가 있다.

\n\n\n\n
![](/images/2020/05/image-29.png)
\n\n\n\n

이런식으로 ASG에 인스턴스를 넣어줄수 있다.

\n\n\n\n
![](/images/2020/05/image-30.png)
\n\n\n\n

정상적으로 추가된것까지 확인된다.

\n\n\n\n
![](/images/2020/05/image-31.png)
\n\n\n\n

-\_-;보안그룹 넣는거부터.. ASG까지..또 내가 모르는게 많았다..

\n\n\n\n\n\n\n\n

ASG 액션에서 연결버튼 하나만 만들어줘도... 이런고민 안했을껀데..

\n\n\n\n\n\n\n\n

음 또 나만 몰랐던 AWS의 기능... 다신 잊지 않기 위해서 포스팅한다.

\n