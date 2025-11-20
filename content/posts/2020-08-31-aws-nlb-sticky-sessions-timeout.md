---
title: "AWS-NLB-Sticky-sessions-timeout"
date: 2020-08-31T14:50:47+09:00
draft: false
categories: ["AWS"]
tags: ["sticky", "nlb", "stickiness"]
slug: "aws-nlb-sticky-sessions-timeout"
aliases:
  - /aws-nlb-sticky-sessions-timeout/
  - /aws-nlb-sticky-sessions-timeout/
---


ALB에 대한 고찰이후 ELB관련 주제의 포스팅을 적는건 오랜만이다.

NLB의 Sticky 에 대해 한번 적어보려 한다.

![](/images/2020/08/image-8.png)

Target group의 속성 이야기다.

NLB sticky는 추가된지 6개월정도 지났지만 아직도 일반적으로 아는 기능은 아니다.
너무 오랜기간 없었던 터라 없다고 아는 사람이 더 많은..ㅋㅋㅋ 그런 기능이다.

<https://docs.aws.amazon.com/ko_kr/elasticloadbalancing/latest/network/load-balancer-target-groups.html>

먼저 Docs 를 링크하고..

NLB의 Routing algorithm 은 ip_hash 방식으로 동작 한다.

<https://docs.aws.amazon.com/ko_kr/elasticloadbalancing/latest/userguide/how-elastic-load-balancing-works.html>

The protocol
The source IP address and source port
The destination IP address and destination port
The TCP sequence number

6개의 조건이 일치하면 같은 target으로 연결해주나, 하나의 조건이라도 달라지면 다른 target으로 연결해주는 것이다. 이 tuple 들이이 일치하지 않더라도 같은 target으로 연결하게 하는 방법이 있다. 그것이 바로 sticky session 인것이다.

stictky session 에서 라우팅 조건은 souce ip 뿐이다. 1 tuple인것이다. 하지만 그렇다고 해서 영원히 같은 인스턴스로 연결해주는것은 아니다. 여기엔 시간 제한이 붙어있다.

-추가 - 수정합니다.
docs에는 souce ip 1tuple로 동작한다 적혀있지만 NLB-multi-AZ(HA)구성을 할경우엔 A RR-EIP가 두개가 붙으므로 예상과는 다르게 동작할것입니다. 또한 1tuple로 동작하는 부분또한 client ip + nlb node ip 로 구성되므로 2tuple 로 동작합니다.

예상과 같은 정상적인 결과를 얻기위해선 Weighted, failover 방식으로 route53을 설정해서 단일존으로 라우팅 해야 동일한 결과를 얻을 수 있습니다.
-도움주신 무무님 감사합니다.

docs 대로라면 1tuple이라 생각했는데 요소는 1tuple이 아니라

Connection idle timeout 이다

NLB의 Connection idle timeout 은 TCP 350 초 UDP 120초다.

- UDP는 태우님이 물어보셔서 추가로 알아봤다.

<https://docs.aws.amazon.com/elasticloadbalancing/latest/network/network-load-balancers.html#connection-idle-timeout>

Elastic Load Balancing sets the idle timeout value for TCP flows to 350 seconds. You cannot modify this value. Clients or targets can use TCP keepalive packets to reset the idle timeout.

Connection idle timeoutElastic Load Balancing sets the idle timeout value for UDP flows to 120 seconds.

그래서 동작은 이렇다.

sticky session 을 켜고 연결이 지속되는 동안은 무조건 같은 target으로 연결되고 마지막 연결부터 350초가 지나고 연결하면 대상/클라이언트 모두 TCP RST 응답을 받아서 sticky session 의 연결이 해제되고 다른 target과 연결되게 되고 다시 sticky로 동작하는거다.

최근에 질문을 받아서 다시한번 정리해봤다.

읽어주셔서 감사하다!
