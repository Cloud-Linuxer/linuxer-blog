---
title: "시작하는 엔지니어를 위해 - 3"
date: 2023-12-06T00:10:34+09:00
draft: false
categories: ["Linux", "기타"]
tags: ["시작하는", "엔지니어를", "위해"]
slug: "for-engineers-starting-out"
aliases:
  - /for-engineers-starting-out/
  - /for-engineers-starting-out/
---


/posts/2020-12-26-시작하는-엔지니어를-위해-2/

시작하는 엔지니어를 위한 글을 쓴지 벌써 3년이 지났습니다.

3년간 저도 성장했고, 더 나은 이야기를 할수 있는 사람이 되었는지도 모르겠습니다.
그럼 이야기를 시작하겠습니다.

먼저 스레드(Thread)를 이야기하려 합니다.

스레드는 사용자가 제어할수 있는 가장 작은 단위의 리소스입니다.
스레드는 프로세스 내에서 독립적인 실행 흐름을 나타내며, 프로세스의 리소스를 공유합니다.
말로는 이해가 안될 수 있으니 한번 프로세스와 스레드를 보여드릴까 합니다.

```bash
[root@ip-172-31-37-46 ~]# ps afxuww | grep httpd root      2908  0.0  1.4 753824 14668 ?        Ss   Sep05   7:57 /usr/sbin/httpd -DFOREGROUND apache   24171  0.1  6.5 1121056 64932 ?       Sl   13:24   0:02  |- /usr/sbin/httpd -DFOREGROUND apache   24215  0.1  6.5 891616 65076 ?        Sl   13:24   0:02  |- /usr/sbin/httpd -DFOREGROUND apache   24226  0.1  6.1 891616 60412 ?        Sl   13:24   0:01  |- /usr/sbin/httpd -DFOREGROUND apache   24227  0.1  6.5 891616 64672 ?        Sl   13:24   0:01  |- /usr/sbin/httpd -DFOREGROUND apache   24298  0.1  6.0 891616 59792 ?        Sl   13:24   0:01  |- /usr/sbin/httpd -DFOREGROUND apache   24602  0.1  6.5 893756 64920 ?        Sl   13:38   0:00  |- /usr/sbin/httpd -DFOREGROUND apache   24603  0.1  5.9 815580 58600 ?        Sl   13:38   0:00  |- /usr/sbin/httpd -DFOREGROUND apache   24615  0.1  5.9 815836 58988 ?        Sl   13:38   0:00  |- /usr/sbin/httpd -DFOREGROUND apache   24640  0.1  6.2 815876 62040 ?        Sl   13:38   0:00  |- /usr/sbin/httpd -DFOREGROUND apache   24674  0.1  6.0 891360 59644 ?        Sl   13:38   0:00  |- /usr/sbin/httpd -DFOREGROUND
```

저의 시그니처 명령어인 ps afxuwww 를 이용하여 프로세스를 확인합니다.
ps afxuwww 명령어는 프로세스리스트를 모두 트리구조로 백그라운드 프로세스도 포함해서 유저 중심으로 넓게 보여주는 명령어립니다.

부모프로세스까지 합쳐서 12개의 프로세스가 구동중입니다. 그렇다면 이프로세스에는 몇개의 쓰레드가 있는지 확인해 봅시다.

