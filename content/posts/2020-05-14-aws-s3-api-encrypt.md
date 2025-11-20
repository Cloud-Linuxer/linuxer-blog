---
title: "AWS-S3-api-encrypt"
date: 2020-05-14T17:47:57+09:00
draft: false
categories: ["AWS"]
tags: ["aws", "s3", "s3.api", "api"]
slug: "aws-s3-api-encrypt"
aliases:
  - /aws-s3-api-encrypt/
  - /aws-s3-api-encrypt/
---


aws bucket ls | xargs -L1 % aws s3api put-bucket-encryption \\
--bucket % \\
--server-side-encryption-configuration '{"Rules": [{"ApplyServerSideEncryptionByDefault": {"SSEAlgorithm": "AES256"}}]}'

s3 api 이용한 모든버킷 AES-256 암호화.
