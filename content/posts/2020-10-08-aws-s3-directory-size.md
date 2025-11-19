---
title: "AWS-S3-directory-size"
date: 2020-10-08T10:24:16+09:00
draft: false
categories: ["AWS"]
tags: ["s3", "sum"]
slug: "aws-s3-directory-size"
aliases:
  - /aws-s3-directory-size/
  - /aws-s3-directory-size/
---


aws s3 ls s3://linuxer-wp/wp-content/uploads/2019/08/ --human-readable --summarize


aws s3 명령어만으로 조합.


![](/images/2020/10/image-1-1024x117.png)

aws s3 ls s3://linuxer-wp/ --recursive --recursive | grep 2020 | awk 'BEGIN {total=0}{total+=$3}END{print total/1024/1024" MB"}'


aws s3 ls + grep + awk total+=$3더한것.


![](/images/2020/10/image-1024x35.png)

