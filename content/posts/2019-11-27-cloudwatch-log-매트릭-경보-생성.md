---
title: "cloudwatch log 매트릭 경보 생성 - log monitoring"
date: 2019-11-27T21:27:15+09:00
draft: false
categories: ["AWS", "Linux"]
tags: ["aws", "cloud watch", "aws disk use", "디스크사용량", "monitoring"]
slug: "cloudwatch-log-매트릭-경보-생성"
aliases:
  - /cloudwatch-log-매트릭-경보-생성/
  - /cloudwatch-log-%eb%a7%a4%ed%8a%b8%eb%a6%ad-%ea%b2%bd%eb%b3%b4-%ec%83%9d%ec%84%b1/
---


오늘의 주제는 인스턴스에서 발생하는 로그를 cloudwatch 로 전송하여 사용하는 법을 포스팅 할거다.

먼저 역할에 정책부터 생성해 보자. 사용하는 정책은 아래와 같다.

{ "Version": "2012-10-17", "Statement": [ { "Effect": "Allow", "Action": [ "logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents", "logs:DescribeLogStreams" ], "Resource": [ "arn:aws:logs:\*:\*:\*" ] } ] }

역할을 인스턴스에 부여하고 인스턴스 내부에서 패키지를 설치해야 한다.

나는 이미 이전에 테스트로 설치해 뒀다.

설치로그이다.

Nov 18 17:17:19 Installed: aws-cli-plugin-cloudwatch-logs-1.4.4-1.amzn2.0.1.noarch
Nov 18 17:17:20 Installed: awslogs-1.1.4-3.amzn2.noarch

실제 설치방법은 yum install 이나 wget 으로 받아 실행하는 방법이 있다.

# yum install awslogs -y

or

# curl <https://s3.amazonaws.com/aws-cloudwatch/downloads/latest/awslogs-agent-setup.py> -O
# python ./awslogs-agent-setup.py --region ap-northeast-2

리전지정 옵션을 넣어주는게 좋다 그렇지 않으면 따로 지정해야 한다.

# vi /etc/awslogs/awscli.conf
[plugins]
 cwlogs = cwlogs
 [default]
 region = ap-northeast-2

그리고 cloudwatch 로 전송할 로그를 지정한다.

# vi /etc/awslogs/awslogs.conf
[/var/log/messages]
 datetime_format = %b %d %H:%M:%S
 file = /var/log/messages
 buffer_duration = 5000
 log_stream_name = test
 initial_position = end_of_file
 log_group_name = linuxer-blog-WG

테스트를 위해 /var/log/messages 를 cloudwatch 로 전송하는 로그이다.

log_stream_name = test
 initial_position = end_of_file
 log_group_name = linuxer-blog-WG

세개의 옵션이 중요하다. end_of_file 은 뒤부터 추가되는 로그를 watch 로 전송한다.

amazon linux 2 는 systemctl 명령어로 서비스를 시작한다

# systemctl restart awslogsd

![](/images/2019/11/image-14-1024x225.png)

설정대로 로그가 올라 오는게 보인다.

![](/images/2019/11/image-15-1024x187.png)

중요한 부분은 이벤트 만료시점을 지정해서 로그로 전송된 용량이 과하게 쌓이지 않도록 해야한다.

![](/images/2019/11/image-16-1024x235.png)

로그 그룹을 체크하면 지표 필터 생성 버튼이 활성화 되고 지표를 생성한다.

지표는 대충 만들어 볼까한다.

![](/images/2019/11/image-17-1024x993.png)

HealthCheck 라는 이름으로 패턴을 설정했다. 보면 샘플로그에서 일치하는 패턴이 보인다. 그리고 지표를 할당한다.

![](/images/2019/11/image-19-1024x579.png)

지표생성은 커스텀 매트릭으로 비용이 발생할수 있으니 조심하도록 하자.

![](/images/2019/11/image-20-1024x199.png)

생성된 지표를 확인하면 위와같다. 그럼 지표를 확인해보자.

![](/images/2019/11/image-21.png)

커스텀메트릭이 정상적으로 만들어진걸 확인할수 있다.

![](/images/2019/11/image-22-1024x339.png)

그래프도 잘생성 됬는지 보면 잘 올라오는게 보인다. 그럼 실제 로그가 발생해서 그래프가 생성됬는지 확인해보자.

![](/images/2019/11/image-24-1024x62.png)

로그가 올라와서 매트릭이 생성된것을 확인할수 있다. 그럼이제 경보를 생성해 보자.

![](/images/2019/11/image-25-1024x615.png)

뭔가 훅지나간거 같겠지만 빠진부분은 sns 설정 뿐이다. SNS는 주제를 만들고 구독을 생성하고 구독으로 watch 에서 sns를 추가하면 된다.

경보생성하는 방법은 따로 자세하게 설명하겠다. 블로깅이 시리즈 물이 될 기미가 보인다.

![](/images/2019/11/image-26-1024x536.png)

그래프처럼 임계치를 지나서 경보상태로 변경됬다가 정상으로 업데이트가 되는 과정이 보인다 정상적으로 지표로 경보가 작동하는것 까지 확인 되었다.

오늘의 목표인 로그전송으로 지표생성 후 경보 생성까지 완료되었다.

이케이스는 tomcat log로 지표를 생성하거나 어플리케이션에서 에러가 발생한 로그 경보를 생성시키는 등으로 사용할 수 있다.

자세하게 만들고 싶었는데 흐름만 구성한거 같아 좀 찜찜한 부분은 차차 보강하겠다.

읽어주셔 감사하다!