```bash
ps -eLf | grep httpd root      2908     1  2908  0    1 Sep05 ?        00:07:57 /usr/sbin/httpd -DFOREGROUND apache   24215  2908 24215  0    6 13:24 ?        00:00:02 /usr/sbin/httpd -DFOREGROUND apache   24215  2908 24216  0    6 13:24 ?        00:00:00 /usr/sbin/httpd -DFOREGROUND apache   24215  2908 24217  0    6 13:24 ?        00:00:00 /usr/sbin/httpd -DFOREGROUND apache   24215  2908 24218  0    6 13:24 ?        00:00:00 /usr/sbin/httpd -DFOREGROUND apache   24215  2908 24219  0    6 13:24 ?        00:00:00 /usr/sbin/httpd -DFOREGROUND apache   24215  2908 24220  0    6 13:24 ?        00:00:00 /usr/sbin/httpd -DFOREGROUND apache   24226  2908 24226  0    6 13:24 ?        00:00:02 /usr/sbin/httpd -DFOREGROUND apache   24226  2908 24228  0    6 13:24 ?        00:00:00 /usr/sbin/httpd -DFOREGROUND apache   24226  2908 24229  0    6 13:24 ?        00:00:00 /usr/sbin/httpd -DFOREGROUND apache   24226  2908 24230  0    6 13:24 ?        00:00:00 /usr/sbin/httpd -DFOREGROUND apache   24226  2908 24231  0    6 13:24 ?        00:00:00 /usr/sbin/httpd -DFOREGROUND apache   24226  2908 24232  0    6 13:24 ?        00:00:00 /usr/sbin/httpd -DFOREGROUND apache   24298  2908 24298  0    6 13:24 ?        00:00:02 /usr/sbin/httpd -DFOREGROUND apache   24298  2908 24308  0    6 13:24 ?        00:00:00 /usr/sbin/httpd -DFOREGROUND apache   24298  2908 24309  0    6 13:24 ?        00:00:00 /usr/sbin/httpd -DFOREGROUND apache   24298  2908 24310  0    6 13:24 ?        00:00:00 /usr/sbin/httpd -DFOREGROUND apache   24298  2908 24311  0    6 13:24 ?        00:00:00 /usr/sbin/httpd -DFOREGROUND apache   24298  2908 24312  0    6 13:24 ?        00:00:00 /usr/sbin/httpd -DFOREGROUND apache   24602  2908 24602  0    6 13:38 ?        00:00:01 /usr/sbin/httpd -DFOREGROUND apache   24602  2908 24609  0    6 13:38 ?        00:00:00 /usr/sbin/httpd -DFOREGROUND apache   24602  2908 24610  0    6 13:38 ?        00:00:00 /usr/sbin/httpd -DFOREGROUND apache   24602  2908 24611  0    6 13:38 ?        00:00:00 /usr/sbin/httpd -DFOREGROUND apache   24602  2908 24612  0    6 13:38 ?        00:00:00 /usr/sbin/httpd -DFOREGROUND apache   24602  2908 24613  0    6 13:38 ?        00:00:00 /usr/sbin/httpd -DFOREGROUND apache   24603  2908 24603  0    6 13:38 ?        00:00:01 /usr/sbin/httpd -DFOREGROUND apache   24603  2908 24604  0    6 13:38 ?        00:00:00 /usr/sbin/httpd -DFOREGROUND apache   24603  2908 24605  0    6 13:38 ?        00:00:00 /usr/sbin/httpd -DFOREGROUND apache   24603  2908 24606  0    6 13:38 ?        00:00:00 /usr/sbin/httpd -DFOREGROUND apache   24603  2908 24607  0    6 13:38 ?        00:00:00 /usr/sbin/httpd -DFOREGROUND apache   24603  2908 24608  0    6 13:38 ?        00:00:00 /usr/sbin/httpd -DFOREGROUND apache   24615  2908 24615  0    6 13:38 ?        00:00:01 /usr/sbin/httpd -DFOREGROUND apache   24615  2908 24623  0    6 13:38 ?        00:00:00 /usr/sbin/httpd -DFOREGROUND apache   24615  2908 24624  0    6 13:38 ?        00:00:00 /usr/sbin/httpd -DFOREGROUND apache   24615  2908 24625  0    6 13:38 ?        00:00:00 /usr/sbin/httpd -DFOREGROUND apache   24615  2908 24626  0    6 13:38 ?        00:00:00 /usr/sbin/httpd -DFOREGROUND apache   24615  2908 24627  0    6 13:38 ?        00:00:00 /usr/sbin/httpd -DFOREGROUND apache   24640  2908 24640  0    6 13:38 ?        00:00:01 /usr/sbin/httpd -DFOREGROUND apache   24640  2908 24654  0    6 13:38 ?        00:00:00 /usr/sbin/httpd -DFOREGROUND apache   24640  2908 24655  0    6 13:38 ?        00:00:00 /usr/sbin/httpd -DFOREGROUND apache   24640  2908 24656  0    6 13:38 ?        00:00:00 /usr/sbin/httpd -DFOREGROUND apache   24640  2908 24657  0    6 13:38 ?        00:00:00 /usr/sbin/httpd -DFOREGROUND apache   24640  2908 24658  0    6 13:38 ?        00:00:00 /usr/sbin/httpd -DFOREGROUND apache   24674  2908 24674  0    6 13:38 ?        00:00:01 /usr/sbin/httpd -DFOREGROUND apache   24674  2908 24676  0    6 13:38 ?        00:00:00 /usr/sbin/httpd -DFOREGROUND apache   24674  2908 24677  0    6 13:38 ?        00:00:00 /usr/sbin/httpd -DFOREGROUND apache   24674  2908 24678  0    6 13:38 ?        00:00:00 /usr/sbin/httpd -DFOREGROUND apache   24674  2908 24679  0    6 13:38 ?        00:00:00 /usr/sbin/httpd -DFOREGROUND apache   24674  2908 24680  0    6 13:38 ?        00:00:00 /usr/sbin/httpd -DFOREGROUND apache   24783  2908 24783  0   22 13:47 ?        00:00:00 /usr/sbin/httpd -DFOREGROUND apache   24783  2908 24790  0   22 13:47 ?        00:00:00 /usr/sbin/httpd -DFOREGROUND apache   24783  2908 24791  0   22 13:47 ?        00:00:00 /usr/sbin/httpd -DFOREGROUND apache   24783  2908 24792  0   22 13:47 ?        00:00:00 /usr/sbin/httpd -DFOREGROUND apache   24783  2908 24793  0   22 13:47 ?        00:00:00 /usr/sbin/httpd -DFOREGROUND apache   24783  2908 24794  0   22 13:47 ?        00:00:00 /usr/sbin/httpd -DFOREGROUND apache   24783  2908 24821  0   22 13:47 ?        00:00:00 /usr/sbin/httpd -DFOREGROUND apache   24783  2908 24822  0   22 13:47 ?        00:00:00 /usr/sbin/httpd -DFOREGROUND apache   24783  2908 24823  0   22 13:47 ?        00:00:00 /usr/sbin/httpd -DFOREGROUND apache   24783  2908 24824  0   22 13:47 ?        00:00:00 /usr/sbin/httpd -DFOREGROUND apache   24783  2908 24825  0   22 13:47 ?        00:00:00 /usr/sbin/httpd -DFOREGROUND apache   24783  2908 24826  0   22 13:47 ?        00:00:00 /usr/sbin/httpd -DFOREGROUND apache   24783  2908 24827  0   22 13:47 ?        00:00:00 /usr/sbin/httpd -DFOREGROUND apache   24783  2908 24828  0   22 13:47 ?        00:00:00 /usr/sbin/httpd -DFOREGROUND apache   24783  2908 24829  0   22 13:47 ?        00:00:00 /usr/sbin/httpd -DFOREGROUND apache   24783  2908 24830  0   22 13:47 ?        00:00:00 /usr/sbin/httpd -DFOREGROUND apache   24783  2908 24831  0   22 13:47 ?        00:00:00 /usr/sbin/httpd -DFOREGROUND apache   24783  2908 24832  0   22 13:47 ?        00:00:00 /usr/sbin/httpd -DFOREGROUND apache   24783  2908 24833  0   22 13:47 ?        00:00:00 /usr/sbin/httpd -DFOREGROUND apache   24783  2908 24834  0   22 13:47 ?        00:00:00 /usr/sbin/httpd -DFOREGROUND apache   24783  2908 24835  0   22 13:47 ?        00:00:00 /usr/sbin/httpd -DFOREGROUND apache   24783  2908 24836  0   22 13:47 ?        00:00:00 /usr/sbin/httpd -DFOREGROUND apache   24798  2908 24798  0    6 13:47 ?        00:00:00 /usr/sbin/httpd -DFOREGROUND apache   24798  2908 24814  0    6 13:47 ?        00:00:00 /usr/sbin/httpd -DFOREGROUND apache   24798  2908 24815  0    6 13:47 ?        00:00:00 /usr/sbin/httpd -DFOREGROUND apache   24798  2908 24816  0    6 13:47 ?        00:00:00 /usr/sbin/httpd -DFOREGROUND apache   24798  2908 24817  0    6 13:47 ?        00:00:00 /usr/sbin/httpd -DFOREGROUND apache   24798  2908 24818  0    6 13:47 ?        00:00:00 /usr/sbin/httpd -DFOREGROUND
```

