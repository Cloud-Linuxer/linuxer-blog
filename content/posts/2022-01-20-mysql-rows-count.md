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

\n

information\_schema 스키마는 랜덤샘플링으로 인하여 값의 오차가 생길수 있으므로 정확하지 않음

\n\n\n\n

검증방법

\n\n\n\n

ANALYZE TABLE 테이블명;SELECT table\_name, table\_rows, round(data\_length/(1024\*1024),2) as 'DATA\_SIZE(MB)', round(index\_length/(1024\*1024),2) as 'INDEX\_SIZE(MB)' FROM information\_schema.TABLES WHERE table\_schema = '데이터베이스명' GROUP BY table\_name ORDER BY data\_length DESC LIMIT 10;

\n\n\n\n

ANALYZE 를 진행하며 테이블 확인 - information\_schema.TABLES 이 계속 변경되는것이 확인됨

\n\n\n\n

따라서 row count 로 만 검증가능

\n\n\n\n

SELECT     COUNT(\*)FROM    테이블명;

\n\n\n\n

대표적으로 자주사용하는 테이블을 카운트하여 비교하는것이 제일 정확

\n