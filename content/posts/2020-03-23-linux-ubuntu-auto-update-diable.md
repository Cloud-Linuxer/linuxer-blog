---
title: "linux-ubuntu-auto-update-diable"
date: 2020-03-23T09:49:56+09:00
draft: false
categories: ["Linux"]
tags: ["ubuntu", "autoupdate"]
slug: "linux-ubuntu-auto-update-diable"
aliases:
  - /linux-ubuntu-auto-update-diable/
  - /linux-ubuntu-auto-update-diable/
---


vi /etc/apt/apt.conf.d/20auto-upgrades


APT::Periodic::Unattended-Upgrade "1";


1로 설정된 옵션을 수정하면 자동업데이트는 꺼진다.


그렇다고 해서 업데이트를 할수없는것은 아니고 수동으로 명령어를 쳐서 가능하다.


#unattended-upgrade --dry-run


명령어를 이용해서 확인하자.
