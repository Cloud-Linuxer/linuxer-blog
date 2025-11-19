---
title: "K8s-one-line-Challenge"
date: 2021-07-22T01:07:03+09:00
draft: false
categories: ["Linux", "Kubernetes"]
tags: ["k8s", "jsonpath", "json", "label", "kubenetes"]
slug: "k8s-one-line-challenge"
aliases:
  - /k8s-one-line-challenge/
  - /k8s-one-line-challenge/
---


![](/images/2021/07/image-1.png)

잔잔한 호수에 돌맹이는 내가던졌다.


![](/images/2021/07/image-2.png)

K8s의 Service는 selector 에서 지정한 label로 pod에게 트래픽을 흘린다.


그런데 아이러니하게도 service 에서 연결된 pod를 한번에 조회할순 없다.


service 에서 selector 나 endpoint를 확인해서 labels 를 보고 확인해야 한다. 그 과정을 한번 보자.


my-service1 이라는 서비스에서 사용하는 pod를 조회할꺼다.


```
k get svc -o wide NAME          TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)        AGE     SELECTOR kubernetes    ClusterIP   198.19.128.1     <none>        443/TCP        2d13h   <none> my-service1   NodePort    198.19.231.233   <none>        80:30001/TCP   2d12h   app=my-nginx1 my-service2   NodePort    198.19.172.176   <none>        80:30002/TCP   2d12h   app=my-nginx2 my-service3   NodePort    198.19.200.20    <none>        80:30003/TCP   2d12h   app=my-nginx3 \nk get pods -l app=my-nginx1 --show-labels \nNAME                         READY   STATUS    RESTARTS   AGE   LABELS my-nginx1-67f499d79c-g7vr7   1/1     Running   0          26h   app=my-nginx1,pod-template-hash=67f499d79c my-nginx1-67f499d79c-j4f9k   1/1     Running   0          26h   app=my-nginx1,pod-template-hash=67f499d79c my-nginx1-67f499d79c-mqxzs   1/1     Running   1          26h   app=my-nginx1,pod-template-hash=67f499d79c
```


kubectl. 에서 svc 를 get하고 -o wide 명령어를 쓰면 selector 가보인다. 거기서 get pod -l app=my-nginx1 이라 일일이 지정해줘야지만 확인할수 있다. 명령어 두줄치면 되긴한데 귀찮다. 이렇게 된이상 한줄치기는 물러설수 없다.


![](/images/2021/07/image.png)

미끼를 물어주신 iamai 님께 감사를 드린다. - 재차 감사! - 예아!


```
kubectl get endpoints |grep my-service1 |awk '{print $2}'|tr "," "\ " |awk -F":" '{print $1}' |grep -f - <(kubectl get po -o wide) my-nginx1-67f499d79c-g7vr7   1/1     Running    0          26h   198.18.0.74    nks-pool-1119-w-gzg   <none>           <none> my-nginx1-67f499d79c-j4f9k   1/1     Running    0          26h   198.18.2.250   nks-pool-1119-w-gzh   <none>           <none> my-nginx1-67f499d79c-mqxzs   1/1     Running    1          26h   198.18.1.208   nks-pool-1119-w-gzi   <none>           <none>\n
```


endpoint 에서 조회된 IP를 awk 로 떼어서 한줄씩으로 변환후 포트를 제거한다. 그리고 pod list 에서 IP가 grep 된 줄만 출력한다.


