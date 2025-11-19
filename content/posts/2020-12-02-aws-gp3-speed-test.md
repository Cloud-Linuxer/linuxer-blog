---
title: "AWS-gp3-speed-test"
date: 2020-12-02T16:46:05+09:00
draft: false
categories: ["AWS", "ec2"]
tags: ["fio", "gp3", "gp2"]
slug: "aws-gp3-speed-test"
aliases:
  - /aws-gp3-speed-test/
  - /aws-gp3-speed-test/
---


![](/images/2020/12/image-10.png)

볼륨 두개를 만들었다


```
mount /dev/nvme1n1p1 /mnt/gp3 mount /dev/nvme2n1p1 /mnt/gp2 yum install gcc zlib-devel wget https://codeload.github.com/axboe/fio/tar.gz/fio-3.24 tar zfxv fio-3.24 cd fio-fio-3.24/ ./configure --prefix=/home/fio make; make install\n
```


필요한 라이브러리 gcc, zlib-devel 설치후 컴파일.


fio 는 나도 처음써보는 툴이다


```
fio --directory=/mnt/gp3 --name fio_test_file --direct=1 --rw=randread \\ --bs=4K --size=1G --numjobs=7 --time_based --runtime=180 --group_reporting \\ --norandommap
```


3분동안 하나의 스레드가 7개의 1G 파일을 4K 단위로 Direct I/O 모드의 Random Read 로 읽는 테스트이다.


```
Jobs: 7 (f=7): [r(7)][100.0%][r=11.7MiB/s][r=3001 IOPS][eta 00m:00s] fio_test_file: (groupid=0, jobs=7): err= 0: pid=2450: Wed Dec  2 06:59:19 2020\n  read: IOPS=3016, BW=11.8MiB/s (12.4MB/s)(2121MiB/180004msec)\n    clat (usec): min=188, max=296635, avg=2319.05, stdev=1213.65\n     lat (usec): min=188, max=296635, avg=2319.21, stdev=1213.65\n    clat percentiles (usec):\n     |  1.00th=[  408],  5.00th=[  922], 10.00th=[ 1287], 20.00th=[ 1598],\n     | 30.00th=[ 1762], 40.00th=[ 1926], 50.00th=[ 2057], 60.00th=[ 2212],\n     | 70.00th=[ 2474], 80.00th=[ 2933], 90.00th=[ 3818], 95.00th=[ 4621],\n     | 99.00th=[ 6194], 99.50th=[ 6587], 99.90th=[ 7767], 99.95th=[ 8455],\n     | 99.99th=[10028]\n   bw (  KiB/s): min= 9848, max=32328, per=100.00%, avg=12069.08, stdev=167.76, samples=2513\n   iops        : min= 2462, max= 8082, avg=3017.27, stdev=41.94, samples=2513\n  lat (usec)   : 250=0.05%, 500=2.12%, 750=1.59%, 1000=1.99%\n  lat (msec)   : 2=40.61%, 4=45.04%, 10=8.59%, 20=0.01%, 50=0.01%\n  lat (msec)   : 250=0.01%, 500=0.01%\n  cpu          : usr=0.12%, sys=0.29%, ctx=543082, majf=0, minf=93\n  IO depths    : 1=100.0%, 2=0.0%, 4=0.0%, 8=0.0%, 16=0.0%, 32=0.0%, >=64=0.0%\n     submit    : 0=0.0%, 4=100.0%, 8=0.0%, 16=0.0%, 32=0.0%, 64=0.0%, >=64=0.0%\n     complete  : 0=0.0%, 4=100.0%, 8=0.0%, 16=0.0%, 32=0.0%, 64=0.0%, >=64=0.0%\n     issued rwts: total=542985,0,0,0 short=0,0,0,0 dropped=0,0,0,0\n     latency   : target=0, window=0, percentile=100.00%, depth=1 \nRun status group 0 (all jobs):\n   READ: bw=11.8MiB/s (12.4MB/s), 11.8MiB/s-11.8MiB/s (12.4MB/s-12.4MB/s), io=2121MiB (2224MB), run=180004-180004msec \nDisk stats (read/write):\n  nvme1n1: ios=542478/13, merge=0/3, ticks=1253070/0, in_queue=1078350, util=99.97%
```


정확히 3000iops 가 나온다.


그럼 로컬 디바이스 테스트 해볼까?


```
fio --directory=/mnt/gp2 --name fio_test_file --direct=1 --rw=randread \\ --bs=4K --size=1G --numjobs=7 --time_based --runtime=180 --group_reporting \\ --norandommap
```


