---
title: "AKOS-Study-Manual-EKS-istio"
date: 2021-09-04T13:03:59+09:00
draft: false
categories: ["AWS", "Kubernetes"]
tags: ["k8s", "istio", "istio-injection"]
slug: "akos-study-manual-eks-istio"
aliases:
  - /akos-study-manual-eks-istio/
  - /akos-study-manual-eks-istio/
---

\n

클러스터를 먼저 프로비저닝 했다. 30분이상이 걸리는 작업이므로 시작해놓고 기다린다.

\n\n\n\n

```
eksctl create cluster --vpc-public-subnets $WKSubnets --name $CLUSTER_NAME --region $AWS_REGION --version 1.21 \\\n> --nodegroup-name $CLUSTER_NAME-nodegroup --node-type t3.medium --nodes 3 --nodes-min 3 --nodes-max 6 \\\n> --with-oidc --node-volume-size=20 --ssh-access --ssh-public-key $MySSHKeypair\n2021-09-04 11:29:11 [ℹ]  eksctl version 0.63.0\n2021-09-04 11:29:11 [ℹ]  using region ap-northeast-2\n2021-09-04 11:29:12 [✔]  using existing VPC (vpc-094808933b68add7c) and subnets (private:map[] public:map[ap-northeast-2a:{subnet-0a603a222db0cce10 ap-northeast-2a 10.0.11.0/24} ap-northeast-2b:{subnet-007964ce4a003361a ap-northeast-2b 10.0.12.0/24} ap-northeast-2c:{subnet-007813cf58631ef3b ap-northeast-2c 10.0.13.0/24}])\n2021-09-04 11:29:12 [!]  custom VPC/subnets will be used; if resulting cluster doesn't function as expected, make sure to review the configuration of VPC/subnets\n2021-09-04 11:29:12 [ℹ]  nodegroup "first-eks-nodegroup" will use "" [AmazonLinux2/1.21]\n2021-09-04 11:29:12 [ℹ]  using EC2 key pair %!q(*string=<nil>)\n2021-09-04 11:29:12 [ℹ]  using Kubernetes version 1.21\n2021-09-04 11:29:12 [ℹ]  creating EKS cluster "first-eks" in "ap-northeast-2" region with managed nodes\n2021-09-04 11:29:12 [ℹ]  will create 2 separate CloudFormation stacks for cluster itself and the initial managed nodegroup\n2021-09-04 11:29:12 [ℹ]  if you encounter any issues, check CloudFormation console or try 'eksctl utils describe-stacks --region=ap-northeast-2 --cluster=first-eks'\n2021-09-04 11:29:12 [ℹ]  CloudWatch logging will not be enabled for cluster "first-eks" in "ap-northeast-2"\n2021-09-04 11:29:12 [ℹ]  you can enable it with 'eksctl utils update-cluster-logging --enable-types={SPECIFY-YOUR-LOG-TYPES-HERE (e.g. all)} --region=ap-northeast-2 --cluster=first-eks'\n2021-09-04 11:29:12 [ℹ]  Kubernetes API endpoint access will use default of {publicAccess=true, privateAccess=false} for cluster "first-eks" in "ap-northeast-2"\n2021-09-04 11:29:12 [ℹ]  2 sequential tasks: { create cluster control plane "first-eks", 3 sequential sub-tasks: { 4 sequential sub-tasks: { wait for control plane to become ready, associate IAM OIDC provider, 2 sequential sub-tasks: { create IAM role for serviceaccount "kube-system/aws-node", create serviceaccount "kube-system/aws-node" }, restart daemonset "kube-system/aws-node" }, 1 task: { create addons }, create managed nodegroup "first-eks-nodegroup" } }\n2021-09-04 11:29:12 [ℹ]  building cluster stack "eksctl-first-eks-cluster"\n2021-09-04 11:29:12 [ℹ]  deploying stack "eksctl-first-eks-cluster"\n2021-09-04 11:29:42 [ℹ]  waiting for CloudFormation stack "eksctl-first-eks-cluster"\n2021-09-04 11:30:12 [ℹ]  waiting for CloudFormation stack "eksctl-first-eks-cluster"\n2021-09-04 11:31:12 [ℹ]  waiting for CloudFormation stack "eksctl-first-eks-cluster"\n2021-09-04 11:32:12 [ℹ]  waiting for CloudFormation stack "eksctl-first-eks-cluster"\n2021-09-04 11:33:12 [ℹ]  waiting for CloudFormation stack "eksctl-first-eks-cluster"\n2021-09-04 11:34:12 [ℹ]  waiting for CloudFormation stack "eksctl-first-eks-cluster"\n2021-09-04 11:35:12 [ℹ]  waiting for CloudFormation stack "eksctl-first-eks-cluster"\n2021-09-04 11:36:12 [ℹ]  waiting for CloudFormation stack "eksctl-first-eks-cluster"\n2021-09-04 11:37:12 [ℹ]  waiting for CloudFormation stack "eksctl-first-eks-cluster"\n2021-09-04 11:38:12 [ℹ]  waiting for CloudFormation stack "eksctl-first-eks-cluster"\n2021-09-04 11:39:12 [ℹ]  waiting for CloudFormation stack "eksctl-first-eks-cluster"\n2021-09-04 11:40:13 [ℹ]  waiting for CloudFormation stack "eksctl-first-eks-cluster"\n2021-09-04 11:41:13 [ℹ]  waiting for CloudFormation stack "eksctl-first-eks-cluster"\n2021-09-04 11:45:14 [ℹ]  building iamserviceaccount stack "eksctl-first-eks-addon-iamserviceaccount-kube-system-aws-node"\n2021-09-04 11:45:14 [ℹ]  deploying stack "eksctl-first-eks-addon-iamserviceaccount-kube-system-aws-node"
```

