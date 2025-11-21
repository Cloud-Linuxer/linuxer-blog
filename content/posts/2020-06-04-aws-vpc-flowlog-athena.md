---
title: "AWS-VPC-Flowlog-Athena"
date: 2020-06-04T12:03:57+09:00
draft: false
categories: ["AWS"]
tags: ["athena", "flowlog"]
slug: "aws-vpc-flowlog-athena"
aliases:
  - /aws-vpc-flowlog-athena/
  - /aws-vpc-flowlog-athena/
---


VPC에서 아웃바운드로 향하는 모든포트를 확인해야하는 일이 생겼다.

그래서 이전 포스팅에서 먼저 과거의 방법을 이용해서 확인했고 이번에는 S3로 전송하여 보려한다.

아래는 이전의 방법으로 확인한 포스팅이다.

https://www.linuxer.name/posts/2020-06-04-aws-vpc-flowlog-kinesis-athena/

현재에는 이런 방법을 사용하지 않는다.

위에 작성한 방법은 ETL 과정을 거치는건데 사실 이렇게 할필요가 전혀없다.

<https://docs.aws.amazon.com/ko_kr/athena/latest/ug/vpc-flow-logs.html>

그냥 이거 따라하면 된다.

VPC-Flowlog 활성화 -S3 -athena

이렇게 간소화 되었다.

![](/images/2020/06/image-13.png)

S3로 보내도록 로그를 생성한다.

S3 버킷 생성하는 부분은 생략한다.

CREATE EXTERNAL TABLE IF NOT EXISTS vpc_flow_logs (
version int,
account string,
interfaceid string,
sourceaddress string,
destinationaddress string,
sourceport int,
destinationport int,
protocol int,
numpackets int,
numbytes bigint,
starttime int,
endtime int,
action string,
logstatus string
)
PARTITIONED BY (`date` date)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ' '
LOCATION 's3://your_log_bucket/prefix/AWSLogs/{subscribe_account_id}/vpcflowlogs/{region_code}/'
TBLPROPERTIES ("skip.header.line.count"="1");

명령어가 정상적으로 실행되면 위와같이 테이블을 확인할수있다

![](/images/2020/06/image-16.png)

![](/images/2020/06/image-15.png)

ALTER TABLE vpc_flow_logs
ADD PARTITION (`date`='2020-06-04')
location 's3://linuxer-blog-log/AWSLogs/328345415633/vpcflowlogs/ap-northeast-2/';

두줄을 적용하면 테이블이 등록된다. 유의할점이 지정한 날에 대한 단일 파티션만 생성된다.

이제 목적한 쿼리를 날려보자.

여기까지 테스트한이유는 아웃바운드의 모든 포트를 확인하기 위함이었다. 이제 쿼리를 해보자.

SELECT sourceport, count(\*) cnt
FROM vpc_flow_logs
WHERE sourceaddress LIKE '10.0%'
GROUP BY sourceport
ORDER BY cnt desc
LIMIT 10;

![](/images/2020/06/image-17.png)

이렇게 확인할수 있었다.

구 방법 부터 현재 권장하는 방법까지 테스트를 해보았고 같은결과를 확인하였다.

여기까지 읽어주셔서 감사하다!

-추가 쿼리

SELECT day_of_week(date) AS
day,
date,
interfaceid,
sourceaddress,
action,
protocol,
destinationaddress,
destinationport
FROM vpc_flow_logs_proc_20200702
WHERE action = 'REJECT' AND sourceaddress = '10.0.1.150'
LIMIT 1000;
