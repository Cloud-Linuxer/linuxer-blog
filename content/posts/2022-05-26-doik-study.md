---
title: "DOIK-Study"
date: 2022-05-26T18:17:09+09:00
draft: false
categories: ["AWS", "Linux", "Kubernetes"]
slug: "doik-study"
aliases:
  - /doik-study/
  - /doik-study/
---


가시다님과 함께하는 스터디는 항상 즐겁다. 이번 스터디엔 라이브로 못해서..일단 바닐라쿠버 배포하고 시작했다.


Headless 서비스는 ClusterIP가 None으로 설정하며 kubeproxy를 통하지않고 pod의 endpoint가 svc에 연결된다.


나는 먼저 NFS 서버를 Headless 로 배포하기로 했다.


```
kind: PersistentVolumeClaim apiVersion: v1 metadata:\n  name: nfs-server-pvc spec:\n  accessModes:\n    - ReadWriteOnce\n  resources:\n    requests:\n      storage: 10Gi\n      \n--- \nkind: Service apiVersion: v1 metadata:\n  name: nfs-service spec:\n  type: ClusterIP\n  clusterIP: None\n  selector:\n    role: nfs\n  ports:\n    # Open the ports required by the NFS server\n    # Port 2049 for TCP\n    - name: tcp-2049\n      port: 2049\n      protocol: TCP \n    # Port 111 for UDP\n    - name: udp-111\n      port: 111\n      protocol: UDP\n      \n    # Port 20048 for TCP\n    - name: tcp-20048\n      port: 20048\n      protocol: TCP --- \napiVersion: v1 kind: ReplicationController metadata:\n  name: nfs-server spec:\n  replicas: 1\n  selector:\n    role: nfs-server\n  template:\n    metadata:\n      labels:\n        role: nfs-server\n    spec:\n      containers:\n      - name: nfs-server\n        image: gcr.io/google_containers/volume-nfs:0.8\n        ports:\n          - name: nfs\n            containerPort: 2049\n          - name: mountd\n            containerPort: 20048\n          - name: rpcbind\n            containerPort: 111\n        securityContext:\n          privileged: true\n        volumeMounts:\n          - mountPath: /exports\n            name: nfs-export\n      volumes:\n        - name: nfs-export-fast\n          persistentVolumeClaim:\n            claimName: nfs-server-pvc-fast\n
```


?


yaml을 deploy 하면 다음과같다.


이제 프로비저너 셋팅이 좀 필요하다. 가시다님께서는 친절하게 프로비저너 셋팅도 다해주셨지만 나는 내가만든 NFS 서버를 사용할거기 때문에 프로비저너를 다시 배포할거다.


```
#지우고 helm delete -n kube-system nfs-provisioner #다시 설치하고 helm install nfs-provisioner -n kube-system nfs-subdir-external-provisioner/nfs-subdir-external-provisioner --set nfs.server=nfs-service.default.svc.cluster.local --set nfs.path=/exports NAME: nfs-provisioner LAST DEPLOYED: Thu May 26 16:10:31 2022 NAMESPACE: kube-system STATUS: deployed REVISION: 1 TEST SUITE: None
```


?


응 잘됬다.


```
(? |DOIK-Lab:default) root@k8s-m:~# k get svc NAME          TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)            AGE kubernetes    ClusterIP   10.200.1.1   <none>        443/TCP            4h30m nfs-service   ClusterIP   None         <none>        2049/TCP,111/UDP   6m29s \n(? |DOIK-Lab:default) root@k8s-m:~# k get ep NAME          ENDPOINTS                            AGE kubernetes    192.168.10.10:6443                   4h30m nfs-service   172.16.158.2:2049,172.16.158.2:111   6m48s \n(? |DOIK-Lab:default) root@k8s-m:~# k get pod -o wide NAME             READY   STATUS    RESTARTS   AGE    IP             NODE     NOMINATED NODE   READINESS GATES nfs-server-pod   1/1     Running   0          7m1s   172.16.158.2   k8s-w1   <none>           <none>
```


?


정상적으로 NFS서버가 잘 배포된것을 확인할수 있다.


```
apiVersion: v1 kind: PersistentVolume metadata:\n  name: mysql-nfs-pv\n  labels:\n    type: mysql-nfs-pv spec:\n  storageClassName: nfs-client\n  capacity:\n    storage: 4Gi\n  accessModes:\n  - ReadWriteOnce          # ReadWriteOnce RWO (1:1 마운트, 읽기 쓰기)\n  nfs:\n    server: 172.16.184.9 # NFS-Server 의 IP\n    path: /1       # NFS 저장소 --- apiVersion: v1 kind: PersistentVolume metadata:\n  name: wp-nfs-pv\n  labels:\n    type: wp-nfs-pv spec:\n  storageClassName: nfs-client\n  capacity:\n    storage: 4Gi\n  accessModes:\n  - ReadWriteOnce\n  nfs:\n    server: 172.16.184.9 # NFS-Server 의 IP\n    path: /2      # NFS 저장소
```


