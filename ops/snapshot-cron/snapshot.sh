#!/bin/sh
set -e
DATE=$(date +%Y%m%d-%H%M)
curl -s -XPUT ${OS_URL:-http://opensearch:9200}/_snapshot/${OS_REPO:-ai-soc-repo}/snap-$DATE
