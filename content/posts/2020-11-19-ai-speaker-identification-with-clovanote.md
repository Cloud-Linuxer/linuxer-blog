---
title: "AI-speaker-identification-with-clovanote"
date: 2020-11-19T12:46:16+09:00
draft: false
categories: ["기타"]
tags: ["clovanote", "ai", "화자구분"]
slug: "ai-speaker-identification-with-clovanote"
aliases:
  - /ai-speaker-identification-with-clovanote/
  - /ai-speaker-identification-with-clovanote/
---


오늘 클로바 노트 어플을 출시한걸 보고 사용해봤습니다.


[클로바노트-아이폰](https://apps.apple.com/gb/app/%ED%81%B4%EB%A1%9C%EB%B0%94%EB%85%B8%ED%8A%B8-ai-%EC%9D%8C%EC%84%B1%EA%B8%B0%EB%A1%9D/id1530010245)


[클로바노드-안드로이드](https://play.google.com/store/apps/details?id=com.naver.clova.minute&hl=ko&gl=US)


![](/images/2020/11/image-30-473x1024.png)

기능을 설명하자면 음성을 텍스트로 변환한다 ~ 이건 근래에 매우 일반화된 기능입니다.Speech Recognition 이라 합니다.
그런데, 이 어플은 음성->텍스트 변환 속도가 엄청나게 빠른것과 화자 구분기능이 있습니다. 화자 구분은 하나의 음성파일에서 각각 다른사람의 대화를 구분해주는 기능이죠.


이기능이 좋은이유는 장시간의 대화록에서 누가 어떤말을 했는지 각각 구분해 주므로 엄청난 편리성이 가미된것이죠.


![](/images/2020/11/image-31-473x1024.png)

위와같이 여러사람의 목소리를 구분해서 보여줍니다.


각각 벤더를 사용하시는 주변분들이 서비스에 대해 알려주셔서 찾아봤습니다.


NaverCloud


<https://www.ncloud.com/product/aiService/clovaSpeech>


Azure


<https://azure.microsoft.com/ko-kr/services/cognitive-services/speaker-recognition/>


GCP


<https://cloud.google.com/speech-to-text/docs/multiple-voices?hl=ko>


AWS


<https://aws.amazon.com/ko/transcribe/>


제가 AI의 트랜드와 기술력에 대해서 너무 몰랐다는 생각이 들었습니다.


각 벤더들마다 각자의 기술력으로 음성을 텍스트로 변환하고 화자구분기능을 모두 가지고있었습니다.


그러나, 이 아이디어 실제로 구현한다는건 많은 고민과 테스트가 필요할것으로 보입니다.


또한 번역API를 예로들면 파파고나 구글번역기의 정확도나 번역방식이 다르듯이 각나라의 음성을 텍스트로 변환하는 방식에서 쌓인 데이터에 의해 정확도가 다를것입니다.


그렇기에 현재는 네이버클로바의 정확도가 한글에 대해선 가장높지 않을까 예상됩니다.


어플덕분에 AI의 현기술의 변곡점과 치열한 벤더들간의 차이를 이해하게된 계기였습니다.


클로바노트의 건승을 기원합니다.


감사합니다.
