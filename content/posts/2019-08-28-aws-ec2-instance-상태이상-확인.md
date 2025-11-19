---
title: "aws ec2 instance 상태이상 확인"
date: 2019-08-28T13:11:55+09:00
draft: false
categories: ["AWS", "Linux"]
tags: ["aws ec2", "ec2", "상태검사", "memory"]
slug: "aws-ec2-instance-상태이상-확인"
aliases:
  - /aws-ec2-instance-상태이상-확인/
  - /aws-ec2-instance-%ec%83%81%ed%83%9c%ec%9d%b4%ec%83%81-%ed%99%95%ec%9d%b8/
---

\n
![](/images/2019/08/IMG\_6201-1024x221.jpg)
\n\n\n\n

갑자기 블로그가 안열렸다. 따로 모니터링을 설정한건 아니라서 다운된지 몰랐다. 먼저 aws console 에서 인스턴스의 상태를 확인해 보기로 했다.

\n\n\n\n
![](/images/2019/08/Screenshot-2019-08-28-at-12.35.31.jpg)
\n\n\n\n

상태검사를 통과 하지못한 인스턴스가 확인된다. 이럴땐 ec2 상태검사 탭을 확인한다.

\n\n\n\n\n\n\n\n
![](/images/2019/08/Screenshot-2019-08-28-at-12.35.09.jpg)
\n\n\n\n

서버가 죽은지 벌써10시간째. 모니터링을 설정해 놨어야 했는데 불찰이 느껴진다. 일 단 트러블 슈팅을 시작한다.

\n\n\n\n

첫번째로 로그인을 진행해 본다. ssm 세션매니저를 통해서 접속해본다.

\n\n\n\n
![](/images/2019/08/Screenshot-2019-08-28-at-12.36.38.jpg)
\n\n\n\n

응. 안돼. 돌아가  
접속할수 없다.

\n\n\n\n

그럼 차선책으로 인스턴스의 스크린샷을 확인해 본다.

\n\n\n\n
![](/images/2019/08/Screenshot-2019-08-28-at-12.37.02.jpg)
\n\n\n\n

인스턴스 설정에서 시스템로그 가져오기는 dmesg 를 보여준다 그래서 이경우에 필요가 없다. 인스턴스가 행이 아니라 리부팅중 멈추거나 인스턴스 부팅 장애의 경우에는 시스템 로그가져오기로 봐야한다.

\n\n\n\n
![](/images/2019/08/Screenshot-2019-08-28-at-12.37.47.jpg)
\n\n\n\n

메모리...메ㅗㅁㅣㄹ............!!!!!!!!!!!!!!

\n\n\n\n

프리티어라 죽었다.

\n\n\n\n

재시작은 안되고 인스턴스를 중지한다. 재시작이 안될경우 중지/시작을 해야한다.

\n\n\n\n

EIP 가 연결되지 않은 인스턴스의 경우엔 IP가 변경된다 EIP를 붙여서 사용하자

\n\n\n\n\n\n\n\n
![](/images/2019/08/Screenshot-2019-08-28-at-12.42.45.jpg)
\n\n\n\n

중지중이다.  
중지중에 모니터링 그래프를 확인해 본다.

\n\n\n\n
![](/images/2019/08/Screenshot-2019-08-28-at-12.43.45.jpg)
\n\n\n\n

며칠전 포스팅했던 cloudwatch 를 이용한 메모리와 하드디스크 체크이다.  
메모리가 훅 날라간게 보인다.

\n\n\n\n
![](/images/2019/08/Screenshot-2019-08-28-at-12.46.08.jpg)
\n\n\n\n

리부팅 완료하고 인스턴스의 상태가 정상으로 변경되었다. 그렇다면 정확한 이유를 알아야한다.

\n\n\n\n\n\n\n\n
![](/images/2019/08/Screenshot-2019-08-28-at-12.48.04-1024x202.jpg)
\n\n\n\n

messages 로그에서 확인한 내용이다 스왑도 없고 메모리도 없어서 죽었다.  
사실 프리티어라 swap 이 없다. 이후에 파일스왑으로 2G정도 만들어줄계획이다.

