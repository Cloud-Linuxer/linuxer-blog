---
title: "ALB sticky session 에 대한 고찰."
date: 2019-10-21T22:47:37+09:00
draft: false
categories: ["AWS"]
tags: ["awsalb", "stickysession", "sticky", "alb"]
slug: "alb-sticky-session-에-대한-고찰"
aliases:
  - /alb-sticky-session-에-대한-고찰/
  - /alb-sticky-session-%ec%97%90-%eb%8c%80%ed%95%9c-%ea%b3%a0%ec%b0%b0/
---


aws 에선 고가용성을 위한 로드벨런서를 지원한다.

로드벨런서의 이야기다.

오늘 3티어 구성에서 세션이 널뛰는 증상이 있었다. 그 이야기를 하기전에 먼저 설명부터 하겠다.

ELB 라는 이름으로 ALB/NLB/CLB로 불린다.

Application Load Balancer, Network Load Balancer, Classic Load Balancer 이다.

오늘 이야기할 로드벨런서는 ALB인데 그중에도 sticky session 이다.

한글 콘솔에서는 고정 세션이라 불린다. 고정세션은 라운드 로빈으로 작동하는 로드벨런서에 세션을 고정해서 사용자의 경험을 지속할수 있도록 도와주는 역할을 한다.

먼저 옵션을 설정하는 방법부터 보자

로드벨런서>대상그룹> 속성편집 을 누른다.

![](/images/2019/10/image-7.png)

그럼 아래와 같은 창이뜨고 활성화를 누르면 고정세션의 시간을 활성화 할수 있다.

![](/images/2019/10/image-8-1024x284.png)

활성화 한 화면은 다음과 같다.

![](/images/2019/10/image-9-1024x230.png)

sticky session 이 정상적으로 붙은지 확인하는 방법은 아래와 같다.

![](/images/2019/10/image-11-1024x324.png)

아직 sticky session 설정을 추가하지 않은상태다.

![](/images/2019/10/image-12-1024x393.png)

sticky session 세션은 cookie로 생성이된다.

Application Load Balancer는 로드 밸런서가 생성한 쿠키만 지원합니다. 쿠키의 이름은 AWSALB입니다. 이러한 쿠키의 콘텐츠는 교체 키를 사용하여 암호화됩니다. 로드 밸런서가 생성한 쿠키는 해독하거나 변경할 수 없습니다.

<https://docs.aws.amazon.com/ko_kr/elasticloadbalancing/latest/application/load-balancer-target-groups.html#sticky-sessions>

3tier로 구성하면 AWSALB 쿠키가 2개가 붙는다.

AWSALB fnCHt1XmAslF4YJP1DdrFja2gFlp58fwxawbSD63gMsYHbSY6ZvL47TP9JyNb1LAqNBb1mt3J0xTVTQrbyFV3KVQmFayhf0C+FIcsOoXDpadKRTlRxNiL2jaijXf N/A N/A N/A 131
JSESSIONID BA145F75466D30D122F5BF83873E0C13 N/A N/A N/A 45
_ga GA1.3.549999545.1568632026 N/A N/A N/A 32
Response Cookies 357
AWSALB 7/4O7AyBPsXTcT9Y3AEE+B3ueRztLwkdTz9TwF/bJ191ItEAMN1HoOk1xsVtWsOjbmuZb68s5gs+6xM2oowR3JgexIIVYIUPWwFkkOWliy3FkwsmeMzQmXsKAkV0 / 2019-10-28T10:50:30.000Z 179
AWSALB UUu3Vbr3MNNBSaaby5Z1dduf11BTf0148wbnE+20aF9Ak+QQWv0ZFGlsBsUZTOWRB9k99mVsAzr0PMgLAiciFD5mJW2FLmNn3ojwbh/EEQFdL5qe6NZCkAFKuLOz / 2019-10-28T10:50:30.000Z 178

alb-web-alb-was-rds 구성이면 쿠키가 좀붙는데 was 가 tomcat 라면

awsalb 쿠키 2개와 jsessoinid 라는 쿠키까지 붙는다.

여기서 awsalb 쿠키는 response 한 alb쿠키를 request 에 재활용한다.

awsalb 쿠키는 지속적으로 변한다. 하지만 sticky session 에의해서 jsessionid값은 연결된 was의 고유값을 지니며 jsessionid 가 변경되면 세션이 초기화 되서 재 매칭이 된다.

이걸 왜포스팅하냐면 sticky 가 정상적으로 붙는데 세션이 was1/2로 붙는 증상이 발생해서 확인하는 방법을 포스팅한거다..

아디오스!
