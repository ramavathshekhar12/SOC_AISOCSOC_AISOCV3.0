# AI-SOC (Open Blueprint Starter)

This repository is a **minimal starter** to help you build your own SOC platform (agent → manager → indexer → dashboard) without Wazuh branding. 
It includes:
- **Agent (Python)** for basic log shipping and FIM-like hashing of watched paths.
- **Manager (FastAPI, Python)** with a simple decoder + rules engine, alerting, OpenSearch indexing, and stubbed Active Response.
- **PT Orchestrator (FastAPI, Python)** to run **safe, allowlisted** nmap and OWASP ZAP scans for approved targets.
- **AI Anomaly Service (FastAPI, Python)** with a basic IsolationForest anomaly scorer for numeric features.
- **OpenSearch** for storage/search.
- **React (Vite) Dashboard** to view alerts and agent status.

> ⚠️ This is a starter/P0 reference. Harden, test, and expand before production. Add TLS, mTLS, RBAC, SSO, audit logging, and CI/CD.
> ✅ Only perform PT scans where you **own/written permission**. The orchestrator enforces an allowlist but you must comply with laws/policies.

## Quick start
1. Install Docker + Docker Compose v2.
2. Copy `.env.example` to `.env` and set secrets.
3. Run: `docker compose up -d --build`
4. Open:
   - Manager API: http://localhost:8000/docs
   - PT Orchestrator: http://localhost:8010/docs
   - AI Anomaly API: http://localhost:8020/docs
   - Dashboard (React): http://localhost:5173
   - OpenSearch Dashboards: http://localhost:5601  (user/pass: admin/admin; change it!)
5. On a test machine, run the agent:
   ```bash
   python agent/agent.py --manager http://localhost:8000 --token YOUR_AGENT_TOKEN --watch /var/log/syslog
   ```

## Services
- `services/manager`: event intake, decoding, rules, alert indexing, AR stubs
- `services/pt_orchestrator`: safe PT actions (nmap, ZAP) behind allowlist + rate limit
- `services/ai_anomaly`: minimalist anomaly detection API for numeric feature vectors
- `agent`: sample Python agent for Linux/Windows (file tail + hash watcher)
- `dashboard`: Vite React app to browse alerts and agents

## Roadmap (suggested)
- mTLS for agent↔manager (client certs)
- RBAC + SSO (OIDC) for APIs and dashboard
- Advanced rule DSL + stateful correlation (frequency/time-window/aggregation)
- Threat intel (MISP/OpenCTI) enrichment and watchlists
- Full FIM whodata (Linux auditd + Windows audit)
- ILM retention tiers; snapshots to object storage
- Active Response guardrails, approvals, and audit trails
- Multi-tenant index/role separation


## Entra OIDC (end-to-end)
Set these in `.env`:
- OIDC_ISSUER, OIDC_AUDIENCE, OIDC_JWKS_URL (server-side token validation)
- VITE_OIDC_AUTHORITY, VITE_OIDC_CLIENT_ID, VITE_OIDC_REDIRECT_URI (frontend login)
Entra tip: add App Roles (L1/L2/L3/Admin) and assign users; include `roles` or `groups` in tokens.

## Windows & Linux collectors
- Windows: run `python agent/windows_event_reader.py` to verify events; or integrate directly by posting to `/intake`.
- Linux: run `python agent/auditd_whodata.py` to see parsed events; add agent code to post these to `/intake`.

## OpenSearch snapshots
- Custom image installs `repository-s3` plugin.
- `snapshot-cron` runs daily snapshots. Register repo and provide S3 credentials in node env/keystore.
