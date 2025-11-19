---
title: "cloud watch monitoring script"
date: 2019-08-22T23:02:08+09:00
draft: false
categories: ["AWS"]
tags: ["aws", "cloud watch", "aws disk use", "모니터링", "디스크사용량", "monitoring"]
slug: "cloud-watch-monitoring-script"
aliases:
  - /cloud-watch-monitoring-script/
  - /cloud-watch-monitoring-script/
---

\n

WEB console   
iam 추가와 watch 지표가 생성 되는 확인만 하면 된다.

\n\n\n\n

필요한 권한  
cloudwatch:PutMetricData  
cloudwatch:GetMetricStatistics  
cloudwatch:ListMetrics  
ec2:DescribeTags

\n\n\n\n

policy 생성

\n\n\n\n

{  
 "Version": "2012-10-17",  
 "Statement": [  
 {  
 "Sid": "VisualEditor0",  
 "Effect": "Allow",  
 "Action": [  
 "cloudwatch:PutMetricData",  
 "ec2:DescribeTags",  
 "cloudwatch:GetMetricStatistics",  
 "cloudwatch:ListMetrics"  
 ],  
 "Resource": "\*"  
 }  
 ]  
 }

\n\n\n\n

생성한 정책을 user를 생성하여 부여

\n\n\n\n

Shell 작업

\n\n\n\n

로그인

\n\n\n\n

**스크립트를 실행하고 설치하는데 필요한 패키지를 설치한다.**

\n\n\n\n

centos  
sudo yum install -y perl-Switch perl-DateTime perl-Sys-Syslog perl-LWP-Protocol-https perl-Digest-SHA.x86\_64 unzip  
cd ~

\n\n\n\n

ubuntu  
sudo apt-get install unzip libwww-perl libdatetime-perl

\n\n\n\n

**cloud watch monitering script download**  
curl https://aws-cloudwatch.s3.amazonaws.com/downloads/CloudWatchMonitoringScripts-1.2.2.zip -O

\n\n\n\n

**압축해제 및 스크립트 테스트할 경로로 이동**  
  
unzip CloudWatchMonitoringScripts-1.2.2.zip && \\  
 rm CloudWatchMonitoringScripts-1.2.2.zip && \\  
 cd aws-scripts-mon

\n\n\n\n

**awscreds.conf 생성** **및 입력**  
  
 cp awscreds.template awscreds.conf

\n\n\n\n

vi awscreds.conf  
AWSAccessKeyId=  
AWSSecretKey=

\n\n\n\n

테스트 명령어 watch 로 전송하지 않음

\n\n\n\n

./mon-put-instance-data.pl --mem-util --verify --verbose

\n\n\n\n

MemoryUtilization: 20.5104909003152 (Percent)  
 Using AWS credentials file <./awscreds.conf>  
 Endpoint: https://monitoring.ap-northeast-2.amazonaws.com  
 Payload: {"MetricData":[{"Timestamp":156646131,"Dimensions":[{"Value":"i-0baaeb0265","Name":"InstanceId"}],"Value":20.5104909003152,"Unit":"Percent","MetricName":"MemoryUtilization"}],"Namespace":"System/Linux","\_\_type":"com.amazonaws.cloudwatch.v2010\_08\_01#PutMetricDataInput"}

\n\n\n\n

정상 응답확인

\n\n\n\n

crontab 등록  
vi /etc/crontab  
#disk metric  
\*/5 \* \* \* \* root /root/aws-scripts-mon/mon-put-instance-data.pl --mem-used-incl-cache-buff --mem-util --disk-space-util --disk-path=/ -disk-path=/home --from-cron  
  
disk-path 는 여러개가 들어가도 상관없다.

\n\n\n\n

systemctl restart crond

\n\n\n\n

설치과정이 정상이라면 아래와같이 linux 시스템으로 지표가 생긴다.

\n\n\n\n
![](/images/2019/08/image-2.png)
\n\n\n\n\n\n\n\n

이로서 모니터링 지표 생성까지 포스팅을 마쳤다.

\n\n\n\n

경보생성은 다른 포스팅이 많으니 생략한다.

\n\n\n\n

history

\n\n\n\n

1444 sudo apt-get install unzip libwww-perl libdatetime-perl1447 ll  
 1448 curl https://aws-cloudwatch.s3.amazonaws.com/downloads/CloudWatchMonitoringScripts-1.2.2.zip -O  
 1449 unzip CloudWatchMonitoringScripts-1.2.2.zip && rm CloudWatchMonitoringScripts-1.2.2.zip && cd aws-scripts-mon  
 1450 ll  
 1451 ./mon-put-instance-data.pl --mem-util --verify --verbose  
1458 vi /etc/crontab   
 1459 /etc/init.d/cron restart

\n\n\n\n\n