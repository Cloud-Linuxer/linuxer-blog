---
title: "aws-rds-readreplica-general_log"
date: 2020-03-27T20:06:04+09:00
draft: false
categories: ["AWS"]
tags: ["rds", "read", "replica"]
slug: "aws-rds-readreplica-general_log"
aliases:
  - /aws-rds-readreplica-general_log/
  - /aws-rds-readreplica-general_log/
---


<https://www.facebook.com/groups/awskrug/permalink/2404835746285102/>

![](/images/2020/03/image-29.png)

다음과 같은 질문이 올라왔다.
바로 생각난건 general_log.. 그래서 Master와 Readreplica 가 각각 다른 Parameter Group(이하 PG)를 가질수 있는지 확인해보기로 했다.

먼저 Readreplica 생성했다.

실제로 읽기복제본을 만들때는 파라메터 그룹을 수정할수 없다.

Master 의 PG를 그대로 사용한다.

![](/images/2020/03/image-30-1024x115.png)

이렇게 모두 생성된 Readreplica 를 수정을 눌러보면

![](/images/2020/03/image-31-1024x510.png)

데이터베이스 옵션에서 파라메터 그룹을 볼수있다.
그래서 나는 따로 PG를 만들어주고..general_log 도 켜줬다.

![](/images/2020/03/image-32-1024x360.png)

dynamic / static 으로 나뉘는데 적용유형이 dynamic이면 PG가 적용된상태에서 라이브로 적용된다. 디비의 재시작이 필요없다.

물론..PG를 변경하게 되면 RDS의 재시작이 필요하다.

그럼 1차 결론으로 마스터와 슬레이브는 생성시엔 같은 PG를 사용한다. PG는 마스터와 슬레이브는 다르게 사용하려면 수정해야한다.

현재구성은 마스터는 general_log를 사용하지 않고, 슬레이브만 사용한다. 그럼 슬레이브에서 제네럴 로그를 쌓는지 확인해 보자.

이상하게 적용이 안되서 보니..

![](/images/2020/03/image-33.png)

보류중이면 말하지;

![](/images/2020/03/image-34.png)

재시작 시켜서 적용해주고~

![](/images/2020/03/image-35-1024x597.png)

잘쌓인다..타임존이 이상하네? 그건 넘어가고..

마스터는 안쌓이는거 확인했고~

질문의 답은 확인할수 없지만..general_log 가 마스터와 슬레이브가 별개로 쌓이는 설정이 가능하고 슬레이브의 용량이 서비스에 영향을 미칠수있다.

정도로 결론 내리겠다.

급한 테스트였지만 결론을 내린다!