\n\n\n\n

EKS를 Setup 하는 과정에 대해선 이전포스팅을 참고하기 바란다.

\n\n\n\n

\nhttps://linuxer.name/2021/08/akos-study-manual-eks-setup/\n

\n\n\n\n

간단한 실습이 있지만..음 istio는 못참지.

\n\n\n\n

가즈아!

\n\n\n\n\n\n\n\n

먼저 istioctl을 설치하자.

\n\n\n\n

```
curl -L https://istio.io/downloadIstio | ISTIO_VERSION=1.10.4 TARGET_ARCH=x86_64 sh -\ntree istio-1.10.4/ -L 2\nmv istio-1.10.4/bin/istioctl /usr/local/bin/istioctl\nistioctl version
```

\n\n\n\n

버전과 상황에 따라 설치 방법이 다를 수 있다.

\n\n\n\n

```
istioctl install --set profile=demo -y
```

\n\n\n\n

demo로 프로파일을 설정하게되면 istio에서 사용하는 모든 오브젝트를 설치해준다. 그러므로 만약 프로덕션에서 사용한다면 원하는 오브젝트만 따로 설치하자.

\n\n\n\n

nginx pod에 istio inject 명령어로 yaml 에 istio를 주입하면 이렇게 된다.

\n\n\n\n

