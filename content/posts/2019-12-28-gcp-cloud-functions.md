---
title: "GCP Cloud Functions"
date: 2019-12-28T16:35:47+09:00
draft: false
categories: ["GCP"]
tags: ["gcp", "gcp cloudfuntionc", "resize", "리사이즈"]
slug: "gcp-cloud-functions"
aliases:
  - /gcp-cloud-functions/
  - /gcp-cloud-functions/
---


12월 29일 미션으로 Cloud Functions 이 포함되어있다.

미션은 이미지 업로드 후 리사이즈.

먼저 cloud functions 이 뭔지부터 알아야 한다. aws 에서 말하는 서버리스 컴퓨팅 서비스이다. 일반적으로 코어나 메모리를 정적으로 할당받아서 사용하는 방식이 아닌것이다.

먼저 Cloud Functions을 사용하기 위해서 진행해야 할 작업이 있다.

gcp의 큰장점을 cloudshell 을 지원한다는 것이다. 인스턴스쉘 이긴 하나 언제 어디서나 shell을 사용할수 있다.

먼저 cloudshell을 실행하면 이런 창이뜬다.

![](/images/2019/12/image-8.png)

여기에 Cloud Functions 을 사용하기 위한 환경을 우선적으로 구성해야 한다.

먼저 cloudshell 은 굉장히 퓨어한 상태로 프로젝트부터 설정해줘야한다.

hoceneco@cloudshell:~$ gcloud config set project sage-facet-22972
 Updated property [core/project].
 hoceneco@cloudshell:~ (sage-facet-22972)

gcloud config set project 명령어로 지정하고

hoceneco@cloudshell:~ (sage-facet-22972)$ gcloud config list
 [component_manager]
 disable_update_check = True
 [compute]
 gce_metadata_read_timeout_sec = 5
 [core]
 account =
 disable_usage_reporting = False
 project = sage-facet-22972
[metrics]
 environment = devshell

gcloud config list 명령어로 지정된 리스트를 확인할 수 있다.

hoceneco@cloudshell:~ (sage-facet-22972)$ sudo gcloud components update
Your current Cloud SDK version is: 274.0.0
 You will be upgraded to version: 274.0.1
┌──────────────────────────────────────────────────┐
 │ These components will be updated. │
 ├──────────────────────────┬────────────┬──────────┤
 │ Name │ Version │ Size │
 ├──────────────────────────┼────────────┼──────────┤
 │ Cloud SDK Core Libraries │ 2019.12.27 │ 12.7 MiB │
 └──────────────────────────┴────────────┴──────────┘

gcloud 구성요소를 업데이트한다 - 꼭할필요는 없다.

오늘 미션에서 필요한 준비물은 Cloud Functions, Google Cloud Vision API, ImageMagick, Cloud Storage 이렇게 다.

hoceneco@cloudshell:~ (sage-facet-22972)$ gsutil mb gs://linuxer-upload
 Creating gs://linuxer-upload/…
 hoceneco@cloudshell:~ (sage-facet-22972)$ gsutil mb gs://linuxer-convert
 Creating gs://linuxer-convert/…

linuxer-upload, linuxer-convert 버킷을 생성하고, 이름에 따라 업로드 와 리사이즈된 이미지를 넣을 버킷이다.

hoceneco@cloudshell:~ (sage-facet-229723)$ git clone https://github.com/GoogleCloudPlatform/nodejs-docs-samples.git
 Cloning into 'nodejs-docs-samples'…
 remote: Enumerating objects: 17312, done.
 remote: Total 17312 (delta 0), reused 0 (delta 0), pack-reused 17312
 Receiving objects: 100% (17312/17312), 15.29 MiB | 7.22 MiB/s, done.
 Resolving deltas: 100% (11332/11332), done.
 hoceneco@cloudshell:~ (sage-facet-229723)$ cd nodejs-docs-samples/functions/imagemagick

git clone https://github.com/GoogleCloudPlatform/nodejs-docs-samples.git
명령어를 이용하여 test code를 다운받고 다운받은 디렉토리로 이동한다.
일단 먼저 테스트하는것은 아래 Docs 를 참고하여 진행하였다.

<https://cloud.google.com/functions/docs/tutorials/imagemagick?hl=ko>

**"버킷에 업로드되는 이미지 중 불쾌감을 주는 이미지를 감지하고 이를 흐리게 처리하는 방법을 설명합니다."** 라고 한다.

