---
title: "NCP-to-AWS-IPsec-multi-Cloud"
date: 2020-11-05T17:50:31+09:00
draft: false
categories: ["AWS", "NCP"]
tags: ["IPsec", "vpn"]
slug: "ncp-to-aws-ipsec-multi-cloud"
aliases:
  - /ncp-to-aws-ipsec-multi-cloud/
  - /ncp-to-aws-ipsec-multi-cloud/
---

\n

NCP와 AWS 의 IPsec VPN을 연결해 보았습니다. Site to Site VPN을 연결하는 것입니다.

\n\n\n\n

아직 NCP에서는 VPC 모드에서 IPsec VPN을 지원하지 않아서 Classic 모드에서 만 연결이 가능합니다.

\n\n\n\n
![](/images/2020/11/image-5.png)
\n\n\n\n

NCP IPsec VPN Gateway 를 먼저 만들어야 AWS Customer Gateway 를 생성할수 있습니다.

\n\n\n\n

NCP IPsec VPN Gateway 를 생성하기 위해선 Private Subnet 을 먼저 생성해야 합니다.  
저는 192.168.1.0/24 로 생성했습니다.

\n\n\n\n
![](/images/2020/11/image.png)
\n\n\n\n

Encryption : aes

\n\n\n\n

D-H Group 은 NCP 에선 1/2/5만 지원합니다.

\n\n\n\n

hash 는 sha 입니다.

\n\n\n\n

확인 버튼을 누르면 생성됩니다.

\n\n\n\n
![](/images/2020/11/image-1-1024x254.png)
\n\n\n\n

확인된 IP는 49.236.139.115 입니다. 이 IP를 Customer Gateway에서 사용하시면 됩니다.

\n\n\n\n
![](/images/2020/11/image-2.png)
\n\n\n\n

다음과 같이 CGW를 만들어 줍니다. 그다음 VGW를 생성해 줘야 합니다.  
Virtual Private Gateway 는 VPC 에 붙이는 가상의 게이트 웨이로 **CGW- tunnel -V**GW 구성으로 통신하게 됩니다.

\n\n\n\n

VGW는 생성하면 VPC에 Attach 해야 합니다.

\n\n\n\n
![](/images/2020/11/image-6.png)
\n\n\n\n

VPN으로 사용하려는 VPC에 연결해 주세요.

\n\n\n\n

이제 터널을 생성해야 합니다.

\n\n\n\n
![](/images/2020/11/image-7.png)
\n\n\n\n

Site to Site VPN 메뉴에서 터널을 생성하면 됩니다.

\n\n\n\n

미리 생성한 VPG와 CGW를 잘 넣어주시고 라우팅 옵션을 static 으로 설정합니다. BGP는 지원하지 않습니다.

\n\n\n\n
![](/images/2020/11/image-8.png)
\n\n\n\n

정적라우팅 대역을 미리 추가해 주는게 편합니다.  
**Local IPv4 Network Cidr** 는 NCP의 대역을 넣어주셔야 합니다.  
**Remote IPv4 Network Cidr** cidr은 AWS 의 대역입니다.

\n\n\n\n
![](/images/2020/11/image-11.png)
\n\n\n\n

Edit Tunnel 1 Options 을 체크해서 터널 옵션을 넣어줍니다.

\n\n\n\n
![](/images/2020/11/image-9.png)
\n\n\n\n

**Pre-Shared Key for Tunnel 1** 에서 key 라고 표기하지만 VPN 인증시에 사용하는 값이라 패스워드처럼 취급되기도 하므로..저는 rkskekfk 로 설정했습니다.

\n\n\n\n
![](/images/2020/11/image-10.png)
\n\n\n\n

위 옵션은 NCP IPsec VPN의 옵션에 맞춰서 체크한 옵션입니다. 모두 체크해도 문제는 없을듯합니다.

\n\n\n\n
![](/images/2020/11/image-12.png)
\n\n\n\n

AWS는 DPD 옵션을 ikev2에서만 지원하므로 AWS VPN 자체에서 터널을 시작하는 기능은 NCP 와의 IPsec VPN 설정에선 사용할수 없는 설정입니다. 이유는 NCP의 IPsec VPN은 ikev1만 지원하기 때문입니다.

\n\n\n\n

지금 설정에선 단일터널만 사용하려기에 tunnel 1만 설정해주려 합니다.

\n\n\n\n
![](/images/2020/11/image-13.png)
\n\n\n\n

버튼눌러서 생성후엔 NCP의 IPsec VPN을 추가해야 합니다.

\n\n\n\n

NCP 콘솔로 이동해서 AWS 의 터널 IP를 이용해서 터널링을 맺어줘야 합니다.

\n\n\n\n

AWS 콘솔에서 VPN Tunnel Details 를 보면 Tunnel 1 의 IP를 확인할 수 있습니다.