총 77개의 스레드가 확인됩니다. 앞서 말했던것과 같이 스레드는 프로세스의 자원을 공유하므로 pid 가 같으면 같은 프로세스의 스레드라 할수있습니다. 그렇다면 각 스레드의 프로세스 갯수를 확인해 보겠습니다.

```bash
ps -eLf | grep httpd | awk '{print $2}' | sort -n | uniq -c
      1 2908
      6 24215
      6 24226
      6 24298
      6 24602
      6 24603
      6 24615
      6 24640
      6 24674
     22 24783
      6 24798
      1 25189
```

ps -eLf 명령어는 중요한부분은 L 옵션입니다. 스레드를 출력하는 옵션입니다. 그다음 명령어는 httpd 스레드의 2번째 행만 발라낸뒤 숫자로 정렬하고 유니크 명령어로 각 카운트를 세었습니다. 뭔가 연관성이 보이지 않나요? 6번째 행에서 보여주는 값이 프로세스내 스레드 갯수입니다.

이렇게 하나의 프로세스는 여러개의 스레드를 가지고있는 것을 확인할수 있습니다.

그럼 시작하는 엔지니어의 글을 작성한다고 했던 제가 왜 스레드니 프로세스니 하는 이야기를 하고 있을까요?

프로세스는 오늘 할 이야기의 시작이자 끝이기 때문입니다.

