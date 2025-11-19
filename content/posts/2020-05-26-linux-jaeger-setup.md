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


jaeger를 다운 받을 위치로 이동한다. 나는 amazon linux 2를 사용했고 일부패키지는 amazon-linux-extra 를 사용했다.


cd /usr/local/src/


위치에서 시작했다.


GOPATH=`pwd`
echo $GOPATH


gopath 를 설정했으면 gopath bin 을 path 로 지정해줘야 한다. 현재위치에서 gopath/bin 은 /usr/local/src/bin 이된다.


export PATH=$PATH:$GOPATH/bin


gopath bin을 설정해줬으면 사전 설치를 한다.


amazon-linux-extras install golang1.11
amazon-linux-extras install epel
curl -sL https://rpm.nodesource.com/setup_8.x | bash -
yum install -y git npm nodejs
npm install -g yarn
go get -u github.com/mjibson/esc
go get github.com/securego/gosec/cmd/gosec


nodejs가 8버전이 필요하다. go 1.11 버전이 최소 요구 버전이다.


이제 본격적인 설치를 시작한다.


git clone https://github.com/jaegertracing/jaeger.git jaeger
cd jaeger/


git clone 뜨고 디렉토리를 이동한다.


설치전에 CONTRIBUTING.md 파일을 꼭읽자.


<https://github.com/jaegertracing/jaeger/blob/master/CONTRIBUTING.md>


git submodule update --init --recursive
make install-tools
make build-ui


여기까지 하면 설치가 완료된거다.


go run -tags ui ./cmd/all-in-one/main.go


명령어로 실행한다.


사이트 확인은 16686 포트이다


[http://IP:16686/search](http://13.124.43.19:16686/search)


으로 접근해서 서비스를 확인하자.


![](/images/2020/05/image-34.png)

이 화면이 뜨면 정상적으로 설치된거다.


읽어주셔서 감사하다.


jaeger 설치를 마친다.
