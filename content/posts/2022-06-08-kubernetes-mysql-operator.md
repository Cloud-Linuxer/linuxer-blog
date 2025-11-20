---
title: "Kubernetes-Mysql-Operator"
date: 2022-06-08T23:55:51+09:00
draft: false
categories: ["Kubernetes"]
slug: "kubernetes-mysql-operator"
aliases:
  - /kubernetes-mysql-operator/
  - /kubernetes-mysql-operator/
---


Mysql Operator 스터디를 진행중에 느꼈다.
Mysql Operator는 현재 나의 판단보다 Operator의 로직이 훨신 빠르고 정확하게 동작할거라는 생각이 들었다.

다른말로는 믿고 써도 될수준에 가깝다 느껴졌다. ~~물론 RDS 못잃어~~

![](/images/2022/06/image.png)

https://dev.mysql.com/doc/mysql-operator/en/mysql-operator-introduction.html

그래서 나는 실습은 그냥..helm으로 다들 하는것 같아서 Operator가 생성하는 Mysql Cluster 의 아키텍처를 파해쳐 볼까한다.

DNS - SRV Record

![](/images/2022/06/image-1.png)

https://www.haproxy.com/documentation/hapee/latest/management/service-discovery/dns-service-discovery/discovery-with-srv-records/

SRV 레코드는 자주 사용 되는 레코드는 아니지만, GSLB혹은 가중치를 이용한 라우팅, 페일오버 등에 사용된다.

https://blog.o3g.org/network/dns-record/

수진님의 포스팅 링크

<https://dev.mysql.com/doc/refman/8.0/en/connecting-using-dns-srv.html>

정리하자면 Mysql Routor 에서 클러스터의 노드별로 srv레코드를 부여하고,

<https://dev.mysql.com/doc/connector-j/8.0/en/connector-j-reference-dns-srv.html>

mysql 8.0.19버전에서 Connector 에서 또한 srv 레코드를 이용할수 있게되어서 Mysql 클러스터는 획기적으로 발전한것이다. 이전에는 mysql 의 HA를 구성하려면 FaceMaker 부터 시작해서 손이 갈부분이 만만치 않게 많았다.

오라클로 인수된 Mysql의 약진이 정말 기대이상이다.

X Protocol

<https://dev.mysql.com/doc/internals/en/x-protocol.html>

X Protocol 은 5.7.12 버전부터 플러그인으로 사용할수 있었다.

![](/images/2022/06/image-2.png)

https://dev.mysql.com/doc/internals/en/x-protocol.html

X protocol 은 Life Cycle, Notifocation 등의 기능을 담당하는데, 이 프로토콜로 서버의 정상유무를 라우터나 오퍼레이터와 통신하여 처리한다.

<https://dev.mysql.com/doc/internals/en/x-protocol-lifecycle-lifecycle.html>

Backup

Backup는 다이렉트로 S3백업이 가능하다는 점이 인상적인데, 정말 바라던 기능이라 충격적일 정도이다.

<https://github.com/bitpoke/mysql-operator/blob/master/docs/backups.md>

다른 Operator 와 비교해보고 싶다면 아래 블로그를 참고하길 바란다.

<https://portworx.com/blog/choosing-a-kubernetes-operator-for-mysql/>

마치며

SRV레코드를 이용하여 Endpoint를 특정하고, X protocol을 이용하여 헬스체크를 하고, 문제가 생기면, 오퍼레이터가 파드를 다시 생성하는 등의 과정이 이루어 진다. 말로는 정말 간단하다. 하지만 이 아키텍처가 쿠버네티스의 탄력성과 신속성과 합쳐짐으로 강력한 시너지를 발생하는것으로 보인다.

사용자의 고민이 많이 없이 사용할수있는 레벨의 솔루션으로 진화한듯싶다.

그간 많은 엔지니어 들이 사랑하던 Mysql 의 진화가 반갑기만하면서..오라클의 품에 있는 My가 두렵다.

그래서 MariaDB Operator를 찾아보았다.

<https://mariadb.com/kb/en/kubernetes-operators-for-mariadb/>

그런데 MariaDB Operator는 이전에 Galera Operator라 불리던 작품인듯한다.

다음에 한번 테스트를 해봐야 겠다....근데 사용자가 정말 없는듯하다.

오퍼레이터 스터디로 인하여 컨테이너 디비에 대해서 새로운 관점이 생기는 것을 느낀다.
