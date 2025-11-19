---
title: "NCP-SSD-Server-IOPS"
date: 2020-07-14T22:53:28+09:00
draft: false
categories: ["Linux", "NCP"]
slug: "ncp-ssd-server-iops"
aliases:
  - /ncp-ssd-server-iops/
  - /ncp-ssd-server-iops/
---


오늘 [7월] 네이버클라우드플랫폼 공인교육 - Professional을 다녀왔습니다.
교육을 받다보니 좀 흥미로운 내용이 있더군요.


NCP의 SSD VM은 최소 IOPS가 4000입니다.


![](/images/2020/07/image-15-1024x131.png)

블로깅을 하던때가 아니라서 포스팅이나 결과를 깔끔하게 정리한게 아니라 공개하긴 어렵지만 AWS에서도 비슷한 테스트를 한적이 있습니다.


EBS- GP2를 20개를 하나의 인스턴스에 붙여서 100 IOPS 인볼륨을 20개를 붙여서 2000 IOPS로 늘려서 디스크 자체의 퍼포먼스를 올리는 테스트를요.


이 테스트는 많은 엔지니어들이 장난식으로 테스트를 진행했고 유효한 결과를 얻은적이 있는 테스트 입니다. 물론 라이브 서버에 도입하기엔 부담이 따르고 리스크에 비해 얻을수 있는 장점이 크지 않다보니 테스트로만 끝낸적이 있습니다.


그런데 제앞에 10G의 기본 IOPS가 4000짜리가 나타난 것입니다.


NCP의 VM이 가진 제한이 볼륨 16개 까지 붙일수 있는데, OS 볼륨을 제외하면 15개 까지.


150G의 용량으로 60000 IOPS라는 계산이 나옵니다. 그럼 NCP 의 최대 IOPS는 얼마인지 볼까요?


![](/images/2020/07/image-16-1024x119.png)

NCP의 IOPS 계산은 1GB당 40IOPS가 증가합니다. 500GB 일때 20000 IOPS 그러니까 볼륨의 가성비는 10G일때 제일 높은셈입니다.


![](/images/2020/07/image-18-1024x175.png)

가성비가 제일 높은 볼륨 15개를 추가할 비용을 계산해보면 월 17280원이 추가되는군요.


그럼 월 17280 원으로 낼수있는 최대 성능을 테스트 해볼겁니다.


사실 객관성은 이쯤해선 망각해도 됩니다.
아무래도 서비스에선 사용하기 어려운 구성이니까요.


먼저 볼륨 15개를 인스턴스에 붙입니다.


그리고 아래 스크립트를 돌려서


#!/bin/sh
for VAR in `fdisk -l | grep "Disk /dev/" | grep -v xvda | awk -F: '{print $1}' | awk '{print $2}`';
do
(echo n; echo p; echo 1; echo 2048; echo; echo t; echo 8e; echo w) | fdisk $VAR
done
a=`fdisk -l | grep '/dev/xvd.1' | grep -v '/dev/xvda' | awk '{print $1}'`
pvcreate $a
vgcreate linuxer-lvm $a
lvcreate -l 38385 -n volume linuxer-lvm
mkdir /lvm
mkfs.xfs -f /dev/linuxer-lvm/volume
mount -t xfs /dev/linxer-lvm/volume /lvm


마운트 까지 완료했습니다.


[root@s1734ba4660a ~]# vgdisplay
--- Volume group ---
VG Name linuxer-lvm
System ID
Format lvm2
Metadata Areas 15
Metadata Sequence No 2
VG Access read/write
VG Status resizable
MAX LV 0
Cur LV 1
Open LV 0
Max PV 0
Cur PV 15
Act PV 15
VG Size 149.94 GiB
PE Size 4.00 MiB
Total PE 38385
Alloc PE / Size 38385 / 149.94 GiB
Free PE / Size 0 / 0
VG UUID YEEHFI-FpvU-fTmE-YnHx-9itm-mhH6-QUsz8j


vg도 잘만들어져서 마운트까지 정상적으로 됩니다.


속도 테스트하려니까 너무 귀찮아서..........................


으앙주금...


여러분 이포스팅은 언젠간 마무리 할테지만...


오늘은 아닌가 봅니다.


굿밤!
