---
title: "AWS-EC2-Root-volume-downsize-amazonlinux2-xfs"
date: 2020-06-23T14:15:53+09:00
draft: false
categories: ["AWS", "Linux"]
tags: ["aws", "resize", "downsize", "xfs", "amazon linux 2"]
slug: "aws-ec2-root-volume-downsize-amazonlinux2-xfs"
aliases:
  - /aws-ec2-root-volume-downsize-amazonlinux2-xfs/
  - /aws-ec2-root-volume-downsize-amazonlinux2-xfs/
---

\n

\nhttps://linuxer.name/2020/06/aws-ec2-root-volume-downsize-amazonlinux1-ext4/\n

\n\n\n\n

작업의 흐름은 위 포스팅을 참고하기 바란다.

\n\n\n\n

지금 포스팅은 xfs grug2 를 사용하는 사용자를 위한 포스팅이다.

\n\n\n\n

amazon linux2 에 소스(xvdg)와 대상(xvdf)볼륨을 연결한다.

\n\n\n\n

디렉토리를 생성하고

\n\n\n\n

# mkdir /mnt/new  
# mkdir /mnt/org

\n\n\n\n

파티션을 생성하고

\n\n\n\n

# fdisk /dev/nvme1n1

\n\n\n\n

파일시스템을 생성하고

\n\n\n\n

# mkfs.xfs -f /dev/nvme1n1p1

\n\n\n\n

마운트한다

\n\n\n\n

# mount -t xfs /dev/xvdf1 /mnt/new  
# mount -t xfs /dev/xvdg1 /mnt/org

\n\n\n\n

rsync 로 데이터를 복사해주고

\n\n\n\n

# rsync -av /mnt/org/\* /mnt/new

\n\n\n\n

싱크가 끝나면 마운트한 경로로 이동한다.

\n\n\n\n

# cd /mnt/new

\n\n\n\n

그리고 blkid 를 이용하여 UUID 를 확인한다.

\n\n\n\n

/dev/nvme1n1: PTUUID="9986d28e" PTTYPE="dos"  
/dev/nvme1n1p1: LABEL="/" UUID="030df8fc-fb40-4ba6-af3e-662df2f52270" TYPE="xfs" PARTUUID="9986d28e-01"  
/dev/nvme0n1: PTUUID="83181c97-6d5e-43c9-9ede-e2f50ead5338" PTTYPE="gpt"  
/dev/nvme0n1p1: LABEL="/" UUID="55da5202-8008-43e8-8ade-2572319d9185" TYPE="xfs" PARTLABEL="Linux" PARTUUID="591e81f0-99a2-498d-93ec-c9ec776ecf42"  
/dev/nvme0n1p128: PARTLABEL="BIOS Boot Partition" PARTUUID="4908ae49-9d5b-423e-a23c-a507a47bacf5"

\n\n\n\n

일반적으론 UUID가 있을거지만.. 그경우엔 UUID 를 넣어주자.

\n\n\n\n

# xfs\_admin -U 'uuidgen' /dev/xvdf1

\n\n\n\n

명령어로 UUID 생성해서 넣어줄수 있다. UUID 가 보인다면 new / org 변수에 UUID 를 export 해주자 UUID 는 사람마다 다들테니 각각 잘확인해서 복붙하자.

\n\n\n\n

# export new=’3a26abfe-67eb-49e4-922a-73f6cd132402’  
# export org=’781f875d-4262-4f01-ba72-d6bd123785f5’  
# sed -i -e "s/$org/$new/g" etc/fstab  
# sed -i -e "s/$org/$new/g" boot/grub2/grub.cfg  
# mount -B /dev dev  
# mount -B /proc /proc  
# mount -B /sys sys  
# chroot .

\n\n\n\n

위 명령어를 치면 /mnt/new 경로에서 지정한 UUID 로 fstab 안의 UUID를 변경하고 grub.cfg 안의 UUID 또한 자동으로 치환해줄거다. 그런다음 3개의 경로를 bind mount 하고 현재위치에서 chroot . 를 치면 chroot 가 현재위치로 변경된다.

\n\n\n\n

# grub2-install /dev/xvdf

\n\n\n\n

chroot 가 정상적으로 먹는다면 볼륨을 변경하면 정상적으로 잘부팅된다.

\n\n\n\n\n\n\n\n

테스트 해보고 꼭 작업하길 바란다.

\n\n\n\n\n\n\n\n

수고하시라!

\n