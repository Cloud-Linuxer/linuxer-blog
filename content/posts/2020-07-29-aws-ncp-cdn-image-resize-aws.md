---
title: "AWS-NCP-CDN-image-resize-AWS"
date: 2020-07-29T13:07:40+09:00
draft: false
categories: ["AWS"]
tags: ["resize", "lamdba", "edge"]
slug: "aws-ncp-cdn-image-resize-aws"
aliases:
  - /aws-ncp-cdn-image-resize-aws/
  - /aws-ncp-cdn-image-resize-aws/
---


AWS 에선 Lambda@Edge를 이용한 Image Resise를 할수 있습니다.


[당근마켓-Lambda@Edge를 사용한 썸네일 생성](https://medium.com/daangn/lambda-edge%EB%A1%9C-%EA%B5%AC%ED%98%84%ED%95%98%EB%8A%94-on-the-fly-%EC%9D%B4%EB%AF%B8%EC%A7%80-%EB%A6%AC%EC%82%AC%EC%9D%B4%EC%A7%95-f4e5052d49f3)


![](https://miro.medium.com/max/3840/1\*H9K0lybLb1FzSh2Ss9KW-w.png)

구성도는 위와 같습니다. 이걸 저도 다른 아키텍쳐로 구성한 경험이 있습니다.


따라하면 되는 부분을 빼버리고 좀 포인트가 필요한 부분만 정리를 하려 합니다.


![](/images/2020/07/image-23-1024x761.png)

Lambda는 이미 생성해둔 상태이고 역할도 부여해서 이제 Lambda@edge 로 배포하는 과정을 진행하는것입니다.


![](/images/2020/07/image-24-1024x129.png)

다음과 같은 메시지가 표시되면 배포가 시작된거라 생각하면 됩니다.


![](/images/2020/07/image-25-1024x362.png)

Designer에 위와 같이 trigger에 cloudfront 가 추가됩니다. 그럼 이 Lambda@edge는 CF의 Behaviors에서 확인할수 있습니다.


![](/images/2020/07/image-26.png)

또한 CF의 Behaviors에 자동으로 추가가 된거까지 보이고, CF의 Status 가 Enabled 상태이면 각 엣지에 Lambda@edge가 정상적으로 배포되었다고 볼수있습니다.


[원본이미지](https://linuxer.name/wp-content/uploads/2020/07/exam-az301-600x600-1.png)


<https://linuxer.name/wp-content/uploads/2020/07/exam-az301-600x600-1.png>


[리사이즈 이미지](https://linuxer.name/wp-content/uploads/2020/07/exam-az301-600x600-1.png?w=200&h=150&f=webp&q=100)


<https://linuxer.name/wp-content/uploads/2020/07/exam-az301-600x600-1.png?w=200&h=150&f=webp&q=100>


위와 같이 리사이즈된것을 확인할수 있습니다. URL 수정을 통해 리사이즈를 컨트롤 할수 있습니다


* - w: '200'
* - h: '150'
* - f: 'webp'
* - q: '90'


Cloud9을 이용하여 배포하고 수정하는 과정 자체가 불편하긴 하나, AWS의 인프라를 이용하여 serverless 환경에서 리사이즈 배포 저장공간 추가로 사용하지 않음 등의 잇점을 생각할때 매우 좋은 방법이라는 생각이 들었습니다.


이때 비용을 생각하지 않을수 없습니다.


REPORT RequestId: 9e879aa6-390e-432b-9baf-84f45b238a4b Duration: 1.88 ms Billed Duration: 50 ms Memory Size: 128 MB Max Memory Used: 107 MB


1회 실행한 로그이며, cloudwatch log group에서 확인할수 있었습니다. 계산은 제 블로그의 이미지 리퀘스트 횟수를 빗대어 계산해 보겠습니다.


All Requests: Total: 45.285 K


저는 Cloudfront 를 이용하여 Image를 제공하고 있고 월 평균 5만건 정도의 리퀘스트가 발생합니다.


1회요청당 0.0000006 USD \* 50000 = 0.003 USD 입니다.


여기에 50ms 를 0.05 \* 50000 = 2500 초를 실행한게 됩니다.


1초당 컴퓨팅 요금은 0.00000625125 USD입니다. 거기에 2500초를 곱합니다.


0.015628125 USD 입니다.


그럼 두가지 계산된 비용을 합칩니다.


0.018628125 USD가 한달 비용으로 발생하게 됩니다. 썼다면 너무 미미한 양이라 과금되는줄도 모르고 썼겠군요..또한 이건 단순계산으로 캐싱된것을 CDN에서 응답하면 람다 사용횟수가 80%는 줄어 들겁니다. HIT율이 80%는 되기 때문입니다.


한화로 환율을 계산하면 22원입니다. 계산이 무의미 하진 않지만..


정말 작은 돈으로 리사이즈를 할수 있다는것을 알수 있었습니다.


이 다음 포스팅은 NCP에서 image-resize를 사용해보고 비용계산을 진행해보려 합니다.


읽어주셔서 감사합니다.
