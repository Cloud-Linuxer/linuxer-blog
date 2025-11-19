---
title: "Ping-MTU-test"
date: 2021-07-07T16:24:35+09:00
draft: false
categories: ["Linux"]
slug: "ping-mtu-test"
aliases:
  - /ping-mtu-test/
  - /ping-mtu-test/
---

\n

MTU 9000 이상을 점보프레임이라 부른다.

\n\n\n\n

점포프레임이 정상적으로 전송되는지 확인하는 방법이다.

\n\n\n\n

```
ping -M do -s 1472 google.com\nPING google.com (172.217.175.110) 1472(1500) bytes of data.\n76 bytes from nrt20s21-in-f14.1e100.net (172.217.175.110): icmp_seq=1 ttl=114 (truncated)\n76 bytes from nrt20s21-in-f14.1e100.net (172.217.175.110): icmp_seq=2 ttl=114 (truncated)\n76 bytes from nrt20s21-in-f14.1e100.net (172.217.175.110): icmp_seq=3 ttl=114 (truncated)
```

\n\n\n\n

1500에 맞춰서 google로 보내면 정상적으로 간다.

\n\n\n\n

```
ping -M do -s 1473 google.com\nPING google.com (172.217.175.110) 1473(1501) bytes of data.\n^C\n--- google.com ping statistics ---\n45 packets transmitted, 0 received, 100% packet loss, time 43999ms
```

\n\n\n\n

1501 은 가지 않는다.

\n\n\n\n

대부분의 클라우드 내부의 이더넷은 점보프레임이 설정되어 있으며 9000이상이다.

\n\n\n\n

```
ifconfig | grep -i MTU | grep eth\neth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 8950
```

\n\n\n\n

외부망으론 1500까지만 전송됨을 확인하였으니 내부망에서 MTU를 확인한다.

\n\n\n\n

```
ping -M do -s 8922 10.0.12.13\nPING 10.0.12.13 (10.0.12.13) 8922(8950) bytes of data.\n8930 bytes from 10.0.12.13: icmp_seq=1 ttl=64 time=0.491 ms\n8930 bytes from 10.0.12.13: icmp_seq=2 ttl=64 time=0.431 ms\n8930 bytes from 10.0.12.13: icmp_seq=3 ttl=64 time=0.483 ms
```

\n\n\n\n

잘된다.

\n\n\n\n

인터페이스에 지정된 MTU는 8950이다.   
ping에선 IP Header(20 Bytes) + ICMP Header(8 Bytes) 28 Bytes 를 뺀 숫자가 ICMP Data 크기이다. 그래서 Ping 로 MTU 테스트할땐 실제 MTU-28을 하여 테스트하면된다.

\n\n\n\n\n