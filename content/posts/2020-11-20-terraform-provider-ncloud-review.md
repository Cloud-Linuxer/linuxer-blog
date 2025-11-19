---
title: "terraform-provider-ncloud-review"
date: 2020-11-20T13:29:50+09:00
draft: false
categories: ["Linux", "기타", "NCP"]
tags: ["ncp", "vault", "navercloud"]
slug: "terraform-provider-ncloud-review"
aliases:
  - /terraform-provider-ncloud-review/
  - /terraform-provider-ncloud-review/
---

\n

오늘 하시코프x네이버클라우드 웨비나에서 terraform 과 Vault 에 대한 웨비나를 청취했습니다.

\n\n\n\n

<https://github.com/NaverCloudPlatform/terraform-provider-ncloud>

\n\n\n\n

이전에 방과후(?) meetup에서 네이버클라우드가 테라폼의 프로바이더로 있다는것을 알았습니다. 그 덕분에 네이버클라우드에서 terraform은 이미 경험이 있는 상태고, Vault도 경험이 있었습니다. 오늘의 주제 중 Secrets Engines이 궁금했습니다.

\n\n\n\n

<https://www.vaultproject.io/docs/secrets>

\n\n\n\n

Secrets engines are components which store, generate, or encrypt data.

\n\n\n\n

시크릿엔진은 데이터를 저장또는 생성하고 암호화하는 구성요소.

\n\n\n\n

AWS 의 Parameter Store / Secrets Manager 와 비슷한 기능을 한다고 생각이 들었습니다. 다른 벤더에서도 비슷한 서비스들이 있습니다.

\n\n\n\n

<https://hackernoon.com/aws-secrets-manager-vs-hashicorp-vault-vs-aws-parameter-store-bcbf60b0c0d1>

\n\n\n\n

<https://www.cloudjourney.io/articles/security/aws_secrets_manager_vs_hashi_vault-su/>

\n\n\n\n\n\n\n\n

가장 일반적인 사용예라 생각되는것은, access key의 암호화라 생각됩니다. 일반적으로 aws-vault 같은 명령어로 지원합니다.

\n\n\n\n

아직 ncp-vault 가 만들어진게 아니라, ncp 내에서 사용하기엔 좀 불편한 부분이 있으리라 생각됩니다. 현재 npc 는 provider로 등록된 상태고 cli 를 지원하므로 차차 지원하리라 생각됩니다.

\n\n\n\n

<https://www.44bits.io/ko/post/securing-aws-credentials-with-aws-vault#%ED%85%8C%EB%9D%BC%ED%8F%BCterraform%EC%97%90%EC%84%9C-%EC%82%AC%EC%9A%A9%ED%95%98%EA%B8%B0>

\n\n\n\n

aws 에서의 vault 사용예입니다.

\n\n\n\n

<https://www.vaultproject.io/docs/secrets/databases/mysql-maria>

\n\n\n\n

mysql-maria db의 user 암호화입니다.

\n\n\n\n\n\n\n\n

이런 방법이 필요한 이유는 결국 어플리케이션 소스의 탈취로 문제를 방지하기 위함입니다. key의 자동로테이션이나, expire time 을가진 key 발급등을 할 수 있습니다.

\n\n\n\n

Vault 는 근래에 들어서 굉장히 핫한 오픈소스라 테스트 해보시는게 좋을것 같습니다.

\n\n\n\n

마무리를 하자면..

\n\n\n\n

템플릿 소스들이 점점 쌓이고 사용예가 늘면 IaC는 점점 더 일반화 될것입니다.

\n\n\n\n

미리미리 IaC를 준비하고 사용방법을 익히는것도 좋을것 같습니다.

\n\n\n\n

조만간 Secrets Engines 사용하기 위해 자동화 스크립트를 적용하는 고민을 한번 해보려 합니다. 시간이 나면 한번 테스트 해봐야겠습니다.

\n\n\n\n\n\n\n\n

읽어주셔서 감사합니다!

\n\n\n\n\n\n\n\n\n