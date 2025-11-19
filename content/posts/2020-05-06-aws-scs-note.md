---
title: "AWS-SCS-note"
date: 2020-05-06T23:20:14+09:00
draft: false
categories: ["기타"]
tags: ["scs", "note"]
slug: "aws-scs-note"
aliases:
  - /aws-scs-note/
  - /aws-scs-note/
---

\n

이아래로는 공부하면서 정리하고 AWS DOCS 에서 발췌한 내용이다.

\n\n\n\n

<https://docs.aws.amazon.com/ko_kr/kms/latest/developerguide/rotate-keys.html>

\n\n\n\n
![이미지에 대체텍스트 속성이 없습니다; 파일명은 image.png 입니다.](/images/2020/05/image.png)
\n\n\n\n

AWS Secrets Manager

\n\n\n\n

<https://docs.aws.amazon.com/ko_kr/secretsmanager/latest/userguide/intro.html>

\n\n\n\n

Secrets Manager는 코드의 암호를 포함해 하드 코딩된 자격 증명을 Secrets Manager에서 프로그래밍 방식으로 보안 암호를 검색하도록 하는 API 호출로 바꿀 수 있습니다. 이렇게 하면 보안 암호가 코드에 더 이상 존재하지 않기 때문에 코드를 검사하는 누군가에 의해 보안 암호가 손상되지 않도록 방지할 수 있습니다. 또한 사용자가 지정된 일정에 따라 Secrets Manager가 자동으로 보안 암호를 교체하도록 구성할 수 있습니다. 따라서 단기 보안 암호로 장기 보안 암호를 교체할 수 있어 손상 위험이 크게 줄어듭니다.

\n\n\n\n

AWS Systems Manager Parameter Store

\n\n\n\n

파라미터 스토어는 애플리케이션 구성 및 보안 데이터를 위한 안전한 중앙 집중식 스토리지를 제공합니다. 파라미터 스토어를 사용하여 구성 데이터를 애플리케이션 코드와 분리할 수 있습니다. 파라미터 스토어는 표준 및 고급의 두 가지 파라미터 계층을 제공합니다. 표준 계층에서는 최대 10,000개의 파라미터와 값 크기로 파라미터당 4KB를 저장할 수 있으며, 고급 계층에서는 최대 100,000개의 파라미터와, 값 크기로 파라미터당 8KB를 저장하고 정책을 파라미터에 추가할 수 있습니다. 지능형 계층화를 통해 파라미터 스토어는 생성 요청 또는 업데이트 요청에서 요청된 기능을 기반으로 계층 선택을 자동화하여 중단 없는 방법으로 고급 계층 기능을 사용할 수 있도록 합니다. 예를 들어 지능형 계층화 설정을 사용하면 계정에 10,000개의 표준 파라미터가 초과되는 경우 후속 파라미터가 고급 파라미터로 만들어져 애플리케이션 코드를 변경할 필요가 없게 됩니다. 지능형 계층화는 기본 계층이라는 새로운 서비스 수준 설정에서 옵션으로 사용할 수 있습니다.

\n\n\n\n

aws config

\n\n\n\n

<https://docs.aws.amazon.com/ko_kr/config/latest/developerguide/config-concepts.html>

\n\n\n\n

aws cloudtrail

\n\n\n\n

<https://docs.aws.amazon.com/ko_kr/awscloudtrail/latest/userguide/awscloudtrail-ug.pdf>

\n\n\n\n

vpc 침투테스트시 허가가 필요없는 서비스가 있음

\n\n\n\n

. <https://aws.amazon.com/security/penetration-testing/>

\n\n\n\n

허용

\n\n\n\n

* Amazon EC2 인스턴스, NAT 게이트웨이 및 Elastic Load Balancer
* Amazon RDS
* Amazon CloudFront
* Amazon Aurora
* Amazon API Gateway
* AWS Lambda 및 Lambda Edge 기능
* Amazon Lightsail 리소스
* Amazon Elastic Beanstalk 환경

\n\n\n\n

금지

\n\n\n\n

Amazon Route 53 Hosted Zones를 통한 DNS zone walking

\n\n\n\n

* 서비스 거부 (DoS), 분산 서비스 거부 (DDoS), 시뮬레이트 DoS, 시뮬레이트 DDoS
* 포트 플러딩
* 프로토콜 플러딩
* 요청 플러딩(로그인 요청 플러딩, API 요청 플러딩)

\n\n\n\n

GuardDuty

\n\n\n\n

GuardDuty는 AWS CloudTrail, Amazon VPC 흐름 로그 및 DNS 로그와 같은 여러 AWS 데이터 원본에 걸쳐 수백억 건의 이벤트를 분석 route53 이아니라 외부 ad 흐름은 확인할수 없음.

\n\n\n\n

SecureString

\n\n\n\n

SecureString 파라미터는 안전한 방식으로 저장되고 참조되어야 하는 모든 민감한 데이터를 뜻합니다. 암호나 라이선스 키처럼 사용자가 일반 텍스트로 수정하거나 참조해서는 안 되는 데이터가 있는 경우, SecureString 데이터 형식을 사용하여 이 파라미터를 생성합니다.

\n\n\n\n

<https://docs.aws.amazon.com/ko_kr/systems-manager/latest/userguide/sysman-paramstore-securestring.html>

\n\n\n\n

aws kms additional authenticated data

\n\n\n\n

암호화 컨텍스트

\n\n\n\n

대칭 CMK를 사용하는 모든 AWS KMS [암호화 작업](https://docs.aws.amazon.com/ko_kr/kms/latest/developerguide/concepts.html#cryptographic-operations)은 데이터에 대한 추가 컨텍스트 정보를 포함할 수 있는 선택적 키–값 페어 세트인 *암호화 컨텍스트*를 수락합니다. AWS KMS는 암호화 컨텍스트를 [추가 인증 정보](https://docs.aws.amazon.com/crypto/latest/userguide/cryptography-concepts.html#term-aad)(AAD)로 사용하여 [인증된 암호화](https://docs.aws.amazon.com/crypto/latest/userguide/cryptography-concepts.html#define-authenticated-encryption)를 지원합니다.

\n\n\n\n

s3-403

\n\n\n\n

<https://aws.amazon.com/premiumsupport/knowledge-center/s3-troubleshoot-403/>

\n\n\n\n

kms-버킷정책-역할의 iam 권한

\n\n\n\n

AWS 리소스에 대한 액세스를 타사에 부여할 때 외부 ID를 사용하는 방법

\n\n\n\n

이따금 AWS 리소스에 대한 액세스를 타사에 부여해야 할 때가 있습니다(액세스 위임). 이 시나리오의 한 가지 중요한 부분은 IAM 역할 신뢰 정책에서 역할 수임자를 지정하는 데 사용할 수 있는 옵션 정보인 외부 ID입니다.

\n\n\n\n

sts:Externald

\n