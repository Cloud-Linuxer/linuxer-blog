---
title: "k8s-Centos7-install"
date: 2020-10-27T09:15:28+09:00
draft: false
categories: ["Kubernetes"]
slug: "k8s-centos7-install"
aliases:
  - /k8s-centos7-install/
  - /k8s-centos7-install/
---

\n

```
#!/bin/sh\nsetenforce 0\nsed -i --follow-symlinks 's/SELINUX=enforcing/SELINUX=disabled/g' /etc/sysconfig/selinux\nswapoff -a\nmodprobe br_netfilter\necho '1' > /proc/sys/net/bridge/bridge-nf-call-iptables\nyum install -y yum-utils device-mapper-persistent-data lvm2\nyum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo\nyum install -y docker-ce\ncat <<EOF > /etc/yum.repos.d/kubernetes.repo\n[kubernetes]\nname=Kubernetes\nbaseurl=https://packages.cloud.google.com/yum/repos/kubernetes-el7-x86_64\nenabled=1\ngpgcheck=1\nrepo_gpgcheck=1\ngpgkey=https://packages.cloud.google.com/yum/doc/yum-key.gpg https://packages.cloud.google.com/yum/doc/rpm-package-key.gpg\nEOF\n\nyum install -y kubelet kubeadm kubectl\nsystemctl enable docker\nsystemctl enable kubelet\nsed -i 's/cgroup-driver=systemd/cgroup-driver=cgroupfs/g' /usr/lib/systemd/system/kubelet.service.d/10-kubeadm.conf
```

\n\n\n\n

K8s centos7 base install

\n\n\n\n

userdate 등에 넣고 쓸수있다.

\n\n\n\n

#Master 에서 작업

\n\n\n\n

```
kubeadm init --pod-network-cidr=사용하려는 pod cidr
```

\n\n\n\n

```
mkdir -p $HOME/.kube\nsudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config\nsudo chown $(id -u):$(id -g) $HOME/.kube/config
```

\n\n\n\n

kubeadm join token 이 나오면 cluster node 에서 join 해준다

\n