```
#전\napiVersion: v1\nkind: Pod\nmetadata:\n  name: pod1\nspec:\n  containers:\n  - name: nginx\n    image: nginx\n    ports:\n    - containerPort: 80\n#후    \nistioctl kube-inject -f pod1.yaml\napiVersion: v1\nkind: Pod\nmetadata:\n  annotations:\n    kubectl.kubernetes.io/default-container: nginx\n    kubectl.kubernetes.io/default-logs-container: nginx\n    prometheus.io/path: /stats/prometheus\n    prometheus.io/port: "15020"\n    prometheus.io/scrape: "true"\n    sidecar.istio.io/status: '{"initContainers":["istio-init"],"containers":["istio-proxy"],"volumes":["istio-envoy","istio-data","istio-podinfo","istio-token","istiod-ca-cert"],"imagePullSecrets":null}'\n  creationTimestamp: null\n  labels:\n    istio.io/rev: default\n    security.istio.io/tlsMode: istio\n    service.istio.io/canonical-name: pod1\n    service.istio.io/canonical-revision: latest\n  name: pod1\nspec:\n  containers:\n  - image: nginx\n    name: nginx\n    ports:\n    - containerPort: 80\n    resources: {}\n  - args:\n    - proxy\n    - sidecar\n    - --domain\n    - $(POD_NAMESPACE).svc.cluster.local\n    - --serviceCluster\n    - pod1.default\n    - --proxyLogLevel=warning\n    - --proxyComponentLogLevel=misc:error\n    - --log_output_level=default:info\n    - --concurrency\n    - "2"\n    env:\n    - name: JWT_POLICY\n      value: third-party-jwt\n    - name: PILOT_CERT_PROVIDER\n      value: istiod\n    - name: CA_ADDR\n      value: istiod.istio-system.svc:15012\n    - name: POD_NAME\n      valueFrom:\n        fieldRef:\n          fieldPath: metadata.name\n    - name: POD_NAMESPACE\n      valueFrom:\n        fieldRef:\n          fieldPath: metadata.namespace\n    - name: INSTANCE_IP\n      valueFrom:\n        fieldRef:\n          fieldPath: status.podIP\n    - name: SERVICE_ACCOUNT\n      valueFrom:\n        fieldRef:\n          fieldPath: spec.serviceAccountName\n    - name: HOST_IP\n      valueFrom:\n        fieldRef:\n          fieldPath: status.hostIP\n    - name: CANONICAL_SERVICE\n      valueFrom:\n        fieldRef:\n          fieldPath: metadata.labels['service.istio.io/canonical-name']\n    - name: CANONICAL_REVISION\n      valueFrom:\n        fieldRef:\n          fieldPath: metadata.labels['service.istio.io/canonical-revision']\n    - name: PROXY_CONFIG\n      value: |\n        {}\n    - name: ISTIO_META_POD_PORTS\n      value: |-\n        [\n            {"containerPort":80}\n        ]\n    - name: ISTIO_META_APP_CONTAINERS\n      value: nginx\n    - name: ISTIO_META_CLUSTER_ID\n      value: Kubernetes\n    - name: ISTIO_META_INTERCEPTION_MODE\n      value: REDIRECT\n    - name: ISTIO_META_WORKLOAD_NAME\n      value: pod1\n    - name: ISTIO_META_OWNER\n      value: kubernetes://apis/v1/namespaces/default/pods/pod1\n    - name: ISTIO_META_MESH_ID\n      value: cluster.local\n    - name: TRUST_DOMAIN\n      value: cluster.local\n    image: docker.io/istio/proxyv2:1.10.4\n    name: istio-proxy\n    ports:\n    - containerPort: 15090\n      name: http-envoy-prom\n      protocol: TCP\n    readinessProbe:\n      failureThreshold: 30\n      httpGet:\n        path: /healthz/ready\n        port: 15021\n      initialDelaySeconds: 1\n      periodSeconds: 2\n      timeoutSeconds: 3\n    resources:\n      limits:\n        cpu: "2"\n        memory: 1Gi\n      requests:\n        cpu: 10m\n        memory: 40Mi\n    securityContext:\n      allowPrivilegeEscalation: false\n      capabilities:\n        drop:\n        - ALL\n      privileged: false\n      readOnlyRootFilesystem: true\n      runAsGroup: 1337\n      runAsNonRoot: true\n      runAsUser: 1337\n    volumeMounts:\n    - mountPath: /var/run/secrets/istio\n      name: istiod-ca-cert\n    - mountPath: /var/lib/istio/data\n      name: istio-data\n    - mountPath: /etc/istio/proxy\n      name: istio-envoy\n    - mountPath: /var/run/secrets/tokens\n      name: istio-token\n    - mountPath: /etc/istio/pod\n      name: istio-podinfo\n  initContainers:\n  - args:\n    - istio-iptables\n    - -p\n    - "15001"\n    - -z\n    - "15006"\n    - -u\n    - "1337"\n    - -m\n    - REDIRECT\n    - -i\n    - '*'\n    - -x\n    - ""\n    - -b\n    - '*'\n    - -d\n    - 15090,15021,15020\n    image: docker.io/istio/proxyv2:1.10.4\n    name: istio-init\n    resources:\n      limits:\n        cpu: "2"\n        memory: 1Gi\n      requests:\n        cpu: 10m\n        memory: 40Mi\n    securityContext:\n      allowPrivilegeEscalation: false\n      capabilities:\n        add:\n        - NET_ADMIN\n        - NET_RAW\n        drop:\n        - ALL\n      privileged: false\n      readOnlyRootFilesystem: false\n      runAsGroup: 0\n      runAsNonRoot: false\n      runAsUser: 0\n  volumes:\n  - emptyDir:\n      medium: Memory\n    name: istio-envoy\n  - emptyDir: {}\n    name: istio-data\n  - downwardAPI:\n      items:\n      - fieldRef:\n          fieldPath: metadata.labels\n        path: labels\n      - fieldRef:\n          fieldPath: metadata.annotations\n        path: annotations\n      - path: cpu-limit\n        resourceFieldRef:\n          containerName: istio-proxy\n          divisor: 1m\n          resource: limits.cpu\n      - path: cpu-request\n        resourceFieldRef:\n          containerName: istio-proxy\n          divisor: 1m\n          resource: requests.cpu\n    name: istio-podinfo\n  - name: istio-token\n    projected:\n      sources:\n      - serviceAccountToken:\n          audience: istio-ca\n          expirationSeconds: 43200\n          path: istio-token\n  - configMap:\n      name: istio-ca-root-cert\n    name: istiod-ca-cert\nstatus: {}\n---\n
```

