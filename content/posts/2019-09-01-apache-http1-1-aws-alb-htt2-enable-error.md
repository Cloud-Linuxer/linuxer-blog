---
title: "apache http1.1 aws alb http2 enable error"
date: 2019-09-01T10:07:43+09:00
draft: false
categories: ["AWS", "Linux"]
tags: ["prefork http2", "apache http2", "amazonlinux", "http2", "alb disable http2"]
slug: "apache-http1-1-aws-alb-htt2-enable-error"
aliases:
  - /apache-http1-1-aws-alb-htt2-enable-error/
  - /apache-http1-1-aws-alb-htt2-enable-error/
---

\n

safari 계열의 브라우저에서 내 블로그가 정상적으로 열리지 않았다.  
\n여러번 시도해야 열렸고, 한번에 열리지 않았다.

\n\n\n\n

이원인을 찾기위해서 로그분석부터 부단한 노력을했으나, 한동안 해결할수 없었다.

\n\n\n\n

그런데 어제 오픈카톡방의 박주혁 님께서 safari에서 정상적으로 열리지 않는다는 스크린샷을 올려주셨다.

\n\n\n\n
![](/images/2019/09/KakaoTalk\_20190901\_002146864-1024x346.png)
\n\n\n\n

인증문제가 아닐까 생각했지만 인증문제는 아니었고 이문제를 해결하기 위해선 내 웹서버의 설정을 설명해야 한다.

\n\n\n\n

amazon linux에서는 httpd-2.4.39-1.amzn2.0.1.x86\_64이 기본으로 설치되는 apache 이다. 그리고 php는 여러가지 버전을 repo로 지원하고 있는데  
 amazon-linux-extras 명령어로 사용가능한 repo를 확인할수 있다.

\n\n\n\n

일단 이부분에서 내가 old한 엔지니어라는 사실을 알았다.  
나는 apache-php 연동은 반드시 module로 연동을 한다.  
 그런데 amazon linux는 amazon-linux-extras install php7.3 명령어를 사용하면 module로 설치하는 것이 아닌 php-fpm 방식으로 php가 설치된다.

\n\n\n\n

그렇기에 나는 몇가지 old한 설정을 추가하였다.

\n\n\n\n

apache 는 온프레미스에서 의례 사용하던 방식인 prefrok 방식으로 설정하였고, php는 fpm이 아닌 module로 셋팅하였다.

\n\n\n\n

여기서 문제가 발생한것이다.  
아래 URL에서 발췌한 내용이다.  
 HTTP/2 is supported in all multi-processing modules that come with httpd. However, if you use the `prefork` mpm, there will be severe restrictions.

\n\n\n\n

<https://httpd.apache.org/docs/trunk/howto/http2.html>

\n\n\n\n

http2 를 사용하려면 prefork를 사용하기 어렵다.  
\n그런데 필자는 prefork 를 사용하였기 때문에 정상적으로 호환이 되지 않은 것이다.

\n\n\n\n

aws alb(http2) - apache (prefork)강제로 http2사용

\n\n\n\n

aws의 ALB는 http2를 기본으로 enable하게 되어있기때문에 정상적인 커넥션이 불가능했던것이다.

\n\n\n\n

일단 급하게 ALB에서 http2를 껏다.

\n\n\n\n
![](/images/2019/09/image-1024x370.png)
\n\n\n\n

그리고 오늘 mpm을 event로 돌리고 http2를 강제로 사용하게 했던 설정을 빼고 php-fpm으로 웹사이트를 사용할수 있게 변경하였다.  
 이후엔 정상적으로 사이트가 동작했으며, 간헐적으로 열리지 않는 증상은 사라졌다.

\n\n\n\n

이글을 빌어 다시한번 박주혁님께 감사를 드린다.

\n\n\n\n

앓던 이가 빠진기분이다.

\n\n\n\n

유레카!

\n