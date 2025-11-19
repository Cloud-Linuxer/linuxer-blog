---
title: "helm-sentry-install-fail"
date: 2023-10-23T17:26:00+09:00
draft: false
categories: ["Kubernetes"]
tags: ["k8s", "sentry", "job", "activeDeadlineSeconds"]
slug: "helm-sentry-install-fail"
aliases:
  - /helm-sentry-install-fail/
  - /helm-sentry-install-fail/
---

\n

```
helm install sentry sentry/sentry\ncoalesce.go:175: warning: skipped value for kafka.config: Not a table.\ncoalesce.go:175: warning: skipped value for kafka.zookeeper.topologySpreadConstraints: Not a table.\nW1023 08:00:35.276931   15594 warnings.go:70] spec.template.spec.containers[0].env[39]: hides previous definition of "KAFKA_ENABLE_KRAFT"\nError: INSTALLATION FAILED: failed post-install: 1 error occurred:\n        * job failed: DeadlineExceeded
```

\n\n\n\n

job failed: DeadlineExceeded 에러가 발생한다.

\n\n\n\n

이 job은 DB가 정상적으로 올라왔는지 확인하는 job이다.

\n\n\n\n

```
k get job\nNAME              COMPLETIONS   DURATION   AGE\nsentry-db-check   0/1           5m23s      5m23s
```

\n\n\n\n

이 Job은 다음을 검증한다.

\n\n\n\n

```
 name: sentry-db-check\n    namespace: sentry\n    resourceVersion: "4700657"\n    uid: 12533bba-b35b-4b7d-9007-8c625b389a98\n  spec:\n    activeDeadlineSeconds: 1000\n    backoffLimit: 6\n    completionMode: NonIndexed\n    completions: 1\n    parallelism: 1\n    selector:\n      matchLabels:\n        batch.kubernetes.io/controller-uid: 12533bba-b35b-4b7d-9007-8c625b389a98\n    suspend: false\n    template:\n      metadata:\n        creationTimestamp: null\n        labels:\n          app: sentry\n          batch.kubernetes.io/controller-uid: 12533bba-b35b-4b7d-9007-8c625b389a98\n          batch.kubernetes.io/job-name: sentry-db-check\n          controller-uid: 12533bba-b35b-4b7d-9007-8c625b389a98\n          job-name: sentry-db-check\n          release: sentry\n        name: sentry-db-check\n      spec:\n        containers:\n        - command:\n          - /bin/sh\n          - -c\n          - |\n            echo "Checking if clickhouse is up"\n            CLICKHOUSE_STATUS=0\n            while [ $CLICKHOUSE_STATUS -eq 0 ]; do\n              CLICKHOUSE_STATUS=1\n              CLICKHOUSE_REPLICAS=3\n              i=0; while [ $i -lt $CLICKHOUSE_REPLICAS ]; do\n                CLICKHOUSE_HOST=sentry-clickhouse-$i.sentry-clickhouse-headless\n                if ! nc -z "$CLICKHOUSE_HOST" 9000; then\n                  CLICKHOUSE_STATUS=0\n                  echo "$CLICKHOUSE_HOST is not available yet"\n                fi\n                i=$((i+1))\n              done\n              if [ "$CLICKHOUSE_STATUS" -eq 0 ]; then\n                echo "Clickhouse not ready. Sleeping for 10s before trying again"\n                sleep 10;\n              fi\n            done\n            echo "Clickhouse is up"\n\n            echo "Checking if kafka is up"\n            KAFKA_STATUS=0\n            while [ $KAFKA_STATUS -eq 0 ]; do\n              KAFKA_STATUS=1\n              KAFKA_REPLICAS=3\n              i=0; while [ $i -lt $KAFKA_REPLICAS ]; do\n                KAFKA_HOST=sentry-kafka-$i.sentry-kafka-headless\n                if ! nc -z "$KAFKA_HOST" 9092; then\n                  KAFKA_STATUS=0\n                  echo "$KAFKA_HOST is not available yet"\n                fi\n                i=$((i+1))\n              done\n              if [ "$KAFKA_STATUS" -eq 0 ]; then\n                echo "Kafka not ready. Sleeping for 10s before trying again"\n                sleep 10;\n              fi\n            done\n            echo "Kafka is up"\n          image: subfuzion/netcat:latest\n          imagePullPolicy: IfNotPresent\n          name: db-check\n          resources:\n            limits:\n              memory: 64Mi\n            requests:\n              cpu: 100m\n              memory: 64Mi\n          terminationMessagePath: /dev/termination-log\n          terminationMessagePolicy: File\n        dnsPolicy: ClusterFirst\n        restartPolicy: Never\n        schedulerName: default-scheduler\n        securityContext: {}\n        terminationGracePeriodSeconds: 30
```

\n\n\n\n

Clickhouse / Kafka 가 실행되어야 job은 정상화 가능하다. 시간이 오래걸리는 작업이므로, hook 의 시간을 늘려주면 job은 더 긴시간 대기한다 helm 의 values.yaml 에서 activeDeadlineSeconds를 늘려주면 된다.

\n\n\n\n

```
hooks:\n  enabled: true\n  removeOnSuccess: true\n  activeDeadlineSeconds: 1000
```

\n\n\n\n

이 시간을 늘려도 문제가 생긴다면 보통 kafka의 pv가 생성되지 않는경우다.

\n\n\n\n

CSI 컨트롤러를 확인해 보는게 좋다.

\n