---
title: "PKOS-5Week-Final!"
date: 2023-04-07T22:26:48+09:00
draft: false
categories: ["Kubernetes"]
tags: ["k8s", "unsafe", "privileged"]
slug: "pkos-5week-final"
aliases:
  - /pkos-5week-final/
  - /pkos-5week-final/
---


마지막 주차이다.

5 주차는 보안 관련한 주제였다. 대표적으로 생각나는 쿠버네티스 보안 사건부터 이야기할까한다.

생각보다 많은 사람들이 쓰는 오픈소스중에 Rancher가 있다.

Rancher가 설치된 클러스터에서 이상한 증상이 발생했다. 배포된 POD가 재대로 성능이 나지않고 WorkerNode의 CPU사용율이 굉장히 높았다. 클러스터 외부에서 원인을 파악할 수 없어서 결국 WokerNode에 SSH를 접속해서 확인했었다.

WorkerNode에선 대량의 마이닝툴이 발견되었다. Pirvate 환경인데다가 외부에서 SSH도 불가능한 환경에서 발생한 침해사고라, 플랫폼의 문제로 대두되었다. 그러던 중 클러스터에서 동작중인 대시보드들을 확인하였다.

당시에는 다들 쿠버네티스에 익숙한 상황이 아니라서 확인이 좀오래 걸렸다.

실상은 사용자의 문제이지만, Rancher 에서 사용되는 privileged모드를 정확히 모르고 사용하여, Rancher 의 privileged 취약점을 통해 API로 손쉽게 대량의 마이닝툴을 인스톨 할수있는 이슈였다.

Rancher 2.4버전까진 privileged모드에 대한 안내가 없지만 2.5버전부턴 생겼다.

![](/images/2023/04/image-1024x157.png)

<https://ranchermanager.docs.rancher.com/v2.5/pages-for-subheaders/rancher-on-a-single-node-with-docker#privileged-access-for-rancher-v25>

가볍게 이전에 경험했던 이야기를 하면서 unsafe 에대한 이야기를 하려한다.

```bash
#kubelet --allowed-unsafe-sysctls
```bash
에 대한 이야기다. 한창 K8S의 성능에 대한 고민이 많던 시기다.
이때에 쿠버네티스 네트워킹에 대해서 한창 많은 공부를 했던것 같다.

K8S의 성능이슈가 발생하였다. 흔히 말하는 쓰로틀링 이슈로 보틀넥이 되는 부분을 찾아야하는 상태였다. 증상은 이랬다. 일정이상의 트래픽이 발생하면 패킷이 드랍됬다.

이문제를 재현하는 것부터 시작했다. 최대한 많은 스트레스를 줘야했기에, 테스트 툴부터 시작했다. Locust를 선택했다. 가볍고 많은 트래픽을 만들수 있는 툴이다. Python 기반이라 테스트 스크립트 작성도 쉽다.

혹시나 같은 네트워크나 같은 클러스터등 다른 요인이 될만한 요소들을 최대한 제거해서 테스트했다. 이 테스트는 거의 2-3주 정도 진행했는데 테스트 결과가 너무 들쭉날쭉했다. 이유는 처음에 나는 CNI를 의심했다.

이유는 네트워크 이슈니까.

그런데 테스트를 진행할수록 CNI는 잘못이 없었다.
오히려 굉장히 최적화가 잘되어있다는 것을 알 수 있었다.

그 테스트를 진행하면서, 서버가 정상적으로 네트워크를 처리못하는 느낌이 들었다. 엔지니어 시절에는 커널파라 미터 튜닝도 은근 자주했기에 backlog / net.core.somaxconn 등을 의심했다.

**net.core.netdev_max_backlog** 옵션은 각 네트워크 별로 커널이 처리하도록 쌓아두는 Queue의 크기를 정해주는 파라미터다.

**net.core.somaxconn** 는 Listen backlog / Linsten 으로 바인딩된 서버 소켓에서 Accept를 기다리는 소캣 카운터의 하드리밋이다.

