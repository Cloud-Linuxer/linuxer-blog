---
title: "gcp-terrafrom-1 with google cloud shell"
date: 2020-01-04T18:55:54+09:00
draft: false
categories: ["GCP"]
tags: ["gcp", "cloudshell", "terraform"]
slug: "gcp-terrafrom-1-with-google-cloud-shell"
aliases:
  - /gcp-terrafrom-1-with-google-cloud-shell/
  - /gcp-terrafrom-1-with-google-cloud-shell/
---


gcp 스터디를 위해서 테라폼의 사용을 익히려고 한다.
그러기 위해선 먼저 테라폼을 gcp cloudshell 에서 사용하는것이 우선이라 생각했다.


테라폼으로 aws내 에선 테스트 경험이 있으므로 gcp 의 네트워크 구성과 환경에 맞춰서 테라폼을 설정하는 방법을 익혀야 했다.


gcp 에서 테라폼을 사용하려면 cloudshell 을 사용하는 방법과 인스턴스를 생성하여 사용하는 방법 아니면 클라이언트 PC에서 사용하는 방법 이렇게 3가지가 있는데 나는 cloudshell 을 매우 좋아하므로 cloudshell 로 진행 할것이다.


먼저 cloud shell 에서 테라폼을 사용하려면 몇가지 단계를 거쳐야 했다.


1 terrafrom install
2 gcp api setup
3 config setting


이 단계를 간단하게 줄여주는 페이지가 있어서 먼저 테스트 해봤다.


<https://www.hashicorp.com/blog/kickstart-terraform-on-gcp-with-google-cloud-shell/>


<https://github.com/terraform-google-modules/docs-examples>


두개의 URL 을 참고하시기 바란다.


URL 을 따라서 진행하던중 terraform init 에서 에러가 발생하였다.


![](/images/2020/01/image-1024x374.png)

Provider "registry.terraform.io/-/google" v1.19.1 is not compatible with Terraform 0.12.18.
 Provider version 2.5.0 is the earliest compatible version. Select it with
 the following version constraint:

 version = "~> 2.5"
 Terraform checked all of the plugin versions matching the given constraint:
 ~> 1.19.0
 Consult the documentation for this provider for more information on
 compatibility between provider and Terraform versions.
 Downloading plugin for provider "random" (hashicorp/random) 2.2.1…
 Error: incompatible provider version


error 는 backing_file.tf 파일에서 발생하고 있었다.
간단하게 version 차이..


cloud shell 의 terrafrom version 은


dellpa34@cloudshell:~/docs-examples/oics-blog$ terraform -version
 Terraform v0.12.18
provider.google v2.20.1
provider.random v2.2.1


provider.google v2.20.1 로 1.19보다 많이 높은 상태였다. 일단 진행해 보기로 했으니.. backing_file.tf 수정


provider "google" {
 version = "~> 1.19.0"
 region = "us-central1"
 zone = "us-central1-c"
 }


provider "google" {
 version = "~> 2.5"
 region = "us-central1"
 zone = "us-central1-c"
 }


수정후에 다시 terraform init 을 실행 하였다.


![](/images/2020/01/image-1-1024x316.png)

Initializing provider plugins…
 Checking for available provider plugins…
 Downloading plugin for provider "google" (hashicorp/google) 2.20.1…
 Terraform has been successfully initialized!
 You may now begin working with Terraform. Try running "terraform plan" to see
 any changes that are required for your infrastructure. All Terraform commands
 should now work.
 If you ever set or change modules or backend configuration for Terraform,
 rerun this command to reinitialize your working directory. If you forget, other
 commands will detect it and remind you to do so if necessary.


정상적으로 실행 되는것을 확인하였다.


init 후에 apply 하니 다시 Warning 과 함께 error 가 발생하였다.


![](/images/2020/01/image-2-1024x107.png)

Warning: Interpolation-only expressions are deprecated
 on main.tf line 9, in resource "google_compute_instance" "instance":
 9: image = "${data.google_compute_image.debian_image.self_link}"


![](/images/2020/01/image-3-1024x145.png)

Error: Error loading zone 'us-central1-a': googleapi: Error 403: Access Not Configured. Compute Engine API has not been used in project 45002 before or it is disabled. Enable it by visiting https://console.developers.google.com/apis/api/compute.googleapis.com/overview?project=304102002 then retry. If you enabled this API recently, wait a few minutes for the action to propagate to our systems and retry., accessNotConfigured
 on main.tf line 1, in resource "google_compute_instance" "instance":
 1: resource "google_compute_instance" "instance" {


이건 이전에도 겪은 케이스 같다...functions api 셋팅할때 발생한 거였는데...googleapi 관련 에러다. cloudshell 에서 컴퓨팅쪽의 api를 사용할 수 없어서 발생하는 에러로 로그에 보이는 페이지로 이동해서 그냥 허용해 준다.


![](/images/2020/01/image-5-1024x253.png)

Enter a value: yes
 google_compute_instance.instance: Creating…
 google_compute_instance.instance: Still creating… [10s elapsed]
 google_compute_instance.instance: Creation complete after 10s [id=vm-instance-optimum-badger]
 Apply complete! Resources: 1 added, 0 changed, 0 destroyed.


허용후에 다시 terraform apply 를 치면 정상적으로 실행이 된다. 그럼 확인해 보자.


![](/images/2020/01/image-6-1024x113.png)

인스턴스가 생성이 됬다. 그렇다면 이젠 간단히 생성하는것 까지 완료했으므로. 이젠 기본 템플릿을 이용한 구성을 만들것이다. 생성한 테라폼은 terraform destroy 명령어로 삭제 했다.


![](/images/2020/01/image-7-1024x183.png)

google_compute_instance.instance: Destroying… [id=vm-instance-optimum-badger]
 google_compute_instance.instance: Still destroying… [id=vm-instance-optimum-badger, 10s elapsed]
 google_compute_instance.instance: Still destroying… [id=vm-instance-optimum-badger, 20s elapsed]
 google_compute_instance.instance: Still destroying… [id=vm-instance-optimum-badger, 30s elapsed]
 google_compute_instance.instance: Destruction complete after 38s
 random_pet.suffix: Destroying… [id=optimum-badger]
 random_pet.suffix: Destruction complete after 0s


정상적으로 삭제되는것을 확인할수 있었다.


gcp cloud shell 에서 terraform 을 사용하는 방법을 테스트해 보았다.
다음엔 VPC 구성과 인스턴스 그룹 생성 로드벨런서 구성까지 한방에 진행할것이다.


여담으로 cloud shell은 진짜 강력한 도구이다.


![](/images/2020/01/image-8-976x1024.png)

스크린샷과 같이 shell을 지원하면서 동시에 에디터도 지원한다.


vi 에 익숙한 나같은경우에는 그냥 vi 로 작업하지만 익숙하지 않은 사용자의 경우에는 우와할정도다..


쓸수록 감탄하는 cloudshell...........
