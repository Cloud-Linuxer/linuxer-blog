---
title: "aws RDS-HA-type-change"
date: 2020-01-30T10:16:40+09:00
draft: false
categories: ["AWS"]
tags: ["rds ha"]
slug: "aws-rds-ha-type-change"
aliases:
  - /aws-rds-ha-type-change/
  - /aws-rds-ha-type-change/
---


rds ha 를 테스트 해보았다.


HA enable 활성화시에 다운타임은 없다.


HA enble -> instance type 변경 t2.micro -> t2.small


HA 동작 10.0.1.12->10.0.1.30


다운타임 3초내외


HA disable instance type 변경 t2.micro -> t2.small 동시설정


HA 동작 10.0.1.30 -> 10.0.1.13


다운타임 3초내외


나름 생각보다 빠른 fail over 였다.
