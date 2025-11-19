---
title: "aws-linuxer의 블로그 톺아보기"
date: 2020-02-04T00:11:19+09:00
draft: false
categories: ["AWS", "기타"]
tags: ["aws 구성도", "구성도", "diagram"]
slug: "aws-linuxer의-블로그-톺아보기"
aliases:
  - /aws-linuxer의-블로그-톺아보기/
  - /aws-linuxer%ec%9d%98-%eb%b8%94%eb%a1%9c%ea%b7%b8-%ed%86%ba%ec%95%84%eb%b3%b4%ea%b8%b0/
---

\n
![](/images/2020/02/리소스-2-1024x812.png)
\n\n\n\n

그 동안 블로그를 운영하면서 블로그에 이것저것 적용해 보느라 시간 가는줄 몰랐다.

\n\n\n\n

대략적인 블로그의 구성도를 그려보았고 구성도를 하나하나 풀어보는 시간을 가져보려한다.

\n\n\n\n

먼저 내블로그는 apm 으로 이루어진 상태였다. 프리티어로 도메인도 없는 상태였고 그냥 테스트 용도 였다.

\n\n\n\n

그 블로그를 먼저 rds 로 분리를 진행 했다.

\n\n\n\n
![](/images/2020/02/image-15.png)
\n\n\n\n

인스턴스한대에 apache + php + mariadb 였던 구성에서 mariadb 를 rds 로 옮겼다.  
그리고 php를 php-fpm 으로 교체 했다.

\n\n\n\n

이시기엔 그냥 구성만 진행하려던 시기라 뭔가 많이 붙이지 않았다. 이 다음 과정에서 로드벨런서를 붙였다.

\n\n\n\n
![](/images/2020/02/image-16-1024x529.png)
\n\n\n\n

ALB를 붙이고 나서 letsencrypt 로 인증서를 붙일가 구매를 할까 고민을 하였으나 결국 ACM을 사용하였다.

\n\n\n\n
![](/images/2020/02/image-17.png)
\n\n\n\n

ALB는 여러개의 인증서를 사용할수 있고 ACM 은 한개의 인증서당 여러개의 도메인을 넣을수있다. 나는 linuxer.name / \*.linuxer.name 루트도메인과 와일드카드로 이루어진 두개의 도메인을 acm으로 사용하고 있다.

\n\n\n\n

이다음 진행한 설정을 s3 upload 다.

\n\n\n\n

s3로 이미지를 업로드하고 cloudfront 로 응답한다. 블로그의 응답속도가 굉장히 올라갔다.

\n\n\n\n
![](/images/2020/02/image-19.png)
\n\n\n\n

cdn.linuxer.name 도메인은 acm 을이용하는데 버지니아 북부에 acm을 설정해야 한다.

\n\n\n\n
![](/images/2020/02/image-20-1024x159.png)
\n\n\n\n

업로드 설정을 마친 다음에는 HA를 구성해 보았다. 이과정에서 redis 나 세션을 공유하기 위한 고민을 하였는데 사실 로그인은 나만해서 의미가 없었다. 또한 upload 도 s3로 해서 그냥 정말로 인스턴스만 만들고 대상그룹에 추가만 하면 바로 multi zone 구성이 바로 되었다. 단순한 wp! 칭찬해

\n\n\n\n
![](/images/2020/02/image-21-1024x239.png)
\n\n\n\n

그다음엔 지금도 수시로 테스트위해서 켜고 끄는RDS의 multiaz 진짜 고가용성을 위해선 아니고 그냥....썼다.

\n\n\n\n
![](/images/2020/02/image-22.png)
\n\n\n\n

이부분은 두가지 이유떄문에 설정을 진행했는데, 먼저 중국의 해커가 너무 접근이 많았다. 또한 블로그에 매일 비아그라 광고가 봇도아니고 손으로 직접올리는 사림이 있었다. IP는 신기하게 매번 조금씩 달랐지만 댓글을 좀 지우다가 귀찮아서 결국 국가 차단을 계획했다.

\n\n\n\n

지오로케이션을 지용하여 중국과 스패머의 국가를 Null 로 라우팅 하였다.

\n\n\n\n
![](/images/2020/02/image-23.png)
\n\n\n\n

중국과 스패머의 국가 이외엔 cloudfront 로 접근된다.  
일반적인 캐싱이나 CDN이 아니라 dynamic cdn 방식이다. 조금이라도 ALB로 빨리 접근하기 위한 방법이나 ...효과는 잘...아마 한국이라 그럴거다.

\n\n\n\n
![](/images/2020/02/image-24.png)
\n\n\n\n

cf 는 버지니아 북부의 acm을 이용하여 도메인을 인증하고 인증된 도메인은 waf 연결된다. waf는 서울리전의 alb에 연결되어있다.

\n\n\n\n

유저는 그럼 route53을통해 cf에 연결되어 waf 를 통과하고 alb에 연결되어 web ec2에 연결되고 rds의 데이터를 읽어서 페이지를 볼수있는거다.

\n\n\n\n

생각보다 설명이 길었는데..아무튼 뭔가 많다.

\n\n\n\n

대략적인 블로그의 구성도를 그리고 역할을 설명하였다.

\n\n\n\n

내블로그지만 나름 재미있게 가꾼거 같다.

\n\n\n\n

즐거운 저녁되시라!

\n