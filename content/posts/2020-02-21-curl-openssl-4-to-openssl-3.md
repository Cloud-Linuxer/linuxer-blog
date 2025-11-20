---
title: "curl-openssl_4 to openssl_3"
date: 2020-02-21T16:00:56+09:00
draft: false
categories: ["Linux"]
tags: ["libcurl", "php-curl", "openssl"]
slug: "curl-openssl_4-to-openssl_3"
aliases:
  - /curl-openssl_4-to-openssl_3/
  - /curl-openssl_4-to-openssl_3/
---


php-curl-openssl 모듈을 사용하게 될 경우 컴파일을 하면 문제가 생겼다.

ubuntu 16 / apache 2.4 / php 5.3 / curl 7.49 / openssl 0.9.8zh

모두 컴파일 된 상태였다.

이과정에서 php 는 CURL_OPENSSL_4 이 아닌 CURL_OPENSSL_3을 요구했고 수정하는 방법이다.

vi  curl-7.54.0/lib/libcurl.vers

HIDDEN
 {
 local:
 __*; _rest*;
 _save\*;
 };
CURL_OPENSSL_4 -> CURL_OPENSSL_3
 {
 global: curl_\*;
 local: \*;
 };

CURL_OPENSSL_4 부분을 CURL_OPENSSL_3 으로 수정해서 컴파일 하자.

./configure --prefix=/usr/local/curl --with-ssl=/usr/local/openssl --enable-versioned-symbols

mv /usr/lib/x86_64-linux-gnu/libcurl.so.4 /usr/lib/x86_64-linux-gnu/libcurl.so.4.orig

ln -s /usr/local/curl/lib/libcurl.so.4.4.0 /usr/lib/x86_64-linux-gnu/libcurl.so.4
