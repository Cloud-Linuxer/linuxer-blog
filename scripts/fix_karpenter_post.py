#!/usr/bin/env python3
import re

def fix_karpenter_post():
    filepath = '/home/linuxer-hugo/content/posts/2023-05-20-eks-nodeless-08-aws-karpenter-topologyspreadconstraints.md'

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Fix the first Provisioner YAML block
    content = content.replace(
        """```
apiVersion: karpenter.sh/v1alpha5 kind: Provisioner metadata:
  name: default spec:
  consolidation:
    enabled: true
  requirements:

    - key: karpenter.k8s.aws/instance-category
      operator: In
      values: [ t, m, c ]
  providerRef:
    name: default --- apiVersion: karpenter.k8s.aws/v1alpha1 kind: AWSNodeTemplate metadata:
  name: default spec:
  subnetSelector:
    karpenter.sh/discovery: "${CLUSTER_NAME}"
  securityGroupSelector:
    karpenter.sh/discovery: "${CLUSTER_NAME}"

```""",
        """```yaml
apiVersion: karpenter.sh/v1alpha5
kind: Provisioner
metadata:
  name: default
spec:
  consolidation:
    enabled: true
  requirements:
    - key: karpenter.k8s.aws/instance-category
      operator: In
      values: [ t, m, c ]
  providerRef:
    name: default
---
apiVersion: karpenter.k8s.aws/v1alpha1
kind: AWSNodeTemplate
metadata:
  name: default
spec:
  subnetSelector:
    karpenter.sh/discovery: "${CLUSTER_NAME}"
  securityGroupSelector:
    karpenter.sh/discovery: "${CLUSTER_NAME}"
```""")

    # Fix the Deployment YAML block
    content = content.replace(
        """```
apiVersion: apps/v1 kind: Deployment metadata:
  name: host-spread spec:
  replicas: 20
  selector:
    matchLabels:
      app: host-spread
  template:
    metadata:
      labels:
        app: host-spread
    spec:
      containers:

      - image: public.ecr.aws/eks-distro/kubernetes/pause:3.2
        name: host-spread
        resources:
          requests:
            cpu: "1"
            memory: 256M
      topologySpreadConstraints:

      - labelSelector:
          matchLabels:
            app: host-spread
        maxSkew: 2
        topologyKey: kubernetes.io/hostname
        whenUnsatisfiable: DoNotSchedule

      - labelSelector:
          matchLabels:
            app: host-spread
        maxSkew: 5
        topologyKey: topology.kubernetes.io/zone
        whenUnsatisfiable: DoNotSchedule
```""",
        """```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: host-spread
spec:
  replicas: 20
  selector:
    matchLabels:
      app: host-spread
  template:
    metadata:
      labels:
        app: host-spread
    spec:
      containers:
      - image: public.ecr.aws/eks-distro/kubernetes/pause:3.2
        name: host-spread
        resources:
          requests:
            cpu: "1"
            memory: 256M
      topologySpreadConstraints:
      - labelSelector:
          matchLabels:
            app: host-spread
        maxSkew: 2
        topologyKey: kubernetes.io/hostname
        whenUnsatisfiable: DoNotSchedule
      - labelSelector:
          matchLabels:
            app: host-spread
        maxSkew: 5
        topologyKey: topology.kubernetes.io/zone
        whenUnsatisfiable: DoNotSchedule
```""")

    # Fix the bash command blocks
    content = content.replace(
        """```
k get node --show-labels | grep -v fargate | awk -F"topology.kubernetes.io/" '{print $3}' | sort zone=ap-northeast-2a zone=ap-northeast-2a zone=ap-northeast-2a zone=ap-northeast-2b zone=ap-northeast-2b zone=ap-northeast-2b zone=ap-northeast-2c

```""",
        """```bash
k get node --show-labels | grep -v fargate | awk -F"topology.kubernetes.io/" '{print $3}' | sort
zone=ap-northeast-2a
zone=ap-northeast-2a
zone=ap-northeast-2a
zone=ap-northeast-2b
zone=ap-northeast-2b
zone=ap-northeast-2b
zone=ap-northeast-2c
```""")

    # Fix the pod listing output
    content = content.replace(
        """```
k get pod NAME                          READY   STATUS    RESTARTS   AGE host-spread-dd5f6c569-49ps7   1/1     Running   0          115s host-spread-dd5f6c569-8772p   1/1     Running   0          115s host-spread-dd5f6c569-9q2hn   1/1     Running   0          115s host-spread-dd5f6c569-b68k2   1/1     Running   0          115s host-spread-dd5f6c569-bfhv5   1/1     Running   0          115s host-spread-dd5f6c569-bqqz2   1/1     Running   0          116s host-spread-dd5f6c569-bsp8m   1/1     Running   0          115s host-spread-dd5f6c569-dh8wx   1/1     Running   0          115s host-spread-dd5f6c569-ffjdg   1/1     Running   0          115s host-spread-dd5f6c569-jghmr   1/1     Running   0          115s host-spread-dd5f6c569-jhbxg   1/1     Running   0          116s host-spread-dd5f6c569-kf69q   1/1     Running   0          115s host-spread-dd5f6c569-ksktv   1/1     Running   0          115s host-spread-dd5f6c569-lbqmv   1/1     Running   0          115s host-spread-dd5f6c569-mbf2g   1/1     Running   0          116s host-spread-dd5f6c569-pd92p   1/1     Running   0          115s host-spread-dd5f6c569-pgphc   1/1     Running   0          115s host-spread-dd5f6c569-ph59g   1/1     Running   0          115s host-spread-dd5f6c569-sdp7d   1/1     Running   0          115s host-spread-dd5f6c569-tf8v9   1/1     Running   0          115s (user-linuxer@myeks:default) [root@myeks-bastion-EC2 EKS]# k get node --show-labels | grep -v fargate | awk -F"topology.kubernetes.io/" '{print $3}' | sort zone=ap-northeast-2a zone=ap-northeast-2a zone=ap-northeast-2a zone=ap-northeast-2b zone=ap-northeast-2b zone=ap-northeast-2c

```""",
        """```
k get pod
NAME                          READY   STATUS    RESTARTS   AGE
host-spread-dd5f6c569-49ps7   1/1     Running   0          115s
host-spread-dd5f6c569-8772p   1/1     Running   0          115s
host-spread-dd5f6c569-9q2hn   1/1     Running   0          115s
host-spread-dd5f6c569-b68k2   1/1     Running   0          115s
host-spread-dd5f6c569-bfhv5   1/1     Running   0          115s
host-spread-dd5f6c569-bqqz2   1/1     Running   0          116s
host-spread-dd5f6c569-bsp8m   1/1     Running   0          115s
host-spread-dd5f6c569-dh8wx   1/1     Running   0          115s
host-spread-dd5f6c569-ffjdg   1/1     Running   0          115s
host-spread-dd5f6c569-jghmr   1/1     Running   0          115s
host-spread-dd5f6c569-jhbxg   1/1     Running   0          116s
host-spread-dd5f6c569-kf69q   1/1     Running   0          115s
host-spread-dd5f6c569-ksktv   1/1     Running   0          115s
host-spread-dd5f6c569-lbqmv   1/1     Running   0          115s
host-spread-dd5f6c569-mbf2g   1/1     Running   0          116s
host-spread-dd5f6c569-pd92p   1/1     Running   0          115s
host-spread-dd5f6c569-pgphc   1/1     Running   0          115s
host-spread-dd5f6c569-ph59g   1/1     Running   0          115s
host-spread-dd5f6c569-sdp7d   1/1     Running   0          115s
host-spread-dd5f6c569-tf8v9   1/1     Running   0          115s

(user-linuxer@myeks:default) [root@myeks-bastion-EC2 EKS]# k get node --show-labels | grep -v fargate | awk -F"topology.kubernetes.io/" '{print $3}' | sort
zone=ap-northeast-2a
zone=ap-northeast-2a
zone=ap-northeast-2a
zone=ap-northeast-2b
zone=ap-northeast-2b
zone=ap-northeast-2c
```""")

    # Fix error log blocks
    content = content.replace(
        """```
2023-05-20T11:03:34.806Z\tERROR\tcontroller.provisioner\tCould not schedule pod, incompatible with provisioner "default", no instance type satisfied resources {"cpu":"1","memory":"256M","pods":"1"} and requirements karpenter.k8s.aws/instance-category In [c m t], kubernetes.io/os In [linux], kubernetes.io/arch In [amd64], karpenter.sh/provisioner-name In [default], karpenter.sh/capacity-type In [on-demand], topology.kubernetes.io/zone In [ap-northeast-2a]\t{"commit": "d7e22b1-dirty", "pod": "default/host-spread-fbbf7c9d9-x4lfd"}
```""",
        """```
2023-05-20T11:03:34.806Z	ERROR	controller.provisioner	Could not schedule pod, incompatible with provisioner "default", no instance type satisfied resources {"cpu":"1","memory":"256M","pods":"1"} and requirements karpenter.k8s.aws/instance-category In [c m t], kubernetes.io/os In [linux], kubernetes.io/arch In [amd64], karpenter.sh/provisioner-name In [default], karpenter.sh/capacity-type In [on-demand], topology.kubernetes.io/zone In [ap-northeast-2a]	{"commit": "d7e22b1-dirty", "pod": "default/host-spread-fbbf7c9d9-x4lfd"}
```""")

    # Fix the topologySpreadConstraints YAML snippet
    content = content.replace(
        """```
      - labelSelector:
          matchLabels:
            app: host-spread
        maxSkew: 2
        topologyKey: kubernetes.io/hostname
        whenUnsatisfiable: DoNotSchedule
```""",
        """```yaml
      - labelSelector:
          matchLabels:
            app: host-spread
        maxSkew: 2
        topologyKey: kubernetes.io/hostname
        whenUnsatisfiable: DoNotSchedule
```""")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Fixed: {filepath}")

if __name__ == '__main__':
    fix_karpenter_post()