hoceneco@cloudshell:~/nodejs-docs-samples/functions/imagemagick (sage-facet-22972)$ gcloud functions deploy blurOffensiveImages --trigger-bucket=gs://linuxer-upload --set-env-vars BLURRED_BUCKET_NAME=gs://linuxer-convert --runtime=nodejs8
 Deploying function (may take a while - up to 2 minutes)…done.
 availableMemoryMb: 256
 entryPoint: blurOffensiveImages
 environmentVariables:
 BLURRED_BUCKET_NAME: gs://linuxer-convert
 eventTrigger:
 eventType: google.storage.object.finalize
 failurePolicy: {}
 resource: projects/_/buckets/linuxer-upload
 service: storage.googleapis.com
 labels:
 deployment-tool: cli-gcloud
 name: projects/sage-facet-22972/locations/us-central1/functions/blurOffensiveImages
 runtime: nodejs8
 serviceAccountEmail: sage-facet-229723@appspot.gserviceaccount.com
 sourceUploadUrl: https://storage.googleapis.com/gcf-upload-us-central1-ede08b3c-b370-408b-ba59-95f296f42e3e/40187a52-802f-4924-98d1-8802e41b24da.zip?GoogleAccessId=service-300346160521@gcf-admin-robot.iam.gserviceaccount.com&Expires=1577509811&Signature=gUhzdRazlnkRrUgPmv2P3tjdw%2BtXTDZq1FDZtzchPBJjkn5trLN6c27mawLRneazA5%2FLFZuUCmBLXIb9%2B5Iaq2M6cM0c9kzCpKGrk41W%2Boh3ST4ybWHsxd1YZi9G4J0uCKCSs1aLw4WPcQ7nCRJhDv5pqBbXXIJUvFTkQqUzH98TnEx2o2u9aJd44iyrpWwEiirxG%2BxHk1sVBBKpdUAbJb%2FYOT0lzH6%2F7y%2FOP51A0kEcRtAbmPYHSt87%2FGZOrNn2qHdQWap4MiT%2BYd4eVLOLTkd%2Fmvv8%2FcjWS4cousamOq8FSvvDC%2BQmvf01AGOgt%2BBrHyDkmAlrLvzemw6989BFlA%3D%3D
 status: ACTIVE
 timeout: 60s
 updateTime: '2019-12-28T04:40:54Z'
 versionId: '1'

gcloud functions deploy 명령어로 functions 을 생성하면 된다. runtime 설정이 각각 사용하는 언어마다 다르므로 버전을 잘확인해보자.

생성이끝나면 명령어로 이미지를 업로드해본다.

hoceneco@cloudshell:~/nodejs-docs-samples/functions/imagemagick (sage-facet-22972)$ gsutil cp zombie-949916_1280.jpg gs://linuxer-upload
 Copying file://zombie-949916_1280.jpg [Content-Type=image/jpeg]…
[1 files][355.3 KiB/355.3 KiB]
 Operation completed over 1 objects/355.3 KiB.

이미지 업로드가 끝나면 functionc로그를 확인하면 정상작동됬는지 확인할수 있다.
첫번째 업로드에선 api 에러가 발생했는데. 이때 콘솔에서 api 를 사용할수 있도록 설정해줬다.

E blurOffensiveImages 909862418886020 2019-12-28 03:42:15.967 Error: 7 PERMISSION_DENIED: Cloud Vision API has not been used in project 300346160521 before or it is disabled. Enable it by visiting https://console.developers.google.com/apis/api/vision.googleapis.com/overview?project= then retry. If you enabled this API recently, wait a few minutes for the action to propagate to our systems and retry.
 at Object.callErrorFromStatus (/srv/node_modules/@grpc/grpc-js/build/src/call.js:30:26)
 at Http2CallStream.call.on (/srv/node_modules/@grpc/grpc-js/build/src/client.js:96:33)
 at emitOne (events.js:121:20)
 at Http2CallStream.emit (events.js:211:7)
 at process.nextTick (/srv/node_modules/@grpc/grpc-js/build/src/call-stream.js:97:22)
 at _combinedTickCallback (internal/process/next_tick.js:132:7)
 at process._tickDomainCallback (internal/process/next_tick.js:219:9)
 D blurOffensiveImages 909862418886020 2019-12-28 03:42:16.027 Function execution took 570 ms, finished with status: 'error'

<https://console.developers.google.com/apis/api/vision.googleapis.com/overview?project=>

링크를 눌러서 이동해서 사용하기 누르면 오래걸리지 않아 api 를 사용할수 있다.
그리고 이미지를 재업로드 하고 로그를 확인하면 다음과 같다.

hoceneco@cloudshell:~/nodejs-docs-samples/functions/imagemagick (sage-facet-229723)$ gcloud functions logs read --limit 100

D blurOffensiveImages 909862418886020 2019-12-28 03:42:16.027 Function execution took 570 ms, finished with status: 'error'
 D blurOffensiveImages 909865384788642 2019-12-28 03:47:22.883 Function execution started
 I blurOffensiveImages 909865384788642 2019-12-28 03:47:28.294 Analyzing zombie-949916_1280.jpg.
 I blurOffensiveImages 909865384788642 2019-12-28 03:47:29.696 Detected zombie-949916_1280.jpg as inappropriate.
 I blurOffensiveImages 909865384788642 2019-12-28 03:47:30.683 Downloaded zombie-949916_1280.jpg to /tmp/zombie-949916_1280.jpg.
 I blurOffensiveImages 909865384788642 2019-12-28 03:47:40.091 Blurred image: zombie-949916_1280.jpg
 I blurOffensiveImages 909865384788642 2019-12-28 03:47:40.414 Uploaded blurred image to: gs://gs://linuxer-convert/zombie-949916_1280.jpg
 D blurOffensiveImages 909865384788642 2019-12-28 03:47:40.419 Function execution took 17551 ms, finished with status: 'ok'
 D blurOffensiveImages 909860416701916 2019-12-28 03:51:04.290 Function execution started
 I blurOffensiveImages 909860416701916 2019-12-28 03:51:04.295 Analyzing zombie-949916_1280.jpg.
 I blurOffensiveImages 909860416701916 2019-12-28 03:51:05.663 Detected zombie-949916_1280.jpg as inappropriate.
 I blurOffensiveImages 909860416701916 2019-12-28 03:51:06.283 Downloaded zombie-949916_1280.jpg to /tmp/zombie-949916_1280.jpg.