```bash
cat /var/lib/kubelet/kubelet.conf apiVersion: kubelet.config.k8s.io/v1beta1 authentication:
  anonymous: {}
  webhook:
    cacheTTL: 0s
  x509: {} authorization:
  webhook:
    cacheAuthorizedTTL: 0s
    cacheUnauthorizedTTL: 0s cpuManagerReconcilePeriod: 0s evictionPressureTransitionPeriod: 0s fileCheckFrequency: 0s httpCheckFrequency: 0s imageMinimumGCAge: 0s kind: KubeletConfiguration logging:
  flushFrequency: 0
  options:
    json:
      infoBufferSize: "0"
  verbosity: 0 memorySwap: {} nodeStatusReportFrequency: 0s nodeStatusUpdateFrequency: 0s runtimeRequestTimeout: 0s shutdownGracePeriod: 0s shutdownGracePeriodCriticalPods: 0s streamingConnectionIdleTimeout: 0s syncFrequency: 0s volumeStatsAggPeriod: 0s
```bash
여기에 박아서 사용할수 있다.

```bash
allowed-unsafe-sysctls: - net.core.netdev_max_backlog - net.core.somaxconn
```bash
설정을 추가했다. 이제 프로세스를 새시작하고 테스트 했다.

```bash
32s                 Normal    NodeReady                 Node/i-0a7504d19e11fb642   Node i-0a7504d19e11fb642 status is now: NodeReady 31s                 Warning   SysctlForbidden           Pod/unsafe                 forbidden sysctl: "net.core.somaxconn" not allowlisted 14s (x6 over 30s)   Warning   FailedMount               Pod/unsafe                 MountVolume.SetUp failed for volume "kube-api-access-8w64p" : object "default"/"kube-root-ca.crt" not registered 4s                  Warning   SysctlForbidden           Pod/unsafe                 forbidden sysctl: "net.core.somaxconn" not allowlisted 4s                  Normal    Scheduled                 Pod/unsafe                 Successfully assigned default/unsafe to i-0a7504d19e11fb642
```bash
어라...이젠 이전에 했던 방법이 안먹는다. 그럼 뭐..더 고전적인 방법이다.

```bash
systemctl status kubelet.service
● kubelet.service - Kubernetes Kubelet Server
     Loaded: loaded (/lib/systemd/system/kubelet.service; enabled; vendor preset: enabled)
```bash
보면 서비스 경로가 보인다. 이안에 kubelet을 시작하기 위한 경로들이 모여있다.

```bash
[Unit] Description=Kubernetes Kubelet Server Documentation=https://github.com/kubernetes/kubernetes After=containerd.service
[Service] EnvironmentFile=/etc/sysconfig/kubelet ExecStart=/usr/local/bin/kubelet "$DAEMON_ARGS" Restart=always RestartSec=2s StartLimitInterval=0 KillMode=process User=root CPUAccounting=true MemoryAccounting=true
[Install] WantedBy=multi-user.target
```bash
우린 /etc/sysconfig/kubelet 에 삽입하면 된다.

```bash
cat /etc/sysconfig/kubelet
DAEMON_ARGS="--anonymous-auth=false --authentication-token-webhook=true --authorization-mode=Webhook --cgroup-driver=systemd --cgroup-root=/ --client-ca-file=/srv/kubernetes/ca.crt --cloud-provider=external --cluster-dns=169.254.20.10 --cluster-domain=cluster.local --enable-debugging-handlers=true --eviction-hard=memory.available<100Mi,nodefs.available<10%,nodefs.inodesFree<5%,imagefs.available<10%,imagefs.inodesFree<5% --feature-gates=CSIMigrationAWS=true,InTreePluginAWSUnregister=true --hostname-override=i-0a7504d19e11fb642 --kubeconfig=/var/lib/kubelet/kubeconfig --max-pods=100 --pod-infra-container-image=registry.k8s.io/pause:3.6@sha256:3d380ca8864549e74af4b29c10f9cb0956236dfb01c40ca076fb6c37253234db --pod-manifest-path=/etc/kubernetes/manifests --protect-kernel-defaults=true --register-schedulable=true --resolv-conf=/run/systemd/resolve/resolv.conf --v=2 --volume-plugin-dir=/usr/libexec/kubernetes/kubelet-plugins/volume/exec/ --cloud-config=/etc/kubernetes/in-tree-cloud.config --node-ip=172.30.52.244 --runtime-request-timeout=15m --container-runtime-endpoint=unix:///run/containerd/containerd.sock --tls-cert-file=/srv/kubernetes/kubelet-server.crt --tls-private-key-file=/srv/kubernetes/kubelet-server.key --config=/var/lib/kubelet/kubelet.conf" HOME="/root"

```bash
여기 DAEMON_ARGS 뒤에 --allowed-unsafe-sysctls 'kernel.msg\*,net.core.somaxconn' 를 추가해준다.