프로세스의 정의는 실행 중인 프로그램의 인스턴스입니다. 이는 코드, 데이터, 스택, 힙과 같은 메모리 영역, 파일 디스크립터, 환경 설정 등을 포함합니다. 운영 체제에서 기본적인 실행 단위로, 시스템 자원과 작업을 관리하는 데 사용됩니다.

이 프로세스를 격리하는 메커니즘을 Namespace 라고 합니다. 네임스페이스는 리눅스에서 프로세스를 격리하는 메커니즘입니다. 각 네임스페이스는 특정 종류의 시스템 자원을 감싸고, 프로세스가 그 자원을 별도로 보도록 합니다. 예를 들어, 네트워크, 파일시스템 마운트 포인트, 사용자 ID 등이 있습니다.

마지막으로 Cgroup 는 프로세스 그룹의 시스템 자원 사용을 제한하고 격리하는 기능을 제공합니다. cgroups를 사용하면 CPU 시간, 시스템 메모리, 네트워크 대역폭 등의 자원을 제어할 수 있습니다. 시스템 자원의 공정한 분배 및 특정 프로세스 그룹의 자원 사용을 제한하여 시스템의 안정성을 보장하는 데 사용됩니다.

Namespace, Cgroup 이 둘은 함께 사용되어 프로세스의 격리 및 자원 관리를 향상시킵니다. 네임스페이스는 격리를 제공하고, Cgroup은 자원의 사용을 제한합니다. 이러한 조합은 효과적인 리소스 관리 및 격리된 환경을 제공하는 컨테이너 기술의 기반이 됩니다.

컨테이너는 가볍고, 이동이 쉬우며, 격리되고, 관리하기 편합니다.

컨테이너는 프로세스 입니다. 호스트 OS 내에서 앞서 보여드렸던, https 프로세스와 동일하다 보면 됩니다. 그러면 docker 에서 실행 중인 httpd 프로세스를 한번 확인해 보겠습니다.

```bash
root     25830  0.3  0.8 711892  8832 ?        Sl   14:22   0:00 /usr/bin/containerd-shim-runc-v2 -namespace moby -id 006385b1389ce918e596adf536fedbf68fcece03b9170cd898ccc70eb79a60d2 -address /run/containerd/containerd.sock root     25853  7.0  0.4   5860  4756 ?        Ss   14:22   0:00  |- httpd -DFOREGROUND 33       25882  0.0  0.3 807096  3720 ?        Sl   14:22   0:00      |- httpd -DFOREGROUND 33       25883  0.0  0.3 807096  3720 ?        Sl   14:22   0:00      |- httpd -DFOREGROUND 33       25884  0.0  0.3 807096  3720 ?        Sl   14:22   0:00      |- httpd -DFOREGROUND
```

Container Runtime (containerd-shim)이 실행한 httpd 컨테이너가 보입니다. 이렇게 보기엔 단순 프로세스 이지만 컨테이너가 실행한 httpd 프로세스 입니다.

앞서 보여드렸던 스레드도 비슷한 형태로 실행 중입니다.

