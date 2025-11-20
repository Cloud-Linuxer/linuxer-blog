---
title: "wordpress s3 cloudfront 적용하기"
date: 2019-09-24T23:18:49+09:00
draft: false
categories: ["AWS"]
tags: ["cloudfront", "s3", "cf", "wp upload", "upload", "s3 wordpress"]
slug: "wordpress-s3-cloudfront-적용하기"
aliases:
  - /wordpress-s3-cloudfront-적용하기/
  - /wordpress-s3-cloudfront-%ec%a0%81%ec%9a%a9%ed%95%98%ea%b8%b0/
---


줄곳 고민하던 s3-uploads / cdn-cloudfront 를 적용하였다.

먼저 wordpress 의 여러 플러그인중에 대중적이며 복잡하지 않은 방식을 채택하였다.

사용한 플러그인은 두가지이다.

![](/images/2019/09/Screenshot-2019-09-24-at-21.42.44-1024x53.jpg)

![](/images/2019/09/Screenshot-2019-09-24-at-21.43.12-1024x53.jpg)

**Amazon Web Services** / **WP Offload Media**

두개의 플러그인을 설치한다.

그리고 AmazonS3FullAccess 권한을 가진 사용자를 Programmatic access 방식으로 생성한다.

![](/images/2019/09/Screenshot-2019-09-24-at-22.22.17-1024x730.jpg)

그리고 버킷을 생성한다. AmazonS3FullAccess full acces 권한을 줬는데 이 권한은 업로드 권한만 줘도 무방하다. 하지만 편한 테스트를위해 전체 권한을 부여하였다.

![](/images/2019/09/Screenshot-2019-09-24-at-22.25.37-1024x666.jpg)

![](/images/2019/09/Screenshot-2019-09-24-at-22.25.58-1024x672.jpg)

일단 모든 퍼블릭 엑세스 차단을 해제한다. 나머지는 모두 기본설정이다.
위 설정은 편한 설정을 위한 선택이므로 각자 개인의 선택을 요한다.

![](/images/2019/09/Screenshot-2019-09-24-at-22.30.25.jpg)

미리 wp-content/uploads 폴더까지 생성한다. 그리고 cloudfront 를 생성한다.

![](/images/2019/09/Screenshot-2019-09-24-at-22.35.00-1024x636.jpg)

**Restrict Bucket Access** -yes
 **Origin Access Identity** - Create a New Identity
**Grant Read Permissions on Bucket** - Yes, Update Bucket Policy
위 순서대로 선택하면 s3 버킷 정책이 자동으로 삽입된다.

{
 "Version": "2008-10-17",
 "Id": "PolicyForCloudFrontPrivateContent",
 "Statement": [
 {
 "Sid": "1",
 "Effect": "Allow",
 "Principal": {
 "AWS": "arn:aws:iam::cloudfront:user/CloudFront Origin Access Identity E2BE1SUSFLL"
 },
 "Action": "s3:GetObject",
 "Resource": "arn:aws:s3:::linuxer-wp1/\*"
 }
 ]
 }

그리고 cloudfront는 https 로만 통신하기 떄문에 route53에 도메인을 생성하여 붙여주는게 좋다. 도메인을 붙일떈 acm 을 생성하여야 한다. acm은 버지니아 북부에서 생성한 acm만 사용할수 있다.

![](/images/2019/09/Screenshot-2019-09-24-at-22.36.11-1-1024x645.jpg)

![](/images/2019/09/Screenshot-2019-09-24-at-22.42.27-1024x320.jpg)

acm은 route53을 사용하면 버튼 클릭 한번으로 생성 가능하다. 하나의 acm에는 50개의 도메인을 추가할수 있다. 간단하게 linuxer.name \*.linuxer.name 을 추가하였다. 여기에 linuxer.com 이나 linuxer.kr namelinuxer.net 등 여러가지의 도메인을 한꺼번에 추가하여 사용할수 있다.

이후 cloudfront 를 생성한다. 이후에 wordpress 플러그인 설정화면으로 진입한다.

![](/images/2019/09/Screenshot-2019-09-24-at-22.47.31-1024x932.jpg)

엑세스키와 시크릿키를 입력하고 save를 하면 디비에 저장이 된다.
디비에 저장하고 싶지 않을경우에 wp-config.php 파일에 추가를 한다.

그리고 플러그인 Offload Media Lite 으로 진입하여 cname 설정을 진행한다.

![](/images/2019/09/Screenshot-2019-09-24-at-22.51.10-1024x162.jpg)

OFF 되어있는 버튼을 누르고 설정된 cloudfront 에 설정한 cname 을 입력한다.
이 설정을 마칠쯤이면 cloudfront 가 Deployed 상태로 변경될것이다.

그러면 이제 테스트 게시물을 작성하여 보자.

![](/images/2019/09/제목-없음-1024x829.png)

업로드가 정상적으로 이루어 지게 되면 이미지가 정상적으로 보이게되고 주소복사를 눌렀을떄 해당 페이지가 cdn 페이지로 열리면 정상적으로 upload-s3-cdn 이 구조로 생성이 된것이다.

그리고 s3 로 uploads 디렉토리를 이동하는것은 선택이다.

하지만 그부분도 진행하였다.

#aws configure
AWS Access Key ID [None]:
 AWS Secret Access Key [None]:
Default region name [None]:ap-northeast-2

aws configure 명령어를 이용하여 이전에 만든 엑세스 키를 입력하고 리전을 지정한다. 그리고 aws s3 명령어를 이용하여 sync 한다.

#aws s3 sync wp-content/uploads/ s3://linuxer-wp/설정한 경로

이전에 업로드된 파일때문에 위와같은 작업을 진행하는것이므로 새로생성하는 wordpress 의 경우엔 하지않아도 괜찮다.

이후로 업로드되는 파일은 s3로 업로드되고 view 는 cloudfront 에서 진행될 것이다.

오늘의 포스트 주제를 주신 전산직 님께 감사드린다!

좋은하루 되시라!
