---
title: "AWS-FinOps-S3-incomplete-multipart-uploads-MPU"
date: 2022-08-13T21:52:03+09:00
draft: false
categories: ["AWS", "FinOps"]
tags: ["s3", "MPU", "incomplete multipart uploads"]
slug: "aws-finops-s3-incomplete-multipart-uploads-mpu"
aliases:
  - /aws-finops-s3-incomplete-multipart-uploads-mpu/
  - /aws-finops-s3-incomplete-multipart-uploads-mpu/
---

\n

S3는 청크 단위로 파일을 잘라서 업로드 할수있는 기능을 제공한다.

\n\n\n\n

이 기능의 정식명칭은 multipart upload 이다.

\n\n\n\n

<https://docs.aws.amazon.com/AmazonS3/latest/userguide/mpuoverview.html>

\n\n\n\n\n\n\n\n

MPU라고 줄여서 부른다.

\n\n\n\n\n\n\n\n

MPU는 업로드 속도를 빠르게 해줄수있는 아주 좋은 기능이지만, 업로드에 실패할 경우 완성되지 않은 청크단위의 파일들이 S3스토리지에 저장되게 된다. 업로드가 정상적으로 이루어진 경우 청크단위로 나뉜 파일을 하나의 파일로 합쳐서 객체로 보이게 되지만, 그렇지 않은 파일은 우리의 눈에 보이지 않지만 S3의 스토리지에 비용만 발생시키며, 하등 쓸모없는 상태로 저장만 되어있는다. 이런 경우를 "incomplete multipart uploads" 라 부른다.

\n\n\n\n

**불완전 멀티파트 업로드**/**완료되지 않은 멀티파트 업로드** 는 Lifecycle 를 통해 삭제 할수있다. 간단한 정책을 만들어서 보여주고자 한다.

\n\n\n\n

설정은 S3 버킷 에서 관리로 가면 수명주기 규칙으로 설정할수 있다.

\n\n\n\n

이설정은 모든 버킷에서 통용적으로 사용할수 있는 규칙이므로 버킷을 생성할때 무조건 넣어도 좋다.

\n\n\n\n
![](/images/2022/08/image-12-824x1024.png)
\n\n\n\n

위와같이 "만료된 객체 삭제 마커 또는 완료되지 않은 멀티파트 업로드 삭제" 체크후 "불완전 멀티파트 업로드 삭제" 를 체크하면 된다. 일수는 1일이 최소값이다.

\n\n\n\n
![](/images/2022/08/image-13-1024x465.png)
\n\n\n\n

정상적으로 삭제가 동작하면 이런식으로 S3 dashboard에서 불완전한 멀티파트업로드 바이트 차트가 0B로 변경되는것을 확인할수 있다.

\n\n\n\n\n\n\n\n

불완전 MPU는 대표적으로 이런경우 생성된다.

\n\n\n\n

MPU 업로드 실패.  
Athena 쿼리 실패  
Redshift UNLOAD 실패등

\n\n\n\n

AWS 서비스에서 S3로 저장하는 액션을 취하다 실패하는경우가 있다면 대부분 "불완전 MPU"가 생성될것이다.

\n\n\n\n

AWS S3 대시보드를 확인하여 "불완전한 MPU" 를 확인하고 삭제해보자.

\n\n\n\n

바닥에 흘리고 다니던 눈먼 동전 줍기가 될것이다.

\n\n\n\n\n\n\n\n

읽어주셔서 감사하다!   
앞으로도 FinOps 시리즈로 찾아 뵙겠다.

\n\n\n\n\n