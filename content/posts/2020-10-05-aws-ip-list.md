---
title: "AWS-IP-list"
date: 2020-10-05T13:37:46+09:00
draft: false
categories: ["AWS"]
slug: "aws-ip-list"
aliases:
  - /aws-ip-list/
  - /aws-ip-list/
---


wget https://ip-ranges.amazonaws.com/ip-ranges.json

wget 으로 먼저 aws 의 IP list 를 받는다.

yum install jq

jq를 다운받는다.

jq '.prefixes[] | select(.region=="ap-northeast-2") | select(.service=="S3") | .ip_prefix' < ip-ranges.json
"52.219.60.0/23"
"52.219.148.0/23"
"52.219.56.0/22"
"52.219.144.0/22"

IP list를 필터하여 확인한다.

jq '.prefixes[] | select(.region=="ap-northeast-2") | select(.service=="S3") | .ip_prefix' < ip-ranges.json | tr -d '"'
52.219.60.0/23
52.219.148.0/23
52.219.56.0/22
52.219.144.0/22

tr 로 " 를 삭제한 예제.
