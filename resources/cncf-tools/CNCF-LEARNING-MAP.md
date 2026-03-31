# CNCF Tools — The Complete Learning Map
## What to Learn, When, Why, and How

> Reference: landscape.cncf.io — 1000+ tools. This guide cuts through the noise.
> Rule: Master the Graduated projects first. They're graduated because they're production-proven.

---

## The CNCF Graduation Ladder

```
Sandbox → Incubating → Graduated
  (experimental)   (production-ready)   (industry standard)
```

Only learn Sandbox tools if they solve a specific problem you have.

---

## Phase-by-Phase Learning Order

### Phase 1 (Weeks 1–4): Foundation — No CNCF Yet
Build Linux, networking, Git mastery first. Every CNCF tool runs on Linux.

### Phase 2 (Weeks 5–10): Core Container Stack

#### Kubernetes (Graduated ⭐ Must-Know #1)
**Why:** The de facto container orchestration platform. 85% of container workloads run on it.
**Learn:** Architecture → Scheduling → Networking → Storage → Security → Autoscaling
**Resources:**
- kubernetes.io/docs (official, excellent)
- Kubernetes in Action (Lukša) — best book
- killer.sh — exam practice
- KodeKloud — hands-on labs
**Certifications:** CKA → CKAD → CKS (do all three)
**Key concepts to master:**
- Control plane components: API server, etcd, scheduler, controller manager
- Data plane: kubelet, kube-proxy, CRI (containerd)
- Networking: CNI plugins, Services, Endpoints, Ingress, DNS (CoreDNS)
- Storage: PV, PVC, StorageClass, CSI drivers
- RBAC: ServiceAccount, Role, ClusterRole, Binding
- Scheduling: affinity, taints/tolerations, resource requests/limits

#### Helm (Graduated ⭐ Must-Know)
**Why:** Package manager for Kubernetes. Every prod deployment uses Helm.
**Learn:** Chart structure → templating → values override → dependencies → OCI registries
**Resources:** helm.sh/docs, ArtifactHub (find charts)
**Key skill:** Write a chart from scratch, not just use existing ones

#### Flux (Graduated) / ArgoCD (Graduated)
**Why:** GitOps — deploy from Git, not CLI. Industry standard for production.
**ArgoCD:** UI-heavy, pull-based, multi-cluster, App of Apps pattern
**Flux:** CLI-first, Kubernetes-native, better multi-tenancy
**Learn both:** know trade-offs for interviews
**Resources:** fluxcd.io, argo-cd.readthedocs.io

#### Harbor (Graduated)
**Why:** Enterprise container registry. Docker Hub is not acceptable in enterprise.
**Features:** Vulnerability scanning (Trivy), image signing, RBAC, geo-replication
**Alternatives:** AWS ECR, GCP Artifact Registry, GitLab Registry
**Learn:** Setup → RBAC → Trivy integration → image signing → replication

#### Containerd (Graduated)
**Why:** The actual container runtime that Kubernetes uses. Docker is a wrapper.
**Learn:** crictl commands (kubectl for containers), image management, config
**Key:** `docker` → `crictl` for K8s container debugging

---

### Phase 3 (Weeks 11–18): Security & Observability

#### Falco (Graduated ⭐ Security Must-Know)
**Why:** Runtime security monitoring for containers. Detects suspicious behaviour.
**What it does:** Monitors system calls via eBPF, alerts on rules (shell in container, 
  unexpected network connection, privilege escalation)
**Resources:** falco.org, Falco rules library
**Learn:** Installation (Helm) → custom rules → integration with alerting
**Consultant pitch:** "Falco gave us compliance-level visibility into container runtime 
  behaviour with zero code changes. We detected a cryptominer in 3 minutes."

#### Open Policy Agent / Gatekeeper (Graduated ⭐ Must-Know)
**Why:** Policy enforcement for Kubernetes. Block non-compliant resources at admission.
**OPA:** General-purpose policy engine, Rego language
**Gatekeeper:** OPA + Kubernetes integration + audit capabilities
**Policies to implement:**
- Block privileged containers
- Require resource limits
- Require specific labels
- Restrict registries to approved list
- Block hostPath mounts
**Resources:** openpolicyagent.org, Gatekeeper library (github.com/open-policy-agent/gatekeeper-library)

