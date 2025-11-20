---
title: "Chapter 20. I/O Redirection"
date: 2020-07-07T11:44:25+09:00
draft: false
categories: ["Linux"]
slug: "chapter-20-i-o-redirection"
aliases:
  - /chapter-20-i-o-redirection/
  - /chapter-20-i-o-redirection/
---


일반적으로 sort 해서 저장하려면 쓰는명령어는

cat filename | sort > filename

이었다면 <> Redirection 을 이용한다면 이래와 같이 설정가능!

sort <filename> filename
