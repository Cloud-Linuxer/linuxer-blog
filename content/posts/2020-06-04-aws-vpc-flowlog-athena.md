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

\n

VPC에서 아웃바운드로 향하는 모든포트를 확인해야하는 일이 생겼다.

\n\n\n\n

그래서 이전 포스팅에서 먼저 과거의 방법을 이용해서 확인했고 이번에는 S3로 전송하여 보려한다.

\n\n\n\n

아래는 이전의 방법으로 확인한 포스팅이다.

\n\n\n\n

\nhttps://linuxer.name/2020/06/aws-vpc-flowlog-kinesis-athena/\n

\n\n\n\n

현재에는 이런 방법을 사용하지 않는다.

\n\n\n\n

위에 작성한 방법은 ETL 과정을 거치는건데 사실 이렇게 할필요가 전혀없다.

\n\n\n\n

<https://docs.aws.amazon.com/ko_kr/athena/latest/ug/vpc-flow-logs.html>

\n\n\n\n

그냥 이거 따라하면 된다.

\n\n\n\n

VPC-Flowlog 활성화 -S3 -athena

\n\n\n\n

이렇게 간소화 되었다.

\n\n\n\n

![](/images/2020/06/image-13.png)

\n\n\n\n

S3로 보내도록 로그를 생성한다.

\n\n\n\n

S3 버킷 생성하는 부분은 생략한다.

\n\n\n\n

CREATE EXTERNAL TABLE IF NOT EXISTS vpc\_flow\_logs (  
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
LOCATION 's3://your\_log\_bucket/prefix/AWSLogs/{subscribe\_account\_id}/vpcflowlogs/{region\_code}/'  
TBLPROPERTIES ("skip.header.line.count"="1");

\n\n\n\n

명령어가 정상적으로 실행되면 위와같이 테이블을 확인할수있다

\n\n\n\n

![](/images/2020/06/image-16.png)

\n\n\n\n
![](/images/2020/06/image-15.png)
\n\n\n\n

ALTER TABLE vpc\_flow\_logs  
ADD PARTITION (`date`='2020-06-04')  
location 's3://linuxer-blog-log/AWSLogs/328345415633/vpcflowlogs/ap-northeast-2/';

\n\n\n\n

두줄을 적용하면 테이블이 등록된다. 유의할점이 지정한 날에 대한 단일 파티션만 생성된다.

\n\n\n\n\n\n\n\n

이제 목적한 쿼리를 날려보자.

\n\n\n\n\n\n\n\n

여기까지 테스트한이유는 아웃바운드의 모든 포트를 확인하기 위함이었다. 이제 쿼리를 해보자.

\n\n\n\n

SELECT sourceport, count(\*) cnt  
FROM vpc\_flow\_logs  
WHERE sourceaddress LIKE '10.0%'  
GROUP BY sourceport  
ORDER BY cnt desc  
LIMIT 10;

\n\n\n\n
![](/images/2020/06/image-17.png)
\n\n\n\n

이렇게 확인할수 있었다.

\n\n\n\n\n\n\n\n

구 방법 부터 현재 권장하는 방법까지 테스트를 해보았고 같은결과를 확인하였다.

\n\n\n\n\n\n\n\n

여기까지 읽어주셔서 감사하다!

\n\n\n\n

-추가 쿼리

\n\n\n\n

SELECT day\_of\_week(date) AS  
day,  
date,  
interfaceid,  
sourceaddress,  
action,  
protocol,  
destinationaddress,  
destinationport  
FROM vpc\_flow\_logs\_proc\_20200702  
WHERE action = 'REJECT' AND sourceaddress = '10.0.1.150'  
LIMIT 1000;

\n