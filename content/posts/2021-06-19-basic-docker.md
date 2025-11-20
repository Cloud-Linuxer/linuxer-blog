---
title: "Basic-Docker"
date: 2021-06-19T01:00:21+09:00
draft: false
categories: ["Linux"]
slug: "basic-docker"
aliases:
  - /basic-docker/
  - /basic-docker/
---


오랜만의 블로깅이다.

오랜만에 글을 쓰는것은 Docker 다.

간단히 도커 설치부터 이야기를 해보겠다. 나는 Redhat 계열의 리눅스를 좋아하므로 Centos7 로 진행하려 한다.

yum 으로 도커를 설치할건데, 몇가지를 선택해야 한다.

도커를 제공하는 레포는 여러가지가 있는데, 나는 Centos 의 Extra repo를 좋아한다. 다른레포를 사용하지 않고 그냥 바로 설치 할수 있기 때문이다.

<https://docs.docker.com/engine/install/centos/>

다음 URL을 참고하자.

물론 최신버전과는 거리가 좀 많다. Extra repo 는 1.13버전을 제공하며, 현재 Docker-ce repo에서 제공하는 버전은 1.20다.

Docker를 사용하기 위해선 6개의 패키지가 필요하다.

```
[root@linuxer ~ ]# yum install -y docker
(1/6): container-selinux-2.119.2-1.911c772.el7_8.noarch.rpm
|  40 kB  00:00:00
(2/6): container-storage-setup-0.11.0-2.git5eaf76c.el7.noarch.rpm
|  35 kB  00:00:00
(3/6): containers-common-0.1.40-11.el7_8.x86_64.rpm
|  43 kB  00:00:00
(4/6): docker-client-1.13.1-162.git64e9980.el7.centos.x86_64.rpm
| 3.9 MB  00:00:00
(5/6): docker-common-1.13.1-162.git64e9980.el7.centos.x86_64.rpm
|  99 kB  00:00:00
(6/6): docker-1.13.1-162.git64e9980.el7.centos.x86_64.rpm
|  18 MB  00:00:00

```

docker 만 설치해도 의존성으로 도커를 사용하기위한 패키지를 설치해준다.
아이러니 하게 yum remove docker 로 삭제하면 docker는 그냥혼자 지워진다. 설치할땐 패거리로 오고 갈땐 혼자간다. 구버전이라 패키지 네이밍도 좀 올드 하다.

docker-ce repo 에서 지원하는 패키지를 확인해보면 이렇다.

```
[root@linuxer ~ ]# yum install -y docker-ce
(1/6): container-selinux-2.119.2-1.911c772.el7_8.noarch.rpm
|  40 kB  00:00:00
(2/6): docker-ce-20.10.7-3.el7.x86_64.rpm
|  27 MB  00:00:00
(3/6): containerd.io-1.4.6-3.1.el7.x86_64.rpm
|  34 MB  00:00:00
(4/6): docker-ce-rootless-extras-20.10.7-3.el7.x86_64.rpm
| 9.2 MB  00:00:00
(5/6): docker-scan-plugin-0.8.0-3.el7.x86_64.rpm
| 4.2 MB  00:00:00
(6/6): docker-ce-cli-20.10.7-3.el7.x86_64.rpm
|  33 MB  00:00:02

```

패키지의 역할을 각각 설명하자면, docker 의 데몬을 실행하기 위한 패키지 그리고 우리가 흔히 쓰는 docker 명령어를 포함한 docker-cli, 그리고 containerd는 컨테이너를 실행하고 노드에서 이미지를 관리하는데 필요한 기능을 제공하는 OCI다. OCI는 Open Container initiative 라고 하는데 업계 표준이라 생각하면 간단하다.

패키지의 이름과 역할 분류가 조금씩 변한거다.

그럼 이제 좀 원론적인 이야기를 한번 해야겠다.

도커는 격리된 프로세스다. 도커를 실행중인 리눅스 시스템에서 아주 쉽게 알수있다.

docker run -d -p 8080:80 ngnix 명령어로 도커를 실행했다.

그리고 도커를 실행중인 호스트에서 ps 명령어를 쳤다.