#### Prometheus (Graduated ⭐ Must-Know #2)
**Why:** The metrics standard. Every K8s cluster runs Prometheus.
**Architecture:** scrape model → TSDB → PromQL → AlertManager
**Learn:**
- PromQL: rate(), sum() by, histogram_quantile(), absent()
- Recording rules (pre-compute expensive queries)
- Alert rules (alerting on symptoms not causes)
- ServiceMonitor / PodMonitor CRDs
- Thanos / Cortex for long-term storage and multi-cluster
**Resources:** prometheus.io/docs, promcon.io talks, "Prometheus: Up & Running" (O'Reilly)

#### Grafana (Graduated ⭐ Must-Know)
**Why:** The dashboard standard. Pairs with Prometheus, Loki, Tempo.
**Learn:**
- Dashboard design for operations (not just pretty charts)
- Golden signals dashboards: latency, traffic, errors, saturation
- SLO/SLA dashboards with burn rate alerting
- Alerting via Grafana (not just Prometheus Alertmanager)
- Grafana Mimir (Prometheus-compatible, scalable)
**Resources:** grafana.com/tutorials, Grafana Labs blog

#### Jaeger (Graduated) / Tempo (Grafana)
**Why:** Distributed tracing. Without it, debugging microservices is guesswork.
**OpenTelemetry (CNCF Graduated):** The standard for instrumentation
- One SDK to instrument your app → works with any backend
- Auto-instrumentation for Java, Python, Node.js (zero code changes!)
**Learn:** OTel SDK → collector → Jaeger/Tempo
**Resources:** opentelemetry.io (excellent docs)

#### Loki (Grafana)
**Why:** Log aggregation that integrates with Grafana. Cheaper than ELK at scale.
**Learn:** LogQL (similar to PromQL), label-based log organization
**Key insight:** Loki doesn't index log content (cheap). Only indexes labels (fast).

#### cert-manager (CNCF Incubating)
**Why:** Automated TLS certificate management in Kubernetes. Manual cert management = incidents.
**Learn:** Issuers (Let's Encrypt, Vault), Certificate CRD, ACME challenges
**Install:** Helm chart → ClusterIssuer → annotate Ingress → auto-renewal

---

### Phase 4 (Weeks 19–26): Platform Engineering & Advanced

#### Backstage (CNCF Incubating ⭐ Platform Engineering)
**Why:** Internal Developer Portal. The interface for your platform.
**What it gives devs:** Service catalog, tech docs, scaffolding templates, 
  runbooks, on-call info — all in one place.
**Learn:** Architecture → plugins → software templates (scaffolding) → TechDocs
**Resources:** backstage.io, backstage.spotify.com (origin story)

#### Crossplane (CNCF Graduated)
**Why:** Infrastructure as Code via Kubernetes. Define cloud resources as CRDs.
**What it does:** `kubectl apply -f database.yaml` → creates actual AWS RDS instance
**Concepts:** Provider (AWS/GCP/Azure), CompositeResourceDefinition (XRD), 
  Composition, Claims
**Resources:** crossplane.io/docs

#### KEDA (CNCF Graduated)
**Why:** Event-driven autoscaling. HPA is CPU/memory only. KEDA scales on anything.
**Scale on:** Kafka lag, SQS queue depth, RabbitMQ messages, Prometheus metrics, 
  Cron schedule, Redis length
**Resources:** keda.sh

#### Cilium (CNCF Graduated ⭐ Networking Must-Know 2024)
**Why:** eBPF-based networking. Replaces iptables, adds network observability.
**What it gives you:** 
- Network policies with Layer 7 awareness (HTTP method, path)
- Hubble: network traffic observability
- Service mesh without sidecars (eBPF-native)
- Significantly better performance than iptables
**Resources:** cilium.io, isovalent.com/labs (free hands-on)

#### Linkerd (CNCF Graduated) / Istio (CNCF Graduated)
**Service mesh — know both, deploy one:**
- **Linkerd:** Simpler, lighter, Rust data plane, better performance
- **Istio:** More features, more complex, Envoy data plane
**What service meshes give you:** mTLS everywhere, traffic management, 
  observability (golden signals per service automatically)
**Resources:** linkerd.io (excellent docs), istio.io

#### Tekton (CNCF Graduated)
**Why:** Cloud-native CI/CD that runs IN Kubernetes. GitOps for your pipelines.
**Concepts:** Task, Pipeline, PipelineRun, Trigger, EventListener
**Resources:** tekton.dev

---

### Phase 5 (Weeks 27–36): Leadership Level Tools

#### OpenCost / Kubecost
**Why:** FinOps — allocate Kubernetes costs to teams/namespaces/apps
**Learn:** Deployment → cost allocation views → team showback reports

#### SPIFFE / SPIRE (CNCF Graduated)
**Why:** Workload identity. Every service gets a cryptographic identity.
**What it solves:** "Is this really service-A calling service-B, or an attacker?"
**Use with:** Vault, Envoy, Istio for zero-trust workload auth

---

## The "Golden Path" Technology Stack
*What a senior DevOps/Platform Engineer knows cold*

```
Compute:        Kubernetes (EKS/GKE/AKS) + Karpenter
Networking:     Cilium (CNI) + Istio/Linkerd (mesh) + Nginx/Envoy (ingress)
Registry:       Harbor / ECR + cosign (signing) + Syft (SBOM)
CI/CD:          GitHub Actions / Tekton + ArgoCD (GitOps) + Argo Rollouts
IaC:            Terraform + Terragrunt + Crossplane (K8s-native infra)
Secrets:        HashiCorp Vault + External Secrets Operator
Policy:         OPA + Gatekeeper + Kyverno (alternative)
Security:       Falco (runtime) + Trivy (scanning) + Grype (alt scanner)
Metrics:        Prometheus + Thanos + Grafana + PagerDuty
Logs:           Loki + Grafana / OpenSearch
Traces:         OpenTelemetry → Tempo / Jaeger
FinOps:         Kubecost / OpenCost
Platform:       Backstage (IDP) + Crossplane (self-service infra)
Identity:       SPIFFE/SPIRE + cert-manager
```

---

## Open Source Projects to Contribute To (Career Booster)

| Project | Why Contribute | Difficulty | Good First Issues |
|---------|---------------|------------|-------------------|
| Kubernetes | The biggest signal | Hard | kubernetes/kubernetes (good-first-issue label) |
| Falco | Security hot area | Medium | falcosecurity/falco |
| OpenTelemetry | Growing fast | Medium | open-telemetry/opentelemetry-collector |
| Crossplane | Platform eng | Medium | crossplane/crossplane |
| Backstage | Plugins ecosystem | Easy-Medium | backstage/backstage |
| KEDA | Scalers | Medium | kedacore/keda |
| cert-manager | K8s ecosystem | Medium | cert-manager/cert-manager |

**How to contribute:**
1. Use the project in a lab → find something confusing
2. Improve the docs (easiest PR, still counts)
3. Fix a `good-first-issue` bug
4. Add a feature after discussing in GitHub issue first
5. Present your contribution at the project's community meeting

Even 1 merged PR to a CNCF Graduated project is a resume differentiator.

---

## CNCF Certifications

| Cert | Time to Prep | Cost | Value |
|------|-------------|------|-------|
| CKA | 6 weeks | $395 | Very High |
| CKAD | 4 weeks | $395 | High |
| CKS | 6 weeks | $395 | Very High |
| KCNA | 2 weeks | $250 | Medium |
| KCSA | 4 weeks | $250 | Medium |

**Order:** CKA → CKAD → CKS. Do all three.  
**Prep:** killer.sh (best mock exams), KodeKloud (best labs), 
         Mumshad's Udemy courses (best video content)
