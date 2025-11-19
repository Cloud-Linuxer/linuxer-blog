---
title: "EKS-prometheus-grafana"
date: 2021-09-18T13:57:14+09:00
draft: false
categories: ["AWS", "Linux", "Kubernetes"]
tags: ["prometheus", "grafana", "EKS"]
slug: "eks-prometheus-grafana"
aliases:
  - /eks-prometheus-grafana/
  - /eks-prometheus-grafana/
---

\n

<https://docs.aws.amazon.com/ko_kr/eks/latest/userguide/prometheus.html>

\n\n\n\n

먼저 프로메테우스를 설치한다.

\n\n\n\n

```
cat << EOF | k apply -f -\n ---\n apiVersion: v1\n kind: PersistentVolumeClaim\n metadata:\n   name: grafana-pvc\n spec:\n   accessModes:\n     - ReadWriteOnce\n   resources:\n     requests:\n       storage: 1Gi\n ---\n apiVersion: apps/v1\n kind: Deployment\n metadata:\n   labels:\n     app: grafana\n   name: grafana\n spec:\n   selector:\n     matchLabels:\n       app: grafana\n   template:\n     metadata:\n       labels:\n         app: grafana\n     spec:\n       securityContext:\n         fsGroup: 472\n         supplementalGroups:\n           - 0\n       containers:\n         - name: grafana\n           image: grafana/grafana:7.5.2\n           imagePullPolicy: IfNotPresent\n           ports:\n             - containerPort: 3000\n               name: http-grafana\n               protocol: TCP\n           readinessProbe:\n             failureThreshold: 3\n             httpGet:\n               path: /robots.txt\n               port: 3000\n               scheme: HTTP\n             initialDelaySeconds: 10\n             periodSeconds: 30\n             successThreshold: 1\n             timeoutSeconds: 2\n           livenessProbe:\n             failureThreshold: 3\n             initialDelaySeconds: 30\n             periodSeconds: 10\n             successThreshold: 1\n             tcpSocket:\n               port: 3000\n             timeoutSeconds: 1\n           resources:\n             requests:\n               cpu: 250m\n               memory: 750Mi\n           volumeMounts:\n             - mountPath: /var/lib/grafana\n               name: grafana-pv\n       volumes:\n         - name: grafana-pv\n           persistentVolumeClaim:\n             claimName: grafana-pvc\n ---\n apiVersion: v1\n kind: Service\n metadata:\n   name: grafana\n spec:\n   ports:\n     - port: 3000\n       protocol: TCP\n       targetPort: http-grafana\n   selector:\n     app: grafana\n   sessionAffinity: None\n   type: LoadBalancer\n EOF
```

\n\n\n\n

<https://grafana.com/docs/grafana/latest/installation/kubernetes/>

\n\n\n\n

설치는 위링크를 참조하고 grafana svc type 만 LoadBalancer 로 변경한다.

\n\n\n\n

```
k get svc\nNAME         TYPE           CLUSTER-IP       EXTERNAL-IP                                                                   PORT(S)          AGE\ngrafana      LoadBalancer   172.20.237.228   af7fa7486f6eb4ad4a6bde897210f4a9-206885623.ap-northeast-2.elb.amazonaws.com   3000:32317/TCP   32m
```

\n\n\n\n

그라파나의 서비스가 다만들어지면 URL로 접근이 가능하다.

\n\n\n\n
![](/images/2021/09/image-10-1024x967.png)
\n\n\n\n

패스워드는 admin / admin 이다.

\n\n\n\n

로그인후 할일은 data source 를 지정하는것이다. 우리는 prometheus 를 이용할것이다.

\n\n\n\n
![](/images/2021/09/image-12-426x1024.png)
\n\n\n\n
![](/images/2021/09/image-11-1024x310.png)
\n\n\n\n

서비스이름/네임스페이스/svc:port 로 지정한다.

\n\n\n\n

save & test 눌러서 잘되는지 확인하자.

\n\n\n\n

그리고 dashboard를 import 하자.

\n\n\n\n
![](/images/2021/09/image-13.png)
\n\n\n\n

<https://grafana.com/grafana/dashboards/11074>

\n\n\n\n

많은 사람이 애용하는 dashboard를 사용할것이다. import 는 ID로 넣으면된다 이경우엔 11074 를 입력하자

\n\n\n\n
![](/images/2021/09/image-14-1024x923.png)
\n\n\n\n

VictoriaMetrics 를 프로메테우스로 지정하자. 그리고 Import 하면 대시보드가 뜬다.

\n\n\n\n
![](/images/2021/09/image-15-1024x661.png)
\n\n\n\n

대략 이런 대시보드가 자동으로 수집된다.

\n\n\n\n\n\n\n\n
![](/images/2021/09/image-16-1024x515.png)

https://grafana.com/grafana/dashboards/13770

\n\n\n\n

그라파나는 사람들이 만들어놓은 대시보드를 이용하기 쉽다.

\n\n\n\n

그리고 node-exporter 로 만들어내는 매트릭리스트를 파악하여 원하는 지표를 사용할수 있다.

\n\n\n\n

<https://prometheus.io/docs/guides/node-exporter/>

\n\n\n\n

위URL을 참고해서 매트릭을 확인하여 보자.

\n\n\n\n

예를 들어서 Dropped packet를 확인하려 한다면 다음 매트릭을 확인할수 있다.

\n\n\n\n
![](/images/2021/09/image-17-1024x579.png)
\n\n\n\n\n\n\n\n

읽어주셔서 감사하다!

\n\n\n\n

올해의 가시다님 과의 스터디가 마무리되었다. 같이 EKS 스터디에 참여해주신분들께 감사를 드리며, 평안한 하루되시라!

\n\n\n\n\n