```bash
ps -eLf | grep httpd root     25853 25830 25853  0    1 14:22 ?        00:00:00 httpd -DFOREGROUND 33       25882 25853 25882  0   27 14:22 ?        00:00:00 httpd -DFOREGROUND 33       25882 25853 25940  0   27 14:22 ?        00:00:00 httpd -DFOREGROUND 33       25882 25853 25941  0   27 14:22 ?        00:00:00 httpd -DFOREGROUND 33       25882 25853 25942  0   27 14:22 ?        00:00:00 httpd -DFOREGROUND 33       25882 25853 25943  0   27 14:22 ?        00:00:00 httpd -DFOREGROUND 33       25882 25853 25944  0   27 14:22 ?        00:00:00 httpd -DFOREGROUND 33       25882 25853 25945  0   27 14:22 ?        00:00:00 httpd -DFOREGROUND 33       25882 25853 25946  0   27 14:22 ?        00:00:00 httpd -DFOREGROUND 33       25882 25853 25947  0   27 14:22 ?        00:00:00 httpd -DFOREGROUND 33       25882 25853 25948  0   27 14:22 ?        00:00:00 httpd -DFOREGROUND 33       25882 25853 25949  0   27 14:22 ?        00:00:00 httpd -DFOREGROUND 33       25882 25853 25950  0   27 14:22 ?        00:00:00 httpd -DFOREGROUND 33       25882 25853 25951  0   27 14:22 ?        00:00:00 httpd -DFOREGROUND 33       25882 25853 25952  0   27 14:22 ?        00:00:00 httpd -DFOREGROUND 33       25882 25853 25953  0   27 14:22 ?        00:00:00 httpd -DFOREGROUND 33       25882 25853 25954  0   27 14:22 ?        00:00:00 httpd -DFOREGROUND 33       25882 25853 25955  0   27 14:22 ?        00:00:00 httpd -DFOREGROUND 33       25882 25853 25956  0   27 14:22 ?        00:00:00 httpd -DFOREGROUND 33       25882 25853 25957  0   27 14:22 ?        00:00:00 httpd -DFOREGROUND 33       25882 25853 25958  0   27 14:22 ?        00:00:00 httpd -DFOREGROUND 33       25882 25853 25959  0   27 14:22 ?        00:00:00 httpd -DFOREGROUND 33       25882 25853 25960  0   27 14:22 ?        00:00:00 httpd -DFOREGROUND 33       25882 25853 25961  0   27 14:22 ?        00:00:00 httpd -DFOREGROUND 33       25882 25853 25962  0   27 14:22 ?        00:00:00 httpd -DFOREGROUND 33       25882 25853 25963  0   27 14:22 ?        00:00:00 httpd -DFOREGROUND 33       25882 25853 25964  0   27 14:22 ?        00:00:00 httpd -DFOREGROUND 33       25882 25853 25965  0   27 14:22 ?        00:00:00 httpd -DFOREGROUND 33       25883 25853 25883  0   27 14:22 ?        00:00:00 httpd -DFOREGROUND 33       25883 25853 25914  0   27 14:22 ?        00:00:00 httpd -DFOREGROUND 33       25883 25853 25915  0   27 14:22 ?        00:00:00 httpd -DFOREGROUND 33       25883 25853 25916  0   27 14:22 ?        00:00:00 httpd -DFOREGROUND 33       25883 25853 25917  0   27 14:22 ?        00:00:00 httpd -DFOREGROUND 33       25883 25853 25918  0   27 14:22 ?        00:00:00 httpd -DFOREGROUND 33       25883 25853 25919  0   27 14:22 ?        00:00:00 httpd -DFOREGROUND 33       25883 25853 25920  0   27 14:22 ?        00:00:00 httpd -DFOREGROUND 33       25883 25853 25921  0   27 14:22 ?        00:00:00 httpd -DFOREGROUND 33       25883 25853 25922  0   27 14:22 ?        00:00:00 httpd -DFOREGROUND 33       25883 25853 25923  0   27 14:22 ?        00:00:00 httpd -DFOREGROUND 33       25883 25853 25924  0   27 14:22 ?        00:00:00 httpd -DFOREGROUND 33       25883 25853 25925  0   27 14:22 ?        00:00:00 httpd -DFOREGROUND 33       25883 25853 25926  0   27 14:22 ?        00:00:00 httpd -DFOREGROUND 33       25883 25853 25927  0   27 14:22 ?        00:00:00 httpd -DFOREGROUND 33       25883 25853 25928  0   27 14:22 ?        00:00:00 httpd -DFOREGROUND 33       25883 25853 25929  0   27 14:22 ?        00:00:00 httpd -DFOREGROUND 33       25883 25853 25930  0   27 14:22 ?        00:00:00 httpd -DFOREGROUND 33       25883 25853 25931  0   27 14:22 ?        00:00:00 httpd -DFOREGROUND 33       25883 25853 25932  0   27 14:22 ?        00:00:00 httpd -DFOREGROUND 33       25883 25853 25933  0   27 14:22 ?        00:00:00 httpd -DFOREGROUND 33       25883 25853 25934  0   27 14:22 ?        00:00:00 httpd -DFOREGROUND 33       25883 25853 25935  0   27 14:22 ?        00:00:00 httpd -DFOREGROUND 33       25883 25853 25936  0   27 14:22 ?        00:00:00 httpd -DFOREGROUND 33       25883 25853 25937  0   27 14:22 ?        00:00:00 httpd -DFOREGROUND 33       25883 25853 25938  0   27 14:22 ?        00:00:00 httpd -DFOREGROUND 33       25883 25853 25939  0   27 14:22 ?        00:00:00 httpd -DFOREGROUND 33       25884 25853 25884  0   27 14:22 ?        00:00:00 httpd -DFOREGROUND 33       25884 25853 25887  0   27 14:22 ?        00:00:00 httpd -DFOREGROUND 33       25884 25853 25888  0   27 14:22 ?        00:00:00 httpd -DFOREGROUND 33       25884 25853 25889  0   27 14:22 ?        00:00:00 httpd -DFOREGROUND 33       25884 25853 25890  0   27 14:22 ?        00:00:00 httpd -DFOREGROUND 33       25884 25853 25891  0   27 14:22 ?        00:00:00 httpd -DFOREGROUND 33       25884 25853 25892  0   27 14:22 ?        00:00:00 httpd -DFOREGROUND 33       25884 25853 25893  0   27 14:22 ?        00:00:00 httpd -DFOREGROUND 33       25884 25853 25894  0   27 14:22 ?        00:00:00 httpd -DFOREGROUND 33       25884 25853 25895  0   27 14:22 ?        00:00:00 httpd -DFOREGROUND 33       25884 25853 25896  0   27 14:22 ?        00:00:00 httpd -DFOREGROUND 33       25884 25853 25897  0   27 14:22 ?        00:00:00 httpd -DFOREGROUND 33       25884 25853 25898  0   27 14:22 ?        00:00:00 httpd -DFOREGROUND 33       25884 25853 25899  0   27 14:22 ?        00:00:00 httpd -DFOREGROUND 33       25884 25853 25900  0   27 14:22 ?        00:00:00 httpd -DFOREGROUND 33       25884 25853 25901  0   27 14:22 ?        00:00:00 httpd -DFOREGROUND 33       25884 25853 25902  0   27 14:22 ?        00:00:00 httpd -DFOREGROUND 33       25884 25853 25903  0   27 14:22 ?        00:00:00 httpd -DFOREGROUND 33       25884 25853 25904  0   27 14:22 ?        00:00:00 httpd -DFOREGROUND 33       25884 25853 25905  0   27 14:22 ?        00:00:00 httpd -DFOREGROUND 33       25884 25853 25906  0   27 14:22 ?        00:00:00 httpd -DFOREGROUND 33       25884 25853 25907  0   27 14:22 ?        00:00:00 httpd -DFOREGROUND 33       25884 25853 25908  0   27 14:22 ?        00:00:00 httpd -DFOREGROUND 33       25884 25853 25909  0   27 14:22 ?        00:00:00 httpd -DFOREGROUND 33       25884 25853 25910  0   27 14:22 ?        00:00:00 httpd -DFOREGROUND 33       25884 25853 25911  0   27 14:22 ?        00:00:00 httpd -DFOREGROUND 33       25884 25853 25912  0   27 14:22 ?        00:00:00 httpd -DFOREGROUND
```

