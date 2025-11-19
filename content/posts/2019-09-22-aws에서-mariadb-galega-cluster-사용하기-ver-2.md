---
title: "aws에서 MariaDB galega Cluster 사용하기 ver.2"
date: 2019-09-22T12:19:21+09:00
draft: false
categories: ["AWS", "Linux"]
tags: ["aws rds", "galera", "mariadb cluster", "db cluster", "multi-az"]
slug: "aws에서-mariadb-galega-cluster-사용하기-ver-2"
aliases:
  - /aws에서-mariadb-galega-cluster-사용하기-ver-2/
  - /aws%ec%97%90%ec%84%9c-mariadb-galega-cluster-%ec%82%ac%ec%9a%a9%ed%95%98%ea%b8%b0-ver-2/
---

\n

지난 포스팅에 이어서 맺음하는 포스팅이다.  
계획은 일주일 이었으나 이주 가까이 galera를 사용하였다.

\n\n\n\n

이주동안 사용량이나 봇들의 동태 이것저것 모니터링을 했지만..  
부하가 없었다.. 그래서 부하테스트는 직접하기로 마음을 먹었다!

\n\n\n\n

먼저 비용부터 보자.

\n\n\n\n
![](/images/2019/09/Screenshot-2019-09-22-at-10.26.19-1024x430.jpg)
\n\n\n\n

Cost Explorer 에서 일별 서비스별로 본 그래프이다.  
여기서 중요한건 EC2 비용인데 0.47$ 정도다. t3.nano 3대 하루 비용인데 1달정도 하면 14.1$ 정도 나온다. 정말 얼마 안나온다. 깜짝놀랄정도.

\n\n\n\n

그렇다면 성능을 확인해 볼까?

\n\n\n\n

구성을 나열하자면 NLB-mariaDB-cluster(t3.nano 3ea) 간단한 구성이다.

\n\n\n\n

지금 이 블로그로 테스트를 진행하여 보았다.

\n\n\n\n

부하테스트 툴은 jmate를 사용하였다.

\n\n\n\n
![](/images/2019/09/Screenshot-2019-09-22-at-09.26.56-1024x235.jpg)
\n\n\n\n

1초동안 100명의 USER가 접속을 시도하고 30초간 유지이다.

\n\n\n\n

총 3000번의 접근을 하게된다.

\n\n\n\n
![](/images/2019/09/Screenshot-2019-09-22-at-09.27.38-1024x354.jpg)
\n\n\n\n

http://linuxer.name 으로 http request 를 하도록 설정하였다.

\n\n\n\n
![](/images/2019/09/Screenshot-2019-09-22-at-10.40.14-1024x416.jpg)
\n\n\n\n

web인스턴스의 CPU / memory 지표이다.  
실제로는 보이는 지표의 2배정도 된다고 보면된다. 5분 평균이라 실제 부하보다 낮은 값으로 보인다. 실제 cpu 부하는 100%라고 보면 된다. 23:45이 galera 00:15 rds다.

\n\n\n\n

나중에 생각해보니 왜 rds 의 그래프가 더 낮을까 의문이 들었는데 rds max connection 때문에 정상적으로 부하가 제한된것 같다. 이런.. 라고 생각했는데 아니었다..그냥 웹서버 php-fpm 제한이었다 ㅠㅠ

\n\n\n\n
![](/images/2019/09/Screenshot-2019-09-22-at-11.05.32-1024x437.jpg)
\n\n\n\n

galera 인스턴스다. 그래프의 평균치라 마찬가지다. 두배정도의 부하가 발생했다고 생각하면 된다. 합쳐서 11%정도의 부하가 발생했다. 그래프에서 안보이는데 A/C의 부하가 동일하게 나타났다.

\n\n\n\n
![](/images/2019/09/Screenshot-2019-09-22-at-11.13.17-1024x507.jpg)
\n\n\n\n

RDS로 옮긴후에 테스트진행하였다. 13%정도의 부하가 발생하였다. 이때

\n\n\n\n
![](/images/2019/09/image-1-1024x486.png)
\n\n\n\n

rds max connection은 꽉찬 상태였다. 이결과로만 보면 내 블로그는 max 커넥션을 더늘려도 괜찮은 거로 보인다. 사용자원에 비해 기본값 max connection 이 낮은 편이라는 결론이 난다.

\n\n\n\n

각설하고 일단 단순비교시에 galera와 rds 의 성능차는 거의 없어 보인다.

\n\n\n\n

비용차이는 NLB 비용이 cost explorer에서 추가되지 않아서 확인할수 없었다.  
그런데 free tire 에서는 NLB가 포함되지 않는데 이상하게 청구되지 않고 있다...땀삐질 너무 쓰는게 없어서 그런가..

\n\n\n\n
![](/images/2019/09/image-2.png)
\n\n\n\n

현재 galera에서 RDS로 전환한 상태이고 마지막 테스트 까지 진행하였다.

\n\n\n\n

추가테스트를 한다면 web서버의 처리량을 늘리고 최대사용자를 테스트하는 방식으로 가야 할것으로 보인다.

\n\n\n\n

이 테스트는 다른것보다 galera가 어느정도 사용가능한 수준이라는 것을 알게 된 과정이었다.

\n\n\n\n

다음에 기회가 된다면 좀더 딥한 성능테스트를 진행해보겠다.

\n\n\n\n

좋은하루되시라!

\n