---
title: "AWS Certified Solutions Architect – Professional Level Sample Exam Questions 풀이 01"
date: 2019-08-31T22:42:41+09:00
draft: false
categories: ["AWS", "Certification"]
tags: ["aws", "sap", "exam", "aws sap", "sap exam", "예제", "샘플", "시험"]
slug: "aws-certified-solutions-architect-professional-level-sample-exam-questions-풀이-01"
aliases:
  - /aws-certified-solutions-architect-professional-level-sample-exam-questions-풀이-01/
  - /aws-certified-solutions-architect-professional-level-sample-exam-questions-%ed%92%80%ec%9d%b4-01/
---


문제는 아래 URL 에서 발췌하였다.


<https://d1.awsstatic.com/Train%20%26%20Cert/docs/AWS_certified_solutions_architect_professional_examsample.pdf>


번역은 google 번역기이며 알아보기 어려운 부분을 조금 수정하였다.
실제 수정한것은 3번문제 조금이며 대부분 구글번역기를 의지하였다.


이번 글에선 3번문제 까지 풀이하였으니 참고바란다.


오역은..구글신님께 확인하시길 바란다.


틀린문제나 오역 오타 테클 환영하오니 이상한부분이 있다면 언제든 댓글달아 주시라!


1번 문제다.


원문
Your company’s on-premises content management system has the following architecture:
 – Application Tier – Java code on a JBoss application server
 – Database Tier – Oracle database regularly backed up to Amazon Simple Storage Service (S3) using the Oracle RMAN backup utility
 – Static Content – stored on a 512GB gateway stored Storage Gateway volume attached to the application server via the iSCSI interface
 Which AWS based disaster recovery strategy will give you the best RTO?
 Deploy the Oracle database and the JBoss app server on EC2. Restore the RMAN Oracle backups from Amazon S3. Generate an EBS volume of static content from the Storage Gateway and attach it to the JBoss EC2 server.
 Deploy the Oracle database on RDS. Deploy the JBoss app server on EC2. Restore the RMAN Oracle backups from Amazon Glacier. Generate an EBS volume of static content from the Storage Gateway and attach it to the JBoss EC2 server. (Glacier does help to give best RTO)
 Deploy the Oracle database and the JBoss app server on EC2. Restore the RMAN Oracle backups from Amazon S3. Restore the static content by attaching an AWS Storage Gateway running on Amazon EC2 as an iSCSI volume to the JBoss EC2 server. (No need to attach the Storage Gateway as an iSCSI volume can just create a EBS volume)
 Deploy the Oracle database and the JBoss app server on EC2. Restore the RMAN Oracle backups from Amazon S3. Restore the static content from an AWS Storage Gateway-VTL running on Amazon EC2 (VTL is Virtual Tape library and doesn’t fit the RTO)


번역본
회사의 온-프레미스 콘텐츠 관리 시스템에는 다음과 같은 아키텍처가 있습니다.
 – 응용 프로그램 계층 – JBoss 응용 프로그램 서버의 Java 코드
 – 데이터베이스 계층 – Oracle RMAN 백업 유틸리티를 사용하여 정기적으로 Amazon Simple Storage Service (S3)에 백업 된 Oracle 데이터베이스
 – 정적 컨텐츠 – iSCSI 인터페이스를 통해 애플리케이션 서버에 연결된 스토리지 게이트웨이 볼륨이 512GB 게이트웨이에 저장
 최고의 RTO를 제공하는 AWS 기반 재해 복구 전략은 무엇입니까?
 A) EC2에 Oracle 데이터베이스 및 JBoss 앱 서버를 배포하십시오. Amazon S3에서 RMAN Oracle 백업을 복원하십시오. 스토리지 게이트웨이에서 정적 컨텐츠의 EBS 볼륨을 생성하여 JBoss EC2 서버에 연결하십시오.
 B) RDS에 Oracle 데이터베이스를 배포하십시오. EC2에 JBoss 앱 서버를 배포하십시오. Amazon Glacier에서 RMAN Oracle 백업을 복원하십시오. 스토리지 게이트웨이에서 정적 컨텐츠의 EBS 볼륨을 생성하여 JBoss EC2 서버에 연결하십시오.
 C) EC2에 Oracle 데이터베이스 및 JBoss 앱 서버를 배포하십시오. Amazon S3에서 RMAN Oracle 백업을 복원하십시오. Amazon EC2에서 실행중인 AWS Storage Gateway를 iSCSI 볼륨으로 JBoss EC2 서버에 연결하여 정적 컨텐츠를 복원하십시오. iSCSI 볼륨이 EBS 볼륨을 생성 할 수 있으므로 스토리지 게이트웨이를 연결할 필요가 없습니다.
 D) EC2에 Oracle 데이터베이스 및 JBoss 앱 서버를 배포하십시오. Amazon S3에서 RMAN Oracle 백업을 복원하십시오. Amazon EC2에서 실행되는 AWS Storage Gateway-VTL에서 정적 컨텐츠를 복원합니다.