\n\n\n\n
![](/images/2020/11/image-14.png)
\n\n\n\n

이 아이피로 Peer IP로 사용해 연결할겁니다.

\n\n\n\n

NCP 에서 Local Network 는 NCP의 Private Subnet Cidr입니다.

\n\n\n\n
![](/images/2020/11/image-15.png)
\n\n\n\n
![](/images/2020/11/image-16.png)
\n\n\n\n

Remote Network 는 172.31.0.0/16 으로 AWS 의 네트워크 입니다.

\n\n\n\n
![](/images/2020/11/image-17.png)
\n\n\n\n

위 이미지대로 선택해주세요.

\n\n\n\n

사실 설명이 필요한 부분이 좀 있는데..과감히 생략합니다.  
이유는 터널시작과 터널통신은 각각 인증방식을 사용하는데 이부분이 NCP는 나누어져서 설정하고 AWS 는 같이 설정합니다....그래서 그냥 따라서 해보시고 어려우면 댓글 남겨주세요.

\n\n\n\n

생성하시면 굉장히 빠른속도로 생성됩니다. 아직 터널을 개시한 상태가 아니기 때문에 inactive 로 보일겁니다. 이때 터널의 상태를 확인할수 있는 방법이 있습니다.

\n\n\n\n\n\n\n\n
![](/images/2020/11/image-18.png)
\n\n\n\n

메뉴에서

\n\n\n\n
![](/images/2020/11/image-19.png)
\n\n\n\n

현재 상태를 확인할 수 있습니다.

\n\n\n\n
![](/images/2020/11/image-20.png)
\n\n\n\n

인터페이스 / 라우팅 / IPsec VPN Tunnel 상태를 확인할수 있습니다.

\n\n\n\n

There are no ipsec sas  
There are no IKEv1 SAs

\n\n\n\n

두줄의 메시지를 확인할수 있으며, 아직 터널이 UP상태가 아니기 때문입니다.

\n\n\n\n

이제 인스턴스가 필요합니다.

\n\n\n\n

네트워크 인터페이스에서 서버에 인터페이스를 붙이고 아이피를 부여해주세요.

\n\n\n\n
![](/images/2020/11/image-21.png)
\n\n\n\n

다음과 같이 글로벌 비공인 IP와 추가한 Private Subnet IP가 보입니다.

\n\n\n\n

인스턴스 내부에서 인터페이스를 설정해주세요.

\n\n\n\n

```
cat <<EOF > /etc/sysconfig/network-scripts/ifcfg-eth1\nDEVICE=eth1\nBOOTPROTO=static\nONBOOT=yes\n#Private Subnet IP로 변경해주세요.\nIPADDR=192.168.1.13\nEOF\nifup eth1
```

\n\n\n\n

이제 라우팅을 추가해야 합니다.

\n\n\n\n

```
ip route add 172.31.0.0/16 via 192.168.1.1 dev eth1
```

\n\n\n\n

추가 명령어 입니다.

\n\n\n\n

```
 ip route del 172.31.0.0/16 via 192.168.1.1
```

\n\n\n\n

라우팅을 잘못 넣게 되면 ip route del 명령어로 라우팅을 삭제할수 있습니다.  
라우팅이 정상적으로 잘 연결되면 이제 AWS 에도 라우팅 테이블을 추가해야 합니다.

\n\n\n\n
![](/images/2020/11/image-22.png)
\n\n\n\n

맨아랫 줄에 추가된 라우팅 테이블은 제일 먼저 만들었던 VGW 입니다.  
이제 양방향으로 통신할 라우팅이 모두 만들어 졌고, 서로 통신할수 있도록 NCP 의 ASG와 AWS 의 SG를 열어주세요.

\n\n\n\n

그리고 NCP의 인스턴스에서 ping 을 날려줍니다. AWS ikev1 은 DPD를 이용할수 없기 때문에 상태방에서 터널을 개시해야 합니다.

\n\n\n\n

```
[root@s17596a9a6e6 ~]# ifconfig | grep inet\n        inet 10.41.151.70  netmask 255.255.254.0  broadcast 10.41.151.255\n        inet 192.168.1.13  netmask 255.255.255.0  broadcast 192.168.1.255\n        inet 127.0.0.1  netmask 255.0.0.0\n[root@s17596a9a6e6 ~]# ping 172.31.36.10\nPING 172.31.36.10 (172.31.36.10) 56(84) bytes of data.\n64 bytes from 172.31.36.10: icmp_seq=1 ttl=62 time=3.93 ms\n64 bytes from 172.31.36.10: icmp_seq=2 ttl=62 time=3.45 ms\n64 bytes from 172.31.36.10: icmp_seq=3 ttl=62 time=3.33 ms\n64 bytes from 172.31.36.10: icmp_seq=4 ttl=62 time=3.44 ms\n
```

\n\n\n\n

