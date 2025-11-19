---
title: "AWS Certified Solutions Architect – Professional Level Sample Exam Questions 풀이 02"
date: 2019-09-09T22:50:45+09:00
draft: false
categories: ["AWS", "Certification"]
tags: ["aws", "sap", "exam", "aws sap", "sap exam", "예제", "샘플", "시험"]
slug: "aws-certified-solutions-architect-professional-level-sample-exam-questions-풀이-02"
aliases:
  - /aws-certified-solutions-architect-professional-level-sample-exam-questions-풀이-02/
  - /aws-certified-solutions-architect-professional-level-sample-exam-questions-%ed%92%80%ec%9d%b4-02/
---

\n

문제는 아래 URL 에서 발췌하였다.

\n\n\n\n

<https://d1.awsstatic.com/Train%20%26%20Cert/docs/AWS_certified_solutions_architect_professional_examsample.pdf>

\n\n\n\n

영문  
\nYou are building a website that will retrieve and display highly sensitive information to users.   
\nThe amount of traffic the site will receive is known and not expected to fluctuate.   
\nThe site will leverage SSL to protect the communication between the clients and the web servers.   
\nDue to the nature of the site you are very concerned about the security of your SSL private key and want to ensure that the key cannot be accidentally or intentionally moved outside your environment.   
\nAdditionally, while the data the site will display is stored on an encrypted EBS volume, you are also concerned that the web servers’ logs might contain some sensitive information; therefore, the logs must be stored so that they can only be decrypted by employees of your company.   
\nWhich of these architectures meets all of the requirements?

\n\n\n\n

A) Use Elastic Load Balancing to distribute traffic to a set of web servers. To protect the SSL private key, upload the key to the load balancer and configure the load balancer to offload the SSL traffic. Write your web server logs to an ephemeral volume that has been encrypted using a randomly generated AES key.  
\nB) Use Elastic Load Balancing to distribute traffic to a set of web servers. Use TCP load balancing on the load balancer and configure your web servers to retrieve the private key from a private Amazon S3 bucket on boot. Write your web server logs to a private Amazon S3 bucket using Amazon S3 server-side encryption.  
\nC) Use Elastic Load Balancing to distribute traffic to a set of web servers, configure the load balancer to perform TCP load balancing, use an AWS CloudHSM to perform the SSL transactions, and write your web server logs to a private Amazon S3 bucket using Amazon S3 server-side encryption.  
\nD) Use Elastic Load Balancing to distribute traffic to a set of web servers. Configure the load balancer to perform TCP load balancing, use an AWS CloudHSM to perform the SSL transactions, and write your web server logs to an ephemeral volume that has been encrypted using a randomly generated AES key.

\n\n\n\n

이문제는 정말 의견이 분분한 문제이다.

\n\n\n\n

댓글 전쟁에 참전 하고 싶다면 아래 URL을 추천한다.

\n\n\n\n

<https://acloud.guru/forums/aws-certified-solutions-architect-professional/discussion/-KVj_o43efIRONfHwq_q/sample_question_4>

\n\n\n\n

댓글에 일본판 문제는 답안을 포함하고 있다는 정보를 얻어 일본판을 찾아보았다.

\n\n\n\n

일본어 문제이다.

\n\n\n\n

ユーザーにとって機密性の高い情報を取得して表示するウェブサイトを構築しています。サイトが受信するトラフィックの量 はわかっていて、上下しないと予想されます。このサイトでは、SSL を活用してクライアントとウェブサーバー間の通信を 保護します。サイトの性質のゆえに、SSL プライベートキーのセキュリティについて非常に懸念しており、キーが誤って、または意図的に環境外に移動されることがないようにしたいと思っています。また、サイトで表示されるデータは暗号化され た EBS ボリュームに保存されますが、ウェブサーバーのログに機密情報が含まれることも懸念しているため、自社の従業 員以外には復号化できないようにログを保存する必要があります。すべての要件を満たすのは次のうちどのアーキテクチャです か?  
\nA) Elastic Load Balancing を使用して、トラフィックを一連のウェブサーバーに分散する。SSL プライベートキーを保護 するため、キーをロードバランサーにアップロードして、SSL トラフィックの負荷を軽減するようにロードバランサーを 設定する。ウェブサーバーのログを、ランダムに生成された AES キーを使用して暗号化されているエフェメラルボリュ ームに書き込む。  
\nB) Elastic Load Balancing を使用して、トラフィックを一連のウェブサーバーに分散する。ロードバランサーで TCP ロードバランシング を使用して、起動時にプライベート Amazon S3 バケットからプライベートキーを取得するよ うにウェブサーバーを設定する。Amazon S3 サーバー側の暗号化を使用して、ウェブサーバーのログをプライベー ト Amazon S3 バケットに書き込む。  
\nC) Elastic Load Balancing を使用して、トラフィックを一連のウェブサーバーに分散する。TCP ロードバランシング を実行するようにロードバランサーを設定する。AWS CloudHSM を使用してウェブサー ー上で SSL トランザクションを処理し、Amazon S3 サーバー側の暗号化を使用して、ウェブサーバーのログをプライベート Amazon S3 バ ケットに書き込む。  
\nD) Elastic Load Balancing を使用して、トラフィックを一連のウェブサーバーに分散する。 TCP ロードバランシングを 実行するためにロードバランサーを設定しする。AWS CloudHSM を使用してウェブサーバー上で SSL トランザクションを処理し、ウェブサーバーのログを、ランダムに生成された AES キーを使用して暗号化されているエフェメラルボ リュームに書き込む。