\n\n\n\n

istio의 sidecar가 nginx pod에 삽입되게 된다.

\n\n\n\n

```
      limits:\n        cpu: "2"\n        memory: 1Gi\n      requests:\n        cpu: 10m\n        memory: 40Mi
```

\n\n\n\n

사용하는 자원의 제한은 위와같다. istio-init(initcontainer) proxy(envoy) 가 추가된다.

\n\n\n\n

```
kubectl label namespace default istio-injection=enabled\nnamespace/default labeled\nkubectl get ns -L istio-injection\nNAME              STATUS   AGE   ISTIO-INJECTION\ndefault           Active   46m   enabled
```

\n\n\n\n

namespace 에 라벨을 붙이면 자동으로 그뒤론 NS 에 sidecar가 붙게된다.

\n\n\n\n

```
k run nginx-istio --image=nginx --restart=Never\npod/nginx-istio created\nk get pod\nNAME          READY   STATUS            RESTARTS   AGE\nnginx-istio   0/2     PodInitializing   0          4s\npod1          2/2     Running           0          5m11s
```

\n\n\n\n

이제 sidecar를 본격적으로 확인해보자.

\n\n\n\n

```
kubectl apply -f istio-1.10.4/samples/addons
```

\n\n\n\n

아까 다운로드한 istio 에서 샘플로제공된 애드온을 설치한다. 위와같은 명령어를 치면 모든 애드온이 설치된다. 애드온내부에 있는 특정 애드온만도 설치가능하니 필요하면 특정 애드온만 설치해도 된다.

\n\n\n\n

kiali.yaml 를 설치할때 kind 에 MonitoringDashboard 가 있어야 설치가 되는데 처음에 한꺼번에 다 배포를 하면 실패한다 그럼 그냥 쿨하게 명령어 한번더 입력해주자.

\n\n\n\n

이제 애드온으로 접근하기위해선 애드온의 서비스를 퍼블릭하게 변경해줘야하는데, 나는 이전에는 yaml를 손수 수정했는데 이부분이 싱크빅하다.

\n\n\n\n

```
k get svc -n istio-system grafana -o yaml | sed -e "s/type: ClusterIP/type: LoadBalancer/" | kubectl apply -f -\nservice/grafana configured\nk get svc -n istio-system kiali -o yaml | sed -e "s/type: ClusterIP/type: LoadBalancer/" | kubectl apply -f -\nservice/kiali configured\nk get svc -n istio-system tracing -o yaml | sed -e "s/type: ClusterIP/type: LoadBalancer/" | kubectl apply -f -\nservice/tracing configured
```

\n\n\n\n

sed 로 수정해서 바로 적용한다. 와우..당연히 내가 못하는건 아닌데 관념의 차이로 인하여 이런 사용을 생각못했다. 다음엔 써먹어야지

\n\n\n\n

