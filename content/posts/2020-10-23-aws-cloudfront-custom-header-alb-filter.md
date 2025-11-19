---
title: "AWS-CloudFront-custom-header-ALB-filter"
date: 2020-10-23T15:30:49+09:00
draft: false
categories: ["AWS"]
tags: ["cloudfront", "cf", "alb", "custom header"]
slug: "aws-cloudfront-custom-header-alb-filter"
aliases:
  - /aws-cloudfront-custom-header-alb-filter/
  - /aws-cloudfront-custom-header-alb-filter/
---

\n

<https://www.notion.so/CloudFront-ALB-f0086dec48b64f0883e0c6de5fd9da4c>

\n\n\n\n
![](/images/2020/10/image-7.png)
\n\n\n\n

Noah.Seo 님의 이야기를 받아서 다른방법을 테스트하게 되었다.

\n\n\n\n
![](/images/2020/10/image-8.png)
\n\n\n\n

4번째 방법이 번득 떠오른탓.

\n\n\n\n

그럼 내가 생각하는 부분은 이렇다.

\n\n\n\n

CloudFront -> ALB

\n\n\n\n

끝...3번 방법은 WAF에서 X-Origin-Verify Custom Header 를 필터링 한다. ALB에서도 비슷한 기능이 있는바. 나는 이전부터 ALB에서 내 블로그 도메인이 아닌 ALB 도메인이나 IP로 접근하는것을 제한한 바가 있다.

\n\n\n\n
![](/images/2020/10/image-9.png)
\n\n\n\n

이 규칙이 바로 그것이다. Host 조건에 따라 Host가 다르면 아무 대상이 없는 blackhole 로 전달하게 된다. 그렇다. Custom Header를 ALB에서 필터링 할거다.

\n\n\n\n\n\n\n\n

CloudFront 에서 Origin 을 수정한다.

\n\n\n\n

단점은 ALB의 부하가 올라간다는것. 규칙에 의해 LCU 사용량이 증가할수 있다는 점이다.

\n\n\n\n

그럼 셋팅해 보자.

\n\n\n\n
![](/images/2020/10/image-10.png)
\n\n\n\n

X-Origin-Verify 헤더 네임을 추가하고 Value 로 test를 추가한다.

\n\n\n\n
![](/images/2020/10/image-12.png)
\n\n\n\n

그리고 ALB의 규칙을 추가한다. 도메인 기반하여 http 헤더가 일치하면 라우팅. 그렇지않으면 두번째 규칙에 의해 blackhole로 전달한다. 지금 현재 정상적으로 헤더가 일치하여 사이트가 뜨는 상태다.

\n\n\n\n

<https://www.linuxer.name/>

\n\n\n\n

로 접근해보면 503에러가 발생하는것을 볼수있다.

\n\n\n\n

재미있는 테스트 거리를 주신 Noah.Seo 님께 감사를 드린다.

\n