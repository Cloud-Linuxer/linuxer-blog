---
title: "AWS Certified DevOps Engineer - Professional-Review - DOP-C01"
date: 2020-09-14T18:24:34+09:00
draft: false
categories: ["AWS", "Certification"]
tags: ["pro", "dop", "dop-c01", "devops"]
slug: "aws-certified-devops-engineer-c01-professional-review"
aliases:
  - /aws-certified-devops-engineer-c01-professional-review/
  - /aws-certified-devops-engineer-c01-professional-review/
---


일명 DOP 라 불리는 시험으로 AWS 에서 존재하는 2개의 pro 시험중 하나이다.


1차 8월 30일
2차 9월 14일 오늘이다.


8월 30일 시험으로는


![](/images/2020/09/image-7.png)

698 점이었다. 52점이 모자랐다.


시험을 보고난뒤 현타가 왔지만 자아성찰을 했다.


나는 서비스는 다써봤다.
안 써봤을리 없지.. 그많은 기간 테스트를 해봤으니, 그런데 단순테스트와 서비스에 대한 개념만으로는 나는 DOP를 통과할수 없었다. SAP 때의 지옥이 떠올랐다. 물론 SAP는 서비스 콤비네이션에 대한 질문이 주를 이루므로 각각의 상황에 알맞는 솔루션을 선택하는거라 나의 주종목인 넓고알기에 딱 어울리는 시험이었다. 그러나 DOP는 좀 달랐다.


나는 개발자로서의 경험이 1도 없는 사람이다. 엔지니어로서 오랜기간 일을했고, git 이나, svn, codecommit 등의 서비스를 써본적은 있어도 말 그대로 써본거지 실제로 내가 이걸 활용해 본적이 없는 것이다. 그렇기에 기능분기라던가 마스터 브랜치 같은 개념이나 아티펙트같은 개념이 잘 와 닿지 않았다.


이 모든건 내가 개발자가 아니기에 OPS의 의 영역엔 강할수 있어도 DEV의 영역에는 이해도가 낮았다 라고 판단했다. 그래서 시험에 떨어진 이후, 나는 CI/CD의 Best Practice를 주로 학습하고 여러명의 개발자가 코드분기 패턴이나 승인 패턴, 테스트패턴에 대한 학습을 했다.


그리고 오늘 시험보기 전에 어느정도 확신이 섰다. 내가 뭘몰랐는지에 대한 이유를 알았기 때문이었다. 역시 시험장은 솔데스크가 좋다. 영우글로벌도 좋은데..


각설하고 학습과정은 이렇다.


먼저 자격증의 요구사항을 분석한다.


<https://d1.awsstatic.com/ko_KR/training-and-certification/docs-devops-pro/AWS-Certified-DevOps-Engineer-Professional_Exam-Guide.pdf>


시험 안내서면 충분하다.


<https://d1.awsstatic.com/ko_KR/training-and-certification/docs-devops-pro/AWS-Certified-DevOps-Engineer-Professional_Sample-Questions.pdf>


샘플문항을 풀어본다.


각자의 공부방법이 있겠지만 acloudguru나 udemy 등을 이용해서 공부해도 좋다.
그리고 나는 youtube 도 애용하는 편이다.


서비스는 사실.. 뭐...


https://jayendrapatil.com/aws-certified-devops-engineer-professional-exam-learning-path/


파틸아저씨의 블로그를 서비스 항목만 참고해서 aws 상에서 만들어 보고 혼자서 실습을 한다. 주로 헤딩을 하며, 생성 구성 사용을 해보고 docs를 나중에 본다.


정독은 쉽지 않다.


어느정도 준비가 되면 연습시험을 본다. 시험 한번합격시에 연습시험 쿠폰을 1개를 주니, 무료 연습시험을 꼭보자.


연습시험에서 낮은 점수를 기록했다해도, 본시험은 그보다 난이도가 낮은 문제가 많이 나오니 너무 걱정말자. 그렇지만.. 걱정 안했다가 내가 8월30일 불합격을 맛봤다.


그 이후 이주간 개발자의 방법을 알기위한 노력을 끊임없이 진행했다.


그중에 가장 많이본건 CI/CD다...


그외에 아키텍처부분은 뭐..그냥 쏘쏘.....


<https://aws.amazon.com/ko/products/developer-tools/>


크게는 여기서 개발자 툴의 범주를 확인했고


<https://aws.amazon.com/ko/codepipeline/faqs/>


<https://aws.amazon.com/ko/codebuild/faqs/?nc=sn&loc=5>


<https://aws.amazon.com/ko/codecommit/faqs/>


<https://aws.amazon.com/ko/codedeploy/?c=dv&sec=srv>


<https://aws.amazon.com/ko/codeartifact/faq/>


<https://aws.amazon.com/ko/xray/?c=dv&sec=srv>


람다를 운영에서 사용하는 방법을 봤다. .serverless 에서의 lambda는 컴퓨팅을 담당하지만 DOP에서의 lambda는 AWS에서의 서비스간 역할을 강하게 묶어주는 역할이 더많은것같다.


<https://aws.amazon.com/ko/lambda/faqs/>


AWS Lambda를 사용하여 AWS 이벤트 처리


이 부분이 중요하다. 그리고 또 Cloudfromation AWS 에서 IaC를 맡고 있으므로 굉장히 중요..그리고 Elasticbeanstalk 아직 ECS 나 EKS는 시험에 드물게 나온다.


또한 배포방식..


<https://aws.amazon.com/ko/premiumsupport/knowledge-center/codepipeline-deploy-cloudformation/>


이런 자습서 꼭 참고하자..보기만 해도 도움이 된다.


https://www.youtube.com/watch?v=NwzJCSPSPZs


https://www.youtube.com/watch?v=T5SyIGKZ0x4


https://www.youtube.com/watch?v=sTTvZ5ItZG0


내가 DOP를 이해하기위해 본것들이다.


정리를 하며 본건 아니라서 좀 중구난방인데 도움이 되길 바란다.


![](/images/2020/09/image-8-1024x418.png)

890점으로 통과했고,


![](https://www.certmetrics.com/amazon/Telerik.Web.UI.WebResource.axd?imgid=24dd2b523d434c689475dc8277ab6163&type=rbi)

![](/images/2020/09/image-9-1024x792.png)

자격증 까지 나왔다.


근래에 자격증 발급속도가 당일 발급이라 만족스럽다.


읽어주셔서 감사합니다!


다음에 또 읽어주세요.!