\n\n\n\n

<http://media.amazonwebservices.com/jp/certification/AWS_certified_solutions_architect_professional_examsample0701_08_final.pdf>

\n\n\n\n

실제로 정답이 하단에 표기되어 있으며, 일본어 판의 답은 D 이다.

\n\n\n\n

구글 번역기  
\n매우 민감한 정보를 검색하여 사용자에게 표시하는 웹 사이트를 구축 중입니다.   
\n사이트에서 수신 할 트래픽의 양은 알려져 있으며 변동하지 않을 것으로 예상됩니다.   
\n이 사이트는 SSL을 활용하여 클라이언트와 웹 서버 간의 통신을 보호합니다.   
\n사이트의 특성상 SSL 개인 키의 보안에 대해 매우 우려하고 있으며 실수로 또는 의도적으로 키를 환경 외부로 이동할 수 없도록합니다.   
\n또한 사이트에 표시 할 데이터는 암호화 된 EBS 볼륨에 저장되지만 웹 서버 로그에는 중요한 정보가 포함될 수 있습니다.   
\n따라서 로그는 회사 직원 만 해독 할 수 있도록 저장해야합니다.   
\n이 중 어느 아키텍처가 모든 요구 사항을 충족합니까?

\n\n\n\n

A) Elastic Load Balancing을 사용하여 트래픽을 일련의 웹 서버에 분산시킵니다. SSL 개인 키를 보호하려면 키를로드 밸런서에 업로드하고 SSL 트래픽을 오프로드하도록로드 밸런서를 구성하십시오. 무작위로 생성 된 AES 키를 사용하여 암호화 된 임시 볼륨에 웹 서버 로그를 작성하십시오.  
\nB) Elastic Load Balancing을 사용하여 트래픽을 일련의 웹 서버에 배포합니다. 로드 밸런서에서 TCP로드 밸런싱을 사용하고 부팅시 프라이빗 Amazon S3 버킷에서 프라이빗 키를 검색하도록 웹 서버를 구성하십시오. Amazon S3 서버 측 암호화를 사용하여 웹 서버 로그를 프라이빗 Amazon S3 버킷에 씁니다.  
\nC) Elastic Load Balancing을 사용하여 트래픽을 웹 서버 세트에 분배하고,로드 밸런서가 TCP로드 밸런싱을 수행하도록 구성하고, AWS CloudHSM을 사용하여 SSL 트랜잭션을 수행하고, Amazon을 사용하여 웹 서버 로그를 프라이빗 Amazon S3 버킷에 쓰고 S3 서버 측 암호화를 사용합니다.  
\nD) Elastic Load Balancing을 사용하여 트래픽을 일련의 웹 서버에 분산시킵니다. TCP로드 밸런싱을 수행하고 AWS CloudHSM을 사용하여 SSL 트랜잭션을 수행하고 임의로 생성 된 AES 키를 사용하여 암호화 된 임시 볼륨에 웹 서버 로그를 쓰도록로드 밸런서를 구성하십시오.

\n\n\n\n

먼저 이문제의 요점을 정리하자면 로그를 암호화 해야되며 어떤 구성이 로그의 암호화를 충족하는지를 물어보는 문제이다.   
 일단 소거법으로 보자.   
 A는 키를 로드벨런서에 업로드 하였으므로 오답. 또한 ssl offloading은 서버와 클라이언트간 암호화는 아니다.  
 B는 가능한 방법이나 일반적인 방법은 아님.  
 C 는 cloudHSM 이뭔지 부터 알아야 한다. cloudHSM은 문제에서 요구하는 ssl 통신 구성이 가능하다.

\n\n\n\n

<https://docs.aws.amazon.com/ko_kr/cloudhsm/latest/userguide/ssl-offload.html>

\n\n\n\n
![](/images/2019/09/ssl-offload-handshake-process.png)
\n\n\n\n

