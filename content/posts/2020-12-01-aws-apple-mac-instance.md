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


![](/images/2020/12/image.png)

오오오오오오!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

**macOS Catalina 10.15.7** 버전을 쓸수있다.

![](/images/2020/12/image-1.png)

뜨든... 인스턴스 유형은 베어 메탈뿐.. 그렇다고 해서 내가 안만들순없지 가즈아!!!!!

-_-;

![](/images/2020/12/image-2.png)

전용 호스트가 필요하다....근데 전용 호스트 갯수는 not support 상태다 service quotas를 늘려야한다.

![](/images/2020/12/image-5.png)

![](/images/2020/12/image-3-1024x258.png)

일단 바로 요청 근데 금방 안되나? 아마 지금 전세계에서 생성 중일거다..증가가 되면 바로 더 진행해 보겠다.

![](/images/2020/12/image-4.png)

Maximum number of running dedicated mac1 hosts.

보류에서 할당량이 요청됨으로 변경됬다.

그리고 오늘 (12월2일) 요청은 허락되지 않고 기본 제공량이 3으로 변경됬다.

![](/images/2020/12/image-13.png)

일단 전용호스트를 만들고, 인스턴스를 생성했다.

![](/images/2020/12/image-14.png)

한방에 인스턴스가 전용호스트를 다 차지한다.

```text
ssh -i linuxer.pem ec2-user@IP
```

ssh는 동일하게 ec2-user 계정으로 접근한다.

SSM을 이용한접근도 가능하다.

![](/images/2020/12/image-15.png)

먼저 vnc 로 접근하는게 목적이므로brew로 vnc server 를 셋팅해야한다.

```bash
sudo /System/Library/CoreServices/RemoteManagement/ARDAgent.app/Contents/Resources/kickstart -configure -allowAccessFor -allUsers -privs -all sudo /System/Library/CoreServices/RemoteManagement/ARDAgent.app/Contents/Resources/kickstart -configure -clientopts -setvnclegacy -vnclegacy yes
sudo /System/Library/CoreServices/RemoteManagement/ARDAgent.app/Contents/Resources/kickstart -configure -clientopts -setvncpw -vncpw supersecret sudo /System/Library/CoreServices/RemoteManagement/ARDAgent.app/Contents/Resources/kickstart -restart -agent -console sudo /System/Library/CoreServices/RemoteManagement/ARDAgent.app/Contents/Resources/kickstart -activate
```
<https://gist.github.com/nateware/3915757>

귀찮아서 이페이지 복붙했다. 위 명령어를 치면 vnc 가활성화 된다.

```bash
sudo dscl . -passwd /Users/ec2-user
```

명령어로 ec2-user의 패스워드를 설정한다.

그리고 VNC viewer 로 접속한다.

![](/images/2020/12/image-16.png)

길고긴 여정을 지나 드디어.. 접속했다.

북미라 너무 느리다..-_-; VNC로 접속하기를 마무리한다.
