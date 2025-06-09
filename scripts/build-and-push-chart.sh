#!/usr/bin/env bash
set -e -o pipefail

helm dependency build ./charts/tmwtd
helm package ./charts/tmwtd
CHART=tmwtd-$(helm show chart ./charts/tmwtd | grep '^version:' | awk '{print $2}').tgz

echo $CHART

helm push $CHART oci://registry-1.docker.io/dingobar/tellmewhattodo
