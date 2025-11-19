---
title: "ubuntu 16.04 pam 패스워드 유효성 제한 libpam-pwquality 설정 포함"
date: 2019-09-06T10:46:47+09:00
draft: false
categories: ["Linux"]
tags: ["유효성", "pam", "isms", "패스워드"]
slug: "ubuntu-16-04-pam-패스워드-유효성-제한-libpam-pwquality-설정-포함"
aliases:
  - /ubuntu-16-04-pam-패스워드-유효성-제한-libpam-pwquality-설정-포함/
  - /ubuntu-16-04-pam-%ed%8c%a8%ec%8a%a4%ec%9b%8c%eb%93%9c-%ec%9c%a0%ed%9a%a8%ec%84%b1-%ec%a0%9c%ed%95%9c-libpam-pwquality-%ec%84%a4%ec%a0%95-%ed%8f%ac%ed%95%a8/
---

\n

패스워드 유효성 검증

\n\n\n\n

로그인 실패 5 계정 잠금 5분  
 #vi /etc/pam.d/common-auth  
 16번째줄 삽입  
 auth required pam\_tally2.so file=/var/log/tallylog deny=5 even\_deny\_root unlock\_time=300

\n\n\n\n

#vi /etc/pam.d/common-account  
 16 줄에 삽입  
 account required pam\_tally2.so

\n\n\n\n

패스워드 만료 모듈 설치  
 #apt-get -y install libpam-pwquality

\n\n\n\n

패스워드 만료 모듈의 경우에는 사용자를 새로 만들때만 영향을 줍니다.  
\n따라서 기존유저에 적용시에는 명령어로 지정해주어야 합니다.

\n\n\n\n

패스워드 사용가능 최대 기간  
 #chage -m (days) (user)

\n\n\n\n

PASS\_MAX\_DAYS 180

\n\n\n\n

패스워드 사용가능 최소 기간  
 #chage -m (days) (user)

\n\n\n\n

PASS\_MIN\_DAYS 2

\n\n\n\n

패스워드 만료전 경고 일수  
 #chage -W (days) (user)

\n\n\n\n

PASS\_WARN\_AGE 7

\n\n\n\n

패스워드 사용시간 제한

\n\n\n\n

#vi /etc/login.defs  
 PASS\_MAX\_DAYS 180

\n\n\n\n

#vi /etc/pam.d/common-password  
 password requisite pam\_pwquality.so retry=3 minlen=10 minclass=3  
 password [success=1 default=ignore] pam\_unix.so obscure use\_authtok try\_first\_pass sha512 remember=2

\n\n\n\n

remember=2 2회 동안 동일한 비밀번호 생성 금지  
\nminlen=10 비밀번호 길이 생성 제한 10자 이상으로   
\nminclass=3 새비밀번호에 필요한 문자 클래스 수 제한 (종류 ⇒ 대문자 / 소문자 / 숫자 / 기타)

\n\n\n\n

참조 URL  
 https://www.server-world.info/en/note?os=Ubuntu\_16.04&p=password

\n\n\n\n\n\n\n\n

isms 기준에 맞춘 ubuntu 16.04 ssh 패스워드 유효성 설정입니다.

\n