재시작 까지하면 프로세스에 추가된 파라미터가 보인다.

```bash
ps afxuwww | grep unsafe root       27576  0.0  0.0   8168   656 pts/0    S+   13:07   0:00                          \\_ grep --color=auto unsafe root       27340  2.3  2.4 1789712 94144 ?       Ssl  13:06   0:00 /usr/local/bin/kubelet --anonymous-auth=false --authentication-token-webhook=true --authorization-mode=Webhook --cgroup-driver=systemd --cgroup-root=/ --client-ca-file=/srv/kubernetes/ca.crt --cloud-provider=external --cluster-dns=169.254.20.10 --cluster-domain=cluster.local --enable-debugging-handlers=true --eviction-hard=memory.available<100Mi,nodefs.available<10%,nodefs.inodesFree<5%,imagefs.available<10%,imagefs.inodesFree<5% --feature-gates=CSIMigrationAWS=true,InTreePluginAWSUnregister=true --hostname-override=i-0a7504d19e11fb642 --kubeconfig=/var/lib/kubelet/kubeconfig --max-pods=100 --pod-infra-container-image=registry.k8s.io/pause:3.6@sha256:3d380ca8864549e74af4b29c10f9cb0956236dfb01c40ca076fb6c37253234db --pod-manifest-path=/etc/kubernetes/manifests --protect-kernel-defaults=true --register-schedulable=true --resolv-conf=/run/systemd/resolve/resolv.conf --v=2 --volume-plugin-dir=/usr/libexec/kubernetes/kubelet-plugins/volume/exec/ --cloud-config=/etc/kubernetes/in-tree-cloud.config --node-ip=172.30.52.244 --runtime-request-timeout=15m --container-runtime-endpoint=unix:///run/containerd/containerd.sock --tls-cert-file=/srv/kubernetes/kubelet-server.crt --tls-private-key-file=/srv/kubernetes/kubelet-server.key --config=/var/lib/kubelet/kubelet.conf --allowed-unsafe-sysctls kernel.msg*,net.core.somaxconn
```bash
```bash
# k events
5s                      Normal    NodeAllocatableEnforced   Node/i-0a7504d19e11fb642   Updated Node Allocatable limit across pods 4s                       Normal    Scheduled                 Pod/unsafe                 Successfully assigned default/unsafe to i-0a7504d19e11fb642 3s                       Normal    Pulling                   Pod/unsafe                 Pulling image "centos:7" k get pod NAME     READY   STATUS    RESTARTS   AGE unsafe   1/1     Running   0          20s
```bash
정상적으로 스케줄링된것이 보인다.

이로서 unsafe 파라미터를 영구적으로 적용할수 있게되었다.

이렇게 파라미터를 적용하고 나서, net.core.somaxconn 을 테스트하였다. 정상적으로 적용된것이 보인다. 사실 단순히 somaxconn만 적용한다고 뭔가 달라지지 않는다. syn_backlog 값도 같이 늘려야 한다. 그리고 적용된 값은 Listen() 시스템 콜을 할때 적용 되기 때문에 이 파라미터 들은 컨테이너가 시작될때 적용된다고 보면 된다.

이런 과정을 거쳐서 테스트를 진행했으나, 실은 트래픽을 20% 더 받았을 뿐 증상이 완화 되지 않았다.

결국 해결은 kubenetes 안에 있지 않았고 Linux 안에 있었다. irqbalance의 smp_affinity 가 정상적으로 인터럽트 해주지 않아서 cpu0만 열심히 일하고 있었던 것이다.

이런과정에서 privileged / unsafe 에 대해서 알게되었다.

5주차 과정을 진행하면서 다시금 그때의 기억과 내용을 자세히 알게되면서 새로운 부분도 알되게었고, 새로이 정리도 하게되었다.

PKOS는 쿠버네티스의 전체적인 패턴과 컴포넌트들을 학습할수 있는 기회였다.
