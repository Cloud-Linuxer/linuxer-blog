---
title: "aws-waf.ver2-review-2-test"
date: 2020-02-02T21:46:58+09:00
draft: false
categories: ["AWS"]
tags: ["aws", "aws waf", "waf", "wafver2"]
slug: "aws-waf-ver2-review-2-test"
aliases:
  - /aws-waf-ver2-review-2-test/
  - /aws-waf-ver2-review-2-test/
---


**Hostcenter 의 Acunetix 취약점 점검툴을 사용하였습니다.**


<https://www.hostcenter.co.kr/Security/security01.aspx>


aws waf.ver2 관리형룰의 성능을 테스트 하고 싶었다.


마침 회사에 web 취약점 점검툴이 있었다. 그래서 테스트를 진행했다.


먼저 COUNT 모드로 점검을 진행했다.


총 점검시간 4시간 15000번의 리퀘스트가 있었다. 첫번째 테스트는 1월10일 두번째 테스트는 1월 30일 이었다.


빨리 진행하고 싶었는데 좀 바빳다.


![](/images/2020/02/image-10-1024x648.png)

1월10일 모니터링 모드 스캔 결과


![](/images/2020/02/image-11-1024x680.png)

1월 30일 차단모드 스캔결과


간략한 결과로만 봐도 high단계의 취약점이 사라리고 medium 단계의 취약점이 하나 사라졌다.


그럼 어떻게 막혔는지 리뷰를 해야하는데...


![](/images/2020/02/image-12-1024x336.png)

일단 테스트시간에 막힌 리퀘스트는 3000개 정도. 15000만건중 20%정도가 막혔다.


![](/images/2020/02/image-13-1024x432.png)

![](/images/2020/02/image-14.png)

Description
Contains rules that are generally applicable to web applications. This provides protection against exploitation of a wide range of vulnerabilities, including those described in OWASP publications and common Common Vulnerabilities and Exposures (CVE).
Capacity: 700


룰중 가장 많은 *Capacity* 를 사용하는 AWS-AWSManagedRulesCommonRuleSet 룰에서 역시나 많은 지분을 차지했다.


분석결과를 설명하기 보단 waf 를 사용해서 확인한 취약점리포트의 일부를 공개하는쪽으로 블로깅을 마친다.


waf 사용전


[linuxer-test1](https://linuxer.name/wp-content/uploads/2020/02/linuxer-test1.pdf)[다운로드](https://linuxer.name/wp-content/uploads/2020/02/linuxer-test1.pdf)


waf 사용후


[linuxer-test2](https://linuxer.name/wp-content/uploads/2020/02/linuxer-test2.pdf)[다운로드](https://linuxer.name/wp-content/uploads/2020/02/linuxer-test2.pdf)


블로깅이 좀 애매한데 다음엔 로깅을 남겨서 다음 포스팅을 준비해보겠다.
