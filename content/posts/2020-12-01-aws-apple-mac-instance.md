---
title: "AWS-apple-MAC-instance"
date: 2020-12-01T14:21:13+09:00
draft: false
categories: ["AWS", "ec2"]
tags: ["aws", "mac", "instance"]
slug: "aws-apple-mac-instance"
aliases:
  - /aws-apple-mac-instance/
  - /aws-apple-mac-instance/
---

\n
![](/images/2020/12/image.png)
\n\n\n\n

오오오오오오!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

\n\n\n\n

**macOS Catalina 10.15.7** 버전을 쓸수있다.

\n\n\n\n
![](/images/2020/12/image-1.png)
\n\n\n\n

뜨든... 인스턴스 유형은 베어 메탈뿐.. 그렇다고 해서 내가 안만들순없지 가즈아!!!!!

\n\n\n\n

-\_-;

\n\n\n\n
![](/images/2020/12/image-2.png)
\n\n\n\n

전용 호스트가 필요하다....근데 전용 호스트 갯수는 not support 상태다 service quotas를 늘려야한다.

\n\n\n\n
![](/images/2020/12/image-5.png)
\n\n\n\n
![](/images/2020/12/image-3-1024x258.png)
\n\n\n\n

일단 바로 요청 근데 금방 안되나? 아마 지금 전세계에서 생성 중일거다..증가가 되면 바로 더 진행해 보겠다.

\n\n\n\n
![](/images/2020/12/image-4.png)
\n\n\n\n

Maximum number of running dedicated mac1 hosts.

\n\n\n\n

보류에서 할당량이 요청됨으로 변경됬다.

\n\n\n\n

그리고 오늘 (12월2일) 요청은 허락되지 않고 기본 제공량이 3으로 변경됬다.

\n\n\n\n
![](/images/2020/12/image-13.png)
\n\n\n\n

일단 전용호스트를 만들고, 인스턴스를 생성했다.

\n\n\n\n
![](/images/2020/12/image-14.png)
\n\n\n\n

한방에 인스턴스가 전용호스트를 다 차지한다.

\n\n\n\n

```
ssh -i linuxer.pem ec2-user@IP
```

\n\n\n\n

.

\n\n\n\n

ssh는 동일하게 ec2-user 계정으로 접근한다.

\n\n\n\n

SSM을 이용한접근도 가능하다.

\n\n\n\n
![](/images/2020/12/image-15.png)
\n\n\n\n

먼저 vnc 로 접근하는게 목적이므로brew로 vnc server 를 셋팅해야한다.

\n\n\n\n

```
sudo /System/Library/CoreServices/RemoteManagement/ARDAgent.app/Contents/Resources/kickstart -configure -allowAccessFor -allUsers -privs -all\nsudo /System/Library/CoreServices/RemoteManagement/ARDAgent.app/Contents/Resources/kickstart -configure -clientopts -setvnclegacy -vnclegacy yes \nsudo /System/Library/CoreServices/RemoteManagement/ARDAgent.app/Contents/Resources/kickstart -configure -clientopts -setvncpw -vncpw supersecret\nsudo /System/Library/CoreServices/RemoteManagement/ARDAgent.app/Contents/Resources/kickstart -restart -agent -console\nsudo /System/Library/CoreServices/RemoteManagement/ARDAgent.app/Contents/Resources/kickstart -activate
```

\n\n\n\n

<https://gist.github.com/nateware/3915757>

\n\n\n\n

귀찮아서 이페이지 복붙했다. 위 명령어를 치면 vnc 가활성화 된다.

\n\n\n\n

```
sudo dscl . -passwd /Users/ec2-user
```

\n\n\n\n

.

\n\n\n\n

명령어로 ec2-user의 패스워드를 설정한다.

\n\n\n\n

그리고 VNC viewer 로 접속한다.

\n\n\n\n
![](/images/2020/12/image-16.png)
\n\n\n\n

길고긴 여정을 지나 드디어.. 접속했다.

\n\n\n\n

북미라 너무 느리다..-\_-; VNC로 접속하기를 마무리한다.

\n