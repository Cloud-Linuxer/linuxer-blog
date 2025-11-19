---
title: "NKS-Linuxer-Blog-trouble-shooting-lifecycle-not-working"
date: 2021-09-02T09:45:47+09:00
draft: false
categories: ["NCP", "Kubernetes"]
tags: ["k8s", "NKS", "lifecycle", "hook", "scale"]
slug: "nks-linuxer-blog-trouble-shooting-lifecycle-not-working"
aliases:
  - /nks-linuxer-blog-trouble-shooting-lifecycle-not-working/
  - /nks-linuxer-blog-trouble-shooting-lifecycle-not-working/
---

\n

블로그를 이전한지 얼마안됬기 때문에 집중모니터링 기간이다.  
먼저 자원부터 본다.

\n\n\n\n

```
k top node\nNAME                  CPU(cores)   CPU%   MEMORY(bytes)   MEMORY%   \nnks-pool-1119-w-gzi   223m         5%     1265Mi          16%       \nnks-pool-1119-w-kvi   172m         4%     1540Mi          20%       \n\nk top pod\nNAME                                             CPU(cores)   MEMORY(bytes)   \nphp-fpm-nginx-deployment-6bc7b6df77-fbdx9        9m           138Mi           \nstorage-nfs-client-provisioner-5b88c7c55-dvtlj   2m           8Mi             \n
```

\n\n\n\n

자원은 얼마안쓰지만..혹시나 사용량이 늘어날까봐 scale을 늘렸다.

\n\n\n\n

```
k scale deployment php-fpm-nginx-deployment --replicas=3\ndeployment.apps/php-fpm-nginx-deployment scaled\n
```

\n\n\n\n

그리고 pod 를 확인했는데...

\n\n\n\n

```
k get pod\nNAME                                             READY   STATUS              RESTARTS   AGE\nphp-fpm-nginx-deployment-6bc7b6df77-bpf2g        2/2     Running             0          19s\nphp-fpm-nginx-deployment-6bc7b6df77-fbdx9        2/2     Running             3          32h\nphp-fpm-nginx-deployment-6bc7b6df77-rfpb2        0/2     ContainerCreating   0          19s\nstorage-nfs-client-provisioner-5b88c7c55-dvtlj   1/1     Running             0          10h
```

\n\n\n\n

생성단계에서 멈춘 pod 가 있었다. 상태를 확인해보니

\n\n\n\n

```
Events:\n  Type     Reason               Age        From                          Message\n  ----     ------               ----       ----                          -------\n  Normal   Scheduled            <unknown>  default-scheduler             Successfully assigned default/php-fpm-nginx-deployment-6bc7b6df77-rfpb2 to nks-pool-1119-w-gzi\n  Normal   Pulled               28s        kubelet, nks-pool-1119-w-gzi  Container image "linuxer-regi.kr.ncr.ntruss.com/php-fpm:12" already present on machine\n  Normal   Created              28s        kubelet, nks-pool-1119-w-gzi  Created container php-fpm\n  Normal   Started              28s        kubelet, nks-pool-1119-w-gzi  Started container php-fpm\n  Normal   Pulled               28s        kubelet, nks-pool-1119-w-gzi  Container image "nginx:1.21" already present on machine\n  Normal   Created              28s        kubelet, nks-pool-1119-w-gzi  Created container nginx\n  Normal   Started              28s        kubelet, nks-pool-1119-w-gzi  Started container nginx\n  Warning  FailedPostStartHook  28s        kubelet, nks-pool-1119-w-gzi  Exec lifecycle hook ([/bin/sh -c chmod 777 /run/php-fpm.sock]) for Container "nginx" in Pod "php-fpm-nginx-deployment-6bc7b6df77-rfpb2_default(6978da29-8045-49a0-9745-6be3cc48c364)" failed - error: command '/bin/sh -c chmod 777 /run/php-fpm.sock' exited with 1: chmod: cannot access '/run/php-fpm.sock': No such file or directory
```

\n\n\n\n

Exec lifecycle hook ([/bin/sh -c chmod 777 /run/php-fpm.sock]) for Container "nginx" in Pod "php-fpm-nginx-deployment-6bc7b6df77-rfpb2\_default(6978da29-8045-49a0-9745-6be3cc48c364)" failed - error: command '/bin/sh -c chmod 777 /run/php-fpm.sock' exited with 1: chmod: cannot access '/run/php-fpm.sock': No such file or directory

\n\n\n\n

lifecycle hook 이 정상동작하지 않았다. 음...이벤트상으론 컨테이너가 생성전에 hook이 동작한건데 이건좀 확인해봐야겠다.

\n\n\n\n

조금있다가 컨테이너가 자동으로 재시작되며 Runing 상태로 변경됬다.

\n\n\n\n

```
k logs php-fpm-nginx-deployment-6bc7b6df77-rfpb2 -c nginx \n/docker-entrypoint.sh: /docker-entrypoint.d/ is not empty, will attempt to perform configuration\n/docker-entrypoint.sh: Looking for shell scripts in /docker-entrypoint.d/\n/docker-entrypoint.sh: Launching /docker-entrypoint.d/10-listen-on-ipv6-by-default.sh\n10-listen-on-ipv6-by-default.sh: info: can not modify /etc/nginx/conf.d/default.conf (read-only file system?)\n/docker-entrypoint.sh: Launching /docker-entrypoint.d/20-envsubst-on-templates.sh\n/docker-entrypoint.sh: Launching /docker-entrypoint.d/30-tune-worker-processes.sh\n/docker-entrypoint.sh: Configuration complete; ready for start up\n2021/09/02 00:30:55 [notice] 1#1: using the "epoll" event method\n2021/09/02 00:30:55 [notice] 1#1: nginx/1.21.1\n2021/09/02 00:30:55 [notice] 1#1: built by gcc 8.3.0 (Debian 8.3.0-6) \n2021/09/02 00:30:55 [notice] 1#1: OS: Linux 5.4.8-050408-generic\n2021/09/02 00:30:55 [notice] 1#1: getrlimit(RLIMIT_NOFILE): 1048576:1048576\n2021/09/02 00:30:55 [notice] 1#1: start worker processes\n2021/09/02 00:30:55 [notice] 1#1: start worker process 22\n2021/09/02 00:30:55 [notice] 1#1: start worker process 23\n2021/09/02 00:30:55 [notice] 1#1: start worker process 24\n2021/09/02 00:30:55 [notice] 1#1: start worker process 25\n
```

\n\n\n\n

logs 도 정상...음...일단 로깅을 모아보고 생각해야겠다.

\n