이과정에서 컨테이너는 프로세스다 라는 개념을 확실하게 알았을 것이라 생각합니다.

그럼 이제 이 컨테이너의 사용을 확장해 봅시다.

```bash
docker ps CONTAINER ID   IMAGE     COMMAND              CREATED         STATUS         PORTS     NAMES 927717d2d026   httpd     "httpd-foreground"   4 seconds ago   Up 3 seconds   80/tcp    stupefied_gagarin 182ddd3df992   httpd     "httpd-foreground"   5 seconds ago   Up 4 seconds   80/tcp    relaxed_lovelace 4d50ad075f73   httpd     "httpd-foreground"   6 seconds ago   Up 5 seconds   80/tcp    upbeat_goldwasser cfb8c7c071b0   httpd     "httpd-foreground"   8 seconds ago   Up 7 seconds   80/tcp    crazy_chandrasekhar
```

```bash
root     26254  0.0  0.9 712212  9312 ?        Sl   14:29   0:00 /usr/bin/containerd-shim-runc-v2 -namespace moby -id cfb8c7c071b06dba1e760939d07649fd1e37a23df917c50002657ca04e0c3e9b -address /run/containerd/containerd.sock root     26276  0.7  0.4   5860  4700 ?        Ss   14:29   0:00  |- httpd -DFOREGROUND 33       26305  0.0  0.3 807096  3664 ?        Sl   14:29   0:00      |- httpd -DFOREGROUND 33       26306  0.0  0.3 807096  3664 ?        Sl   14:29   0:00      |- httpd -DFOREGROUND 33       26307  0.0  0.3 807096  3664 ?        Sl   14:29   0:00      |- httpd -DFOREGROUND root     26408  0.0  0.9 711892  9524 ?        Sl   14:29   0:00 /usr/bin/containerd-shim-runc-v2 -namespace moby -id 4d50ad075f73631dfc8ae7c25130ef309857a0d4d300176f4571c5dd19fe1e9b -address /run/containerd/containerd.sock root     26430  0.7  0.4   5860  4636 ?        Ss   14:29   0:00  |- httpd -DFOREGROUND 33       26458  0.0  0.3 807096  3792 ?        Sl   14:29   0:00      |- httpd -DFOREGROUND 33       26459  0.0  0.3 807096  3788 ?        Sl   14:29   0:00      |- httpd -DFOREGROUND 33       26460  0.0  0.3 807096  3792 ?        Sl   14:29   0:00      |- httpd -DFOREGROUND root     26561  0.0  0.8 711892  8872 ?        Sl   14:29   0:00 /usr/bin/containerd-shim-runc-v2 -namespace moby -id 182ddd3df992943a4f94d8455d5f535a66c6891b7151d5c1d60409f8085c8cc5 -address /run/containerd/containerd.sock root     26584  0.7  0.4   5860  4644 ?        Ss   14:29   0:00  |- httpd -DFOREGROUND 33       26612  0.0  0.3 807096  3780 ?        Sl   14:29   0:00      |- httpd -DFOREGROUND 33       26613  0.0  0.3 807096  3780 ?        Sl   14:29   0:00      |- httpd -DFOREGROUND 33       26614  0.0  0.3 807096  3780 ?        Sl   14:29   0:00      |- httpd -DFOREGROUND root     26715  0.0  0.8 712148  8640 ?        Sl   14:29   0:00 /usr/bin/containerd-shim-runc-v2 -namespace moby -id 927717d2d02634bc6d4a31913356a2cb4aa08315ac1ed81e53d96861c46d816c -address /run/containerd/containerd.sock root     26738  0.7  0.4   5860  4812 ?        Ss   14:29   0:00  |- httpd -DFOREGROUND 33       26767  0.0  0.3 807096  3696 ?        Sl   14:29   0:00      |- httpd -DFOREGROUND 33       26768  0.0  0.3 807096  3696 ?        Sl   14:29   0:00      |- httpd -DFOREGROUND 33       26769  0.0  0.3 807096  3696 ?        Sl   14:29   0:00      |- httpd -DFOREGROUND
```