```
fio-3.24 Starting 7 processes Jobs: 7 (f=7): [r(7)][100.0%][r=11.7MiB/s][r=2997 IOPS][eta 00m:00s] fio_test_file: (groupid=0, jobs=7): err= 0: pid=1316: Wed Dec  2 07:13:16 2020\n  read: IOPS=3016, BW=11.8MiB/s (12.4MB/s)(2121MiB/180004msec)\n    clat (usec): min=192, max=298525, avg=2318.95, stdev=1162.93\n     lat (usec): min=192, max=298525, avg=2319.12, stdev=1162.93\n    clat percentiles (usec):\n     |  1.00th=[  457],  5.00th=[  963], 10.00th=[ 1254], 20.00th=[ 1565],\n     | 30.00th=[ 1729], 40.00th=[ 1909], 50.00th=[ 2057], 60.00th=[ 2245],\n     | 70.00th=[ 2540], 80.00th=[ 3032], 90.00th=[ 3818], 95.00th=[ 4490],\n     | 99.00th=[ 5932], 99.50th=[ 6259], 99.90th=[ 6915], 99.95th=[ 7373],\n     | 99.99th=[ 8455]\n   bw (  KiB/s): min= 9808, max=26696, per=100.00%, avg=12069.37, stdev=141.33, samples=2513\n   iops        : min= 2452, max= 6674, avg=3017.34, stdev=35.33, samples=2513\n  lat (usec)   : 250=0.01%, 500=1.48%, 750=1.61%, 1000=2.48%\n  lat (msec)   : 2=41.05%, 4=44.98%, 10=8.40%, 20=0.01%, 250=0.01%\n  lat (msec)   : 500=0.01%\n  cpu          : usr=0.12%, sys=0.30%, ctx=543092, majf=0, minf=90\n  IO depths    : 1=100.0%, 2=0.0%, 4=0.0%, 8=0.0%, 16=0.0%, 32=0.0%, >=64=0.0%\n     submit    : 0=0.0%, 4=100.0%, 8=0.0%, 16=0.0%, 32=0.0%, 64=0.0%, >=64=0.0%\n     complete  : 0=0.0%, 4=100.0%, 8=0.0%, 16=0.0%, 32=0.0%, 64=0.0%, >=64=0.0%\n     issued rwts: total=543002,0,0,0 short=0,0,0,0 dropped=0,0,0,0\n     latency   : target=0, window=0, percentile=100.00%, depth=1 \nRun status group 0 (all jobs):\n   READ: bw=11.8MiB/s (12.4MB/s), 11.8MiB/s-11.8MiB/s (12.4MB/s-12.4MB/s), io=2121MiB (2224MB), run=180004-180004msec \nDisk stats (read/write):\n  nvme2n1: ios=542683/0, merge=0/0, ticks=1253810/0, in_queue=1076380, util=99.74%
```


엥 결과가 같다..왜지? 3000iops 로 고정된다 gp2인데..


gp3를 분리하고 테스트한다.


![](/images/2020/12/image-12.png)

```
Jobs: 7 (f=7): [r(7)][75.6%][r=11.7MiB/s][r=3001 IOPS][eta 00m:44s]
```


그럼 gp3연결하고 iops 를 올리고 다시 gp3 에 테스트한다.


```
fio-3.24 Starting 7 processes Jobs: 7 (f=7): [r(7)][100.0%][r=23.4MiB/s][r=6002 IOPS][eta 00m:00s] fio_test_file: (groupid=0, jobs=7): err= 0: pid=1393: Wed Dec  2 07:29:50 2020\n  read: IOPS=6033, BW=23.6MiB/s (24.7MB/s)(4242MiB/180002msec)\n    clat (usec): min=146, max=327858, avg=1158.79, stdev=1152.61\n     lat (usec): min=146, max=327858, avg=1158.95, stdev=1152.62\n    clat percentiles (usec):\n     |  1.00th=[  281],  5.00th=[  371], 10.00th=[  441], 20.00th=[  586],\n     | 30.00th=[  685], 40.00th=[  766], 50.00th=[  848], 60.00th=[  947],\n     | 70.00th=[ 1090], 80.00th=[ 1434], 90.00th=[ 2343], 95.00th=[ 3294],\n     | 99.00th=[ 5014], 99.50th=[ 5342], 99.90th=[ 6456], 99.95th=[ 8455],\n     | 99.99th=[26608]\n   bw (  KiB/s): min=16360, max=37232, per=100.00%, avg=24140.01, stdev=241.45, samples=2513\n   iops        : min= 4090, max= 9308, avg=6035.00, stdev=60.36, samples=2513\n  lat (usec)   : 250=0.64%, 500=13.39%, 750=23.96%, 1000=26.32%\n  lat (msec)   : 2=23.16%, 4=9.85%, 10=2.63%, 20=0.01%, 50=0.04%\n  lat (msec)   : 100=0.01%, 250=0.01%, 500=0.01%\n  cpu          : usr=0.24%, sys=0.53%, ctx=1086208, majf=0, minf=87\n  IO depths    : 1=100.0%, 2=0.0%, 4=0.0%, 8=0.0%, 16=0.0%, 32=0.0%, >=64=0.0%\n     submit    : 0=0.0%, 4=100.0%, 8=0.0%, 16=0.0%, 32=0.0%, 64=0.0%, >=64=0.0%\n     complete  : 0=0.0%, 4=100.0%, 8=0.0%, 16=0.0%, 32=0.0%, 64=0.0%, >=64=0.0%\n     issued rwts: total=1085994,0,0,0 short=0,0,0,0 dropped=0,0,0,0\n     latency   : target=0, window=0, percentile=100.00%, depth=1 \nRun status group 0 (all jobs):\n   READ: bw=23.6MiB/s (24.7MB/s), 23.6MiB/s-23.6MiB/s (24.7MB/s-24.7MB/s), io=4242MiB (4448MB), run=180002-180002msec \nDisk stats (read/write):\n  nvme2n1: ios=1085375/0, merge=0/0, ticks=1249280/0, in_queue=1077940, util=100.00%
```


gp3의 iops 가 올라간건 확인이 된다.


정리하자면 gp2의 성능테스트시에 iops 가 3000으로 고정된다. 아마 대역폭기반 계산이라 정확하게 3000으로 측정되어 실제 디스크의 iops 가 아닌거 같다.


대역폭을 측정할수 있는 툴인가........툴을까봐야하는데 귀찮다..그건 나중에...-_-;
