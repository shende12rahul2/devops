# Phase 3: Enterprise Best Practices
**Weeks 11–18 | 320 hours | 40 hrs/week**

> Consultant framing: "I design and operate enterprise-grade platforms with audit-ready security, SLO-based reliability, and cost governance — making them compliant, observable, and financially accountable."

---

## Enterprise Projects

### Project 8: Full Observability Platform (Week 14)
**Business Problem:** Engineering org with 40 microservices. When something breaks, nobody knows if it's the service, the network, the database, or the platform. MTTR is 90 minutes average.

```
observability-platform/
├── prometheus/
│   ├── prometheus.yaml               # Helm values
│   ├── rules/
│   │   ├── golden-signals.yaml       # Latency, traffic, errors, saturation
│   │   ├── slo-alerts.yaml           # Burn rate alerts
│   │   └── infrastructure.yaml      # Node, pod, PV alerts
│   ├── recording-rules/
│   │   └── precompute.yaml           # Expensive queries precomputed
│   └── thanos/                      # Long-term storage
├── grafana/
│   ├── dashboards/
│   │   ├── slo-overview.json         # Error budget dashboard
│   │   ├── service-map.json          # Service dependencies
│   │   ├── golden-signals.json       # Per-service golden signals
│   │   ├── kubernetes-nodes.json     # Infrastructure
│   │   └── on-call-assistant.json    # What on-call needs to see
│   └── provisioning/
├── opentelemetry/
│   ├── collector-config.yaml        # OTel collector pipeline
│   ├── instrumentation/
│   │   ├── java-agent.yaml          # Auto-instrumentation for Java
│   │   ├── python-sdk-example.py    # Manual instrumentation example
│   │   └── go-sdk-example.go
│   └── sampling-config.yaml         # Tail-based sampling rules
├── loki/
│   ├── loki-config.yaml
│   └── logql-examples.md            # Common log queries for on-call
├── alertmanager/
│   ├── config.yaml                  # Routing: critical → PagerDuty, warning → Slack
│   └── templates/
│       ├── slack.tmpl
│       └── pagerduty.tmpl
└── docs/
    ├── on-call-runbook.md
    ├── slo-definitions.md            # What we promise, how we measure
    └── alert-philosophy.md           # Why we alert on symptoms not causes
```

**SLO Definitions (must implement):**
```yaml
# slo-definitions.yaml
slos:
  - service: payment-service
    sli: "rate(http_requests_total{status!~'5..'}[5m]) / rate(http_requests_total[5m])"
    slo_target: 99.9
    error_budget_window: 30d
    alert_burn_rates:
      - severity: critical
        burn_rate: 14.4  # Consumes 1hr of budget in 5min → page
        window: 5m
      - severity: warning
        burn_rate: 6     # Consumes 1hr of budget in 30min → ticket
        window: 30m
```

**Business Impact to document:**
- MTTR before: 90 minutes → after: 8 minutes
- Alert noise: 200 alerts/week → 12 actionable alerts/week
- Incident detection: reactive → proactive (catch before users notice)

---

### Project 9: DevSecOps Pipeline (Week 11-12)
```
devsecops-pipeline/
├── .github/workflows/
│   └── secure-pipeline.yml           # Full security gates
├── scanning/
│   ├── trivy-config.yaml             # Image + IaC scanning
│   ├── semgrep-rules/                # Custom SAST rules for your stack
│   ├── gitleaks-config.toml          # Secret detection config
│   └── grype-config.yaml             # Vulnerability scanning
├── sbom/
│   └── generate-sbom.sh              # Syft SBOM generation
├── signing/
│   └── cosign-sign.sh                # Keyless signing with OIDC
├── vault/
│   ├── policies/
│   │   ├── ci-policy.hcl             # CI/CD read-only policy
│   │   └── app-policy.hcl            # App runtime policy
│   ├── auth/
│   │   └── k8s-auth.tf               # K8s auth backend config
│   └── secrets/
│       └── dynamic-db-creds.hcl      # Dynamic database credentials
├── opa/
│   └── policies/
│       ├── block-privileged.rego      # Block privileged containers
│       ├── require-limits.rego        # Require resource limits
│       └── approved-registries.rego   # Only internal registry
└── compliance/
    ├── cis-k8s-benchmark.sh          # CIS K8s benchmark runner
    └── evidence-collector.sh          # SOC2 evidence automation
```