```
[root@linuxer ~ ]# ps afxuwww
/usr/bin/containerd-shim-runc-v2 -namespace moby -id
\\_ nginx: master process nginx -g daemon off; \\_ nginx: worker process \\_ nginx: worker process
```

ps afxuwww 명령어에서 보기쉽게 트리만 떼온 상태다. containerd-shim-runc 데몬이 nginx를 실행중인것을 알 수 있다. 이것만으로도 컨테이너는 프로세스다. 라는것을 알수있다.

이렇기에 컨테이너는 불 안정함을 띄고 있고, 취약한 부분이 있다.

이제 도커 파일을 이야기해보려한다.

근래엔 도커파일의 사용법을 다들 잘아는 터라 Docs 로 대체한다.

<https://docs.docker.com/engine/reference/builder/>

근래에 내가 만든 도커파일은 이렇다.

```
FROM centos:7 LABEL maintainer "linuxer<linuxer@linuxer.name>" LABEL "purpose"="practice" ENV PATH /opt/remi/php80/root/usr/sbin:$PATH RUN yum -y update RUN yum -y install epel-release RUN yum -y install https://rpms.remirepo.net/enterprise/remi-release-7.rpm RUN yum -y install nginx php80-php-fpm RUN mkdir /var/run/php RUN mkdir /root/bin ADD www.conf /etc/opt/remi/php80/php-fpm.d/ ADD php.ini /etc/opt/remi/php80/ ADD nginx.conf /etc/nginx/ ADD index.php /usr/share/nginx/html/ ADD start.sh /root/bin/ RUN chmod 755 /root/bin/start.sh WORKDIR /usr/share/nginx/html/ EXPOSE 80 CMD ["/bin/bash", "-c", "/root/bin/start.sh"]
```

ngnix와 php80 버전을 합친 Dockerfile이다.

ADD한 파일들은 직접 파라미터를 수정한터라 스킵하고 start.sh에 대해서 이야기하려한다. 일반적으로 컨테이너는 포그라운드에서 동작한다. 백그라운드에서 동착한다면 작업을 마친 프로세스는 스스로 종료된다. 여기에서 문제가 발생한다. 도커는 CMD로 시작되는 프로세스는 아무리 많이 입력 되어도 마지막 줄만 실행된다. 그렇기에 두개의 프로세스를 한번에 실행할수 없었다. 이게바로..포그라운드의 문제점이었다.

이문제점을 회피하기위해서 수십가지의 테스트를 하였다.

CMD ["php-fpm", "-f", "&", "nginx", "-g", "daemon", "off"]

이런짓까지.. 하지만 실패했고 결국 스크립트를 작성하여 실행하도록 하고 **fg %1** 과같은 명령어를 썼다.

```
[root@linuxer ~ ]# cat start.sh
#!/bin/bash set -m /opt/remi/php80/root/usr/sbin/php-fpm --nodaemonize \\ --fpm-config /etc/opt/remi/php80/php-fpm.conf & \\ /usr/sbin/nginx fg %1
```

다른사람들에게 팁을 얻으려고 했으나, 안티 패턴인지 딱히 다들 말이없었다. 컨테이너이므로 쪼개 라는 대답을 얻었다. 나도 알고있는 부분인지라 사실 쪼갤까 했지만 일단 스크립트를 써서 완성을 했다.

이렇게 완성한 컨테이너 를 실행해 보면

```
[root@linuxer ~ ]# ps afxuwww /usr/bin/containerd-shim-runc-v2 -namespace moby -id 4
      \\_ php-fpm: master process (/etc/opt/remi/php80/php-fpm.conf)
      |   \\_ php-fpm: pool www
      |   \\_ php-fpm: pool www
      |   \\_ php-fpm: pool www
      |   \\_ php-fpm: pool www
      |   \\_ php-fpm: pool www
      \\_ nginx: master process /usr/sbin/nginx
          \\_ nginx: worker process
          \\_ nginx: worker process

```

두개의 부모프로세스를 가진 컨테이너를 확인할수 있다.

사실 이건 테스트 하느라 만든 방법이고 실제로는 nginx 를 lb로 이용하여 php-fpm 으로 라우팅 하는 구조를 만들꺼다. 그전에 손풀기로 만들어본 이미지 이나, 나름 재미있어서 포스팅까지 진행했다.

**좋은밤되시라!**
