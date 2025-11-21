---
title: "pod graceful shutdown"
date: 2023-03-15T00:24:22+09:00
draft: false
categories: ["Kubernetes"]
tags: ["lifecycle", "preStop"]
slug: "pod-graceful-shutdown"
aliases:
  - /pod-graceful-shutdown/
  - /pod-graceful-shutdown/
---


```yaml
    spec:
      containers:

        - name: nginx
          image: nginx:latest
          ports:

            - containerPort: 80
          resources:
            limits:
              cpu: 500m
            requests:
              cpu: 200m
          lifecycle:
            preStop:
              exec:
                command: ["/bin/sleep", "30"]
```

.

hpa 발생시 pod의 갑작스런 종료로 pod에 연결된 사용자가 502를 받게된다.

모든 리퀘스트를 처리 후에 종료되도록 30초간의 유예를 준다 설정 변경 lifecycle preStop 를 이용하여 우아한 종료를!
