---
title: "CLOUDNET@ AWS네트워킹 강의 나눔이벤트"
date: 2023-04-16T14:14:46+09:00
draft: false
categories: ["기타"]
slug: "cloudnet-aws네트워킹-강의-나눔이벤트"
aliases:
  - /cloudnet-aws네트워킹-강의-나눔이벤트/
  - /cloudnet-aws%eb%84%a4%ed%8a%b8%ec%9b%8c%ed%82%b9-%ea%b0%95%ec%9d%98-%eb%82%98%eb%88%94%ec%9d%b4%eb%b2%a4%ed%8a%b8/
---


이번에 CLOUDNET@ 에서 인프런에 강의를 오픈했다.

<https://inf.run/Xpv1>

1호 영업사원으로 뛰기로 말한 전적이 있기에 추첨으로 강의 나눔 이벤트를 했

총 60분이 참여해주셨고, 간단하게 코드를 짰다.

```
import random
def select_random_winner(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        names = file.readlines()
    winner = random.choice(names).strip()
    return winner
filename = "name_list.txt" winner = select_random_winner(filename) print(f"축하합니다! 상품 당첨자는 {winner}님입니다!")
```

랜덤으로 코드만들어서 돌렸다.

```
python3 select_random_winner.py 축하합니다! 상품 당첨자는 김신님입니다!
```

![](/images/2023/04/image-2.png)

김신님께서 당첨되셨다.

축하합니다!