정상적으로 Site to Site VPN이 연결된것을 확인할수 있습니다.

\n\n\n\n

이렇게 정상적으로 VPN이 연결 되면 AWS 콘솔에선 터널이 UP 상태가 되고,  
NCP 콘솔에선 active 로 표시됩니다. 그리고 마지막으로 정상적으로 터널링이 맺어져서 통신이 되면 NCP 콘솔에서 아래와 같이 확인할수 있습니다.

\n\n\n\n

```
KEv1 SAs:\n\nActive SA: 1\nRekey SA: 0 (A tunnel will report 1 Active and 1 Rekey SA during rekey)\nTotal IKE SA: 1\n\n1 IKE Peer: 3.34.211.29\nType : L2L Role : initiator\nRekey : no State : MM_ACTIVE\ninterface: outside\nCrypto map tag: outside_map, seq num: 1, local addr: 49.236.139.115\n\naccess-list outside_cryptomap_1 extended permit ip 192.168.1.0 255.255.255.0 172.31.0.0 255.255.0.0\nlocal ident (addr/mask/prot/port): (192.168.1.0/255.255.255.0/0/0)\nremote ident (addr/mask/prot/port): (172.31.0.0/255.255.0.0/0/0)\ncurrent_peer: 3.34.211.29\n\n\n#pkts encaps: 827, #pkts encrypt: 827, #pkts digest: 827\n#pkts decaps: 764, #pkts decrypt: 764, #pkts verify: 764\n#pkts compressed: 0, #pkts decompressed: 0\n#pkts not compressed: 827, #pkts comp failed: 0, #pkts decomp failed: 0\n#pre-frag successes: 0, #pre-frag failures: 0, #fragments created: 0\n#PMTUs sent: 0, #PMTUs rcvd: 0, #decapsulated frgs needing reassembly: 0\n#TFC rcvd: 0, #TFC sent: 0\n#Valid ICMP Errors rcvd: 0, #Invalid ICMP Errors rcvd: 0\n#send errors: 0, #recv errors: 0\n\nlocal crypto endpt.: 49.236.139.115/0, remote crypto endpt.: 3.34.211.29/0\npath mtu 1500, ipsec overhead 74(44), media mtu 1500\nPMTU time remaining (sec): 0, DF policy: copy-df\nICMP error validation: disabled, TFC packets: disabled\ncurrent outbound spi: C7CCEEBF\ncurrent inbound spi : E2B83FD5\n\ninbound esp sas:\nspi: 0xE2B83FD5 (3803725781)\nSA State: active\ntransform: esp-aes esp-sha-hmac no compression\nin use settings ={L2L, Tunnel, PFS Group 2, IKEv1, }\nslot: 0, conn_id: 264200192, crypto-map: outside_map\nsa timing: remaining key lifetime (sec): 108\nIV size: 16 bytes\nreplay detection support: Y\nAnti replay bitmap:\n0x00000000 0x00000001\nspi: 0xEED2584F (4006762575)\nSA State: active\ntransform: esp-aes esp-sha-hmac no compression\nin use settings ={L2L, Tunnel, PFS Group 2, IKEv1, Rekeyed}\nslot: 0, conn_id: 264200192, crypto-map: outside_map\nsa timing: remaining key lifetime (sec): 0\nIV size: 16 bytes\nreplay detection support: Y\nAnti replay bitmap:\n0x00000000 0x00000001\noutbound esp sas:\nspi: 0xC7CCEEBF (3352096447)\nSA State: active\ntransform: esp-aes esp-sha-hmac no compression\nin use settings ={L2L, Tunnel, PFS Group 2, IKEv1, }\nslot: 0, conn_id: 264200192, crypto-map: outside_map\nsa timing: remaining key lifetime (sec): 108\nIV size: 16 bytes\nreplay detection support: Y\nAnti replay bitmap:\n0x00000000 0x00000001\nspi: 0xC47BC9E1 (3296446945)\nSA State: active\ntransform: esp-aes esp-sha-hmac no compression\nin use settings ={L2L, Tunnel, PFS Group 2, IKEv1, Rekeyed}\nslot: 0, conn_id: 264200192, crypto-map: outside_map\nsa timing: remaining key lifetime (sec): 0\nIV size: 16 bytes\nreplay detection support: Y\nAnti replay bitmap:\n0x00000000 0x00000001
```

\n\n\n\n

이 포스팅은 과정 자체만 설명하고 자세한 프로토콜이나, 인증방식은 설명하지 않았습니다.

\n\n\n\n

사용자의 레벨에서 따라만 해도 VPN 터널링이 가능한 수준의 포스팅을 하려했으나, VPN이 조금 난이도가 있는거 같습니다.

\n\n\n\n

진행하다가 궁금하신 부분은 댓글남겨주세요.

\n\n\n\n\n\n\n\n

읽어주셔서 감사합니다.

\n