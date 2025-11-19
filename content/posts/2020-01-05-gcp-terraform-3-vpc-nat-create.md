---
title: "gcp terraform-3 vpc-nat create"
date: 2020-01-05T15:25:55+09:00
draft: false
categories: ["GCP"]
tags: ["gcp", "terraform", "nat"]
slug: "gcp-terraform-3-vpc-nat-create"
aliases:
  - /gcp-terraform-3-vpc-nat-create/
  - /gcp-terraform-3-vpc-nat-create/
---

\n

vpc-nat 를 연결하기로 했다.  
어젠 subnet 을 만들었고 오늘은 망분리 환경을 구성하기 위해 nat 를 넣었다.

\n\n\n\n

main.tf

\n\n\n\n

resource "google\_compute\_subnetwork" "us-central1-subnet" {  
 name = "${local.name\_suffix}-us-central1-subnet"  
 ip\_cidr\_range = "10.2.0.0/16"  
 region = "us-central1"  
 network = "${google\_compute\_network.vpc.self\_link}"  
 }  
 resource "google\_compute\_router" "us-central1-router" {  
 name = "${local.name\_suffix}-us-central1-router"  
 region = google\_compute\_subnetwork.us-central1-subnet.region  
 network = google\_compute\_network.vpc.self\_link  
 }  
 resource "google\_compute\_address" "address" {  
 count = 2  
 name = "${local.name\_suffix}-nat-manual-ip-${count.index}"  
 region = google\_compute\_subnetwork.us-central1-subnet.region  
 }  
 resource "google\_compute\_router\_nat" "nat\_manual" {  
 name = "${local.name\_suffix}-us-central1-router-nat"  
 router = google\_compute\_router.us-central1-router.name  
 region = google\_compute\_router.us-central1-router.region  
nat\_ip\_allocate\_option = "MANUAL\_ONLY"  
 nat\_ips = google\_compute\_address.address.\*.self\_link  
  
source\_subnetwork\_ip\_ranges\_to\_nat = "LIST\_OF\_SUBNETWORKS"  
 subnetwork {  
 name = "${local.name\_suffix}-us-central1-subnet"  
 source\_ip\_ranges\_to\_nat = ["10.2.0.0/16"]  
 }  
 }  
  
resource "google\_compute\_network" "vpc" {  
 name = "${local.name\_suffix}-vpc"  
 auto\_create\_subnetworks = false  
 }

\n\n\n\n

backing\_file.tf

\n\n\n\n

locals {  
 name\_suffix = “linuxer”  
 }  
 provider “google” {  
 region = “us-central1”  
 zone = “us-central1-c”  
 }

\n\n\n\n
![](/images/2020/01/image-20-1024x542.png)
\n\n\n\n
![](/images/2020/01/image-19-866x1024.png)
\n\n\n\n

vpc 와 nat nat route 까지 정상적으로 만들어져서 동작하는 것을 확인할 수 있었다.

\n\n\n\n

리전당 nat는 1개를 꼭만들어야 했다.

\n\n\n\n

현재 생성한 tf는 subnet 하나에 대한 설정이다. 다른 리전으로도 네임만 수정을 적절히 하면 수정해서 쓸수 있다.

\n\n\n\n\n