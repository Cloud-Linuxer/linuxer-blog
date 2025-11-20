---
title: "Wordpress-https"
date: 2020-09-11T00:56:00+09:00
draft: false
categories: ["기타"]
slug: "wordpress-https"
aliases:
  - /wordpress-https/
  - /wordpress-https/
---


![](/images/2020/09/image-5.png)

워드 프레스를 사용하는 사이트중에 이런메시지가 뜬다

**이 사이트의 보안 연결(HTTPS)은 완벽하지 않습니다.**

이건 모든 컨텐츠가 HTTPS로 전송되지 않고 HTTP로 전송되는 컨텐츠가 있다는 이야기다.

이경우에 모든 컨텐츠를 HTTPS 로 전송하도록 몇줄만 넣어주면 된다.

vi 로 wp-admin.php 를 열고 <?php 뒤에 붙여 넣어주자.

--소스가 waf에 걸려서 업로드가 안된다-_-; 마음에 여유가 생기면...--

<https://wordpress.stackexchange.com/questions/170165/wordpress-wp-admin-https-redirect-loop>

여기서 57번 답변을 참조하자

이것만 넣으면 모든 컨텐츠가 HTTPS 로 전송된다.
