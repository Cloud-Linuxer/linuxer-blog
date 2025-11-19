---
title: "Argo-Rollouts-Pod-Lifecycle"
date: 2023-12-28T15:54:49+09:00
draft: false
categories: ["Kubernetes"]
tags: ["preStop", "argo rollouts", "terminationGracePeriodSeconds"]
slug: "argo-rollouts-pod-lifecycle"
aliases:
  - /argo-rollouts-pod-lifecycle/
  - /argo-rollouts-pod-lifecycle/
---


Argo Rollouts 의 쿨다운에 대한 이야기를 하려고한다.


이글은 Argo Roullouts 의 scaleDownDelaySeconds 옵션부터 preStop terminationGracePeriodSeconds 까지의 과정을 다룬다.


Argo Rollouts 는 배포를 도와주는 툴로 블루그린 카나리등과 같은 부분을 도와주는 도구이다. 간략하게 동작을 설명하겠다.


![](/images/2023/12/image-10-1024x684.png)

블루그린이 완료된이후 RS는 축소하지 않고 30초간 대기한다. 이 30초간 대기하는 옵션이 scaleDownDelaySeconds다. 혹시나모를 롤백 상황에 대해서 기다리는 옵션인것이다. 이시간이 종료되면 이제 RS는 replicas 를 0으로 수정해서 pod 들은 축소된다.


replicas 가 0으로 수정되면 pod는 일반적인 pod 의 lifecycle 를 거친다. pod 는 여러 차례 말했지만 N+1개의 컨테이너의 집합이고 컨테이너는 프로세스이므로 프로세스의 종료 과정이 그대로 pod 의 lifecycle 를 따르나 쿠버네티스는 이 프로세스를 컨트롤하는 고도화된 툴이므로 다양한 과정을 컨트롤 할수있게 만들어져 있다.


pod 의 종료과정에는 여러 작업을 끼워넣을수 있으며 그 과정중의 하나가 preStop hook 이다. preStop Hook이 설정되면 preStop hook 이 끝날때까지 컨테이너는 종료되지않으며 PreStop 훅이 종료된 시점에 TERM 을 날린다. 그리고terminationGracePeriodSeconds 은 pod 가 종료되는 시점부터 설정된 시간이 끝나면 KILL 시그널을 날린다.


결론적으로 preStop HooK은 terminationGracePeriodSeconds 보다 클수 없다. terminationGracePeriodSeconds 시간내에 행해져야 하고, preStop Hook 보다 커야지만 Graceful 하게 동작할수있다.
