---
title: "AWS Certified Data Engineer - Associate - 합격후기"
date: 2024-03-16T10:19:08+09:00
draft: false
categories: ["AWS", "Certification"]
tags: ["DEA", "DEA-C01", "Data Engineer"]
slug: "aws-certified-data-engineer-associate-review"
aliases:
  - /aws-certified-data-engineer-associate-review/
  - /aws-certified-data-engineer-associate-review/
---


![](/images/2024/03/image.png)

DEA-C01 합격 후기를 쓰러왔다.

AWS Certified Data Engineer - Associate 자격증은 2024년 3월 12일 정식으로 출시되었으며, 취득일은 3월 14일이다.

먼저 DEA 시험은 Beta 시기를 거쳐서 오픈했는데, 그 이전에 <https://explore.skillbuilder.aws/learn> 에서 강의를 이미 오픈했다. 나는 사실 자격증을 얼른 취득하고 싶어서 조금씩 공부를 해놓고 있었다.

~~(올서티가 마려웠다.)~~

<https://aws.amazon.com/ko/certification/certified-data-engineer-associate/>

공부의 시작은 시험안내서 이다.

<https://d1.awsstatic.com/ko_KR/training-and-certification/docs-data-engineer-associate/AWS-Certified-Data-Engineer-Associate_Exam-Guide.pdf>

내가 본 안내서에서 중요하다 생각하는 부분이다.

* 프로그래밍 개념을 적용하면서 데이터를 수집 및 변환하고 데이터 파이프라인을

* 오케스트레이션합니다. - **Glue / Step Function**

* 최적의 데이터 스토어를 선택 및 데이터 모델을 설계하고 데이터 스키마를
  카탈로그화하고 데이터 수명 주기를 관리합니다. - **S3 / RDS(PostgresSQL) / RedShift / Dynamodb**

* 데이터 파이프라인을 운영화하고 유지 관리 및 모니터링합니다. 데이터를 분석하고
  데이터 품질을 보장합니다. - **Kinesis / Glue**

* 적절한 인증, 권한 부여, 데이터 암호화, 프라이버시 및 거버넌스를 구현하고 로깅을
  사용합니다. 로깅을 활성화합니다. - **CloudTrail / lake formation**

서론만으로도 데이터엔지니어의 역할이 보인다. 적절한 데이터 스토어(데이터 레이크 / 데이터 웨어하우스 / 데이터베이스등) 에 파이프라인을 통하여 수집 변환 적제를 하는것이 핵심이고, 이과정에서 암호화, 모니터링, 거버넌스틀 통한 제어를 하는것이다.

어떤 시험을 볼때도 안내서가 제일 중요하다. 재대로 안보면 시험에서 어이없게 떨어질수 있다. 테스크 설명을 보면서 AWS의 서비스를 연상할수 있는게 가장 중요한 포인트이다.

그러면 예를 들어서 시험안내서의 1.1 데이터수집에서 <데이터를 수집하는 AWS 서비스의 처리량 및 지연 시간 특성> 에 대해서 이야기 해보겠다. 일반적으로 AWS에서는 데이터를 수집하는 Kinesis 이다. Kinesis 는 보통 Stream 과 Firehose 로 구분된다. 이 두가지를 헷갈리는 사람이 많은데, 나 같은 경우엔 이두가지를 이렇게 나눈다

| 기능/특징 | Kinesis Data Streams | Kinesis Data Firehose |
| --- | --- | --- |
| 주요 용도 | 실시간 데이터 스트리밍 처리 및 분석을 위한 고수준 API 제공. 사용자가 스트림 데이터를 자세히 제어하고 관리할 수 있음. | 데이터를 실시간으로 수집하고, 변환하여 S3, Redshift, Elasticsearch, Splunk 등의 AWS 서비스로 쉽게 로드. |
| 데이터  스토리지 | 스트림 내의 데이터는 최대 7일까지 저장 가능. 데이터 보존 기간 사용자 설정 가능. | Firehose는 스스로 데이터를 저장하지 않음. 바로 다음 대상으로 전송. |
| 데이터  처리 | 사용자는 스트림 데이터를 읽고 처리하기 위해 자체 소비자(예: EC2 인스턴스, Lambda 함수)를 관리해야 함. | 데이터 변환 및 필터링 기능 내장. Lambda를 사용하여 데이터 변환 가능. |
| 대상  서비스  통합 | Kinesis Data Streams 자체는 직접적인 데이터 저장 대상을 제공하지 않음. 소비자가 데이터를 읽고 처리한 후 저장소에 저장 필요. | S3, Redshift, Elasticsearch 및 Splunk로 데이터를 직접 전송할 수 있음. |
| 관리  편의성 | 높은 수준의 관리와 모니터링 필요. 사용자가 스트림과 데이터 소비자를 직접 관리. | 관리가 훨씬 쉬움. AWS가 대부분의 관리 작업을 자동으로 처리. |
| 시작 난이도 | 설정과 관리에 더 많은 단계와 고려 사항이 있음. | 설정이 간단하며, 몇 분 내에 데이터 스트리밍 시작 가능. |
| 실시간  처리 | 거의 실시간으로 데이터 처리 및 분석 가능. | 거의 실시간으로 데이터를 수집하고 대상 서비스로 전송. |
| 비용 | 데이터 스트림의 샤드 수, PUT 요청 수, 데이터 전송량 등에 따라 비용이 결정됨. | 전송된 데이터의 양에 따라 비용이 결정됨. |

이런형태의 차이점을 이해하고 있으면 이제 두가지 서비스를 고려할때 바로 판단할수 있다. 또한 이 두가지 서비스는 실시간이 아니다. 거의(실시간)이다. 더 실시간으로 처리해야한다면 큐서비스를 사용해야한다.

시험 안내서의 범위는 너무 넓으니 속성으로 공부하고 싶다면 이제 사전테스트를 해야한다.

<https://explore.skillbuilder.aws/learn/course/external/view/elearning/18868/exam-prep-official-pretest-aws-certified-data-engineer-associate-dea-c01-korean>

나는 사전테스트를 여러차례 풀었고 해체하 듯 하나하나 Docs를 찾아가며 봤다. 예제문제가 훨씬어렵다. 예제문제 85%이상이면 시험을 봐도 좋을거 같다.

나는 다시 AWS의 모든 자격증을 획득했다.

![](/images/2024/03/image-1-1024x388.png)

읽어주셔서 감사하고 좋은하루 되시라!