정상적으로 컨버팅이 된거다.

원본

![](/images/2019/12/image-12.png)

블러처리된것.

![](/images/2019/12/image-11.png)

자동으로 블러 처리가 완료된것을 확인할수 있다.

오늘의 미션은 resize이므로 resize를 하기위해선 index.js를 수정해야한다.
오늘의 실습에선 GraphicsMagick for node.js 을 이용해서 테스트를 진행했으므로 아주 수월했다. 원래사용한 blur 부분만 수정하면 될거 같았다.

<https://aheckmann.github.io/gm/docs.html>

blur
 Accepts a radius and optional sigma (standard deviation).
 gm("img.png").blur(radius [, sigma])

옵션은 위와 같고

resize
 Resize the image.
options
 %, @, !, < or > see the GraphicsMagick docs for details
 gm("img.png").resize(width [, height [, options]])
 To resize an image to a width of 40px while maintaining aspect ratio: gm("img.png").resize(40)
 To resize an image to a height of 50px while maintaining aspect ratio: gm("img.png").resize(null, 50)
 To resize an image to a fit a 40x50 rectangle while maintaining aspect ratio: gm("img.png").resize(40, 50)
 To override the image's proportions and force a resize to 40x50: gm("img.png").resize(40, 50, "!")

그러니까

![](/images/2019/12/image-13.png)

이부분을 .blur(0, 16) 부분을 resize 옵션으로 변경만 하면되는것이다.

![](/images/2019/12/image-14.png)

.resize(200, 200) 으로 수정을 하였다.
그리고 functions deploy 하고

gcloud functions deploy blurOffensiveImages --runtime nodejs8 --trigger-bucket=gs://linuxer-upload --set-env-vars BLURRED_BUCKET_NAME=gs://linuxer-convert
 Deploying function (may take a while - up to 2 minutes)…done.
 availableMemoryMb: 256
 entryPoint: blurOffensiveImages
 environmentVariables:
 BLURRED_BUCKET_NAME: gs://linuxer-convert
 eventTrigger:
 eventType: google.storage.object.finalize
 failurePolicy: {}
 resource: projects/_/buckets/linuxer-upload
 service: storage.googleapis.com
 labels:
 deployment-tool: cli-gcloud
 name: projects/sage-facet-22972/locations/us-central1/functions/blurOffensiveImages
 runtime: nodejs8
 serviceAccountEmail: sage-facet-22972@appspot.gserviceaccount.com
 sourceUploadUrl: https://storage.googleapis.com/gcf-upload-us-central1-ede08b3c-b370-408b-ba59-95f296f2e3e/4a80effd-0371-4317-8651-0416cffc0563.zip?GoogleAccessId=service-300346160521@gcf-admin-robot.iam.gserviceaccount.com&Expires=1577519172&Signature=CrNrgjDfo8gsr%2FoeGkcEiRvnMskkK5J4JHRoDMyh9DpXnXmp4ivWOlRsQ136GL9iK4FBvsxmAtIby4WgTECry4dYU%2FN6UkfjZSBLVtzJnJxR%2F5h7ZLY9PMd%2BDYcV1AAVbw9i1paFgBNjAq1WhNiMmmXonFBpyRHBlqMLn4CKuW7QAmA7NXOugTpQY3b%2BQ9E1ia9uIZtNwqcKfv1C1GM8e2%2FdKhMwwlUPU2EYy9gb4nirHvsdrYbzdewabmPwlRtgq1b2wTjWiuMM53vO9fDy6skNaB58tqumSfUeHM%2FTrjQrlqGejjon2cx9IlH9xF5kGKfLGzBesXEHj%2B6K6ZqilA%3D%3D
 status: ACTIVE
 timeout: 60s
 updateTime: '2019-12-28T07:17:00Z'
 versionId: '5'

정상적으로 생성이 되면 업로드를 진행하였다.

D blurOffensiveImages 909966712855810 2019-12-28 07:17:16.904 Function execution started
 I blurOffensiveImages 909966712855810 2019-12-28 07:17:17.003 Analyzing zombie-949916_1280.jpg.

functions 이 정상적으로 실행이 완료되고

![](/images/2019/12/image-15.png)

이미지가 리사이즈 되는것을 확인할수 있었다.
 355.3KB -> 12.69KB로 작아졌다. 물론이미지 사이즈도..

lamdba에 비해 사용이 너무편해서 깜짝놀랐다.

기능과 범위에 대해 알수있는 미션이었다. 유익함 별 다섯개.
