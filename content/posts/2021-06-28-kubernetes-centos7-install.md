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


작년 10월 작성했던 install script가 달라졌다.

```
<#!/bin/sh setenforce 0 sed -i --follow-symlinks 's/SELINUX=enforcing/SELINUX=disabled/g' /etc/sysconfig/selinux swapoff -a modprobe br_netfilter echo '1' > /proc/sys/net/bridge/bridge-nf-call-iptables yum install -y yum-utils device-mapper-persistent-data lvm2 yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo yum install -y docker-ce cat <<EOF > /etc/yum.repos.d/kubernetes.repo [kubernetes] name=Kubernetes baseurl=https://packages.cloud.google.com/yum/repos/kubernetes-el7-x86_64 enabled=1 gpgcheck=1 repo_gpgcheck=1 gpgkey=https://packages.cloud.google.com/yum/doc/yum-key.gpg https://packages.cloud.google.com/yum/doc/rpm-package-key.gpg EOF yum install -y kubelet kubeadm kubectl sed -i "s|ExecStart=/usr/bin/dockerd -H fd:// --containerd=/run/containerd/containerd.sock|ExecStart=/usr/bin/dockerd -H fd:// --containerd=/run/containerd/containerd.sock --exec-opt native.cgroupdriver=systemd|" /usr/lib/systemd/system/docker.service echo "net.bridge.bridge-nf-call-ip6tables = 1" >> /etc/sysctl.conf echo "net.bridge.bridge-nf-call-iptables = 1" >> /etc/sysctl.conf echo "net.ipv4.ip_forward = 1" >> /etc/sysctl.conf sysctl -p systemctl enable docker systemctl enable kubelet
```

큰 틀의 변화라면 작년의 클러스터 설치에선 kubeadm.conf 에서 docker와 kube의 cgroup을 변경해주는 방식이 었다면 근래에는 Docker의 Cgroup를 변경해야한다.

```
error: failed to run Kubelet: failed to create kubelet: misconfiguration: kubelet cgroup driver: "systemd" is different from docker cgroup driver: "cgroupfs"
```

그렇지 않으면 위와같은 에러가 발생한다. 이에러를 피하기위해 sed 로 Docker의 systemctl service file에서 docker exec 구문에 --exec-opt native.cgroupdriver=systemd native driver의 실행을 수정해 주면된다.

변경된지 확인하는방법은

```
docker info | grep systemd Cgroup Driver: systemd
```

명령어로 cgroup 를 확인할수 있다.

여기까지 확인되었으면, 작업한 Server의 스냅샷을 생성후, 스냅샷을 기반으로 워커노드3대를 생성한다.

위에작성한 스크립트는 init script 에서도 프로비저닝시에 사용할수있도록 만들었으니 그냥 사용해도 된다.

스냅샷이 잘 생성되면 kubectl init 를 하자.

```
kubeadm init --pod-network-cidr=10.254.0.0/16
```

init 가 끝나면 config 를 복사해준다

```
mkdir -p $HOME/.kube sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config sudo chown $(id -u):$(id -g) $HOME/.kube/config export KUBECONFIG=/etc/kubernetes/admin.conf

```

명령어로 복사를한다. 설치과정에서 프린팅된다 admin.conf 까지 같이 export 한다.

```
You should now deploy a pod network to the cluster. Run "kubectl apply -f [podnetwork].yaml" with one of the options listed at:
  https://kubernetes.io/docs/concepts/cluster-administration/addons/
Then you can join any number of worker nodes by running the following on each as root:
kubeadm join 10.0.10.9:6443 --token 6ghues.yxwqnp87920d4arm \\ \t--discovery-token-ca-cert-hash sha256:49c750f19ef34b5f3ab73ceb91a2ce540a65418b693c24a1ee5acaeee2e80972

```

다음과 같은 내용이 프린팅되는데 join 부분만 쓰면된다.

woker node에서 join한다

```
[preflight] Running pre-flight checks \t[WARNING Hostname]: hostname "k8s-worker-003" could not be reached \t[WARNING Hostname]: hostname "k8s-worker-003": lookup k8s-worker-003 on 169.254.169.53:53: no such host [preflight] Reading configuration from the cluster... [preflight] FYI: You can look at this config file with 'kubectl -n kube-system get cm kubeadm-config -o yaml' [kubelet-start] Writing kubelet configuration to file "/var/lib/kubelet/config.yaml" [kubelet-start] Writing kubelet environment file with flags to file "/var/lib/kubelet/kubeadm-flags.env" [kubelet-start] Starting the kubelet [kubelet-start] Waiting for the kubelet to perform the TLS Bootstrap...
This node has joined the cluster: * Certificate signing request was sent to apiserver and a response was received. * The Kubelet was informed of the new secure connection details.
Run 'kubectl get nodes' on the control-plane to see this node join the cluster.
```

다음 메시지가 나오면 정상적으로 클러스터가 셋팅된 것이다.

```
echo 'source <(kubectl completion bash)' >>~/.bashrc kubectl completion bash >/etc/bash_completion.d/kubectl echo 'alias k=kubectl' >>~/.bashrc echo 'complete -F __start_kubectl k' >>~/.bashrc
```

bash 에서 shell 자동완성 설정까지 넣어주면 완성이다.

TAB을 이용한 자유를 누려보자!