```
ubectl get svc -n istio-system\nNAME                   TYPE           CLUSTER-IP      EXTERNAL-IP                                                                    PORT(S)                                                AGE\ngrafana                LoadBalancer   172.20.162.75   a6d32baedc66b4633bb7fbb0875c6132-465014933.ap-northeast-2.elb.amazonaws.com    3000:30572/TCP                                                3m51s\nistio-egressgateway    ClusterIP      172.20.129.21   <none>                                                                         80/TCP,443/TCP                                                21m\nistio-ingressgateway   LoadBalancer   172.20.95.93    a0e6177dd9cb64884bd2893028c04328-781274984.ap-northeast-2.elb.amazonaws.com    15021:31227/TCP,80:30590/TCP,443:32395/TCP,31400:32264/TCP,15443:32750/TCP   21m\nistiod                 ClusterIP      172.20.90.49    <none>                                                                         15010/TCP,15012/TCP,443/TCP,15014/TCP                                        21m\njaeger-collector       ClusterIP      172.20.99.248   <none>                                                                         14268/TCP,14250/TCP                                                3m51s\nkiali                  LoadBalancer   172.20.96.205   a313dbdb158064d578d88c0a022bc845-1007771282.ap-northeast-2.elb.amazonaws.com   20001:30296/TCP,9090:30713/TCP                                               3m51s\nprometheus             ClusterIP      172.20.50.6     <none>                                                                         9090/TCP                                                3m50s\ntracing                LoadBalancer   172.20.58.118   a9da5b64099ed4fd3b5abdf3b1cd9ebe-68617878.ap-northeast-2.elb.amazonaws.com     80:30295/TCP                                                3m51s\nzipkin                 ClusterIP      172.20.76.230   <none>                                                                         9411/TCP                                                3m51s
```

\n\n\n\n

샘플 manifest 중에 bookinfo 가 있다.

\n\n\n\n
![](/images/2021/09/image-6-1024x682.png)
\n\n\n\n

샘플에서 보여주는것은 트래픽이 어떻게 흐르는지 시각화로 보여주는것이다.

\n\n\n\n
![](/images/2021/09/image-7-1024x383.png)
\n\n\n\n

문제가 생길경우 다음과같이 UI 와 로깅으로 확인이 가능하다.

\n\n\n\n

```
apiVersion: networking.istio.io/v1alpha3\nkind: VirtualService\nmetadata:\n  name: reviews\nspec:\n  hosts:\n    - reviews\n  http:\n  - route:\n    - destination:\n        host: reviews\n        subset: v2\n      weight: 50\n    - destination:\n        host: reviews\n        subset: v3\n      weight: 50
```

\n\n\n\n

위의 에러는 기본적인 destination rule 을 설정하지 않은 상태로 review 에 대한 룰을 설정해서 그렇다.

\n\n\n\n

```
apiVersion: networking.istio.io/v1alpha3\nkind: DestinationRule\nmetadata:\n  name: productpage\nspec:\n  host: productpage\n  subsets:\n  - name: v1\n    labels:\n      version: v1\n---\napiVersion: networking.istio.io/v1alpha3\nkind: DestinationRule\nmetadata:\n  name: reviews\nspec:\n  host: reviews\n  subsets:\n  - name: v1\n    labels:\n      version: v1\n  - name: v2\n    labels:\n      version: v2\n  - name: v3\n    labels:\n      version: v3\n---\napiVersion: networking.istio.io/v1alpha3\nkind: DestinationRule\nmetadata:\n  name: ratings\nspec:\n  host: ratings\n  subsets:\n  - name: v1\n    labels:\n      version: v1\n  - name: v2\n    labels:\n      version: v2\n  - name: v2-mysql\n    labels:\n      version: v2-mysql\n  - name: v2-mysql-vm\n    labels:\n      version: v2-mysql-vm\n---\napiVersion: networking.istio.io/v1alpha3\nkind: DestinationRule\nmetadata:\n  name: details\nspec:\n  host: details\n  subsets:\n  - name: v1\n    labels:\n      version: v1\n  - name: v2\n    labels:\n      version: v2\n---
```

\n\n\n\n

destination rule 을 설정하고 보면 reviews rule 이 정상적으로 작동하는것을 알수있다.

\n\n\n\n
![](/images/2021/09/image-9.png)

적용전

\n\n\n\n
![](/images/2021/09/image-8.png)

적용후

\n\n\n\n

가중치에 의하여 v2/v3로만 라우팅 되는것을 확인할수 있다.

\n\n\n\n

istio는 조만간 블로그에 적용후에 더 자세히 다뤄보도록 하겠다.

\n\n\n\n

좋은 주말되시라!

\n