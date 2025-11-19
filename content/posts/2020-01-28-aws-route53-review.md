---
title: "aws-route53-review"
date: 2020-01-28T10:54:53+09:00
draft: false
categories: ["AWS", "기타"]
tags: ["aws route53", "a aaaa", "recode"]
slug: "aws-route53-review"
aliases:
  - /aws-route53-review/
  - /aws-route53-review/
---


요 며칠간 CF관련 이슈로 고민이 많았다.


ipv6 부터 SK LTE까지...


이문제가 발생한 원인은 먼저


SK LTE DNS 에서의 ipv6라우팅이 가장 큰 원인일테고..
같은 cloudfront에서도 발생하는 빈도차가 있었으므로 그 원인을 파악하고 해결하는 법을 서술하려고한다.


먼저 A alias는 ipv4로 라우팅한다. - A record 는 ipv4를 라우팅 하므로..


![](/images/2020/01/image-74.png)

>linuxer.name
이름: linuxer.name
 Addresses: 52.85.231.10
 52.85.231.111
 52.85.231.68
 52.85.231.42


그렇다면 alias 를쓰는 사용자는 cf관련 문제를 겪지 않았을 것이다.


Route 53 [별칭 레코드](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/resource-record-sets-choosing-alias-non-alias.html)는 AWS 리소스와 같은 별칭 대상의 DNS 이름에 내부적으로 매핑됩니다. Route 53은 조정 작업과 소프트웨어 업데이트를 위해 별칭 대상의 DNS 이름과 연결된 IP 주소를 모니터링합니다. Route 53 이름 서버의 신뢰할 수 있는 응답에는 A 레코드(IPv4 주소에 대한 레코드) 또는 AAAA 레코드(IPv6 주소에 대한 레코드)와 별칭 대상의 IP 주소가 포함되어 있습니다.
 <https://aws.amazon.com/ko/premiumsupport/knowledge-center/route-53-create-alias-records/>


내용을 확인해 보면 신뢰할수 있는 응답에 ipv4-ipv6를 응답하게 되어있다고 나와있다.


따라서..alias는 문제가 없었다.


그렇다면 문제가 있었을 cf는 무엇일까?


cname 을 사용하던 도메인들이다.


cname을 설정하면 이렇다.


![](/images/2020/01/image-75.png)

>test2.linuxer.name
 서버: UnKnown
 Address: 210.219.173.151
권한 없는 응답:
 이름: d19f2uxthc0s83.cloudfront.net
 Addresses: 2600:9000:2150:1a00:10:3683:b8c0:93a1
 2600:9000:2150:8000:10:3683:b8c0:93a1
 2600:9000:2150:c000:10:3683:b8c0:93a1
 2600:9000:2150:6400:10:3683:b8c0:93a1
 2600:9000:2150:8c00:10:3683:b8c0:93a1
 2600:9000:2150:1000:10:3683:b8c0:93a1
 2600:9000:2150:7800:10:3683:b8c0:93a1
 2600:9000:2150:e200:10:3683:b8c0:93a1
 52.85.231.10
 52.85.231.111
 52.85.231.68
 52.85.231.42
 Aliases: test2.linuxer.name


ipv6 와 ipv4를 모두응답한다. 이 경우 ipv6가 우선라우팅이 된다.


그래서 결국 route53 공식문서를 확인해보니 A/AAAA를 같이쓰라고 되어있다.


cloudfront 는 cname 을 제공하고 A record를 사용할경우 cloudfront 의 IP변경에 대응할수 없다. 그렇기 때문에 일반적으로 A alias 를 사용하라 한것이다.


명시적인 레코드의 분리를 뜻하는 것이다. 일반적으로 잘 발생하는 문제는 아닌것으로 보이나, cname 을 사용하게되면 이렇다.


일반적으로 도메인에 요청을 할때 레코드를 지정해서 쿼리하진 않는다.
그래서 cname 으로 요청하게되면 cname 에 연결된 모든 record가 응답하게 되고 그 결과 값에 따라서 ipv6 가 존재하면 ipv6 로 라우팅 된다.


nslookup 결과
>test2.linuxer.name
 서버: dns.google
 Address: 8.8.8.8권한 없는 응답:
 이름: d19f2uxthc0s83.cloudfront.net
 Addresses: 2600:9000:2139:e200:10:3683:b8c0:93a1
 2600:9000:2139:fa00:10:3683:b8c0:93a1
 2600:9000:2139:4c00:10:3683:b8c0:93a1
 2600:9000:2139:7400:10:3683:b8c0:93a1
 2600:9000:2139:5400:10:3683:b8c0:93a1
 2600:9000:2139:aa00:10:3683:b8c0:93a1
 2600:9000:2139:2600:10:3683:b8c0:93a1
 2600:9000:2139:6c00:10:3683:b8c0:93a1
 99.86.144.35
 99.86.144.128
 99.86.144.34
 99.86.144.126
 Aliases: test2.linuxer.name


따라서 route53을 사용할때 A/AAAA를 분리해서 사용하라는 말이다.


그런데 말입니다.


![그런데 말입니다에 대한 이미지 검색결과](https://img1.daumcdn.net/thumb/R800x0/?scode=mtistory2&fname=https%3A%2F%2Ft1.daumcdn.net%2Fcfile%2Ftistory%2F99AE38335A090A7102)

A레코드는 쓸수 없잖아? cf는 IP가 바뀌니까..


그래서 결론이 난다.  **확실하게 정해준다.**


A Alias AAAA alias 를 사용하는걸 권장한다.
같은계정내 자원이라면!


아니라면?


cname 을 사용할수 밖에 없다면 CloudFront 의 IPv6 를 **끄자.**


CloudFront Distributions > General > Enable IPv6


![](/images/2020/01/image-76.png)

![](/images/2020/01/image-78.png)

체크박스만 누르고 Yes, Edit 만 누르면 된다.


참쉽죠.


참곤란한 이슈였다. 참고-URL


<https://www.facebook.com/groups/awskrug/permalink/2278291878939490/>


<https://tools.ietf.org/html/rfc3484?fbclid=IwAR0Ca2JDM55CpyhZSjtiR7EYhySfzADdLMRX2q-rWZoAM-z8BHbqismCQfk#section-2.1>


https://twitter.com/fortyfourbits/status/1220241946343403520?ref_src=twsrc%5Etfw%7Ctwcamp%5Etweetembed%7Ctwterm%5E1220241946343403520&ref_url=https%3A%2F%2Flinuxer.name%2F2020%2F01%2Faws-route53-%25ec%259d%2598-%25ec%259d%2591%25eb%258b%25b5%25ec%259d%25b4%25ec%2583%2581%2F


읽어주셔서 감사하다!
