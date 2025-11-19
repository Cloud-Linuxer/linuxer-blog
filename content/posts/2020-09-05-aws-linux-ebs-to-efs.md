---
title: "AWS-Linux-EBS-to-EFS"
date: 2020-09-05T22:39:15+09:00
draft: false
categories: ["AWS", "Linux", "ec2"]
tags: ["승광", "rclone", "rsync", "tar", "sync"]
slug: "aws-linux-ebs-to-efs"
aliases:
  - /aws-linux-ebs-to-efs/
  - /aws-linux-ebs-to-efs/
---

\n

아키텍쳐를 수정중에 EBS에서 EFS로 파일을 넘길일이 생겼다.

\n\n\n\n

300G 가량의 대량의 파일이 있는 디렉토리를 sync 해야했다.

\n\n\n\n

EBS는 GP2로 400G, 1200IOPS를 가진 볼륨이었다. 스냅샷에서 볼륨을 생성해서 4T로 확장하여 12000IOPS를 가진 볼륨에서 테스트를 진행하였다.

\n\n\n\n

새벽에 먼저 싱크를 진행한 내용이 있는데 network out 이 40mb를 넘지 않았다.

\n\n\n\n

싱크는

\n\n\n\n

rsync -av /src /dst

\n\n\n\n

로 진행한것 같았다. rsync 의 속도를 끌어 올리기 위해 테스트했으나 실패. 속도는 40mb 에서 더 이상 올라가지 않았다.

\n\n\n\n

그래서 강구한 방법이 tar 를 이용한 데이터 이동이었다.

\n\n\n\n

tar -C <src> -cf - . | tar -C <dst> -xf -

\n\n\n\n

속도는 170mb 정도 그러나, 치명적인 단점이 존재했다. 소유권과 퍼미션을 가져오지 않는것이었다.

\n\n\n\n

-\_-; 파일이동이라 함은..소유권과 퍼미션을 그대로 가져가야하는데...그게 안됬다. 그래서 임시 방편으로

\n\n\n\n

tar -cvf /dst/file.tar /src

\n\n\n\n

명령어로 EBS의 데이터를 tar 로 압축해서 EFS로 저장하는 명령어로 작업했다.

\n\n\n\n

이때 속도는 170MB 정도.. tar로 압축하지 않고 pipeline 으로 보냈을때와 동일한 방식이지만 소유권과 퍼미션을 유지할수 있는 방법이다.

\n\n\n\n

그렇지만 속도가 마음에 들지 않았다.

\n\n\n\n

물망에 rclone / rdiff-backup 가 있었다.

\n\n\n\n

rclone 은 씅광님이 추천해줘서 오후내내 테스트를 했다. 그런데 속도가 너무 잘나오는데 문제는 퍼미션과 소유권을 가져올수 없는것이다.

\n\n\n\n

그래서 승광님께서 주신 힌트로 테스트를 진행했다.

\n\n\n\n

clone sync /src /dst --checkers 128 --transfers 128

\n\n\n\n

속도는 놀라웠다. T3a.medium type의 **네트워크 성능(Gbps)** 이라 표기된 5G를 모두쓰는것이었다.

\n\n\n\n
![](/images/2020/09/image-1.png)
\n\n\n\n

이렇게 network 를 모두 사용하는것은 처음이라 신기할정도로 rclone는 빨랐다.

\n\n\n\n

300G 모두 sync하는데 1시간 30분밖에 걸리지 않았으니까..

\n\n\n\n

그런데 여기서 rclone은 문제가 발생한다.

\n\n\n\n

<https://rclone.org/local/#filenames>

\n\n\n\n

### Filenames

\n\n\n\n

Filenames should be encoded in UTF-8 on disk. This is the normal case for Windows and OS X.

\n\n\n\n

There is a bit more uncertainty in the Linux world, but new distributions will have UTF-8 encoded files names. If you are using an old Linux filesystem with non UTF-8 file names (eg latin1) then you can use the `convmv` tool to convert the filesystem to UTF-8. This tool is available in most distributions' package managers.

\n\n\n\n

If an invalid (non-UTF8) filename is read, the invalid characters will be replaced with a quoted representation of the invalid bytes. The name `gro\\xdf` will be transferred as `gro‛DF`. `rclone` will emit a debug message in this case (use `-v` to see), eg

\n\n\n\n

인코딩 문제인데 이건...하...나중에 rsync 로 남은파일을 채워볼까 생각했지만 불확실성이 너무 컷다. 파일의 누락이 너무많았다

\n\n\n\n

그래도 테스트는 그냥 진행했고 싱크속도 무지빠르고 쓸만했다.

\n\n\n\n

그래서 이후에 소유권과 퍼미션을 넣어주는 작업을 궁리했다.

\n\n\n\n

getfacl -R /src > file.list  
sed 's/src/dst/g' file.list  
cd /dst  
setfacl --restore=file.list

\n\n\n\n

4줄의 명령어로 소유권과 퍼미션을 그대로 가져오는 방법을 찾았다.

\n\n\n\n

이제 인코딩 문제만 해결하면된다 생각했지만, 안정성의 문제때문에

\n\n\n\n

tar로 압축해서 넘기를 방식으로 계속진행하기로 생각했다.

\n\n\n\n\n\n\n\n

오늘 적당한 낚시와 어드바이스를 주신 승광님께 감사드린다!

\n