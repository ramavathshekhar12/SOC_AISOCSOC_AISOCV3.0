# ILM & S3 Snapshots

1) Apply ILM (Index State Management) policy:
```bash
curl -XPUT http://localhost:9200/_plugins/_ism/policies/ai-soc-ilm -H 'Content-Type: application/json' --data-binary @ilm-policy.json
```

2) Create an index template to attach the policy:
```bash
curl -XPUT http://localhost:9200/_index_template/ai-soc-alerts -H 'Content-Type: application/json' -d '{
  "index_patterns": ["ai_soc-alerts*"],
  "template": { "settings": { "index.plugins.index_state_management.policy_id": "ai-soc-ilm" } }
}'
```

3) Install the `repository-s3` plugin in OpenSearch and register snapshot repository:
```bash
# Build a custom image or install plugin in Dockerfile:
# RUN ./bin/opensearch-plugin install --batch repository-s3

curl -XPUT http://localhost:9200/_snapshot/ai-soc-repo -H 'Content-Type: application/json' --data-binary @snapshot-repo.json
```

4) Take a snapshot:
```bash
curl -XPUT http://localhost:9200/_snapshot/ai-soc-repo/snap-$(date +%Y%m%d)
```

> For AWS auth, set env vars or configure cloud credentials on the node. For MinIO, set endpoint overrides.
