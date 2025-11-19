---
title: "linux-jaeger-setup"
date: 2020-05-26T09:47:50+09:00
draft: false
categories: ["Linux"]
tags: ["jaeger", "tracing"]
slug: "linux-jaeger-setup"
aliases:
  - /linux-jaeger-setup/
  - /linux-jaeger-setup/
---

\n

jaeger를 다운 받을 위치로 이동한다. 나는 amazon linux 2를 사용했고 일부패키지는 amazon-linux-extra 를 사용했다.

\n\n\n\n

cd /usr/local/src/

\n\n\n\n

위치에서 시작했다.

\n\n\n\n

GOPATH=`pwd`  
echo $GOPATH

\n\n\n\n

gopath 를 설정했으면 gopath bin 을 path 로 지정해줘야 한다. 현재위치에서 gopath/bin 은 /usr/local/src/bin 이된다.

\n\n\n\n

export PATH=$PATH:$GOPATH/bin

\n\n\n\n

gopath bin을 설정해줬으면 사전 설치를 한다.

\n\n\n\n

amazon-linux-extras install golang1.11  
amazon-linux-extras install epel  
curl -sL https://rpm.nodesource.com/setup\_8.x | bash -  
yum install -y git npm nodejs  
npm install -g yarn  
go get -u github.com/mjibson/esc  
go get github.com/securego/gosec/cmd/gosec

\n\n\n\n

nodejs가 8버전이 필요하다. go 1.11 버전이 최소 요구 버전이다.

\n\n\n\n

이제 본격적인 설치를 시작한다.

\n\n\n\n

git clone https://github.com/jaegertracing/jaeger.git jaeger  
cd jaeger/

\n\n\n\n

git clone 뜨고 디렉토리를 이동한다.

\n\n\n\n

설치전에 CONTRIBUTING.md 파일을 꼭읽자.

\n\n\n\n

<https://github.com/jaegertracing/jaeger/blob/master/CONTRIBUTING.md>

\n\n\n\n

git submodule update --init --recursive  
make install-tools  
make build-ui

\n\n\n\n

여기까지 하면 설치가 완료된거다.

\n\n\n\n

go run -tags ui ./cmd/all-in-one/main.go

\n\n\n\n

명령어로 실행한다.

\n\n\n\n

사이트 확인은 16686 포트이다

\n\n\n\n

[http://IP:16686/search](http://13.124.43.19:16686/search)

\n\n\n\n

으로 접근해서 서비스를 확인하자.

\n\n\n\n
![](/images/2020/05/image-34.png)
\n\n\n\n

이 화면이 뜨면 정상적으로 설치된거다.

\n\n\n\n

읽어주셔서 감사하다.

\n\n\n\n

jaeger 설치를 마친다.

\n