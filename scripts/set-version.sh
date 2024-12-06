#!/usr/bin/env bash

# This script sets the version in the poetry.lock file as well as the chart based
# on the VERSION file content

VERSION="$(cat VERSION)"

# Set version in chart
sed -i "s/^version:.*$/version: ${VERSION}/" ./charts/tmwtd/Chart.yaml
sed -i "s/^appVersion:.*$/appVersion: ${VERSION}/" ./charts/tmwtd/Chart.yaml

# Set version in poetry
sed -i "s/^version = .*$/version = \"${VERSION}\"/" ./pyproject.toml
