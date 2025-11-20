---
title: "gcp VPC 및 network 미션"
date: 2019-11-30T12:50:57+09:00
draft: false
categories: ["GCP"]
tags: ["gcp lb", "gcp vpc", "gcp"]
slug: "gcp-network-미션"
aliases:
  - /gcp-network-미션/
  - /gcp-network-%eb%af%b8%ec%85%98/
---


1.Pub pri.db네트워크 만들고 2.elb설정해오기 .서버는 private만 존재 3.nat도 만들고 서버에서 인터넷접속 확인하기까지.

가 일단 나는 목표인데 청개구리 속성상 미션대로 진행할리가 없다 나는..

먼저 구글은 bastion host 가 대부분의 구성도에서 빠져있다. 외부IP가 없는 상태로 pri 에 속한 네트웤에도 gcp console로 접속을 할수 있는것. 어떤 원리도 작동되는것인지 먼저 파봐야 겠다.

![](/images/2019/11/image-29-1024x105.png)

외부IP는 없는상태이다. 방화벽에서 22번만 any 로 열어준 상태로

![](/images/2019/11/image-30-1024x620.png)

ssh 가 붙는다. ????? ssh가 맞는지 확인해본다.

![](/images/2019/11/image-31-1024x227.png)

다른 세션을 이용하거나 에이전트 방식일줄 알았으나 아니다. 외부의 접속을 받는 상태인거다. 이상태라면 aws 식으로 말하자면 igw 에 연결되어있는 퍼블릭상태에서 퍼블릭IP만 없는 요상한 상태인것으로 정확한 의미에서 망분리가 아닌것이다.

그렇다면 일단 정확한 망분리를 진행해 보기로 하였다.

![](/images/2019/11/image-32-1024x49.png)

외부로 핑이 간다. 그렇다는건 인터넷으로 연결된 라우팅을 가지고 있다는것!

![](/images/2019/11/image-33.png)

그렇지만 Private google access 를 껏다 키며 테스트를 진행해 보았으나 결과는 같았다.

![](/images/2019/11/image-34.png)

[hoceneco@instance-1 ~]$ ping google.comPING google.com (74.125.124.113) 56(84) bytes of data.

ping 이 외부의 IP를 정상적으로 가져온다. 그럼 인터널 DNS가 존재하는 걸까?

![](/images/2019/11/image-35-1024x117.png)

internal dns 가 존재하는걸 확인했다. 내부 DNS 가 응답하므로 IP만 가져오는것이다. 그렇지만 이게 완벽하게 Private subnet인지는 알수없다.

$ last
hoceneco pts/1 35.235.240.242 Fri Nov 29 11:47 still logged in
hoceneco pts/0 35.235.240.240 Fri Nov 29 11:39 still logged in
reboot system boot 4.18.0-80.11.2.e Fri Nov 29 11:26 still running

외부에서 접근 IP가 찍히기 때문. 고민이 많이되었다. Private subnet 이여야 DB를 생성할수 있는 기반이 생기는것인데 구글에선 인스턴스가 에이전트로 통신하는 방식이 아닌 ssh 를 사용하기떄문에 nat를 사용하여 인스턴스 까지 도달한다 생각하므로 일반적인 망분리의 기준에서 매우 벗어나는 것이다.

<https://cloud.google.com/vpc/docs/private-google-access?hl=ko>

링크를 보면

# 비공개 Google 액세스

비공개 Google 액세스를 사용하면 비공개 IP 주소만 있는 GCP 인스턴스가 네트워크의 방화벽 규칙에 따라 Google API 및 서비스의 공개 IP 주소에 액세스할 수 있습니다.

## 비공개 Google 액세스 및 VPC 서브넷

비공개 Google 액세스 기능은 Google 공개 API로 송신되는 트래픽이 확인되면 이를 가로채 Google 내부로 라우팅합니다. 비공개 Google 액세스 서브넷에 있는 VM과 Google API 간의 트래픽은 항상 Google 네트워크 내에서 유지됩니다.