---

### Project 10: Chaos Engineering Programme (Week 16)

```
chaos-engineering/
├── gamedays/
│   ├── gameday-template.md           # How to run a gameday
│   └── gameday-001-pod-failure.md    # First gameday report
├── experiments/
│   ├── pod-failure/
│   │   └── litmus-chaos.yaml         # Random pod deletion
│   ├── network-latency/
│   │   └── network-chaos.yaml        # Add 200ms latency
│   ├── cpu-stress/
│   │   └── cpu-hog.yaml              # CPU exhaustion test
│   ├── memory-stress/
│   │   └── memory-hog.yaml           # Memory pressure
│   └── node-drain/
│       └── node-drain.sh             # Drain a node gracefully
├── steady-state/
│   └── steady-state.yaml             # Define normal before chaos
├── hypothesis/
│   └── hypothesis-template.md        # Scientific method for chaos
└── reports/
    └── experiment-001-report.md      # Results + learnings
```

---

## Interview Preparation — Phase 3

### Week 14: Observability (Critical Questions)

**Q: A microservice is slow. How do you diagnose it using your observability stack?**
```
Structured approach — I call this the "4 Signals Funnel":

1. Traffic: is the request volume normal? Sudden spike = capacity issue.
   PromQL: rate(http_requests_total{service="payment"}[5m])

2. Errors: is error rate elevated?  
   PromQL: rate(http_errors_total[5m]) / rate(http_requests_total[5m])

3. Latency: which percentile is affected? p50? p99?
   PromQL: histogram_quantile(0.99, rate(http_duration_seconds_bucket[5m]))

4. Saturation: is any resource saturated?
   CPU: rate(container_cpu_usage_seconds_total[5m])
   Memory: container_memory_usage_bytes / container_spec_memory_limit_bytes

5. If application metrics don't explain it: go to traces.
   Find the slowest trace in Jaeger/Tempo. Identify which span is slow.
   Is it the DB call? External API? Internal computation?

6. Logs: now you know WHAT is slow. Logs tell you WHY.
   LogQL: {app="payment"} |= "error" | json | latency > 1000

Result: I should know the root cause in under 5 minutes with proper observability.
Without it, the same diagnosis takes 45-90 minutes of guesswork.
```

**Q: Design an alerting system that doesn't cause alert fatigue.**
```
The problem with traditional alerting: you alert on thresholds, 
not on user impact. Result: noisy, desensitised on-call.

My approach:
1. Alert on symptoms (user experience), not causes (CPU at 80%)
2. Use SLO-based burn rate alerting:
   - "We're burning our error budget 14x faster than normal" = page
   - "We're burning it 3x faster" = ticket (not a page)
   
3. Alert levels:
   - Critical (pager): customer impact NOW, error budget burning fast
   - Warning (Slack): potential future problem, investigate tomorrow
   - Info (dashboard only): interesting, investigate when convenient

4. Each alert must have: what's broken, impact, runbook link, ownership
5. Every alert reviewed monthly: if it fired and nobody acted, delete it
6. Target: <5 actionable pages per week per on-call

In one previous system: went from 200 alerts/week to 12 high-signal ones.
On-call happiness score went from 2/10 to 7/10.
```

*(All 80 questions for Phase 3 in weekly interview-prep files)*

---

## CNCF Tools — Phase 3 Deep Dives

| Week | Tool | What You'll Build |
|------|------|-------------------|
| 11 | Falco + Trivy | Runtime security monitoring + pipeline scanning |
| 12 | HashiCorp Vault + ESO | Dynamic secrets for all services |
| 13 | Istio/Linkerd | mTLS service mesh + traffic management |
| 14 | Prometheus + OTel + Loki | Full observability stack |
| 15 | SLO framework | Error budget dashboards + burn rate alerts |
| 16 | LitmusChaos | Automated chaos experiment pipeline |
| 17 | Kubecost | Cost per team/namespace/app reporting |
| 18 | OPA + Gatekeeper | Policy-as-code for compliance |