이 문제를 알기 위해선 먼저 알아야할것들이 있다. 이 문제의 주제가 무엇인지 문제를 읽으면 바로 알아야한다. 주제는 재해복구이다.
 그럼 두번째로 알아야할것은 문제에서 요구하는 기준이 무엇인가 이다. '최고의 RTO(recovery time objective)'이다.


<https://zetawiki.com/wiki/%EB%B3%B5%EA%B5%AC%EC%8B%9C%EC%A0%90%EB%AA%A9%ED%91%9C_RPO,_%EB%B3%B5%EA%B5%AC%EC%8B%9C%EA%B0%84%EB%AA%A9%ED%91%9C_RTO>


그럼 보기에서 제일빨리 aws로 복구할수 있는 방법을 찾으면 된다.


참 쉽죠?


방법을 찾기전에 구성을 먼저 뜯어보자.


jboss를 aws에 구축한다면 역시 ec2외엔 답이없다.
 데이터 베이스는 Oracle RMAN으로 s3로 백업을 한다고 하는데 이건 볼륨 백업이 아니라 데이터베이스 파일 단위의 백업이다.

 정적 컨텐츠는 iSCSI로 연결된 스토리지 게이트웨이 512GB다 이것은 스토리지게이트웨이에서 볼륨게이트웨이 그리고 용량 언급이 있었으므로 저장볼륨 방식이다.
 저장볼륨 방식으로 사용중이면 스냅샷을 생성해서 EBS볼륨을 생성하여 ec2에 연결하는 작업이 가능하다.


<https://docs.aws.amazon.com/ko_kr/storagegateway/latest/userguide/StorageGatewayConcepts.html>


정리하자면, aws 로 재해복구시에 최적의 RTO를 가지게 하려면 JBoss를 ec2로 만들고 oracle의 백업본이 있는 s3에서 백업을 복구하고 스토리지 게이트웨이 스냅샷에서 EBS 볼륨을 생성하여 EC2에 연결하면 된다.


정리한 내용에 최대한 부합하는 답변을 골라보자.

 A) EC2에 Oracle 데이터베이스 및 JBoss 앱 서버를 배포하십시오. Amazon S3에서 RMAN Oracle 백업을 복원하십시오. 스토리지 게이트웨이에서 정적 컨텐츠의 EBS 볼륨을 생성하여 JBoss EC2 서버에 연결하십시오.


위 에서 서술한 내용과 흡사하다 지연될 만한 부분은 없다.


B) RDS에 Oracle 데이터베이스를 배포하십시오. EC2에 JBoss 앱 서버를 배포하십시오. Amazon Glacier에서 RMAN Oracle 백업을 복원하십시오. 스토리지 게이트웨이에서 정적 컨텐츠의 EBS 볼륨을 생성하여 JBoss EC2 서버에 연결하십시오.

Glacier에서 백업을 복원하므로 최고의 RTO는 어렵다. 그래서 B는 틀렸다.


C) EC2에 Oracle 데이터베이스 및 JBoss 앱 서버를 배포하십시오. Amazon S3에서 RMAN Oracle 백업을 복원하십시오. Amazon EC2에서 실행중인 AWS Storage Gateway를 iSCSI 볼륨으로 JBoss EC2 서버에 연결하여 정적 컨텐츠를 복원하십시오.

ISCSI 볼륨을 ec2에 연결해야 하므로 틀렸다 EBS볼륨을 생성하여 연결하는것이 훨씬 빠르다. 그래서 C 도 틀렸다.


