---
title: "Argo-WorkFlow/Events"
date: 2023-03-21T22:59:41+09:00
draft: false
categories: ["Linux", "Kubernetes"]
tags: ["argo", "workflow", "event", "argoworkflow", "argoevents"]
slug: "argo-workflow-events"
aliases:
  - /argo-workflow-events/
  - /argo-workflow-events/
---


이글은 Argo WorkFlow로 CI를 하려했던 나의 경험담을 담고있다.


Argo WorkFlow를 쓰려고 결심하고 리서칭하는 중이라면 AirFlow가 있다. 돌아가라.


Argo WorkFlow는 Flow마다 Pod를 생성한다. 그대가 원하는 패턴이 맞는지 다시한번 생각하라. 매 Flow 마다 Pod가 만들어 지는것이 맞는가? 그렇다면 맞다 Argo WorkFlow 다.


그럼다면 다시 묻는다 CI를 위해서 Argo를 찾는것인가? K8S에서 다양한 CRD에 익숙하고 강력한 러닝커브는 즐거움으로 생각되고 CNCF에 기여하는게 꿈이라면 말리지 않겠다. 잘왔다. Argo WorkFlow/Events다.


이 글에선 CI를 다룬다. 물론 글이 깊진 않다. 하지만 찍먹으론 충분한 수준으로 그대에게 전달할 것이다. 먼저 Argo-WorkFlow 를 설치해야한다.


Argo 를 이용한 CI의 길은 친절하지 않다. 먼저 WorkFlow 설치는 이렇다.


<https://github.com/argoproj/argo-workflows/releases/download/v3.4.5/install.yaml>


다운 받는다.


<https://argoproj.github.io/argo-workflows/quick-start/>


에는 포트포워딩을 하는 방식이지만 우리는 Ingress 를 이용할거다. 그러기 위해선 install.yaml을 수정해야한다.


친절하게 하나하나 다설명하고 싶지만 내 의욕이 그렇게 길지 않기 때문에 대충 설명하겠다.


<https://github.com/Cloud-Linuxer/Argo-test/blob/main/Argo-WorkFlow-install.yaml>


이파일을 다운받던가 아래처럼 수정하자.


![](/images/2023/03/image.png)

1257 / 1258 라인을 을 추가해야한다. 그래야 백엔드가 HTTP로 동작하고 인증모드가 서버로 동작한다 혹시 쓰고싶다면 sso 를 붙여야한다.


```
k create ns argo k apply -f Argo-WorkFlow-install.yaml \ncustomresourcedefinition.apiextensions.k8s.io/clusterworkflowtemplates.argoproj.io created customresourcedefinition.apiextensions.k8s.io/cronworkflows.argoproj.io created customresourcedefinition.apiextensions.k8s.io/workflowartifactgctasks.argoproj.io created customresourcedefinition.apiextensions.k8s.io/workfloweventbindings.argoproj.io created customresourcedefinition.apiextensions.k8s.io/workflows.argoproj.io created customresourcedefinition.apiextensions.k8s.io/workflowtaskresults.argoproj.io created customresourcedefinition.apiextensions.k8s.io/workflowtasksets.argoproj.io created customresourcedefinition.apiextensions.k8s.io/workflowtemplates.argoproj.io created serviceaccount/argo created serviceaccount/argo-server created role.rbac.authorization.k8s.io/argo-role created clusterrole.rbac.authorization.k8s.io/argo-aggregate-to-admin created clusterrole.rbac.authorization.k8s.io/argo-aggregate-to-edit created clusterrole.rbac.authorization.k8s.io/argo-aggregate-to-view created clusterrole.rbac.authorization.k8s.io/argo-cluster-role created clusterrole.rbac.authorization.k8s.io/argo-server-cluster-role created rolebinding.rbac.authorization.k8s.io/argo-binding created clusterrolebinding.rbac.authorization.k8s.io/argo-binding created clusterrolebinding.rbac.authorization.k8s.io/argo-server-binding created configmap/workflow-controller-configmap created service/argo-server created priorityclass.scheduling.k8s.io/workflow-controller created deployment.apps/argo-server created deployment.apps/workflow-controller created
```


CRD부터 SA role 등등 마지막으로 2개의 deployment를 만든다. 그럼 내가 추가한 설정이 잘추가 됬는 지 확인하고 싶다면 argo-server 의 시작 로그를 확인한다.


