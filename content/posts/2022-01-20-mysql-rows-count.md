---
title: "Mysql-Rows-count"
date: 2022-01-20T11:52:01+09:00
draft: false
categories: ["Linux"]
slug: "mysql-rows-count"
aliases:
  - /mysql-rows-count/
  - /mysql-rows-count/
---


information_schema 스키마는 랜덤샘플링으로 인하여 값의 오차가 생길수 있으므로 정확하지 않음

검증방법

ANALYZE TABLE 테이블명;SELECT table_name, table_rows, round(data_length/(1024\*1024),2) as 'DATA_SIZE(MB)', round(index_length/(1024\*1024),2) as 'INDEX_SIZE(MB)' FROM information_schema.TABLES WHERE table_schema = '데이터베이스명' GROUP BY table_name ORDER BY data_length DESC LIMIT 10;

ANALYZE 를 진행하며 테이블 확인 - information_schema.TABLES 이 계속 변경되는것이 확인됨

따라서 row count 로 만 검증가능

SELECT     COUNT(\*)FROM    테이블명;

대표적으로 자주사용하는 테이블을 카운트하여 비교하는것이 제일 정확
