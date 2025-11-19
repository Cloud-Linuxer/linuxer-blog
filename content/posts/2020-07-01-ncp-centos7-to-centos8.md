---
title: "NCP-CentOS7-to-CentOS8"
date: 2020-07-01T15:55:43+09:00
draft: false
categories: ["Linux", "NCP"]
tags: ["ncp", "centos7-8", "centos8", "dnf", "upgrade"]
slug: "ncp-centos7-to-centos8"
aliases:
  - /ncp-centos7-to-centos8/
  - /ncp-centos7-to-centos8/
---

\n

NCP 에선 centos8을 지원하지 않는다. 그런데 yum update 를 해서 커널이 변경되면 정상적으로 부팅되지 않는다.

\n\n\n\n

![](/images/2020/07/image.png)

\n\n\n\n

![](/images/2020/07/image-1.png)

\n\n\n\n

이런 내용들이 인스턴스를 생성할때 안내된다.

\n\n\n\n

그런데, 어제 퇴근후 Meetup과정에서 KR-2 zone은 yum update 가 가능하다는 내용을 전달 받았다. 어쩐지 가끔 yum update 해도 정상적으로 부팅되는 인스턴스가 있더라니..

\n\n\n\n

[퇴근길 Meetup](https://www.facebook.com/download/305343453973867/%5B%ED%87%B4%EA%B7%BC%EA%B8%B8%20TECH%20MEETUP%5D%EC%84%9C%EB%B2%84%20%EA%B4%80%EB%A6%AC%20%EC%9E%90%EB%8F%99%ED%99%94%20%EC%8B%A4%EC%8A%B5.pdf?av=100001902490507&eav=AfbyIBla8RPDS-_AL-wtUsGl8Qwot0fM0rB4V4w3eqon3d6sDveqfyC_5QS-f9Vsl60&hash=AcoieWQQqGEJKD29) - 퇴근길 Tech Meetup 서버 관리 자동화 자료이다.

\n\n\n\n

여기에서 이상함을 느끼고 여쭤봤더니 KR-2에서 하라고 하셨다..그래서 오늘작업의 힌트를 얻었다...

\n\n\n\n

최신의 OS 를 사용하고 싶은건 엔지니어의 본능이 아닌가? 그래서 테스트를 시작했다.

\n\n\n\n

\nhttps://www.tecmint.com/upgrade-centos-7-to-centos-8/\n

\n\n\n\n

준비물은 다음과 같다.

\n\n\n\n

![](/images/2020/07/image-2.png)

\n\n\n\n

서버이미지 centos 7.3으로 생성된 인스턴스 한대다.

\n\n\n\n

ACG-포트포워딩-root password 확인 이런 부분은 서버생성 가이드를 참고하자.

\n\n\n\n

<https://docs.ncloud.com/ko/compute/compute-1-1-v2.html>

\n\n\n\n\n\n\n\n

인스턴스를 생성하고 인스턴스에 접속하자 마자 할일은 yum update 이다.

\n\n\n\n

yum update -y

\n\n\n\n

업데이트를 마무리하면 epel repo를 설치해 사용할 수 있다.

\n\n\n\n

yum install epel-release -y

\n\n\n\n

epel을 설치하는 이유는 dnf 를 사용하기 위함이다. yum->dnf 로 패키지 설치 방법을 변경할거다.

\n\n\n\n

**yum install -y yum-utils rpmconf   
rpmconf -a**

\n\n\n\n

rpmconf -a 를 입력하면 패키지의 conf를 업데이트 할지를 물어본다.

\n\n\n\n
![](/images/2020/07/image-3.png)
\n\n\n\n

/etc/sysctl.conf   
/etc/profile  
/etc/shells  
/etc/login.defs  
/etc/nsswitch.conf  
다섯개의 파일에 대해서 물어보는데 나는 모두 새로 인스톨하는것을 택했다. centos8 로 갈꺼니까.

\n\n\n\n

package-cleanup --leaves  
package-cleanup --orphans

\n\n\n\n

다음은 패키지를 cleanup 하고, epel 을 설치한 이유인 dnf 를 설치한다.

\n\n\n\n

yum install dnf -y

\n\n\n\n

dnf 는 centos8 부터 기본적용된 rpm 패키지 관리 패키지인데 yum 에서 dnf로 변경됬다.   
dnf 를 설치했다면 yum 을 지우자.

\n\n\n\n

dnf -y remove yum yum-metadata-parser  
rm -Rf /etc/yum

\n\n\n\n

yum 을 지우고,

\n\n\n\n

dnf install -y http://mirror.centos.org/centos/8/BaseOS/x86\_64/os/Packages/centos-repos-8.2-2.2004.0.1.el8.x86\_64.rpm http://mirror.centos.org/centos/8/BaseOS/x86\_64/os/Packages/centos-release-8.2-2.2004.0.1.el8.x86\_64.rpm http://mirror.centos.org/centos/8/BaseOS/x86\_64/os/Packages/centos-gpg-keys-8.2-2.2004.0.1.el8.noarch.rpm

\n\n\n\n

이제 centos8의 repo를 설치한다.

\n\n\n\n

dnf -y upgrade https://dl.fedoraproject.org/pub/epel/epel-release-latest-8.noarch.rpm

\n\n\n\n

epel7 을 epel8로 업데이트 한다. 이제 centos8 패키지를 다운받을 수 있다.

\n\n\n\n

dnf clean all

\n\n\n\n

dnf 캐시를 clean 한다.

\n\n\n\n

rpm -e `rpm -q kernel`   
rpm -e --nodeps sysvinit-tools

\n\n\n\n

rpm 명령어로 커널을 지운다. 여기서 모든 패키지가 삭제되지 않기때문에 후처리가 좀 필요하다.

\n\n\n\n

dnf remove kernel-devel-3.10.0-1127.13.1.el7.x86\_64 kernel-devel-3.10.0-327.22.2.el7.x86\_64 kernel-devel-3.10.0-514.2.2.el7.x86\_64 redhat-rpm-config iprutils-2.4.17.1-3.el7\_7.x86\_64 sysvinit-tools-2.88-14.dsf.el7.x86\_64 sysvinit-tools-2.88-14.dsf.el7.x86\_64 python36-rpmconf-1.0.22-1.el7.noarch

\n\n\n\n

후에 의존성이 걸릴 패키지를 미리 삭제한다. 이 경우 NCP centos7.3 인스턴스에 맞춰서 의존성 패키지를 삭제한것이다. 의존성 문제가 발생하면 더삭제 해줘야 한다. 부담감 느끼지 말고 막 날리자. 안되면 처음부터 다시하면 된다.

\n\n\n\n

dnf -y --releasever=8 --allowerasing --setopt=deltarpm=false distro-sync

\n\n\n\n

명령어로 centos8 패키지를 설치한다. 새로 설치되는 패키지들을 유심히 보면 el8.x86\_64 로 끝난다 centos8 사용하는 패키지 명으로 RHEL8 이라는 뜻이다. centos8 패키지가 잘설치된다는 소리다.

\n\n\n\n

Complete!

\n\n\n\n

이 단어가 보이면 거의 다된거다.

\n\n\n\n

dnf -y install kernel-core  
dnf -y groupupdate "Core" "Minimal Install"

\n\n\n\n

dnf groupupdate 로 Core 와 Minimal Install 까지 업데이트 해주면 이제 된거다.

\n\n\n\n

[root@s17308f26023 ~]# uname -a  
Linux s17308f26023 3.10.0-514.2.2.el7.x86\_64 #1 SMP Tue Dec 6 23:06:41 UTC 2016 x86\_64 x86\_64 x86\_64 GNU/Linux  
[root@s17308f26023 ~]# cat /etc/redhat-release  
CentOS Linux release 8.2.2004 (Core)

\n\n\n\n

리부팅을 아직 안해서 릴리즈는 올라갔으나, 커널버전은 centos7 이다. 이제 리부팅 해주자.

\n\n\n\n

[root@s17308f26023 ~]# date  
Wed Jul 1 15:50:15 KST 2020  
[root@s17308f26023 ~]# cat /etc/redhat-release  
CentOS Linux release 8.2.2004 (Core)  
[root@s17308f26023 ~]# uname -a  
Linux s17308f26023 4.18.0-193.6.3.el8\_2.x86\_64 #1 SMP Wed Jun 10 11:09:32 UTC 2020 x86\_64 x86\_64 x86\_64 GNU/Linux

\n\n\n\n

이제 NCP에서 Centos8을 올렸다!

\n\n\n\n\n\n\n\n

차후 커널지원이나 업데이트에 따라서 OS가 정상작동하지 않을수 있다. 모니터링이 문제가 될거라 생각했는데 잘돈다...

\n\n\n\n

![](/images/2020/07/image-4-1024x483.png)

\n\n\n\n

Centos8을 NCP에서 사용하고 싶다면 한번 진행해 보시기 바란다.

\n\n\n\n\n\n\n\n

읽어 주셔서 감사하다!

\n