?


nfs-service.svc.cluster.local domain을 이용하려 하였으나, PV 에서 domain으로 설정시 nfs-provisioner 정상적으로 마운트 되지 않았다.


**headless NFS를 하려고 한것이나, 실패하였다.
지원하지 않는다.(결론)**


![](/images/2022/05/image-32-1024x64.png)

다음과 같은 증상이었다. IP로 프로비저너 설치후엔 잘되었다.


```
--- apiVersion: v1 kind: PersistentVolumeClaim metadata:\n  labels:\n    app: wordpress\n  name: mysql-pv-claim spec:\n  storageClassName: nfs-client\n  accessModes:\n  - ReadWriteOnce\n  resources:\n    requests:\n      storage: 4Gi\n  selector:\n    matchLabels:\n      type: "mysql-nfs-pv" --- apiVersion: v1 kind: PersistentVolumeClaim metadata:\n  labels:\n    app: wordpress\n  name: wp-pv-claim spec:\n  storageClassName: nfs-client\n  accessModes:\n  - ReadWriteOnce\n  resources:\n    requests:\n      storage: 4Gi\n  selector:\n    matchLabels:\n      type: "wp-nfs-pv"
```


?


selector를 이용하여 PV를 사용하도록 설정해 주었다


```
Every 2.0s: kubectl get svc,pods,pv,pvc -o wide                                                                                                                                                                    k8s-m: Thu May 26 18:10:41 2022 \nNAME                      TYPE        CLUSTER-IP    EXTERNAL-IP   PORT(S)                      AGE     SELECTOR service/kubernetes        ClusterIP   10.200.1.1    <none>        443/TCP                      7h56m   <none> service/nfs-service       ClusterIP   None          <none>        2049/TCP,111/UDP,20048/TCP   71m     role=nfs service/wordpress         NodePort    10.200.1.33   <none>        80:30387/TCP                 3m25s   app=wordpress,tier=frontend service/wordpress-mysql   ClusterIP   None          <none>        3306/TCP                     3m25s   app=wordpress,tier=mysql \nNAME                                   READY   STATUS    RESTARTS   AGE     IP              NODE     NOMINATED NODE   READINESS GATES pod/nfs-server-rxvf7                   1/1     Running   0          71m     172.16.184.9    k8s-w2   <none>           <none> pod/wordpress-859f989bbb-msppd         1/1     Running   0          3m25s   172.16.158.21   k8s-w1   <none>           <none> pod/wordpress-mysql-66fb7cfb68-z9vj5   1/1     Running   0          3m25s   172.16.158.20   k8s-w1   <none>           <none> \nNAME                                                        CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM                         STORAGECLASS   REASON   AGE     VOLUMEMODE persistentvolume/mysql-nfs-pv                               4Gi        RWO            Retain           Bound    default/mysql-pv-claim        nfs-client              3m32s   Filesystem persistentvolume/pvc-adc24c97-ca67-4700-b3c5-2fc51c4cce01   10Gi       RWO            Delete           Bound    default/nfs-server-pvc-fast   local-path              71m     Filesystem persistentvolume/wp-nfs-pv                                  4Gi        RWO            Retain           Bound    default/wp-pv-claim           nfs-client              3m32s   Filesystem \nNAME                                        STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   AGE     VOLUMEMODE persistentvolumeclaim/mysql-pv-claim        Bound    mysql-nfs-pv                               4Gi        RWO            nfs-client     3m25s   Filesystem persistentvolumeclaim/nfs-server-pvc-fast   Bound    pvc-adc24c97-ca67-4700-b3c5-2fc51c4cce01   10Gi       RWO            local-path     71m     Filesystem persistentvolumeclaim/wp-pv-claim           Bound    wp-nfs-pv                                  4Gi        RWO            nfs-client     3m25s   Filesystem\n
```


?


서비스가 잘 작동하는것을 확인하였다.


