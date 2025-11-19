---
title: "aws cloud watch 여러대의 인스턴스에 대한 하나의 경보 생성.ver2"
date: 2019-08-26T17:26:29+09:00
draft: false
categories: ["AWS", "Linux"]
tags: ["aws", "watch", "경보생성", "여러대", "수학표현식"]
slug: "aws-cloud-watch-여러대의-인스턴스에-대한-하나의-경보-생성"
aliases:
  - /aws-cloud-watch-여러대의-인스턴스에-대한-하나의-경보-생성/
  - /aws-cloud-watch-%ec%97%ac%eb%9f%ac%eb%8c%80%ec%9d%98-%ec%9d%b8%ec%8a%a4%ed%84%b4%ec%8a%a4%ec%97%90-%eb%8c%80%ed%95%9c-%ed%95%98%eb%82%98%ec%9d%98-%ea%b2%bd%eb%b3%b4-%ec%83%9d%ec%84%b1/
---

\n

cloudwatch 경보생성 입니다.

\n\n\n\n

여러대의 인스턴스를 하나로 묶어서 경보생성할때 사용하는 방법입니다.

\n\n\n\n
![](/images/2019/08/image-4-1.png)
\n\n\n\n

경보 생성을 누릅니다.

\n\n\n\n\n\n\n\n

* ![](/images/2019/08/image-3-1.png)

\n\n\n\n\n\n\n\n

지표 선택을 눌러서 지표를 확인합니다.이번에 경보를 생성할 지표는 "CPUUtilization"입니다.

\n\n\n\n\n\n\n\n

* ![](/images/2019/08/image-1.jpeg)

\n\n\n\n
![](/images/2019/08/image-6.png)
\n\n\n\n

검색하여 체크 후에 '그래프로 표시된 지표' 를 누릅니다.  
\n표시된 지표는 9개 까지 체크하여 추가할수 있습니다.

\n\n\n\n

제한사항으로

\n\n\n\n
![](/images/2019/08/image-5.png)
\n\n\n\n

 수학표현식을 추가합니다.  
수학 표현식은 상황에 따라 잘 사용하기로 바랍니다.<https://docs.aws.amazon.com/ko_kr/AmazonCloudWatch/latest/monitoring/using-metric-math.html>  
이번에는 CPU사용량이 1대라도 70% 를 넘을 경우 경보를 생성할 것이므로 사용한 표현식은 MAX(METRICS()) 입니다.

\n\n\n\n

* ![](/images/2019/08/image-9-1.png)

\n\n\n\n\n\n\n\n

전체를 체크할 경우 아래와 같이 지표선택 버튼이 활성화 되지 않습니다.

\n\n\n\n

* ![](/images/2019/08/image-8-1.png)

\n\n\n\n

사용할 수학 표현식 하나만 체크해야 생성이 가능합니다.

\n\n\n\n

* ![](/images/2019/08/image-7-1.png)

\n\n\n\n

위와같이 지표를 생성후에 경보생성은 SNS 를 사용해야 하므로 SNS 사용법은 각자 확인해보시기 바랍니다.

\n\n\n\n

즐거운 하루되세요~

\n