D) EC2에 Oracle 데이터베이스 및 JBoss 앱 서버를 배포하십시오. Amazon S3에서 RMAN Oracle 백업을 복원하십시오. Amazon EC2에서 실행되는 AWS Storage Gateway-VTL에서 정적 컨텐츠를 복원합니다.

 AWS Storage Gateway-VTL은 가상 테이프 라이브러리다.
 VTL은 테이프 드라이브 단위로 제공되기때문에 문제에서 제공한 512GB 볼륨이 제공되지 않는다. 그래서 D도 틀렸다.


그래서 A가 정답이다.


**A) EC2에 Oracle 데이터베이스 및 JBoss 앱 서버를 배포하십시오. Amazon S3에서 RMAN Oracle 백업을 복원하십시오. 스토리지 게이트웨이에서 정적 컨텐츠의 EBS 볼륨을 생성하여 JBoss EC2 서버에 연결하십시오.**


2번 문제다.


원문
An ERP application is deployed across multiple AZs in a single region. In the event of failure, the Recovery Time Objective (RTO) must be less than 3 hours, and the Recovery Point Objective (RPO) must be 15 minutes. The customer realizes that data corruption occurred roughly 1.5 hours ago. What DR strategy could be used to achieve this RTO and RPO in the event of this kind of failure?


A) Take 15-minute DB backups stored in Amazon Glacier, with transaction logs stored in Amazon S3 every 5 minutes.
B) Use synchronous database master-slave replication between two Availability Zones.
C) Take hourly DB backups to Amazon S3, with transaction logs stored in S3 every 5 minutes.
D) Take hourly DB backups to an Amazon EC2 instance store volume, with transaction logs stored in Amazon S3 every 5 minutes.


번역본
ERP 애플리케이션은 단일 지역의 여러 AZ에 배포됩니다. 장애가 발생한 경우 RTO (Recovery Time Objective)는 3 시간 미만이어야하고 RPO (Recovery Point Objective)는 15 분이어야합니다. 고객은 약 1.5 시간 전에 데이터 손상이 발생했음을 알고 있습니다. 이러한 종류의 장애 발생시이 RTO 및 RPO를 달성하기 위해 어떤 재해복구 전략을 사용할 수 있습니까?


A) Amazon Glacier에 저장된 15 분 DB 백업을 5 분마다 Amazon S3에 저장된 트랜잭션 로그와 함께 수행하십시오.
B) 두 가용 영역간에 동기식 데이터베이스 마스터-슬레이브 복제를 사용하십시오.
C) 5 분마다 S3에 트랜잭션 로그가 저장된 Amazon S3에 시간별 DB 백업을 수행합니다.
D) Amazon S3에 5 분마다 저장된 트랜잭션 로그를 사용하여 Amazon EC2 인스턴스 스토어 볼륨에 매시간 DB 백업을 수행합니다.


1번 문제와 동일하게 재해복구관련 주제이다. 여기서 주목이야할 단어는 RTO / RPO 다
 장애 발생 시점 부터 복구 완료 시점까지 걸리는 시간을 RTO 라고하며 RPO는 데이터를 손실했을떄 감내할수 있는 시간을 RPO라고 한다.


<https://zetawiki.com/wiki/%EB%B3%B5%EA%B5%AC%EC%8B%9C%EC%A0%90%EB%AA%A9%ED%91%9C_RPO,_%EB%B3%B5%EA%B5%AC%EC%8B%9C%EA%B0%84%EB%AA%A9%ED%91%9C_RTO>


그럼 문제에선 장애 발생시 3시간안에 복구 유실되는 데이터는 15분. 풀어서 쓰자면 서비스는 3시간내에 다시 정상화 되어야 하며, 데이터의 백업로테이션은 최대 15분이다.


문항을 살펴 보자


A) Amazon Glacier에 저장된 15 분 DB 백업을 5 분마다 Amazon S3에 저장된 트랜잭션 로그와 함께 수행하십시오.


Glacier 는 RTO 충족할수 없다. 그래서 틀렸다.
 <https://aws.amazon.com/ko/glacier/>


B) B) 두 가용 영역간에 동기식 데이터베이스 마스터-슬레이브 복제를 사용하십시오.


