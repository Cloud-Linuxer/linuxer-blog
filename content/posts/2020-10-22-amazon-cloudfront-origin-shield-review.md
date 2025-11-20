---
title: "Amazon CloudFront Origin Shield-Review"
date: 2020-10-22T14:51:37+09:00
draft: false
categories: ["AWS"]
tags: ["cloudfront", "cf", "Origin", "Shield", "Origin Shield"]
slug: "amazon-cloudfront-origin-shield-review"
aliases:
  - /amazon-cloudfront-origin-shield-review/
  - /amazon-cloudfront-origin-shield-review/
---


![](/images/2020/10/image-2.png)

Origin Shield 가 출시 되었다.

Origin 에 전달되는 리퀘스트의 횟수를 줄여 관리비용을 줄인다고 한다.

먼저 캐싱율을 보자.

![](/images/2020/10/image-3.png)

70%대다.

개판이다..이게 어떻게 변할까?

![](/images/2020/10/image-4.png)

**Origin Shield Region** 으로 서울리전을 선택했다.

설정자체는 어려울게 하나도 없고 일단....

기다려 봐야겠다.

그리고 하루정도 지난상태로 포스팅 쓰는것을 이어간다.

먼저 어제의 히트율

![](/images/2020/10/image-5.png)

21 ~ 22일의 히트율.

![](/images/2020/10/image-6-1024x633.png)

22 ~ 23일 오? 효과가 있다.

더 모니터링 이후 내용을 추가하겠다.

![](/images/2020/10/image-13.png)

오후에 추가한 내용 오...히트율이 엄청올라간다. 만세! 유효한 효과가 있음을 확인하였다.
