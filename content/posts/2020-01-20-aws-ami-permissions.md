---
title: "aws-ami-Permissions-ami공유"
date: 2020-01-20T14:24:53+09:00
draft: false
categories: ["AWS"]
tags: ["AMI", "권한", "공유"]
slug: "aws-ami-permissions"
aliases:
  - /aws-ami-permissions/
  - /aws-ami-permissions/
---

\n

ami 를 공유하는 방법을 포스팅해 볼까한다.

\n\n\n\n

계정간 인스턴스 이동을 진행하려면 꼭 알아야한다.

\n\n\n\n

ami 메뉴에서 권한수정을 클릭한다.

\n\n\n\n
![](/images/2020/01/image-67.png)
\n\n\n\n

공유할 계정의 aws 계정 번호를 입력하여 권한을 추가한다.

\n\n\n\n
![](/images/2020/01/image-65.png)
\n\n\n\n
![](/images/2020/01/image-66.png)
\n\n\n\n

공유된 계정에서 인스턴스 생성 페이지에서 나의 AMI에서 소유권에 나와 공유됨만 체크해본다.

\n\n\n\n
![](/images/2020/01/image-68.png)
\n\n\n\n

공유된 AMI를 확인한다.

\n\n\n\n

다른 방법으로 ami 를 확인할수 있는데

\n\n\n\n
![](/images/2020/01/image-69.png)
\n\n\n\n
![](/images/2020/01/image-70.png)
\n\n\n\n

공유 받은 계정에서 프라이빗 이미지를 검색해서 확인할수 있다.

\n\n\n\n\n\n\n\n

리전이 다르다면 스냅샷을 리전복사 한다음에 공유를 하자.

\n\n\n\n\n\n\n\n

끝!

\n