```
k logs argo-server-5779fd7868-nb77l \ntime="2023-03-21T12:56:22.411Z" level=info msg="not enabling pprof debug endpoints" time="2023-03-21T12:56:22.411Z" level=info authModes="[server]" baseHRef=/ managedNamespace= namespace=argo secure=false ssoNamespace=argo time="2023-03-21T12:56:22.412Z" level=warning msg="You are running in insecure mode. Learn how to enable transport layer security: https://argoproj.github.io/argo-workflows/tls/" time="2023-03-21T12:56:22.412Z" level=warning msg="You are running without client authentication. Learn how to enable client authentication: https://argoproj.github.io/argo-workflows/argo-server-auth-mode/" time="2023-03-21T12:56:22.412Z" level=info msg="SSO disabled" time="2023-03-21T12:56:22.422Z" level=info msg="Starting Argo Server" instanceID= version=v3.4.5 time="2023-03-21T12:56:22.422Z" level=info msg="Creating event controller" asyncDispatch=false operationQueueSize=16 workerCount=4 time="2023-03-21T12:56:22.425Z" level=info msg="GRPC Server Max Message Size, MaxGRPCMessageSize, is set" GRPC_MESSAGE_SIZE=104857600 time="2023-03-21T12:56:22.425Z" level=info msg="Argo Server started successfully on http://localhost:2746" url="http://localhost:2746"
```


automode 에 [server] 이 들어가있다면 정상적으로 먹은거다. 기본이 Clinet다. 그리고 서버 시작로그에 url 에 https 가 아니라 http 면 백엔드가 http 인거다.


여기까지 하면 이제 WorkFlow를 사용할 준비가 아직 안된거다. 이건 단순히 컨트롤러와 argo-server UI까지만 설치한거다.


우리는 이제 왜 내글의 제목이 Argo-WorkFlow/Events 인지 알게 된다.


Argo 프로젝트로 CI를 하기위해선 WF만으로는 할수없다. Events 를 써야한다.


<https://github.com/Cloud-Linuxer/Argo-test/blob/main/Argo-Events-install.yaml>