그렇다. 자동 내부라우팅 기능일 뿐이었다.

오 그럼 db통신을 공개 API로 진행하면 내부라우팅으로 자동으로 전환해준다는것. 결국 실제 Private subnet의 사용은 아닌것이다.

이글은 스터디 이전에 작성되었고 스터디 이후 어느정도 생각이 정리되었다.

생각을 정리하기 위해서 테스트한 내용이다.

External IP 가 없는 인스턴스와 External IP 이 부여된 인스턴스 두가지를 생성하였다.

![](/images/2019/12/image-1024x143.png)

Internal IP만 존재하는 인스턴스는 외부와 통신할수 없다. 신기하게 console SSH로는 붙는다. AWS 의 구체화된 망구성과는 다르게 GCP의 망분리 구성은 구체적인 부분이 있지만 AWS와는 다른 개념이었다.

AWS의 망구성은 계층적이고 구체적인데 GCP의 망구성은 단순하다.

다른 표현이 딱히 있는거 같지 않다. External IP의 유무로 public / private 을 나눈다. 글로벌 인프라로 VPC를 생성하고 리전에 subnet이 종속된다. subnet 하단에 az가 나눠지게 된다. AWS의 역할별 subnet은 만들순 있으나 GCP에선 의미가 없는것이다.

테스트를 위해서 Internal IP만 가진 인스턴스를 로드벨런서에 연결했다.

![](/images/2019/12/image-1-1024x681.png)

인스턴스는 instance-group1 에 묶여서 로드벨런서에 연결했다.

로드벨런서의 구성은 차차 언급하기로하고 NAT가 없는 상태의 인스턴스이지만 로드벨런서의 요청에는 착실히 응답하였다. 만족스럽다.

![](/images/2019/12/image-3-1024x301.png)

만족스러운 이유는 따로있다. GCP는 private 인스턴스 임에도 불구하고 ssh 접속으로 작업이 가능하고, 로드벨런서 또한 잘되니까 보안도 챙기는데 작업도 편한 그런느낌이다.

정상적인 네트워크의 테스트를 위해서 Cloud NAT 또한 넣어서 진행했다.

NAT 생성은 단순하다.

![](/images/2019/12/image-2-709x1024.png)

NAT name / VPC / Region / Nat route / IP 옵션만 지정해주면 바로 생성이된다.

로드벨런서는 먼저 세가지로 분류가 되는데 선행되어야 하는 작업이 있다.
인스턴스 그룹을 생성해야한다. 인스턴스 그룹은 managed / unmanaged 로 나뉜다.

![](/images/2019/12/image-4.png)

빠른 관리형이냐 아니냐로 생각하면 편하다.

<https://cloud.google.com/compute/docs/instance-groups/?hl=ko>

링크를 참조하자.

인스턴스 그룹을 만들었으면 LB를 생성할수 있는데 backend / frontend / Host and path rules 을 설정하면 로드벨런서를 생성할수 있다. AWS 서비스에 매칭해서 보면

backend는 대상그룹 frontend 는 리스너 Host and path rules 은 규칙이라 생각하면 된다.

![](/images/2019/12/image-5-1024x667.png)

AWS와는 제일큰 다른점은 오토스케일링이 인스턴스 그룹에서 굉장히 직관적인 방식으로 지원한다는 점이다. 또한 로드벨런서의 엔드포인트가 애니캐스트로 IP가 1개만 나온다. 다른 로드벨런서처럼 zone apex에 대한 고민을 하지 않아도 된다는 것이 굉장한 장점이다.

![](/images/2019/12/image-6-1024x587.png)

로드벨런서가 CDN을 지원하는건 좀 충격이었다.

일단 gcp는 vpc 그리고 인스턴스 개개별이 공개와 비공개로 설정되어 따로 망에 대한 설정이 필요없는 점. 그리고 로드벨런서의 애니캐스트가 장점인것을 알게되었다.

정리해야지 하고 생각하다가 오늘에서야 정리하지만 유익한 스터디였다.