이미지를 참고하기 바란다.  
 따라서 C는 현재 아키텍처의 요구사항에 충족한다.  
 D또한 요구사항에 충족하는데 cloudHSM을 사용하고 임시볼륨에 웹서버 로그를 저장한다.  
 인스턴스가 재부팅될 경우 데이터가 사라지게 되는데 문제에는 로그의 보관기일이 정해져있거나 로그를 남겨야하는 내용은 없다.  
 따라서 C/D가 갈리게 된다. 개인적으론 답을 C라고 생각하는데 다른 생각이 있으신 분은 답글을 달아주시기 바란다.

\n\n\n\n\n\n\n\n

일본판에선 D가 정답이므로 시험에 나오면 D를 선택하는게 좋을것 같다.

\n\n\n\n

영문  
\nYou are designing network connectivity for your fat client application. The application is designed for business travelers who must be able to connect to it from their hotel rooms, cafes, public Wi-Fi hotspots, and elsewhere on the Internet. You do not want to publish the application on the Internet. Which network design meets the above requirements while minimizing deployment and operational costs?  
\nA) Implement AWS Direct Connect, and create a private interface to your VPC. Create a public subnet and place your application servers in it.  
\nB) Implement Elastic Load Balancing with an SSL listener that terminates the back-end connection to the application.  
\nC) Configure an IPsec VPN connection, and provide the users with the configuration details. Create a public subnet in your VPC, and place your application servers in it.  
\nD) Configure an SSL VPN solution in a public subnet of your VPC, then install and configure SSL VPN client software on all user computers. Create a private subnet in your VPC and place your application servers in it.

\n\n\n\n

구글 번역기  
\n팻 클라이언트 애플리케이션을위한 네트워크 연결을 설계하고 있습니다. 이 응용 프로그램은 호텔 객실, 카페, 공공 Wi-Fi 핫스팟 및 기타 인터넷에서 연결할 수 있어야하는 비즈니스 여행객을 위해 설계되었습니다. 인터넷에 응용 프로그램을 게시하고 싶지 않습니다. 배포 및 운영 비용을 최소화하면서 위의 요구 사항을 충족하는 네트워크 설계는 무엇입니까?  
\nA) AWS Direct Connect를 구현하고 VPC에 대한 개인 인터페이스를 생성하십시오. 퍼블릭 서브넷을 생성하고 애플리케이션 서버를 그 안에 배치하십시오.  
\nB) 애플리케이션에 대한 백엔드 연결을 종료하는 SSL 리스너를 사용하여 Elastic Load Balancing을 구현합니다.  
\nC) IPsec VPN 연결을 구성하고 사용자에게 구성 세부 정보를 제공하십시오. VPC에 퍼블릭 서브넷을 생성하고 애플리케이션 서버를 퍼블릭 서브넷에 배치하십시오.  
\nD) VPC의 퍼블릭 서브넷에서 SSL VPN 솔루션을 구성한 다음 모든 사용자 컴퓨터에서 SSL VPN 클라이언트 소프트웨어를 설치 및 구성하십시오. VPC에 프라이빗 서브넷을 생성하고 애플리케이션 서버를 배치하십시오.

\n\n\n\n

팻 클라이언트  
 <https://ko.wikipedia.org/wiki/팻_클라이언트>

\n\n\n\n

많은 기능을 제공하는 어플리케이션을 인터넷에 게시하지 않고 배포하고 싶다.  
\n이건 vpn이다. 그리고 배포및 운영비용 최소화. 그럼 vpn 을 사용하여 비용 최적화를 해보자

\n\n\n\n

A는 DC를 사용한다 비용최적화에서 오답.  
 B는 인터넷에 연결되어야 한다. 오답.  
 C는 IPSec VPN을 사용한다. aws IPSec VPN은   
<http:// https://docs.aws.amazon.com/ko_kr/vpn/latest/s2svpn/VPC_VPN.html>  
 ipsec vpn으로 vpn 장비가 필요하다. 비용도 든다. 그래서 오답  
 D는 비용 효율적이며, 문제의 조건에 충족한다. 정답이다.

\n\n\n\n

따라서 D가 정답이다.

\n\n\n\n