4개의 컨테이너가 구동중이고, 각자 격리된 형태입니다. 자원만 충분하다면 컨테이너를 ulimit 에 설정된 openfile 이 받아주는 한계에서 굉장히 많은 컨테이너를 실행할수 있습니다. 컨테이너 네트워크또한 호스트와 분리한다면 더욱더 많은 컨테이너를 실행할수 있습니다.

이러한 컨테이너의 형태는 우리 엔지니어들이 입이 마르고 닳도록 말하는 kubernetes 와 연결되어있습니다.

N+1개로 이루어진 Pod는 Node에 스케줄링됩니다. 위에서 예제로 보인 4개의 컨테이너의 실행은 네번이나 run 커멘드를 실행해야 하므로 아주 귀찮습니다. Kubernetes 에서 100개의 컨테이너를 생성하는 방법은 아래와 같습니다.

```bash
apiVersion: apps/v1 kind: Deployment metadata:
  name: httpd-deployment spec:
  replicas: 100
  selector:
    matchLabels:
      app: httpd
  template:
    metadata:
      labels:
        app: httpd
    spec:
      containers:

      - name: httpd
        image: httpd:latest
        ports:

        - containerPort: 80
```

이 매니패스트를 **kubectl apply -f httpd-deployment.yaml** 명령어로 실행만 하면 100개의 pod가 실행됩니다.

이제 로드벨런싱을 이야기해야 할듯한데 사실 이부분도 쿠버네티스의 오브젝트들이 적절히 잘 만들어져 있기에 간단히 할수 있습니다.