\n\n\n\n

Aug 27 21:19:51 ip-10-0-0-12 kernel: active\_anon:214310 inactive\_anon:7454 isolated\_anon:0#012 active\_file:326 inactive\_file:360 isolated\_file:0#012 unevictable:0 dirty:0 writeback:0 unstable:0#012 slab\_reclaimable:3331 slab\_unreclaimable:5159#012 mapped:7669 shmem:7487 pagetables:3235 bounce:0#012 free:12190 free\_pcp:180 free\_cma:0  
\nAug 27 21:19:51 ip-10-0-0-12 kernel: Node 0 active\_anon:857240kB inactive\_anon:29816kB active\_file:1304kB inactive\_file:1440kB unevictable:0kB isolated(anon):0kB isolated(file):0kB mapped:30676kB dirty:0kB writeback:0kB shmem:29948kB shmem\_thp: 0kB shmem\_pmdmapped: 0kB anon\_thp: 0kB writeback\_tmp:0kB unstable:0kB all\_unreclaimable? no  
\nAug 27 21:19:51 ip-10-0-0-12 kernel: Node 0 DMA free:4464kB min:736kB low:920kB high:1104kB active\_anon:11168kB inactive\_anon:44kB active\_file:0kB inactive\_file:0kB unevictable:0kB writepending:0kB present:15988kB managed:15904kB mlocked:0kB kernel\_stack:0kB pagetables:32kB bounce:0kB free\_pcp:0kB local\_pcp:0kB free\_cma:0kBAug 27 21:19:51 ip-10-0-0-12 kernel: lowmem\_reserve[]: 0 932 932 932  
\nAug 27 21:19:51 ip-10-0-0-12 kernel: Node 0 DMA32 free:44296kB min:44316kB low:55392kB high:66468kB active\_anon:846072kB inactive\_anon:29772kB active\_file:1304kB inactive\_file:1440kB unevictable:0kB writepending:0kB present:1032192kB managed:991428kB mlocked:0kB kernel\_stack:6352kB pagetables:12908kB bounce:0kB free\_pcp:720kB local\_pcp:720kB free\_cma:0kB  
\nAug 27 21:19:51 ip-10-0-0-12 kernel: lowmem\_reserve[]: 0 0 0 0  
\nAug 27 21:19:51 ip-10-0-0-12 kernel: Node 0 DMA: 84kB (UME) 88kB (UME) 1116kB (UE) 932kB (UE) 964kB (UME) 4128kB (UE) 5256kB (UME) 1512kB (E) 11024kB (E) 02048kB 04096kB = 4464kBAug 27 21:19:51 ip-10-0-0-12 kernel: Node 0 DMA32: 10224kB (UE) 4008kB (UE) 24116kB (UME) 13832kB (UME) 14364kB (UME) 61128kB (UE) 12256kB (ME) 13512kB (UE) 21024kB (UM) 02048kB 04096kB = 44296kB  
\nAug 27 21:19:51 ip-10-0-0-12 kernel: Node 0 hugepages\_total=0 hugepages\_free=0 hugepages\_surp=0 hugepages\_size=2048kB

\n\n\n\n

그럼 왜 스왑도 메모리도 없었을까? 웹서버 이므로 웹로그를 확인해 보았다.

\n\n\n\n
![](/images/2019/08/Screenshot-2019-08-28-at-12.50.42-1024x161.jpg)
\n\n\n\n

어제 급하게 포스팅하느라 업로드한 파일들을 재대로 처리못하고 죽은거다.

\n\n\n\n

아놔~~~~~~~~~~~~

\n\n\n\n

이후로 모니터링 체크하나 만들어서 알럿하도록 설정하는 포스팅을 작성하겠다.

\n\n\n\n

좋은하루 되시라!

\n\n\n\n

* ![](/images/2019/08/IMG\_6202-576x1024.png)
\n\n\n\n

사이트는 잘열리는것을 확인할수 있었다!

\n