영문  
\nYour company hosts an on-premises legacy engineering application with 900GB of data shared via a central file server. The engineering data consists of thousands of individual files ranging in size from megabytes to multiple gigabytes. Engineers typically modify 5-10 percent of the files a day. Your CTO would like to migrate this application to AWS, but only if the application can be migrated over the weekend to minimize user downtime. You calculate that it will take a minimum of 48 hours to transfer 900GB of data using your company’s existing 45-Mbps Internet connection. After replicating the application’s environment in AWS, which option will allow you to move the application’s data to AWS without losing any data and within the given timeframe?  
\nA) Copy the data to Amazon S3 using multiple threads and multi-part upload for large files over the weekend, and work in parallel with your developers to reconfigure the replicated application environment to leverage Amazon S3 to serve the engineering files.  
\nB) Sync the application data to Amazon S3 starting a week before the migration, on Friday morning perform a final sync, and copy the entire data set to your AWS file server after the sync completes.  
\nC) Copy the application data to a 1-TB USB drive on Friday and immediately send overnight, with Saturday delivery, the USB drive to AWS Import/Export to be imported as an EBS volume, mount the resulting EBS volume to your AWS file server on Sunday.  
\nD) Leverage the AWS Storage Gateway to create a Gateway-Stored volume. On Friday copy the application data to the Storage Gateway volume. After the data has been copied, perform a snapshot of the volume and restore the volume as an EBS volume to be attached to your AWS file server on Sunday.

\n\n\n\n

구글 번역본  
\n회사는 중앙 파일 서버를 통해 900GB의 데이터를 공유하는 온-프레미스 레거시 엔지니어링 응용 프로그램을 호스팅합니다. 엔지니어링 데이터는 메가 바이트에서 수기가 바이트에 이르는 수천 개의 개별 파일로 구성됩니다. 엔지니어는 일반적으로 하루에 5-10 %의 파일을 수정합니다. CTO는이 애플리케이션을 AWS로 마이그레이션하려고하지만 주말 동안 애플리케이션을 마이그레이션하여 사용자 중단 시간을 최소화 할 수있는 경우에만 해당합니다. 회사의 기존 45Mbps 인터넷 연결을 사용하여 900GB의 데이터를 전송하는 데 최소 48 시간이 소요될 것으로 계산합니다. AWS에서 애플리케이션 환경을 복제 한 후 데이터 손실없이 주어진 기간 내에 애플리케이션 데이터를 AWS로 이동할 수있는 옵션은 무엇입니까?  
\nA) 주말 동안 대용량 파일에 대해 다중 스레드 및 다중 부분 업로드를 사용하여 데이터를 Amazon S3에 복사하고 개발자와 병행하여 Amazon S3를 활용하여 엔지니어링 파일을 제공하도록 복제 된 애플리케이션 환경을 재구성합니다.  
\nB) 마이그레이션 1 주일 전부터 금요일 아침에 최종 동기화를 수행하고 동기화가 완료된 후 전체 데이터 세트를 AWS 파일 서버에 복사하여 애플리케이션 데이터를 Amazon S3에 동기화합니다.  
\nC) 금요일에 애플리케이션 데이터를 1TB USB 드라이브에 복사하고 토요일 배달을 통해 USB 드라이브를 AWS Import / Export로 전송하여 EBS 볼륨으로 가져 오면 결과 EBS 볼륨을 AWS 파일 서버에 마운트합니다. 일요일에.  
\nD) AWS Storage Gateway를 활용하여 게이트웨이 저장 볼륨을 생성합니다. 금요일에 애플리케이션 데이터를 Storage Gateway 볼륨에 복사하십시오. 데이터를 복사 한 후 볼륨의 스냅 샷을 수행하고 일요일에 AWS 파일 서버에 연결할 EBS 볼륨으로 볼륨을 복원하십시오.

\n\n\n\n

이문제는 굉장히 기분이 나쁜 유형의 문제이다. 하지만 마이그레이션 문제로 단골문제인거 같다.

\n\n\n\n

먼저 900G를 aws로 마이그레이션 하는것이다. 45mbps로 이동시간은 2일이다.

\n\n\n\n

A 회선이 느리므로 병목이 발생한다. 멀티파트 업로드가 소용이 없다. 오답이다.  
 B 파일의 변경이 많이 발생하지 않으므로 가능한 방법이다.  
 C의 경우 굉장히 긴가민가 했다. AWS Import/Export Disk는 일부리전에서 사용가능하긴 하나 인터넷을 사용하지 않음으로 병목도 없고   
 도착시부터 업로드가 시작되어 정상적으로 작업이 진행될것이라 생각했지만 usb 메모리의 속도는 그보다 떨어진다. 그래서 정해진 시간에 마이그레이션이 불가능하다는 결론에 도달했다.  
 그 결론에 도달한 이유는 '데이터 로드 시간은 기본적으로 디바이스 속도에 의해 좌우' 아래 URL을 참고하기 바란다.  
 <https://aws.amazon.com/ko/snowball/disk/faqs/>  
 D AWS Storage Gateway는 네트워크를 이용하므로 동일하게 병목이 발생한다 따라서 오답이다.

\n\n\n\n

그래서 위 문제의 정답은 B다.

\n