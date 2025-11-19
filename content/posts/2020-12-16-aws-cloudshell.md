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

\n
![](/images/2020/12/image-18.png)
\n\n\n\n

OK! Thank You!

\n\n\n\n\n\n\n\n

amazon linux2 기반의 클라우드 쉘이다.

\n\n\n\n

가볍고 빠르고 일부리전만 지원하고..

\n\n\n\n

얼른한국 리전도 지원해주세요.!

\n\n\n\n

본격적으로 스펙을 파악해 보자.

\n\n\n\n

```
-bash-4.2# df -h\nFilesystem      Size  Used Avail Use% Mounted on\noverlay          30G   12G   17G  41% /\ntmpfs            64M     0   64M   0% /dev\nshm             1.9G     0  1.9G   0% /dev/shm\ntmpfs           1.9G     0  1.9G   0% /sys/fs/cgroup\n/dev/nvme1n1     30G   12G   17G  41% /aws/mde\n/dev/loop0      976M  2.6M  907M   1% /home\ntmpfs           1.9G     0  1.9G   0% /proc/acpi\ntmpfs           1.9G     0  1.9G   0% /sys/firmware
```

\n\n\n\n

은근무거운데?

\n\n\n\n

```
-bash-4.2# free\n              total        used        free      shared  buff/cache   available\nMem:        3977864      270404     2099668         392     1607792     3495176\nSwap:             0           0           0
```

\n\n\n\n

메모리 수준 무엇?

\n\n\n\n

```
-bash-4.2# cat /proc/cpuinfo | grep model\nmodel           : 85\nmodel name      : Intel(R) Xeon(R) Platinum 8175M CPU @ 2.50GHz\nmodel           : 85\nmodel name      : Intel(R) Xeon(R) Platinum 8175M CPU @ 2.50GHz
```

\n\n\n\n

CPU 좋고 용량 좋고 메모리 좋고

\n\n\n\n

```
[cloudshell-user@ip-10-0-153-179 ~]$ sudo systemctl start httpd\nFailed to get D-Bus connection: Operation not permitted
```

\n\n\n\n

서비스는 실행할수 없고..

\n\n\n\n

그래고 엄청 짱짱하네..

\n\n\n\n

기다려온 만큼 성능이 좋다!

\n