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


vpc-nat 를 연결하기로 했다.
어젠 subnet 을 만들었고 오늘은 망분리 환경을 구성하기 위해 nat 를 넣었다.

main.tf

resource "google_compute_subnetwork" "us-central1-subnet" {
 name = "${local.name_suffix}-us-central1-subnet"
 ip_cidr_range = "10.2.0.0/16"
 region = "us-central1"
 network = "${google_compute_network.vpc.self_link}"
 }
 resource "google_compute_router" "us-central1-router" {
 name = "${local.name_suffix}-us-central1-router"
 region = google_compute_subnetwork.us-central1-subnet.region
 network = google_compute_network.vpc.self_link
 }
 resource "google_compute_address" "address" {
 count = 2
 name = "${local.name_suffix}-nat-manual-ip-${count.index}"
 region = google_compute_subnetwork.us-central1-subnet.region
 }
 resource "google_compute_router_nat" "nat_manual" {
 name = "${local.name_suffix}-us-central1-router-nat"
 router = google_compute_router.us-central1-router.name
 region = google_compute_router.us-central1-router.region
nat_ip_allocate_option = "MANUAL_ONLY"
 nat_ips = google_compute_address.address.\*.self_link

source_subnetwork_ip_ranges_to_nat = "LIST_OF_SUBNETWORKS"
 subnetwork {
 name = "${local.name_suffix}-us-central1-subnet"
 source_ip_ranges_to_nat = ["10.2.0.0/16"]
 }
 }

resource "google_compute_network" "vpc" {
 name = "${local.name_suffix}-vpc"
 auto_create_subnetworks = false
 }

backing_file.tf

locals {
 name_suffix = “linuxer”
 }
 provider “google” {
 region = “us-central1”
 zone = “us-central1-c”
 }

![](/images/2020/01/image-20-1024x542.png)

![](/images/2020/01/image-19-866x1024.png)

vpc 와 nat nat route 까지 정상적으로 만들어져서 동작하는 것을 확인할 수 있었다.

리전당 nat는 1개를 꼭만들어야 했다.

현재 생성한 tf는 subnet 하나에 대한 설정이다. 다른 리전으로도 네임만 수정을 적절히 하면 수정해서 쓸수 있다.