```
(? |DOIK-Lab:default) root@k8s-m:~/yaml/yaml# k exec nfs-server-rxvf7 -it -- /bin/bash [root@nfs-server-rxvf7 /]# cd /exports/ [root@nfs-server-rxvf7 exports]# ll total 32 drwxr-xr-x 5 systemd-bus-proxy root 4096 May 26 09:07 1 drwxr-xr-x 5                33   33 4096 May 26 09:07 2 -rw-r--r-- 1 root              root   16 May 26 07:59 index.html [root@nfs-server-rxvf7 exports]# cd 1 [root@nfs-server-rxvf7 1]# ll total 110608 -rw-rw---- 1 systemd-bus-proxy input       56 May 26 09:07 auto.cnf -rw-rw---- 1 systemd-bus-proxy input 50331648 May 26 09:07 ib_logfile0 -rw-rw---- 1 systemd-bus-proxy input 50331648 May 26 09:07 ib_logfile1 -rw-rw---- 1 systemd-bus-proxy input 12582912 May 26 09:07 ibdata1 drwx------ 2 systemd-bus-proxy input     4096 May 26 09:07 mysql drwx------ 2 systemd-bus-proxy input     4096 May 26 09:07 performance_schema drwx------ 2 systemd-bus-proxy input     4096 May 26 09:07 wordpress [root@nfs-server-rxvf7 1]# cd .. [root@nfs-server-rxvf7 exports]# cd 2 [root@nfs-server-rxvf7 2]# ll total 192 -rw-r--r--  1 33 33   418 Sep 25  2013 index.php -rw-r--r--  1 33 33 19935 Jan  2  2017 license.txt -rw-r--r--  1 33 33  7413 Dec 12  2016 readme.html -rw-r--r--  1 33 33  5447 Sep 27  2016 wp-activate.php drwxr-xr-x  9 33 33  4096 Oct 31  2017 wp-admin -rw-r--r--  1 33 33   364 Dec 19  2015 wp-blog-header.php -rw-r--r--  1 33 33  1627 Aug 29  2016 wp-comments-post.php -rw-r--r--  1 33 33  2764 May 26 09:07 wp-config-sample.php -rw-r--r--  1 33 33  3154 May 26 09:07 wp-config.php drwxr-xr-x  4 33 33  4096 Oct 31  2017 wp-content -rw-r--r--  1 33 33  3286 May 24  2015 wp-cron.php drwxr-xr-x 18 33 33 12288 Oct 31  2017 wp-includes -rw-r--r--  1 33 33  2422 Nov 21  2016 wp-links-opml.php -rw-r--r--  1 33 33  3301 Oct 25  2016 wp-load.php -rw-r--r--  1 33 33 34327 May 12  2017 wp-login.php -rw-r--r--  1 33 33  8048 Jan 11  2017 wp-mail.php -rw-r--r--  1 33 33 16200 Apr  6  2017 wp-settings.php -rw-r--r--  1 33 33 29924 Jan 24  2017 wp-signup.php -rw-r--r--  1 33 33  4513 Oct 14  2016 wp-trackback.php -rw-r--r--  1 33 33  3065 Aug 31  2016 xmlrpc.php
```


?


목적이었던 NFS도 정상적으로 작동한다.


```
(? |DOIK-Lab:default) root@k8s-m:~/yaml# k scale deployment wordpress --replicas=3 \n(? |DOIK-Lab:default) root@k8s-m:~/yaml# k get pod NAME                               READY   STATUS    RESTARTS   AGE nfs-server-rxvf7                   1/1     Running   0          77m wordpress-859f989bbb-8r5zh         1/1     Running   0          47s wordpress-859f989bbb-msppd         1/1     Running   0          8m38s wordpress-859f989bbb-xhbs9         1/1     Running   0          47s wordpress-mysql-66fb7cfb68-z9vj5   1/1     Running   0          8m38s \n(? |DOIK-Lab:default) root@k8s-m:~/yaml# k get pv NAME                                       CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM                         STORAGECLASS   REASON   AGE mysql-nfs-pv                               4Gi        RWO            Retain           Bound    default/mysql-pv-claim        nfs-client              9m6s pvc-adc24c97-ca67-4700-b3c5-2fc51c4cce01   10Gi       RWO            Delete           Bound    default/nfs-server-pvc-fast   local-path              77m wp-nfs-pv                                  4Gi        RWO            Retain           Bound    default/wp-pv-claim           nfs-client              9m6s (? |DOIK-Lab:default) root@k8s-m:~/yaml# k get pvc NAME                  STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   AGE mysql-pv-claim        Bound    mysql-nfs-pv                               4Gi        RWO            nfs-client     9m2s nfs-server-pvc-fast   Bound    pvc-adc24c97-ca67-4700-b3c5-2fc51c4cce01   10Gi       RWO            local-path     77m wp-pv-claim           Bound    wp-nfs-pv                                  4Gi        RWO            nfs-client     9m2s
```


?


볼륨도 잘공유하여 프로비저닝 된것을 확인할수 있다. ㅜㅜ