```
[root@linuxer-bastion ~]# kubectl get endpoints NAME          ENDPOINTS                                         AGE kubernetes    10.0.12.10:6443,10.0.12.11:6443,10.0.12.16:6443   2d13h my-service1   198.18.0.74:80,198.18.1.208:80,198.18.2.250:80    2d13h my-service2   198.18.0.173:80,198.18.1.155:80,198.18.2.120:80   2d13h my-service3   198.18.0.6:80,198.18.1.139:80,198.18.2.70:80      2d13h [root@linuxer-bastion ~]# kubectl get endpoints |grep my-service1 \nmy-service1   198.18.0.74:80,198.18.1.208:80,198.18.2.250:80    2d13h [root@linuxer-bastion ~]# kubectl get endpoints |grep my-service1 |awk '{print $2}' 198.18.0.74:80,198.18.1.208:80,198.18.2.250:80 [root@linuxer-bastion ~]# kubectl get endpoints |grep my-service1 |awk '{print $2}'|tr "," "\ " \n198.18.0.74:80 198.18.1.208:80 198.18.2.250:80 [root@linuxer-bastion ~]# kubectl get endpoints |grep my-service1 |awk '{print $2}'|tr "," "\ " |awk -F":" '{print $1}' \n198.18.0.74 198.18.1.208 198.18.2.250 [root@linuxer-bastion ~]# kubectl get endpoints |grep my-service1 |awk '{print $2}'|tr "," "\ " |awk -F":" '{print $1}' |grep -f - <(kubectl get po -o wide) my-nginx1-67f499d79c-g7vr7   1/1     Running    0          26h   198.18.0.74    nks-pool-1119-w-gzg   <none>           <none> my-nginx1-67f499d79c-j4f9k   1/1     Running    0          26h   198.18.2.250   nks-pool-1119-w-gzh   <none>           <none> my-nginx1-67f499d79c-mqxzs   1/1     Running    1          26h   198.18.1.208   nks-pool-1119-w-gzi   <none>           <none> [root@linuxer-bastion ~]# kubectl get po -o wide NAME                         READY   STATUS     RESTARTS   AGE   IP             NODE                  NOMINATED NODE   READINESS GATES busybox                      0/1     Init:0/2   0          26h   198.18.2.60    nks-pool-1119-w-gzh   <none>           <none> my-nginx1-67f499d79c-g7vr7   1/1     Running    0          26h   198.18.0.74    nks-pool-1119-w-gzg   <none>           <none> my-nginx1-67f499d79c-j4f9k   1/1     Running    0          26h   198.18.2.250   nks-pool-1119-w-gzh   <none>           <none> my-nginx1-67f499d79c-mqxzs   1/1     Running    1          26h   198.18.1.208   nks-pool-1119-w-gzi   <none>           <none> my-nginx2-659945d9d8-2sggt   1/1     Running    1          26h   198.18.1.155   nks-pool-1119-w-gzi   <none>           <none> my-nginx2-659945d9d8-cjkft   1/1     Running    0          26h   198.18.2.120   nks-pool-1119-w-gzh   <none>           <none> my-nginx2-659945d9d8-szw59   1/1     Running    0          26h   198.18.0.173   nks-pool-1119-w-gzg   <none>           <none> my-nginx3-694994cd8c-l4m6k   1/1     Running    1          26h   198.18.1.139   nks-pool-1119-w-gzi   <none>           <none> my-nginx3-694994cd8c-lbqsd   1/1     Running    0          26h   198.18.2.70    nks-pool-1119-w-gzh   <none>           <none> my-nginx3-694994cd8c-xjzkc   1/1     Running    0          26h   198.18.0.6     nks-pool-1119-w-gzg   <none>           <none> nginx                        1/1     Running    0          26h   198.18.0.80    nks-pool-1119-w-gzg   <none>           <none>
```


이해를 돕기위해 결과를 한줄씩 쳐서 출력했다.


iamai 님의 shell에 대한 이해도를 볼수있었다.


나는 grep를 쓰지않고 출력하고 싶었다. 여러 엔지니어들을 보면 jsonpath로 예쁘게 깍는것이 부러웠다. 방법은 다양했다 json | jq 부터 jsonpath custom-columns 까지 방법이 많은데 나도 한번 써볼까 싶었다.


```
k get pod -l $(k get svc my-service1 -o=jsonpath='{..selector}' | sed 's/map//' | sed 's/:/=/' | tr -s '[[:space:]]' ' ') --show-labels NAME                         READY   STATUS    RESTARTS   AGE   LABELS my-nginx1-67f499d79c-g7vr7   1/1     Running   0          26h   app=my-nginx1,pod-template-hash=67f499d79c my-nginx1-67f499d79c-j4f9k   1/1     Running   0          26h   app=my-nginx1,pod-template-hash=67f499d79c my-nginx1-67f499d79c-mqxzs   1/1     Running   1          26h   app=my-nginx1,pod-template-hash=67f499d79c
```


