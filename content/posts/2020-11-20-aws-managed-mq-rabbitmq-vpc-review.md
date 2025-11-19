---
title: "AWS-managed-MQ-RabbitMQ-VPC-review"
date: 2020-11-20T18:03:47+09:00
draft: false
categories: ["AWS"]
tags: ["aws", "rebbitMQ", "mq"]
slug: "aws-managed-mq-rabbitmq-vpc-review"
aliases:
  - /aws-managed-mq-rabbitmq-vpc-review/
  - /aws-managed-mq-rabbitmq-vpc-review/
---

\n

관리형 RabbitMQ가 나왔다.

\n\n\n\n
![짤방백업봇 on Twitter: "놀라울 만큼, 그 누구도 관심을 주지 않았다.… "](https://pbs.twimg.com/media/DfK2m9TU0AMj\_S1.jpg)
\n\n\n\n

놀랄만큼 아무도 관심을 가지지 않았다. 안타깝....

\n\n\n\n

그래서 내가 관심을 주기로 했다.

\n\n\n\n

RabbitMQ VPC 설정을 확인해 보자!

\n\n\n\n
![](/images/2020/11/image-34.png)
\n\n\n\n

생성모드는 단일과 클러스터 두가지가 있다. 단일구성부터 보자

\n\n\n\n
![](/images/2020/11/image-36.png)
\n\n\n\n

퍼블릭엑세스는 VPC 내에 속하며 서브넷을 선택할수 있다.

\n\n\n\n
![](/images/2020/11/image-37.png)
\n\n\n\n

프라이빗 엑세스를 선택해야 보안그룹를 선택할수 있다. 이게 가장 큰 차이점.  
그리고 한번 퍼블릭으로 생성한 MQ는 영원히 퍼블릭이다. 프라이빗은 영원히 프라이빗..

\n\n\n\n

그리고 이 포스팅을 시작하게 된 가장 큰 계기..

\n\n\n\n
![](/images/2020/11/image-38.png)
\n\n\n\n

클러스터 모드에서 퍼블릭 엑세스를 사용한 RabbitMQ 는 VPC 외부에 만들어진다.

\n\n\n\n
![](/images/2020/11/image-39.png)
\n\n\n\n
![](/images/2020/11/image-40.png)
\n\n\n\n
![](/images/2020/11/image-41.png)
\n\n\n\n
![](/images/2020/11/image-42.png)
\n\n\n\n

그냥 VPC 컨트롤하는 설정이 없다.

\n\n\n\n
![](/images/2020/11/image-43.png)
\n\n\n\n

프라이빗으로 설정하면 VPC에 생성...

\n\n\n\n

같은 RabbitMQ임에도 VPC 내부 / 외부 / 보안그룹 유 /무 접근제어 방식이 다른것이 인상적이었다. RDS와 같이 VPC 내부에 만들어져서 편리하게 전환할 수 있는 방식이 아니기에 생성 초기부터 명확하게 아키텍처를 구상해야 하는 것이다.

\n\n\n\n

RabbitMQ의 VPC 설정은 변경이 불가능하다!!

\n\n\n\n

읽어주셔서 감사합니다!

\n\n\n\n\n