동기식 복제는 백업이 아니며 장애또한 동기되므로 틀렸다.


C) 5 분마다 S3에 트랜잭션 로그가 저장된 Amazon S3에 시간별 DB 백업을 수행합니다.


5분마다 트랜잭션로그는 RPO에 충족하며 시간마다 DB백업은 RTO를 충족한다.


D) Amazon S3에 5 분마다 저장된 트랜잭션 로그를 사용하여 Amazon EC2 인스턴스 스토어 볼륨에 매시간 DB 백업을 수행합니다.


인스턴스 스토어는 인스턴스가 종료될시에 데이터를 유실하므로 백업의 좋은 방법이 아니다.


따라서 정답은 C다.


3번 문제다.


원문
The Marketing Director in your company asked you to create a mobile app that lets users post sightings of good deeds known as random acts of kindness in 80-character summaries. You decided to write the application in JavaScript so that it would run on the broadest range of phones, browsers, and tablets. Your application should provide access to Amazon DynamoDB to store the good deed summaries. Initial testing of a prototype shows that there aren’t large spikes in usage. Which option provides the most costeffective and scalable architecture for this application?


A) Provide the JavaScript client with temporary credentials from the Security Token Service using a Token Vending Machine (TVM) on an EC2 instance to provide signed credentials mapped to an Amazon Identity and Access Management (IAM) user allowing DynamoDB puts and S3 gets. You serve your mobile application out of an S3 bucket enabled as a web site. Your client updates DynamoDB.
B) Register the application with a Web Identity Provider like Amazon, Google, or Facebook, create an IAM role for that provider, and set up permissions for the IAM role to allow S3 gets and DynamoDB puts. You serve your mobile application out of an S3 bucket enabled as a web site. Your client updates DynamoDB.
C) Provide the JavaScript client with temporary credentials from the Security Token Service using a Token Vending Machine (TVM) to provide signed credentials mapped to an IAM user allowing DynamoDB puts. You serve your mobile application out of Apache EC2 instances that are load-balanced and autoscaled. Your EC2 instances are configured with an IAM role that allows DynamoDB puts. Your server updates DynamoDB.
D) Register the JavaScript application with a Web Identity Provider like Amazon, Google, or Facebook, create an IAM role for that provider, and set up permissions for the IAM role to allow DynamoDB puts. You serve your mobile application out of Apache EC2 instances that are load-balanced and autoscaled. Your EC2 instances are configured with an IAM role that allows DynamoDB puts. Your server updates DynamoDB.


번역본
회사의 마케팅 디렉터는 사용자가 임의의 친절한 행동으로 알려진 선의의 목격을 80자 요약을 게시 할 수있는 모바일 앱을 만들도록 요청했습니다. 광범위한 전화, 브라우저 및 태블릿에서 실행될 수 있도록 JavaScript로 응용 프로그램을 작성하기로 결정했습니다. 애플리케이션은 '80자 요약'을 저장하기 위해 Amazon DynamoDB에 대한 액세스를 제공해야합니다. 프로토 타입을 처음 테스트 한 결과 사용량이 크게 증가하지 않은 것으로 나타났습니다. 이 응용 프로그램에 가장 비용 효율적이고 확장 가능한 아키텍처를 제공하는 옵션은 무엇입니까?