시작부터 iamai 님과의 다른접근을 볼수있다. 나는 label로 접근했고, iamai 님은 IP로 접근했다.


selector 는 label을 기반으로 pod와 매핑되기때문에 IP가 우선이 되서는 안된다 생각했다. IP는 고정된 값이 아니므로. 그래서 label 을 사용하기로 생각했다.


```
[root@linuxer-bastion ~]# k get svc my-service1 -o=jsonpath='{..selector}' \nmap[app:my-nginx1] [root@linuxer-bastion ~]# k get svc my-service1 -o=jsonpath='{..selector}' | sed 's/map//' \n[app:my-nginx1] [root@linuxer-bastion ~]# k get svc my-service1 -o=jsonpath='{..selector}' | sed 's/map//' | sed 's/:/=/' \n[app=my-nginx1] [root@linuxer-bastion ~]# k get svc my-service1 -o=jsonpath='{..selector}' | sed 's/map//' | sed 's/:/=/' | tr -s '[[:space:]]' ' '\n app=my-nginx1
```


먼저 jsonpath를 이용하여 service의 selector를 찾는다 여기서 sed 명령어로 map[app:my-nginx1] 이라는 문자열을 두번 파이프라인하여 [app=my-nginx1]로 변환된다. json으로 출력한 문자열은 = -> : 으로 치환되어 표기된다. 그래서 변경해줘야 했다. 괄호를 벗겼다. 괄호를 벗은 값은 내가 처음부터 원했던 service - selector - label 이다. 이제 이값을 이용해서 pod 를 리스팅 하고 label를 보면 완성이다.


```
k get pod -l $(k get svc my-service1 -o=jsonpath='{..selector}' /| sed 's/map//' | sed 's/:/=/' | tr -s '[[:space:]]' ' ') --show-labels NAME                         READY   STATUS    RESTARTS   AGE   LABELS my-nginx1-67f499d79c-g7vr7   1/1     Running   0          26h   app=my-nginx1,pod-template-hash=67f499d79c my-nginx1-67f499d79c-j4f9k   1/1     Running   0          26h   app=my-nginx1,pod-template-hash=67f499d79c my-nginx1-67f499d79c-mqxzs   1/1     Running   1          26h   app=my-nginx1,pod-template-hash=67f499d79c
```


내가 작성한 스크립트는 폰트크기 15다


```
k get ep -o custom-columns=IP:.subsets[].addresses[].ip IP 10.0.12.10 198.18.0.74 198.18.0.173 198.18.0.6\n
```


성주님께서 주신 IP 추출 팁


오랜만에 머리를 굴렸더니 재미있었다.


오늘도 같이 머리를 싸매서 고민을 해주신 봄님, iamai 님, 성주님께 감사를 드린다.


더좋은 아이디어나 생각이 있다면 얼른 결과를 공유해주시길 바란다!


즐거운 새벽되시라!


하고 누우려는데 성주님께서 주신 IP list 로 하나더 만들고 싶었다.


```
k get ep my-service1 -o custom-columns=IP:.subsets[].addresses[*].ip | tr "," "\ " | grep -v IP | grep -f - <(kubectl get po -o wide --show-labels) \nmy-nginx1-67f499d79c-g7vr7   1/1     Running    0          27h   198.18.0.74    nks-pool-1119-w-gzg   <none>           <none>            app=my-nginx1,pod-template-hash=67f499d79c my-nginx1-67f499d79c-j4f9k   1/1     Running    0          27h   198.18.2.250   nks-pool-1119-w-gzh   <none>           <none>            app=my-nginx1,pod-template-hash=67f499d79c my-nginx1-67f499d79c-mqxzs   1/1     Running    1          27h   198.18.1.208   nks-pool-1119-w-gzi   <none>           <none>            app=my-nginx1,pod-template-hash=67f499d79c
```


성주님+iamai님의 조언을 합쳤다 중간에 grep -v IP 는 내 생각이다.


시원하게 끝내고 잔다!


정말로 좋은새벽되시라.
