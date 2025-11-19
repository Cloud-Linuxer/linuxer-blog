---
title: "AWS-userdata-glusterFS-install"
date: 2020-06-29T16:01:43+09:00
draft: false
categories: ["AWS", "Linux"]
tags: ["userdata", "glusterfs"]
slug: "aws-userdata-glusterfs-install"
aliases:
  - /aws-userdata-glusterfs-install/
  - /aws-userdata-glusterfs-install/
---

\n

#!/bin/bash  
(echo n; echo p; echo 1; echo 2048; echo; echo t; echo 83; echo w) | fdisk /dev/xvdf  
mkfs.xfs -i size=512 /dev/xvdf1  
mkdir -p /bricks/brick1  
echo "/dev/xvdf1 /bricks/brick1 xfs defaults 1 2" >> /etc/fstab  
mount -a && mount  
yum install -y centos-release-gluster  
yum install -y xfsprogs glusterfs-server  
systemctl enable glusterd  
systemctl start glusterd  
Setenforce 0  
sed -i 's/^SELINUX=.*/SELINUX=disabled/g' /etc/sysconfig/selinux && cat /etc/sysconfig/selinux echo "* soft nofile 65535" >> /etc/security/limits.conf  
echo "\* hard nofile 65535" >> /etc/security/limits.conf  
chmod 744 /etc/rc.d/rc.local

\n\n\n\n

ec2 userdata glusterfs install 스크립트 입니다.

\n\n\n\n\n\n\n\n

<https://wiki.centos.org/SpecialInterestGroup/Storage/gluster-Quickstart>

\n