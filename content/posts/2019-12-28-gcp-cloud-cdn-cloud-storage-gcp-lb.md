---
title: "GCP cloud CDN-cloud storage - GCP-LB"
date: 2019-12-28T18:09:06+09:00
draft: false
categories: ["GCP"]
tags: ["gcp cdn", "gcp storage"]
slug: "gcp-cloud-cdn-cloud-storage-gcp-lb"
aliases:
  - /gcp-cloud-cdn-cloud-storage-gcp-lb/
  - /gcp-cloud-cdn-cloud-storage-gcp-lb/
---

\n

cloud storage 를 생성했다. cloudshell 로 생성하여

\n\n\n\n

gsutil mb gs://linuxer-upload

\n\n\n\n

명령어 한줄로 일단 생성은 잘됬다.

\n\n\n\n
![](/images/2019/12/image-16.png)
\n\n\n\n

그래서 GUI로 생성해봤다.

\n\n\n\n
![](/images/2019/12/image-17.png)
\n\n\n\n
![](/images/2019/12/image-19.png)
\n\n\n\n

멀티리전은 전 세계일거라 막연히 생각했는데 미국/유럽/아시아다.

\n\n\n\n
![](/images/2019/12/image-20.png)
\n\n\n\n

..?너무 스토리지 분할이 애매한거 같은데..이럼 스텐다드만 써야 하는거 아닌가..

\n\n\n\n
![](/images/2019/12/image-21.png)
\n\n\n\n

객체별 제어도 가능하다. 생성을 누르니까 버킷이름을 DNS로 생성해서 도메인의 소유권을 인증해야 했다. **DNS 레코드를 통해 도메인 소유권 인증** 을 진행해야 한다.

\n\n\n\n

<https://search.google.com/search-console/welcome>

\n\n\n\n

사이트로 이동해서

\n\n\n\n
![](/images/2019/12/image-22.png)
\n\n\n\n

도메인을 입력하고

\n\n\n\n
![](/images/2019/12/image-23.png)
\n\n\n\n

txt 레코드를 입력했다.

\n\n\n\n

-> set q=txt  
 -> gs.linuxer.name  
 서버: [116.125.124.254]  
 Address: 116.125.124.254  
 권한 없는 응답:  
 gs.linuxer.name text = "google-site-verification=x1bcH219nXSYlS22cVVN7QNhROkqHWxjGmMtTKOxFCk"

\n\n\n\n

그리고 nslookup 으로 조회 정상적으로 조회가 잘된다.

\n\n\n\n
![](/images/2019/12/image-24.png)
\n\n\n\n

이상하게 구글에선 확인이 늦다. 왜지? 걸어야 하는딩;;

\n\n\n\n
![](/images/2019/12/image-25.png)
\n\n\n\n

txt 레코드..설정도 이상한게 없다. 아............급 막혔다. 그래서 루트도메인에 걸려있던 spf 레코드를 지우고 설정해봤는데..

\n\n\n\n
![](/images/2019/12/image-26.png)
\n\n\n\n

한번 실패하더니 소유권 확인이 가능했다.

\n\n\n\n
![](/images/2019/12/image-27.png)
\n\n\n\n
![](/images/2019/12/image-28.png)
\n\n\n\n

소유자가 확인이 되는데 아직도 버킷은 생성이 안된다.....왜죠??gcp 님? 그래서 브라우저를 종료하고 다시 생성했더니 정상적으로 됬다..

\n\n\n\n

이제 생성한 도메인을 백엔드로 두고 CDN을 연결할 것이다.

\n\n\n\n

네트워크 서비스 > Cloud CDN 서비스가 있다.

\n\n\n\n

CDN 을 생성하기 위해선 로드벨런서가 필요하다.

\n\n\n\n

먼저 로드벨런서를 생성하자.

\n\n\n\n
![](/images/2019/12/image-29.png)
\n\n\n\n

백엔드를 생성하고~백엔드를 생성하면 자동으로 라우팅 규칙도 생성된다.

\n\n\n\n

인증서도 생성해 준다.

\n\n\n\n
![](/images/2019/12/image-31.png)
\n\n\n\n

SSL 인증서 'linuxer-cert'을(를) 만들지 못했습니다. 오류: Invalid value for field 'resource.managed.domains[0]': '\*.linuxer.name'. Wildcard domains not supported.

\n\n\n\n
![](/images/2019/12/image-33.png)
\n\n\n\n

에러가 발생한다 acm 을 염두에 두고 와일드카드로 생성했는데 와일드 카드는 안된단다.. 이런..그래서 gs.linuxer.name 으로 생성했다.

\n\n\n\n
![](/images/2019/12/image-34.png)
\n\n\n\n

LB 생성하면서 CDN 을 켜는 속성이 존재해서 켜줬다.

\n\n\n\n
![](/images/2019/12/image-35.png)
\n\n\n\n

Google 관리형 SSL 인증서는 인증서당 도메인 이름 1개만 지원하며 와일드 카드 일반 이름이나 주체 대체 이름 여러 개를 지원하지 않습니다.   
 <https://cloud.google.com/load-balancing/docs/ssl-certificates>

\n\n\n\n

인증서 프로비저닝이 실패했다. 그래서 얼른 프로토콜을 HTTP로 돌리고 테스트했는데 새로운걸 알았다.

\n\n\n\n
![](/images/2019/12/image-36.png)
\n\n\n\n

프런트엔드의 IP가 다르다. 헐..? 이러면 애니캐스트고 뭐고 소용없는거 아냐? 그래서 하나더 만들어 봤다.

\n\n\n\n
![](/images/2019/12/image-37.png)
\n\n\n\n

음.. 뭐지.. 이해할수가 없는 하나의 백엔드에 여러개의 프런트엔드를 붙인건데 IP가 다르다...이거 어떻게 이해해야하지..? 생각해보니 임시IP로 생성해서 그런것 같다.

\n\n\n\n

일단 CDN 붙이고

\n\n\n\n
![](/images/2019/12/image-38.png)
\n\n\n\n

아 익명...

\n\n\n\n
![](/images/2019/12/image-39.png)
\n\n\n\n
![](/images/2019/12/image-40.png)
\n\n\n\n
![](/images/2019/12/Screenshot-2019-12-28-at-18.06.26.jpg)
\n\n\n\n

allusers 가 view 권한을 가지게 된 이후로 정상적으로 보인다.

\n\n\n\n

조금 애매한부분은 세밀한 권한 관리가 되지 않는 점이 좀 애매하달까..

\n\n\n\n\n