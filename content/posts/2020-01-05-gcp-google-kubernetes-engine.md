---
title: "gcp- Google Kubernetes Engine"
date: 2020-01-05T14:15:25+09:00
draft: false
categories: ["GCP"]
tags: ["gcp", "k8s", "kubectl", "Kubernetes"]
slug: "gcp-google-kubernetes-engine"
aliases:
  - /gcp-google-kubernetes-engine/
  - /gcp-google-kubernetes-engine/
---

\n

<https://cloud.google.com/kubernetes-engine/docs/quickstart?hl=ko>

\n\n\n\n

먼저 cloud shell 에서 프로젝트 지정하고 리전(아님)을 지정한다. - 수정- zone 을 지정한다.

\n\n\n\n

linuxer@cloudshell:~ (elated-ranger-263505)$ gcloud config set compute/zone us-central1-a   
 Updated property [compute/zone].

\n\n\n\n

그리고 컨테이너 클러스터를 생성한다.

\n\n\n\n

linuxer@cloudshell:**~ (elated-ranger-263505)**$ gcloud container clusters create linuxer-k8s

\n\n\n\n
![](/images/2020/01/image-13-1024x116.png)

WARNING: Currently VPC-native is not the default mode during cluster creation. In the future, this will become the default mode and can be disabled using `--no-enable-ip-ali as` flag. Use `--[no-]enable-ip-alias` flag to suppress this warning.  
 WARNING: Newly created clusters and node-pools will have node auto-upgrade enabled by default. This can be disabled using the `--no-enable-autoupgrade` flag.  
 WARNING: Starting in 1.12, default node pools in new clusters will have their legacy Compute Engine instance metadata endpoints disabled by default. To create a cluster with  
 legacy instance metadata endpoints disabled in the default node pool, run `clusters create` with the flag `--metadata disable-legacy-endpoints=true`.  
 WARNING: Your Pod address range (`--cluster-ipv4-cidr`) can accommodate at most 1008 node(s).  
 This will enable the autorepair feature for nodes. Please see https://cloud.google.com/kubernetes-engine/docs/node-auto-repair for more information on node autorepairs.  
 ERROR: (gcloud.container.clusters.create) ResponseError: code=403, message=Kubernetes Engine API is not enabled for this project. Please ensure it is enabled in Google Cloud  
 Console and try again: visit https://console.cloud.google.com/apis/api/container.googleapis.com/overview?project=elated-ranger-26 to do so.

\n\n\n\n

api error 는 역시나 사이트로 이동해서 허용해준다.

\n\n\n\n

zone 을 지정하지 않고 리전을 자꾸 지정해서 클러스터를 생성할 수 없었다.

\n\n\n\n

서태호님께서 잘못된 부분을 알려주셨다. 덕분에 진행할수 있었다.ㅜㅜ다행

\n\n\n\n

gcloud container clusters get-credentials linuxer-k8s@cloudshell:~ (jth3434-197516)$ gcloud config set compute/zone us-central1-a

\n\n\n\n
![](/images/2020/01/image-17-1024x261.png)
\n\n\n\n

정상적으로 클러스터를 생성하고

\n\n\n\n

@cloudshell:~ (jth3434-197516)$ gcloud container clusters get-credentials linuxer-k8s

\n\n\n\n

클러스터 사용자 인증하고~

\n\n\n\n

<https://github.com/GoogleCloudPlatform/kubernetes-engine-samples/tree/master/hello-app>

\n\n\n\n

URL 참고하시고 hello-app 으로 deployment 한다.

\n\n\n\n

@cloudshell:~/hello-app (jth3434-197516)$ kubectl create deployment hello-server --image=gcr.io/google-samples/hello-app:1.0

\n\n\n\n

hello-app ver 1.0 이다. dockerfile 을 확인하면 컨테이너 설정을 확인할수 있다.

\n\n\n\n

kubectl expose 를 이용하여 생성한 파일을 노출한다.

\n\n\n\n
![](/images/2020/01/image-18-1024x154.png)
\n\n\n\n

@cloudshell:~/hello-app (jth3434-197516)$ kubectl get pods  
 NAME READY STATUS RESTARTS AGE  
 hello-server-64db4d4dc7-xtrcd 1/1 Running 0 12m  
 @cloudshell:~/hello-app (jth3434-197516)$ kubectl get service hello-server  
 NAME TYPE CLUSTER-IP EXTERNAL-IP PORT(S) AGE  
 hello-server LoadBalancer 10.35.255.80 35.223.145.93 80:30201/TCP 5m30s

\n\n\n\n

그리고 get pads 으로 pads 의 상태를 확인하고 서비스를 확인해서 정상적으로 external-ip로 접속했을때 접속이 되면 정상이다.

\n\n\n\n\n