```bash
apiVersion: v1 kind: Service metadata:
  name: httpd-loadbalancer spec:
  selector:
    app: httpd
  ports:

    - protocol: TCP
      port: 80
      targetPort: 80
  type: LoadBalancer
```

이러한 형태로 선언만 하면 이제 끝입니다. 이런 방법으로 우리는 httpd Container를 쉽게 만들수 있습니다. 그럼 프로세스에 이어서 바로 쿠버네티스로 넘어왔는데, 뭔가 빠져있다 생각하지 않나요? 바로 노드입니다. 쿠버네티스는 컨테이너 오케스트레이션이라 불립니다. 연결된 Node에 API를 이용하여 애플리케이션과 서비스를 구성하고 관리하고 조정합니다.

드디어 오늘의 이야기의 핵심에 다가가고 있습니다.

쿠버네티스는 결국 리눅스에 설치됩니다.

우리는 Pod와 Service 오브젝트는 간단히 다룰수있지만 추상화의 너머에 있는 Kubernetes의 프로세스와 노드에서 돌고있는 Kubelet 에 대해선 간단히 다룰수 없습니다.

![](/images/2023/12/image-1-1024x490.png)

POD/ Service / Deployment

![](/images/2023/12/image-2-1024x477.png)

Control Plane (쿠버네티스 컴포넌트)

추상화된 그 너머는 파악하기도 쉽지 않습니다.

<https://kubernetes.io/ko/docs/concepts/overview/components/>

우리는 다양한 것들이 추상화되어있는 시대를 살고있습니다. 그래서 그 심연을 들여다 보면 멘탈이 날아가는 일이 비일비재 합니다. 이러한 일들에 내성을 가지고 이겨내기위해선 결국엔 기본능력이 오르는 수밖에 없습니다.

기본능력이라 함은 리눅스 입니다.

항상 리눅스를 잘하려면 어떻게 해야하나요? 라는 질문을 듣습니다. 리눅서로서 사실 죄송한 말이지만 리눅스를 잘하는 기준은 어디에도 없고 리눅스 서버운영에는 많은 명령어가 필요하지 않습니다. 대부분 10개이내의 명령어를 사용합니다. 하지만 대부분의 일은 그 명령어들 내에서 처리됩니다.

그렇다면 리눅스를 잘하려면 어떻게 해야하냐? 결국엔 다양한 명령어들을 경험하고 손에 익어서 문제가 발생한 시점에 그 명령어를 사용해서 시스템을 점검하는것이 리눅스를 잘하는 것입니다.

저 같은 경우엔 처음보는 시스템도 30분이면 대부분 파악이 됩니다.

그 힘은 다양한 리눅스 환경에서 헤멘탓이 큽니다.
디렉토리 구조 패키지형태 명령어 스타일 배포판 마다 조금씩 다릅니다. 이런경우 저는 레드헷 계열 리눅스를 편하게 쓰지만 처음 보는 리눅스라 해서 어려워하지 않습니다. 이유는 간단합니다.

리눅스는 프로세스를 볼수 있습니다.

앞서서 이야기한 ps 명령어가 그러합니다 ps 명령어는 실행중인 프로세스를 면밀히 관찰할수 있게하고, 실행한 프로세스의 위치 ,구조, 사용중인 자원들을 볼수 있게 합니다.

시스템의 대부분의 힌트는 프로세스 리스트에 있습니다.

시작하는 엔지니어라면 리눅스의 구조 동작을 먼저 공부하시고 그 다음엔 명령어 프로세스 동작 그리고 간단한 스크립트도 짜보는것을 추천합니다. 또한 리눅스에선 다양한 명령어 들이 있습니다. 지금 이순간에도 누군가가 리눅스의 명령어를 만들고 있을 것입니다. 자신만의 명령어를 만들어도 좋습니다. 리눅스에 익숙해지고 많이 두드려 보세요.

손가락에 익은 명령어는 시스템을 배신하지 않습니다.

~~사실 가끔 합니다 (rm -rf \*) 과 같은..누구나 하는 실수입니다.(저는안했습니다.)~~

기승전리눅스를 이야기하게 되었네요.

하지만 리눅스는 현대의 IT를 이끌고있는 근간이고 대부분의 시스템이 리눅스에서 구동된다는 사실을 안다면 근본인 리눅스를 하지 않을수 없다 생각합니다.

이제 제가 하려던 이야기를 다풀어 낸것 같습니다.

오늘도 읽어주셔서 감사합니다.

**좋은밤 되시라!**
