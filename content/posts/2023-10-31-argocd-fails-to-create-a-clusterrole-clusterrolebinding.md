---
title: "ArgoCD Fails to create a clusterrole/clusterrolebinding."
date: 2023-10-31T16:12:03+09:00
draft: false
categories: ["Kubernetes"]
tags: ["argocd", "project", "RBAC"]
slug: "argocd-fails-to-create-a-clusterrole-clusterrolebinding"
aliases:
  - /argocd-fails-to-create-a-clusterrole-clusterrolebinding/
  - /argocd-fails-to-create-a-clusterrole-clusterrolebinding/
---

\n

In some cases, Cluster RBAC does not work with ArgoCD.

\n\n\n\n
![](/images/2023/10/image.png)
\n\n\n\n

Control cluster resources with "CLUSTER RESOURCE ALLOW LIST". When you create a new ArgoCD project, it has no permissions by default, so it can only operate within the namespace to NOT create cluster RBAC.

\n