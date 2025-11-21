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


<https://docs.aws.amazon.com/ko_kr/eks/latest/userguide/prometheus.html>

먼저 프로메테우스를 설치한다.

```
cat << EOF | k apply -f -
 ---
 apiVersion: v1
 kind: PersistentVolumeClaim
 metadata:
   name: grafana-pvc
 spec:
   accessModes:

     - ReadWriteOnce
   resources:
     requests:
       storage: 1Gi
 ---
 apiVersion: apps/v1
 kind: Deployment
 metadata:
   labels:
     app: grafana
   name: grafana
 spec:
   selector:
     matchLabels:
       app: grafana
   template:
     metadata:
       labels:
         app: grafana
     spec:
       securityContext:
         fsGroup: 472
         supplementalGroups:

           - 0
       containers:

         - name: grafana
           image: grafana/grafana:7.5.2
           imagePullPolicy: IfNotPresent
           ports:

             - containerPort: 3000
               name: http-grafana
               protocol: TCP
           readinessProbe:
             failureThreshold: 3
             httpGet:
               path: /robots.txt
               port: 3000
               scheme: HTTP
             initialDelaySeconds: 10
             periodSeconds: 30
             successThreshold: 1
             timeoutSeconds: 2
           livenessProbe:
             failureThreshold: 3
             initialDelaySeconds: 30
             periodSeconds: 10
             successThreshold: 1
             tcpSocket:
               port: 3000
             timeoutSeconds: 1
           resources:
             requests:
               cpu: 250m
               memory: 750Mi
           volumeMounts:

             - mountPath: /var/lib/grafana
               name: grafana-pv
       volumes:

         - name: grafana-pv
           persistentVolumeClaim:
             claimName: grafana-pvc
 ---
 apiVersion: v1
 kind: Service
 metadata:
   name: grafana
 spec:
   ports:

     - port: 3000
       protocol: TCP
       targetPort: http-grafana
   selector:
     app: grafana
   sessionAffinity: None
   type: LoadBalancer
 EOF
```
<https://grafana.com/docs/grafana/latest/installation/kubernetes/>

설치는 위링크를 참조하고 grafana svc type 만 LoadBalancer 로 변경한다.

```
k get svc NAME         TYPE           CLUSTER-IP       EXTERNAL-IP                                                                   PORT(S)          AGE grafana      LoadBalancer   172.20.237.228   af7fa7486f6eb4ad4a6bde897210f4a9-206885623.ap-northeast-2.elb.amazonaws.com   3000:32317/TCP   32m
```
그라파나의 서비스가 다만들어지면 URL로 접근이 가능하다.

![](/images/2021/09/image-10-1024x967.png)

패스워드는 admin / admin 이다.

로그인후 할일은 data source 를 지정하는것이다. 우리는 prometheus 를 이용할것이다.

![](/images/2021/09/image-12-426x1024.png)

![](/images/2021/09/image-11-1024x310.png)

서비스이름/네임스페이스/svc:port 로 지정한다.

save & test 눌러서 잘되는지 확인하자.

그리고 dashboard를 import 하자.

![](/images/2021/09/image-13.png)

<https://grafana.com/grafana/dashboards/11074>

많은 사람이 애용하는 dashboard를 사용할것이다. import 는 ID로 넣으면된다 이경우엔 11074 를 입력하자

![](/images/2021/09/image-14-1024x923.png)

VictoriaMetrics 를 프로메테우스로 지정하자. 그리고 Import 하면 대시보드가 뜬다.

![](/images/2021/09/image-15-1024x661.png)

대략 이런 대시보드가 자동으로 수집된다.

![](/images/2021/09/image-16-1024x515.png)

https://grafana.com/grafana/dashboards/13770

그라파나는 사람들이 만들어놓은 대시보드를 이용하기 쉽다.

그리고 node-exporter 로 만들어내는 매트릭리스트를 파악하여 원하는 지표를 사용할수 있다.

<https://prometheus.io/docs/guides/node-exporter/>

위URL을 참고해서 매트릭을 확인하여 보자.

예를 들어서 Dropped packet를 확인하려 한다면 다음 매트릭을 확인할수 있다.

![](/images/2021/09/image-17-1024x579.png)

읽어주셔서 감사하다!

올해의 가시다님 과의 스터디가 마무리되었다. 같이 EKS 스터디에 참여해주신분들께 감사를 드리며, 평안한 하루되시라!