A) EC2 인스턴스에서 TVM (Token Vending Machine)을 사용하여 Security Token Service의 임시 자격 증명을 JavaScript 클라이언트에 제공하여 DynamoDB 넣기 및 S3 가져 오기를 허용하는 IAM (Amazon Identity and Access Management) 사용자에 매핑 된 서명 된 자격 증명을 제공합니다. 웹 사이트로 활성화 된 S3 버킷에서 모바일 애플리케이션을 제공합니다. 클라이언트가 DynamoDB를 업데이트합니다.
B) Amazon, Google 또는 Facebook과 같은 Web Identity Provider에 애플리케이션을 등록하고 해당 제공자에 대한 IAM 역할을 생성하고 S3 가져 오기 및 DynamoDB 넣기를 허용하는 IAM 역할에 대한 권한을 설정하십시오. 웹 사이트로 활성화 된 S3 버킷에서 모바일 애플리케이션을 제공합니다. 클라이언트가 DynamoDB를 업데이트합니다.
C) TVM (Token Vending Machine)을 사용하여 Security Token Service의 임시 자격 증명을 JavaScript 클라이언트에 제공하여 DynamoDB가 넣을 수있는 IAM 사용자에게 매핑 된 서명 된 자격 증명을 제공합니다. 로드 밸런싱되고 자동 확장되는 Apache EC2 인스턴스에서 모바일 애플리케이션을 제공합니다. EC2 인스턴스는 DynamoDB 풋을 허용하는 IAM 역할로 구성됩니다. 서버가 DynamoDB를 업데이트합니다.
D) Amazon, Google 또는 Facebook과 같은 Web Identity Provider에 JavaScript 애플리케이션을 등록하고 해당 제공자에 대한 IAM 역할을 생성하고 DynamoDB Put을 허용하는 IAM 역할에 대한 권한을 설정하십시오. 로드 밸런싱되고 자동 확장되는 Apache EC2 인스턴스에서 모바일 애플리케이션을 제공합니다. EC2 인스턴스는 DynamoDB 풋을 허용하는 IAM 역할로 구성됩니다. 서버가 DynamoDB를 업데이트합니다.


트위터 처럼 문자 제한이 있는 앱이고, JavaScript로 만들어져 있으며 여러 플랫폼에서 사용 가능하고 DynamoDB에 액세스 해야하며 확장성을 지녀야하며 비용 효율적인 아키텍쳐를 선택하면 된다.
사실 주목할점은 확장성과 비용효율이다.


A) EC2 인스턴스에서 TVM (Token Vending Machine)을 사용하여 Security Token Service의 임시 자격 증명을 JavaScript 클라이언트에 제공하여 DynamoDB 넣기 및 S3 가져 오기를 허용하는 IAM (Amazon Identity and Access Management) 사용자에 매핑 된 서명 된 자격 증명을 제공합니다. 웹 사이트로 활성화 된 S3 버킷에서 모바일 애플리케이션을 제공합니다. 클라이언트가 DynamoDB를 업데이트합니다.


EC2 를 사용하므로 확장성을 가지기 어렵다. 확장성에 대한 다른언급이 없으므로 단일인스턴스로 간주한다.


B) Amazon, Google 또는 Facebook과 같은 Web Identity Provider에 애플리케이션을 등록하고 해당 제공자에 대한 IAM 역할을 생성하고 S3 가져 오기 및 DynamoDB 넣기를 허용하는 IAM 역할에 대한 권한을 설정하십시오. 웹 사이트로 활성화 된 S3 버킷에서 모바일 애플리케이션을 제공합니다. 클라이언트가 DynamoDB를 업데이트합니다.


s3 정적 호스팅으로 웹을 호스팅하기에 확장성을 지니는 구성이며, 따로 ec2를 사용거나 하지않기에 비용 효율적이다.


C) TVM (Token Vending Machine)을 사용하여 Security Token Service의 임시 자격 증명을 JavaScript 클라이언트에 제공하여 DynamoDB가 넣을 수있는 IAM 사용자에게 매핑 된 서명 된 자격 증명을 제공합니다. 로드 밸런싱되고 자동 확장되는 Apache EC2 인스턴스에서 모바일 애플리케이션을 제공합니다. EC2 인스턴스는 DynamoDB 풋을 허용하는 IAM 역할로 구성됩니다. 서버가 DynamoDB를 업데이트합니다.
로드벨런싱을 사용하여 확장성을 지니나 비용효율적이지 못하다.


D) Amazon, Google 또는 Facebook과 같은 Web Identity Provider에 JavaScript 애플리케이션을 등록하고 해당 제공자에 대한 IAM 역할을 생성하고 DynamoDB Put을 허용하는 IAM 역할에 대한 권한을 설정하십시오. 로드 밸런싱되고 자동 확장되는 Apache EC2 인스턴스에서 모바일 애플리케이션을 제공합니다. EC2 인스턴스는 DynamoDB 풋을 허용하는 IAM 역할로 구성됩니다. 서버가 DynamoDB를 업데이트합니다.
C와 같은 이유이다. 로드벨런싱을 사용하여 확장성을 지니나 비용효율적이지 못하다.


따라서 정답은 B이다.
