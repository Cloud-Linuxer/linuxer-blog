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

\n

```
    spec:\n      containers:\n        - name: nginx\n          image: nginx:latest\n          ports:\n            - containerPort: 80\n          resources:\n            limits:\n              cpu: 500m\n            requests:\n              cpu: 200m\n          lifecycle:\n            preStop:\n              exec:\n                command: ["/bin/sleep", "30"]
```

\n\n\n\n

.

\n\n\n\n

.

\n\n\n\n

hpa 발생시 pod의 갑작스런 종료로 pod에 연결된 사용자가 502를 받게된다.

\n\n\n\n

모든 리퀘스트를 처리 후에 종료되도록 30초간의 유예를 준다 설정 변경 lifecycle preStop 를 이용하여 우아한 종료를!

\n