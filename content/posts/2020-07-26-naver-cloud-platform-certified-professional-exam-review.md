---
title: "NAVER-Cloud-Platform-Certified-Professional-exam-review"
date: 2020-07-26T15:39:51+09:00
draft: false
categories: ["Certification", "NCP"]
tags: ["ncp", "NAVER Cloud Platform Certified Professional", "Professional", "pro", "ncloud"]
slug: "naver-cloud-platform-certified-professional-exam-review"
aliases:
  - /naver-cloud-platform-certified-professional-exam-review/
  - /naver-cloud-platform-certified-professional-exam-review/
---

\n

안녕하세요. [누리클라우드](https://nuricloud.com/) / [호스트센터](https://www.hostcenter.co.kr/) 의 정태환입니다.

\n\n\n\n

얼마전에 NCA 시험을 봤고 후기를 공유했습니다.   
그 이후에 급하게 NCP 시험을 준비했습니다.

\n\n\n\n

시험 일정의 제한 때문에 7월 9일, 16일 21일 해서 세차례의 시험을 보았고 합격하였습니다.

\n\n\n\n
![](/images/2020/07/image-21-1024x229.png)
\n\n\n\n

NCP시험은 일단 필기와 실기로 나누어져 있습니다.

\n\n\n\n

필기는 NCA시험과 동일하고 문항수는 troubleshooting은 30문항 나머지는 40문항이었습니다. 합격점은 60%로 NCA과 동일합니다. 그렇지만 생각보다 난이도가 있었습니다.

\n\n\n\n

첫번째로 NCP 시험은 아키텍트나 개발자의 시험이 아닙니다. 특정 역할에 대한 시험이 아닌, NCP USER에 대한 시험이라 봐야 합니다. 거기에 덧붙여서 USER 로서의 사용법과 상식을 시험한다 정도로 생각하면됩니다.

\n\n\n\n

NCA 시험보다 NCP 시험이 좀더 수월한 느낌이었습니다.

\n\n\n\n

저는 troubleshooting 을 먼저 보고 나머지 과목을 봤는데요, 사실저는 SE라 은근 자신있었던 부분이긴 합니다. 그래서 시험을 얼른보고 싶어서 7월 14일 부터 17일 까지 NCP pro 교육에 참가하기로 신청해놓은 상태에서 미리 시험을 봤습니다.

\n\n\n\n\n\n\n\n

**troubleshooting** - 207

\n\n\n\n

troubleshooting 은 정말 재미있는 과목입니다. 리눅스 윈도우 NCP의 문제가 생겼을떄 어떻게 처리를 해야하는지를 주로 물어보는 과목이었거든요.

\n\n\n\n

예를 들어서 실무에서 이야기를 해보자면, 콘솔에서 확인했을떄 인스턴스의 CPU 부하가 높은상태라면.. 인스턴스에 접속해서 어떤 프로세스에서 CPU점유가 높은지 확인할것입니다.

\n\n\n\n

이때 linux 라면 ps afuxwww 나 top, htop 등의 명령어를 이용해서 부하를 확인할것이고  
windows라면 작업관리자라던가 PerfMonitor 같은 서드파티 툴을 이용한 분석을 할것입니다.

\n\n\n\n

이것처럼 NCP의 시험은 심화적인 내용은 아니지만 기본적으로 시험을 통해 실무에서 사용할 내용들이 출제되었습니다.

\n\n\n\n

엔지니어로서 트러블슈팅을 항상 가까이하는 저로서는 나름 즐거운 내용의 과목었습니다.

\n\n\n\n

또한, 실기는 NCP console를 보고 ssh 로 접속하여 제시된 여러문제를 풀어나가는 문제였는데, troubleshooting은 NCP 콘솔에 어느정도 익숙한 상태이고, Loadbalancer에 대해 사용경험이 있어야 했습니다. 저 같은 경우엔 출제자의 의도를 잘못 이해하여 설정하는 방법은 모두 알고있었으나, 1문제를 다른 방법으로 해결하려 했습니다. 다행히 2문제는 정확하게 푼상태라 합격할수 있었습니다.

\n\n\n\n\n\n\n\n

두번째로 7월 16일에 응시한 Compute / Storage 는 Domain에 Overview 가 있습니다.

\n\n\n\n\n\n\n\n

**Overview,Compute/Storage** - 200

\n\n\n\n

Overview 는 NCP 전반적인 서비스에 대한 질문을 하므로 서비스 마다 대략적인 설명을 할수 있어야 합니다.

\n\n\n\n

Cloud Hoop은 NCP에서 만든 apache Hoop 을 이용해 개발한 분석 서비스입니다. 이와같이 간략하게 나마 서비스에 대한 카테고리와 정의 정도는 알고있어야 합니다.

\n\n\n\n

또한 RUA(Real User Analytics) / ELSA (Effective Log Search & Analytics) 같이 서비스의 명칭을 줄이기도 하므로 서비스의 이름은 꼭 다 알고 있는것이 좋습니다.

\n\n\n\n

저또한 모든 서비스를 알고있는것은 아니었기에.. 시험을 보면서 모르는 문제가 속출했습니다.

\n\n\n\n

필기는 서버유형에 대한 질문이나 파라메터의 최소값 최대값에 대한 문제들도 있었으니, 외움이 필요한 내용도 은근 있었습니다.

\n\n\n\n

실기는 주가되는 내용은 Compute 와 Nas 설정이었습니다. Linux 명령어에 대한 이해와 Compute / Storage 에 대한 실습은 두가지 카테고리에 속한 서비스가 많지 않으니 처음부터 끝까지 한번씩만 해보신다면 어려울게 없다 생각되는 실습이었습니다.

\n\n\n\n\n\n\n\n

마지막으로 7월 21일에 응시한 202 Network / Media Database / Management / Analytics 시험은 NCP 에서 주관하는 [7월] 네이버클라우드플랫폼 공인교육 - Professional 을 전주에 마치고 시험을 응시했습니다.

\n\n\n\n

교육에서는 DB 생성 fali over, 미디어 서비스 특성들을 골고루 교육받은 다음에 진행하였습니다.

\n\n\n\n\n\n\n\n

**Network / Media Database / Management / Analytics - 202**

\n\n\n\n

인상적인 서비스는 미디어 카테고리의 Image Optimizer 였습니다.

\n\n\n\n

이 서비스는 AWS Lamdba@edge 로 고객사의 요청에 의해 리사이즈 하는 기능을 구현해본적이 있는 서비스 였습니다. 간략하게 설명하자면 Image Optimizer는 오브젝트 스토리지에 있는 이미지를 CDN으로 캐싱할때 URL request로 파라메터를 입력받아 입력받은 값대로 이미지를 가공한다음 CDN에 캐싱하여 동일한 URL과 쿼리로 request할 경우 CDN에서 가공된 이미지를 제공하는 서비스입니다.

\n\n\n\n

이때 Lamdba@edge에 익숙하지 않아서 반나절이상 헤멘기억이 납니다. 그런데 NCP에선 3분이면 생성하고 사용하고. 더욱 다양한 기능들이 추가되있는것을 보고 굉장히 감탄했습니다.

\n\n\n\n

기본적으로 공부방법은 동일합니다. 카테고리에 속한 모든 서비스를 일단 생성 및 주요기능들을 테스트 합니다. 생성만하고 인터페이스를 익히는것만으로도 굉장히 도움이 됩니다. 그 이후에 일반적인 개념의 공부가 추가되어야 했습니다.

\n\n\n\n

subnet 서브넷에 대한 개념이 없이는 풀수 없는 문제가 있었습니다. subneting 에 대한 기본적인 이해는 있어야 했습니다.

\n\n\n\n

NCA 에서 했던 과목들이라 좀 익숙한 부분도 있었지만 CDN, GCDN, NAT, IPSEC-VPN 등 실제로 설정해보시면 어느부분이 중요한 부분인지 쉽게 알수 있습니다.

\n\n\n\n

Global Route Manager 를 예로 들면 NCP 에서 제공하는 DNS는 기본적인 DNS만을 제공하고 GSLB는 Global Route Manager 서비스에서 제공한다던가 하는 DNS를 사용하는 서비스이지만 어떻게 다른지를 알아야 합니다.

\n\n\n\n

Load Balancer 의 경우에는 Round Robin / Least Connection / Source IP Hash 방식의 부하분산을 지원하는데 각각 어떤 방식으로 Client를 분산해주는지 정확히 알아야 합니다.

\n\n\n\n

실기의 경우에는 싱가폴리전과 한국리전을 각각 사용해야 했던점을 제외하면 어려운 부분이 딱히 없었습니다.

\n\n\n\n\n\n\n\n

시험을 마치면 일반적으로 실기채점은 길게 5일까지도 걸렸습니다. 그리고 모든 시험에 합격 이후에 하루정도의 시간이 지나고 자격증이 발급되었습니다.

\n\n\n\n\n\n\n\n

![](/images/2020/07/image-22.png)

\n\n\n\n\n\n\n\n

NCP-PRO 시험 후기를 마무리하겠습니다.

\n\n\n\n

감사합니다.

\n