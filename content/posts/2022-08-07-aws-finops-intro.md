---
title: "AWS FinOps - Intro"
date: 2022-08-07T15:16:12+09:00
draft: false
categories: ["AWS", "FinOps"]
tags: ["FinOps", "비용관리", "비용", "cost", "fin", "Finance"]
slug: "aws-finops-intro"
aliases:
  - /aws-finops-intro/
  - /aws-finops-intro/
---

\n

이번엔 FinOps에 대한 이야기를 할거다.

\n\n\n\n

먼저 본론으로 들어가기 전에 FinOps에 대한 정의부터 이야기할까 한다.

\n\n\n\n

우리가 흔히 알고있는 DevOps는 Development 과 operations 의 합성어 이다.  
FinOps는 이 DevOps 에 Finance를 더한것이다. ( Finance + Development + Operations )  
IT infra 상에서 발생하는 비용을 제어하고 투자하는 방식을 말하는것이다.

\n\n\n\n

'투자' 라고 말하면 의아 할수도 있는데 클라우드 상의 자원은 무한하지만 사용자에게 할당된 비용은 유한하다.  
그렇기에 제한된 비용내에서 적절한곳에 맞는 리소스를 투입하는것이 FinOps 에서 투자인것이다.

\n\n\n\n

FinOps의 목적은 절약이 아니다.  
FinOps는 제한적인 예산에서 낭비되는 비용을 줄여 리소스가 필요한곳에 투입하는것이 FinOps 목적인 것이다.  
절약에서 '만' 끝난다면 지속적으로 줄여야하는 비용의 압박에 씨달릴 것이다.

\n\n\n\n

또한 비용관리는 반드시 필요하나, 이 비용관리가 비즈니스의 편의성을 해치고, 확장성과 탄력성에 영향을 준다면 당신을 FinOps를 잘못이해 하고있는것이다.

\n\n\n\n

예를 들어 RI를 구매 후 워크로드가 변화에도 불구하고 RI때문에 유연한 리소스를 사용하지 못한다면 잘못된 방식의 비용관리를 하고 있는 것이다. RI 때문에 서버추가에 대한 고민이나 원하는 유형의 인스턴스를 사용하지 못한다는 것은 클라우드를 사용하는 방식도 아니며, 이런경우 차라리 On-Premises로 의 회귀가 더 저렴할것이며 사용패턴도 맞을것이다.

\n\n\n\n

차후 포스팅 할 내용에서는 먼저 가장 간단히 보고 절약할 부분부터 새로운 아키텍처가 필요한 부분까지 작성할 것이다.

\n\n\n\n

FinOps의 세계가 얼마나 짜릿하고 즐거운 분야인지 같이 느껴보면 좋겠다.

\n\n\n\n

함께 돈을 버는 엔지니어의 세계로 가보자.

\n\n\n\n\n