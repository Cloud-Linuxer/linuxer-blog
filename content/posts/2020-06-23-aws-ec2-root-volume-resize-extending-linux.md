---
title: "AWS-EC2-Root-Volume-Resize-Extending-linux"
date: 2020-06-23T10:35:07+09:00
draft: false
categories: ["AWS", "Linux"]
tags: ["aws", "resize", "volume"]
slug: "aws-ec2-root-volume-resize-extending-linux"
aliases:
  - /aws-ec2-root-volume-resize-extending-linux/
  - /aws-ec2-root-volume-resize-extending-linux/
---


<https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/recognize-expanded-volume-linux.html>


리눅스 볼륨 확장은 이 docs 를 참고하자. 먼저 오늘 테스트할 ami 는 amazon linux 1 이다.


[root@ip-172-31-43-226 ~]# df -h
Filesystem Size Used Avail Use% Mounted on
devtmpfs 483M 60K 483M 1% /dev
tmpfs 493M 0 493M 0% /dev/shm
/dev/xvda1 7.9G 1.2G 6.6G 15% /


root 볼륨은 8G 로 1.2G를 사용중이다. 이걸 20G로 늘릴거다.


먼저 볼륨 태그를 잘확인한다.


amazon linux 1 은 ext4 에 /dev/xvda1 로 / 가 설정되고
amazon linux 2 는 xfs 에 /dev/nvme1n1p1 으로 / 가 설정 된다


확장 자체는 디바이스의 파티션을 지정해서 확장하므로 일반적으로 볼륨 하나당 하나의 파티션을 사용하는것을 권장한다. on-prem 처럼 하나의 볼륨에 여러개의 파티션을 사용한다면 확장은 힘들다.


볼륨수정을 눌러서 진행한다.


![](/images/2020/06/image-1-8.png)

볼륨을 수정하면 optimizing 과정을 거쳐서 확장된다. 디스크를 사용중에도 확장할수 있으나, 안전한 작업을 위한다면 스냅샷을 생성하고 확장하자.


![](/images/2020/06/image-1-9.png)

* ![](/images/2020/06/image-1-10.png)

![](/images/2020/06/image-1-11.png)

Disk /dev/xvda: 21.5 GB, 21474836480 bytes, 41943040 sectors
Units = sectors of 1 \* 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disk label type: dos
Disk identifier: 0x00000000
Device Boot Start End Blocks Id System
/dev/xvda1 1 16777215 8388607+ ee GPT


/dev/xvda: 21.5 GB 볼륨이 확장된게 보인다.


현재 상태는 볼륨만 확장된것이고 파티션을 확장해야 한다.


# growpart /dev/xvda 1
CHANGED: disk=/dev/xvda partition=1: start=4096 old: size=16773086,end=16777182 new: size=41938910,end=41943006


amazon linux 1 의 경우엔 파티션이 xvda 로 보여서 xvda 의 첫번째 파티션은 1번을 확장한다.


amazon linux 2 의 경우엔 파티션이 nvme1n1p1 으로 보이므로 실제 명령어는


# growpart /dev/nvme1n1 1


로 명령어를 쳐야 한다. growpart 로 파티션을 확장하면 Disk label type: dos -> Disk label type: gpt 변경되고,


![](/images/2020/06/image-1-13.png)

![](/images/2020/06/image-1-14.png)

위처럼 디스크 라벨 부터 파티션 타입까지 변경된다.


fdisk -l 명령어로 확인하며 진행하자.


이제 다음은 파일시스템의 확장이 필요하다. 파일시스템 확장은 resize2fs 명령어로 확장한다.


# resize2fs /dev/xvda1
resize2fs 1.43.5 (04-Aug-2017)
Filesystem at /dev/xvda1 is mounted on /; on-line resizing required
old_desc_blocks = 1, new_desc_blocks = 2
The filesystem on /dev/xvda1 is now 5242363 (4k) blocks long.


그럼 볼륨 확장이 완료된다.


볼륨확장에 대해 정리하자면 이렇다.


실제 볼륨을 확장하고 파티션을 확장하고 파일시스템을 확장한다.


# df -h
Filesystem Size Used Avail Use% Mounted on
devtmpfs 483M 60K 483M 1% /dev
tmpfs 493M 0 493M 0% /dev/shm
/dev/xvda1 20G 1.3G 19G 7% /


정상적으로 확장된 파티션을 확인할수 있다.


xfs 에서 파티션 확장은 xfs_growfs 명령어를 사용한다. 참고하자.
