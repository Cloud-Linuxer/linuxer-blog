---
title: "AWS-CloudShell"
date: 2020-12-16T09:10:03+09:00
draft: false
categories: ["AWS"]
slug: "aws-cloudshell"
aliases:
  - /aws-cloudshell/
  - /aws-cloudshell/
---


![](/images/2020/12/image-18.png)

OK! Thank You!

amazon linux2 기반의 클라우드 쉘이다.

가볍고 빠르고 일부리전만 지원하고..

얼른한국 리전도 지원해주세요.!

본격적으로 스펙을 파악해 보자.

```
-bash-4.2# df -h Filesystem      Size  Used Avail Use% Mounted on overlay          30G   12G   17G  41% / tmpfs            64M     0   64M   0% /dev shm             1.9G     0  1.9G   0% /dev/shm tmpfs           1.9G     0  1.9G   0% /sys/fs/cgroup /dev/nvme1n1     30G   12G   17G  41% /aws/mde /dev/loop0      976M  2.6M  907M   1% /home tmpfs           1.9G     0  1.9G   0% /proc/acpi tmpfs           1.9G     0  1.9G   0% /sys/firmware
```
은근무거운데?

```
-bash-4.2# free
              total        used        free      shared  buff/cache   available Mem:        3977864      270404     2099668         392     1607792     3495176 Swap:             0           0           0
```
메모리 수준 무엇?

```
-bash-4.2# cat /proc/cpuinfo | grep model model           : 85 model name      : Intel(R) Xeon(R) Platinum 8175M CPU @ 2.50GHz model           : 85 model name      : Intel(R) Xeon(R) Platinum 8175M CPU @ 2.50GHz
```
CPU 좋고 용량 좋고 메모리 좋고

```
[cloudshell-user@ip-10-0-153-179 ~]$ sudo systemctl start httpd Failed to get D-Bus connection: Operation not permitted
```
서비스는 실행할수 없고..

그래고 엄청 짱짱하네..

기다려온 만큼 성능이 좋다!
