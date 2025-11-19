---
title: "kubernetes-CentOS7-install"
date: 2021-06-28T23:13:44+09:00
draft: false
categories: ["Linux", "Kubernetes"]
slug: "kubernetes-centos7-install"
aliases:
  - /kubernetes-centos7-install/
  - /kubernetes-centos7-install/
---

\n

작년 10월 작성했던 install script가 달라졌다.

\n\n\n\n

```
<#!/bin/sh\nsetenforce 0\nsed -i --follow-symlinks 's/SELINUX=enforcing/SELINUX=disabled/g' /etc/sysconfig/selinux\nswapoff -a\nmodprobe br_netfilter\necho '1' > /proc/sys/net/bridge/bridge-nf-call-iptables\nyum install -y yum-utils device-mapper-persistent-data lvm2\nyum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo\nyum install -y docker-ce\ncat <<EOF > /etc/yum.repos.d/kubernetes.repo\n[kubernetes]\nname=Kubernetes\nbaseurl=https://packages.cloud.google.com/yum/repos/kubernetes-el7-x86_64\nenabled=1\ngpgcheck=1\nrepo_gpgcheck=1\ngpgkey=https://packages.cloud.google.com/yum/doc/yum-key.gpg https://packages.cloud.google.com/yum/doc/rpm-package-key.gpg\nEOF\nyum install -y kubelet kubeadm kubectl\nsed -i "s|ExecStart=/usr/bin/dockerd -H fd:// --containerd=/run/containerd/containerd.sock|ExecStart=/usr/bin/dockerd -H fd:// --containerd=/run/containerd/containerd.sock --exec-opt native.cgroupdriver=systemd|" /usr/lib/systemd/system/docker.service\necho "net.bridge.bridge-nf-call-ip6tables = 1" >> /etc/sysctl.conf\necho "net.bridge.bridge-nf-call-iptables = 1" >> /etc/sysctl.conf\necho "net.ipv4.ip_forward = 1" >> /etc/sysctl.conf\nsysctl -p\nsystemctl enable docker\nsystemctl enable kubelet
```

\n\n\n\n

.

\n\n\n\n

큰 틀의 변화라면 작년의 클러스터 설치에선 kubeadm.conf 에서 docker와 kube의 cgroup을 변경해주는 방식이 었다면 근래에는 Docker의 Cgroup를 변경해야한다.

\n\n\n\n

```
error: failed to run Kubelet: failed to create kubelet:\nmisconfiguration: kubelet cgroup driver: "systemd" is different from docker cgroup driver: "cgroupfs"
```

\n\n\n\n

.

\n\n\n\n

그렇지 않으면 위와같은 에러가 발생한다. 이에러를 피하기위해 sed 로 Docker의 systemctl service file에서 docker exec 구문에 --exec-opt native.cgroupdriver=systemd native driver의 실행을 수정해 주면된다.

\n\n\n\n

변경된지 확인하는방법은

\n\n\n\n

```
docker info | grep systemd\nCgroup Driver: systemd
```

\n\n\n\n

.

\n\n\n\n

명령어로 cgroup 를 확인할수 있다.

\n\n\n\n

여기까지 확인되었으면, 작업한 Server의 스냅샷을 생성후, 스냅샷을 기반으로 워커노드3대를 생성한다.

\n\n\n\n

위에작성한 스크립트는 init script 에서도 프로비저닝시에 사용할수있도록 만들었으니 그냥 사용해도 된다.

\n\n\n\n

스냅샷이 잘 생성되면 kubectl init 를 하자.

\n\n\n\n

```
kubeadm init --pod-network-cidr=10.254.0.0/16
```

\n\n\n\n

.

\n\n\n\n

init 가 끝나면 config 를 복사해준다

\n\n\n\n

```
mkdir -p $HOME/.kube\nsudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config\nsudo chown $(id -u):$(id -g) $HOME/.kube/config\nexport KUBECONFIG=/etc/kubernetes/admin.conf\n
```

\n\n\n\n

.

\n\n\n\n

명령어로 복사를한다. 설치과정에서 프린팅된다 admin.conf 까지 같이 export 한다.

\n\n\n\n

```
You should now deploy a pod network to the cluster.\nRun "kubectl apply -f [podnetwork].yaml" with one of the options listed at:\n  https://kubernetes.io/docs/concepts/cluster-administration/addons/\n\nThen you can join any number of worker nodes by running the following on each as root:\n\nkubeadm join 10.0.10.9:6443 --token 6ghues.yxwqnp87920d4arm \\\n\t--discovery-token-ca-cert-hash sha256:49c750f19ef34b5f3ab73ceb91a2ce540a65418b693c24a1ee5acaeee2e80972 \n
```

\n\n\n\n

.

\n\n\n\n

다음과 같은 내용이 프린팅되는데 join 부분만 쓰면된다.

\n\n\n\n

woker node에서 join한다

\n\n\n\n

```
[preflight] Running pre-flight checks\n\t[WARNING Hostname]: hostname "k8s-worker-003" could not be reached\n\t[WARNING Hostname]: hostname "k8s-worker-003": lookup k8s-worker-003 on 169.254.169.53:53: no such host\n[preflight] Reading configuration from the cluster...\n[preflight] FYI: You can look at this config file with 'kubectl -n kube-system get cm kubeadm-config -o yaml'\n[kubelet-start] Writing kubelet configuration to file "/var/lib/kubelet/config.yaml"\n[kubelet-start] Writing kubelet environment file with flags to file "/var/lib/kubelet/kubeadm-flags.env"\n[kubelet-start] Starting the kubelet\n[kubelet-start] Waiting for the kubelet to perform the TLS Bootstrap...\n\nThis node has joined the cluster:\n* Certificate signing request was sent to apiserver and a response was received.\n* The Kubelet was informed of the new secure connection details.\n\nRun 'kubectl get nodes' on the control-plane to see this node join the cluster.
```

\n\n\n\n

.

\n\n\n\n

다음 메시지가 나오면 정상적으로 클러스터가 셋팅된 것이다.

\n\n\n\n

```
echo 'source <(kubectl completion bash)' >>~/.bashrc\nkubectl completion bash >/etc/bash_completion.d/kubectl\necho 'alias k=kubectl' >>~/.bashrc\necho 'complete -F __start_kubectl k' >>~/.bashrc
```

\n\n\n\n

.

\n\n\n\n

bash 에서 shell 자동완성 설정까지 넣어주면 완성이다.

\n\n\n\n

TAB을 이용한 자유를 누려보자!

\n