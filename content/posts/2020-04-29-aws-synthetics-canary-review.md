---
title: "AWS-CloudWatch-Synthetics-Canary-review"
date: 2020-04-29T10:01:16+09:00
draft: false
categories: ["AWS"]
tags: ["aws", "watch", "Synthetics", "Canary"]
slug: "aws-synthetics-canary-review"
aliases:
  - /aws-synthetics-canary-review/
  - /aws-synthetics-canary-review/
---

\n

드디어!!드디어!!드디어!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

\n\n\n\n

AWS에도 웹모니터링 기능이 생겼다.

\n\n\n\n

진짜 너무 기다려왔던 기능이다.

\n\n\n\n\n\n\n\n

사용법도 간단하고 지표도 바로나오고..이거 완전 물건이다.

\n\n\n\n

바로 셋팅해봤다.

\n\n\n\n
![](/images/2020/04/image-29.png)
\n\n\n\n

블루 프린트를 사용해서 테스트를 했다.

\n\n\n\n
![](/images/2020/04/image-30.png)
\n\n\n\n

4가지의 블루프린트를 제공하고 스크립트를 수정할수도 있으나 귀찮다.

\n\n\n\n
![](/images/2020/04/image-31.png)
\n\n\n\n

일정은 뭐....알아서 나는 5분으로 만들고 나중에 1분으로 수정했다. 일단 나머지 파라메터를 다 기본으로 설정하고 진행했다.

\n\n\n\n

생성하면 진짜 간단하게 보여준다.

\n\n\n\n
![](/images/2020/04/image-33.png)
\n\n\n\n
![](/images/2020/04/image-34.png)
\n\n\n\n
![](/images/2020/04/image-35.png)
\n\n\n\n

핵심은 이거다. 그냥 사이트 모니터링을 해주고

\n\n\n\n
![](/images/2020/04/image-36.png)
\n\n\n\n

지연된 URL을 체크해준다.

\n\n\n\n

나같은경우엔 사이트 모니터링을

\n\n\n\n
![](/images/2020/04/image-37.png)
\n\n\n\n

1분마다 하고 5분 평균 임계값을 1로 설정하여 상당히 예민한 모니터링 설정을 하였다. 사이트 URL 체크가 1번만 실패해도 SNS로 경보가 동작한다.

\n\n\n\n
![](/images/2020/04/image-38.png)
\n\n\n\n

t2.micro 의 경우에는 인스턴스의 CPU가 좀 오르는게 보였으나.. 뭐 이정도는 감당할 만하다. 모니터링으로 인해 부하가 발생하는것이 불편하다면 특정 모니터링 URL만 만들어서 부하를 줄여서 모니터링 하는것이 방법일것이다.

\n\n\n\n

지금 까지는 target group에 의존한 모니터링을 사용하였는데 이젠 서비스에 대한 모니터링이 가능한 순간이 와서 너무 즐겁다.

\n\n\n\n

일단 블로그에 충분한 테스트 이후에 api 와 프로덕션 환경에서 사용해 봐야겠다.

\n\n\n\n\n\n\n\n

포스팅을 작성하고 나중에 비용계산을 진행해 보았다.

\n\n\n\n

단순계산으로

\n\n\n\n

1분마다 모니터링 하면 60\*24\*31=44604\*0.0012 USD=53.568=USD

\n\n\n\n

5분마다 면....11USD 정도 이다-\_-;;;

\n\n\n\n\n\n\n\n

음....모니터링 치고 비싼데...????????????????ㅠㅠ

\n\n\n\n

적용하기 전에 비용꼭 계산해보고 사용하자..

\n\n\n\n\n\n\n\n

읽어줏셔서 감사하다!

\n\n\n\n\n\n\n\n\n