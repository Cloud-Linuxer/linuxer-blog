---
title: "Linux-cache-drop"
date: 2021-01-11T10:13:10+09:00
draft: false
categories: ["linuxer?"]
slug: "linux-cache-drop"
aliases:
  - /linux-cache-drop/
  - /linux-cache-drop/
---


리눅스에서 메모리 누수를 찾지 못할때 최후의 방법으로 cache 를 drop 하는 방법이 있다.

```
sync && echo 3 > /proc/sys/vm/drop_caches
```