원래 Argo-WorkFlow 와 Argo-Events 는 namespace로 분리되어있지만 나는 이 CRD의 지저분함을 견딜수없어서 argo namespace 하나로 구성했다 [Argo-Events-install.yaml](https://github.com/Cloud-Linuxer/Argo-test/blob/main/Argo-Events-install.yaml) 파일은 namespace를 수정한 파일이다.


```
 k apply -f Argo-Events-install.yaml \ncustomresourcedefinition.apiextensions.k8s.io/eventbus.argoproj.io created customresourcedefinition.apiextensions.k8s.io/eventsources.argoproj.io created customresourcedefinition.apiextensions.k8s.io/sensors.argoproj.io created serviceaccount/argo-events-sa created clusterrole.rbac.authorization.k8s.io/argo-events-aggregate-to-admin created clusterrole.rbac.authorization.k8s.io/argo-events-aggregate-to-edit created clusterrole.rbac.authorization.k8s.io/argo-events-aggregate-to-view created clusterrole.rbac.authorization.k8s.io/argo-events-role created clusterrolebinding.rbac.authorization.k8s.io/argo-events-binding created configmap/argo-events-controller-config created deployment.apps/controller-manager created
```


<https://github.com/Cloud-Linuxer/Argo-test/blob/main/Argo-EventsBus.yaml>


이벤트 버스는 Argo-Event 를 하면서 가장 인상적인 아키텍처였다.


```
k apply -f Argo-EventsBus.yaml \neventbus.argoproj.io/default created
```


이유는 이렇다.


```
 k get pod NAME                                  READY   STATUS    RESTARTS   AGE argo-server-5779fd7868-nb77l          0/1     Running   0          25m controller-manager-78bbd4559b-sd28w   1/1     Running   0          3m53s eventbus-default-stan-0               2/2     Running   0          72s eventbus-default-stan-1               2/2     Running   0          63s eventbus-default-stan-2               2/2     Running   0          54s workflow-controller-5f7f4d8-96bnm     1/1     Running   0          25m\n
```


세개의 이벤트 버스가 pod 로 뜨고,


![](/images/2023/03/image-1-1024x418.png)

https://argoproj.github.io/argo-events/concepts/architecture/


event source와 sonser 사이에서 버스역할을 하는 pod 가 있는것이었다.


여기까지 왔다면, 이제 Argo-WorkFlow/Events 를 사용할 준비가 완료된것이다.


그럼 한번 Ingress 를 배포해보자


<https://github.com/Cloud-Linuxer/Argo-test/blob/main/Argo-Server-Ingress.yaml>


```
apiVersion: networking.k8s.io/v1 kind: Ingress metadata:\n  name: argo-ingress\n  annotations:\n    alb.ingress.kubernetes.io/scheme: internet-facing\n    alb.ingress.kubernetes.io/target-type: ip\n    alb.ingress.kubernetes.io/listen-ports: '[{"HTTP": 80}]'\n    alb.ingress.kubernetes.io/security-groups: sg-0cd215a1ea38d94bf\n    alb.ingress.kubernetes.io/subnets: subnet-0b00bab5bde81c736,subnet-0928ee0c6eaaecea2\n    alb.ingress.kubernetes.io/backend-protocol: HTTP\n    alb.ingress.kubernetes.io/healthcheck-protocol: HTTP\n    alb.ingress.kubernetes.io/healthcheck-path: / spec:\n  ingressClassName: alb\n  rules:\n    - http:\n        paths:\n        - path: /\n          pathType: Prefix\n          backend:\n            service:\n              name: argo-server\n              port:\n                number: 2746
```


어차피 보안그룹 서브넷만 수정해서 넣자. 바로된다. 만약안되면 pod가 존재하는 node의 보안그룹에 2746포트를 열지않아서 그렇다. 열어주자.


![](/images/2023/03/image-2.png)

그러면 꼴뚜기 친구를 볼수있다. 이제 WorkFlow UI 까지 띄우고 Events 를 사용할 준비가 마무리 된거다.


git webhook을 이용한 간단한 테스트 정도만 이어 갈거다 걱정하지 마라. 먼저 알아야 할것은 workflow / Events 라는 놈은 CRD를 떡칠해 놨기에 우리가 생각하는 K8S의 컴포넌트 동작과는 다르다. K8S의 컴포넌트를 이용하긴 하나, 받아서 던져주는 EventBus 같은녀석도 있기때문에 Ingress 가 정상적으로 동작해도 Bus를 탈수없는 경우도 있다.


그럼 Events 로 가기전에 CRD의 RBAC를 설치해야 한다.


```
 # sensor rbac k apply -f https://raw.githubusercontent.com/argoproj/argo-events/master/examples/rbac/sensor-rbac.yaml\n # workflow rbac k apply -f https://raw.githubusercontent.com/argoproj/argo-events/master/examples/rbac/workflow-rbac.yaml
```


나는 이 RBAC를 적용하면서 사실 살짝 현타가 왔다. CRD의 모든 동작을 알순없더라도 적어도 내가 통제할수는 있는 레벨이어야 하는데 너무 쪼개진 컴포넌트 들이 나를 힘들게 했다.


자 그럼 이제 이벤트소스-웹훅-센서-트리거 를 배포해 보자.


사실 엄청 거창해 보이지만 yaml 로는 두개다.


<https://github.com/Cloud-Linuxer/Argo-test/blob/main/Argo-EventSource.yaml>


```
apiVersion: argoproj.io/v1alpha1 kind: EventSource metadata:\n  name: webhook spec:\n  service:\n    ports:\n      - port: 12000\n        targetPort: 12000\n  webhook:\n    example:\n      port: "12000"\n      endpoint: /\n      method: POST
```


EventSource 의 yaml 은 하나지만 CRD라 Service 와 Pod를 배포해준다.


```
 k get all -l eventsource-name=webhook NAME                                             READY   STATUS    RESTARTS   AGE pod/webhook-eventsource-r7x58-8575c749bb-fsjnf   1/1     Running   0          6m \nNAME                              TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)     AGE service/webhook-eventsource-svc   ClusterIP   100.64.116.226   <none>        12000/TCP   6m \nk get eventsources.argoproj.io \nNAME      AGE webhook   10m\n
```


eventsource-name=webhook label 이 붙는다. owner나 이런 저런것도 붙는다.


![](/images/2023/03/image-3.png)

그럼 이제 Sonser를 배포할거다. 이벤트소스를 통해 전달받은 웹훅을 센서가 받아서 트리거를 호출하고 실행한다.


<https://github.com/Cloud-Linuxer/Argo-test/blob/main/Argo-Sensor-Webhook.yaml>


```
k apply -f Argo-Sensor-Webhook.yaml \nsensor.argoproj.io/webhook created
```


배포가 완료되면


![](/images/2023/03/image-4.png)

이렇게 Argo WorkFlow UI에서 확인할수 있다.
그럼 웹훅까지 발생시켜 보자.


웹훅도 Ingress 로 받을 거다.


```
k get svc NAME                        TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)                      AGE argo-server                 ClusterIP   100.68.95.174    <none>        2746/TCP                     37m eventbus-default-stan-svc   ClusterIP   None             <none>        4222/TCP,6222/TCP,8222/TCP   64m webhook-eventsource-svc     ClusterIP   100.64.116.226   <none>        12000/TCP                    14m\n
```


Service를 보면 webhook-eventsource-svc Eventsource 가 있다. 이걸 Ingress 로 연결해야한다. Ingress 를 생성하면 이런식으로 두개의 Ingress 가 생긴다.


```
k get ingress NAME                       CLASS   HOSTS   ADDRESS                                                                    PORTS   AGE argo-eventsource-ingress   alb     *       k8s-argo-argoeven-44fe46d880-57919429.ap-northeast-2.elb.amazonaws.com     80      26s argo-ingress               alb     *       k8s-argo-argoingr-17062136f1-1802335500.ap-northeast-2.elb.amazonaws.com   80      44m
```


그럼 argo-eventsource-ingress 쪽으로 웹훅을 날려보자.


```
curl -d '{"message":"this is my first webhook"}' -H "Content-Type: application/json" -X POST http://k8s-argo-argoeven-44fe46d880-57919429.ap-northeast-2.elb.amazonaws.com success
```


success가 떨어질것이다. 그럼 정상적으로 실행됬는지 UI에서 확인해보자.


![](/images/2023/03/image-5-1024x288.png)

WorkFlow가 생성된게 보인다. 그럼 이걸 CLI 에서도 확인해보자.


```
k get wf NAME            STATUS      AGE   MESSAGE webhook-9vzcz   Succeeded   88s
```


정상적으로 완료됬다. 그럼 대량의 웹훅을 날린다면???


![](/images/2023/03/image-6-1024x199.png)

헤헤 주거라 WorkFlow!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


![](/images/2023/03/image-7-1024x576.png)

![](/images/2023/03/image-8-1024x904.png)

대량으로 생성된걸 확인할수 있다. 이때 pod는?


```
k get pod | grep webhook webhook-4j9gq                                0/2     Completed   0          108s webhook-4q646                                0/2     Completed   0          101s webhook-6k44h                                0/2     Completed   0          96s webhook-96w4x                                0/2     Completed   0          106s webhook-9vzcz                                0/2     Completed   0          3m58s webhook-blmsq                                0/2     Completed   0          107s webhook-eventsource-r7x58-8575c749bb-fsjnf   1/1     Running     0          26m webhook-fq6d5                                0/2     Completed   0          102s webhook-fzh2t                                0/2     Completed   0          103s webhook-g58r9                                0/2     Completed   0          103s webhook-gk9wb                                0/2     Completed   0          98s webhook-mh6b2                                0/2     Completed   0          104s webhook-mm9qx                                0/2     Completed   0          105s webhook-n9x4k                                0/2     Completed   0          106s webhook-nhd8l                                0/2     Completed   0          109s webhook-ps8z6                                0/2     Completed   0          109s webhook-qnnbd                                0/2     Completed   0          100s webhook-qrm8d                                0/2     Completed   0          97s webhook-rcztl                                0/2     Completed   0          98s webhook-sensor-lqv7w-6459d75dbb-xlkh8        1/1     Running     0          13m webhook-vs2tm                                0/2     Completed   0          99s webhook-xtfbh                                0/2     Completed   0          104s webhook-z6twq                                0/2     Completed   0          108s\n
```


늘어난다.


나는 이다음 github webhook과 인증인가 Ingress 보호등 다양한 부분을 확인하고 테스트했다. 그이후엔 셀프로 이걸 관리하면서 사용할거라면 안하는게 맞다는 결론을 내렸다.


여러분도 Workflow를 적용하려 한다면 고충이 클것이다.


이포스팅이 여러분의 앞날에 삽질을 줄여주길 바란다. 이만!
