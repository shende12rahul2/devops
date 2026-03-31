# Phase 2: Core DevOps Stack — Depth Over Breadth
**Weeks 5–10 | 240 hours | 40 hrs/week**

> Consultant framing: "I architect and operate container platforms that let engineering teams ship 10x faster with 70% fewer incidents — and I can prove it with DORA metrics."

---

## Phase Checklist

### Week 5 — Docker & Container Internals
- [ ] Lab 5.1: Build containers from scratch using namespaces manually
- [ ] Lab 5.2: Multi-stage Dockerfile optimisation (1GB → 50MB)
- [ ] Lab 5.3: Container security hardening + Trivy scanning
- [ ] Lab 5.4: Docker networking — bridge, overlay, host
- [ ] Lab 5.5: Private registry setup with authentication
- [ ] Project: Production-grade containerised microservices platform

### Week 6 — Kubernetes Core Architecture
- [ ] Lab 6.1: K8s control plane deep dive (kubeadm cluster from scratch)
- [ ] Lab 6.2: Pod scheduling — affinity, taints, tolerations
- [ ] Lab 6.3: ConfigMaps, Secrets, ServiceAccounts
- [ ] Lab 6.4: Services — ClusterIP, NodePort, LoadBalancer, Headless
- [ ] Lab 6.5: PersistentVolumes, StorageClasses, dynamic provisioning
- [ ] Project: Multi-tier production application on Kubernetes

### Week 7 — Kubernetes Security & Advanced Features
- [ ] Lab 7.1: RBAC — full implementation with least privilege
- [ ] Lab 7.2: Network Policies — zero-trust pod networking
- [ ] Lab 7.3: HPA, VPA, Cluster Autoscaler setup
- [ ] Lab 7.4: Helm chart authoring from scratch
- [ ] Lab 7.5: ArgoCD GitOps deployment pipeline
- [ ] Project: Secure, auto-scaling production K8s cluster

### Week 8 — CI/CD Pipeline Engineering
- [ ] Lab 8.1: GitHub Actions — reusable workflows + matrix builds
- [ ] Lab 8.2: Build a full pipeline: test → scan → build → sign → deploy
- [ ] Lab 8.3: Canary deployment with automated rollback
- [ ] Lab 8.4: Feature flags with LaunchDarkly / Flagsmith
- [ ] Lab 8.5: Pipeline performance — caching, parallelism
- [ ] Project: Enterprise CI/CD Platform

### Week 9 — Infrastructure as Code (Terraform + Ansible)
- [ ] Lab 9.1: Terraform modules — reusable, versioned
- [ ] Lab 9.2: Remote state with locking (S3 + DynamoDB)
- [ ] Lab 9.3: Terragrunt for DRY multi-env IaC
- [ ] Lab 9.4: Ansible roles with molecule testing
- [ ] Lab 9.5: Policy as Code with Sentinel / OPA
- [ ] Project: Multi-environment AWS infrastructure platform

### Week 10 — Cloud Architecture & AWS Deep Dive
- [ ] Lab 10.1: VPC design — multi-AZ, private/public subnets, NAT
- [ ] Lab 10.2: IAM — roles, SCPs, permission boundaries
- [ ] Lab 10.3: EKS cluster with Karpenter autoscaler
- [ ] Lab 10.4: CloudWatch → Prometheus federation
- [ ] Lab 10.5: AWS Well-Architected review of your project
- [ ] Project: Production AWS multi-account architecture

---

## 🏗️ Enterprise Projects

### Project 5: Production Containerised Microservices Platform
**Duration:** Weeks 5–6 (Saturday deep work sessions)  
**Business Problem:** An e-commerce company's monolith is slowing them down — 1 deploy/week, 4-hour deployment windows, any change risks the whole app. Your job: containerise and orchestrate 5 microservices.

**Architecture:**
```
internet → nginx-ingress → [user-service, product-service, order-service, 
                            payment-service, notification-service]
                         ↓
                    [PostgreSQL, Redis, RabbitMQ]
```

**Deliverables:**
```
microservices-platform/
├── services/
│   ├── user-service/
│   │   ├── Dockerfile                 # Multi-stage, distroless, <20MB
│   │   ├── .dockerignore
│   │   └── health/health.go           # /health and /ready endpoints
│   ├── product-service/
│   ├── order-service/
│   ├── payment-service/
│   └── notification-service/
├── k8s/
│   ├── namespaces/
│   ├── deployments/
│   ├── services/
│   ├── ingress/
│   ├── configmaps/
│   ├── secrets/                       # External Secrets Operator refs
│   ├── rbac/
│   ├── network-policies/
│   └── hpa/
├── helm/
│   └── platform-chart/               # Single chart, values per env
├── compose/
│   └── docker-compose.yml            # Local dev only
└── docs/
    ├── architecture.md
    ├── runbook.md
    └── business-impact.md            # REQUIRED: quantify the improvement
```

**Technical requirements — non-negotiable:**
- All images < 50MB (multi-stage builds)
- Resource requests AND limits on every container
- Liveness and readiness probes on every deployment
- Network policies: deny all → explicit allow
- RBAC: dedicated ServiceAccount per service, no default SA
- Secrets via External Secrets Operator (not plain K8s secrets)
- HPA on all services (min 2, max 10 replicas)
- PodDisruptionBudget on all services

**CNCF Tools used:**
- Kubernetes, Helm, ArgoCD, External Secrets Operator, cert-manager

**Business Impact template:**
```markdown
## Business Impact
- Deployment frequency: 1/week → 20/day
- Lead time for changes: 3 days → 45 minutes
- MTTR: 4 hours → 12 minutes  
- Change failure rate: 15% → 2%
- Environment provisioning: 2 days → 8 minutes
```

---

### Project 6: Enterprise CI/CD Platform
**Duration:** Week 8 (intensive)  
**Business Problem:** 50 engineers, 20 repositories, no standard pipeline. Some repos deploy manually via SSH. Others have half-written GitHub Actions. Security team finds secrets in git history every month.

**What you build:**

```
ci-cd-platform/
├── .github/
│   ├── workflows/
│   │   ├── reusable-build.yml         # Shared build workflow
│   │   ├── reusable-test.yml          # Shared test workflow  
│   │   ├── reusable-security-scan.yml # Trivy + Semgrep + Gitleaks
│   │   ├── reusable-deploy.yml        # Argo rollouts integration
│   │   └── reusable-notify.yml        # Slack/PagerDuty notification
│   └── composite-actions/
│       ├── setup-tools/               # Install standard toolchain
│       ├── docker-build-push/         # Build + push + sign with cosign
│       └── deploy-and-verify/         # Deploy + smoke test + rollback
├── pipelines/
│   ├── microservice-pipeline.yml      # Template for any microservice
│   ├── library-pipeline.yml           # For shared libraries
│   └── infrastructure-pipeline.yml    # For Terraform changes
├── deployment-strategies/
│   ├── blue-green/
│   │   ├── switch.sh                  # Traffic switch script
│   │   └── rollback.sh
│   ├── canary/
│   │   ├── argo-rollout.yaml          # Argo Rollouts definition
│   │   └── analysis-template.yaml     # Automated canary analysis
│   └── feature-flags/
│       └── flagsmith-config.yml
├── security/
│   ├── sbom-generation.yml            # Syft SBOM in pipeline
│   ├── slsa-provenance.yml            # SLSA level 2 provenance
│   └── image-signing.yml             # cosign with OIDC (keyless)
└── docs/
    ├── pipeline-standards.md          # The "golden path"
    ├── onboarding.md                  # How to adopt this pipeline
    └── security-gates.md             # What gets blocked and why
```

**The pipeline must block deploys when:**
- Any critical or high CVE in container image
- Secrets found in code (Gitleaks)
- SAST high-severity findings (Semgrep)
- Tests fail
- Image not signed with cosign

**CNCF Tools:** Tekton (alternative to GHA), Argo Rollouts, cosign, Syft, Grype

---

### Project 7: Multi-Environment AWS Infrastructure Platform
**Duration:** Week 9–10  
**Business Problem:** Startup scaled from 1 to 50 engineers. Infrastructure is manual clicks in AWS console. No consistency between dev, staging, prod. No audit trail. Ops spends 40% of time on environment provisioning.

```
aws-infra-platform/
├── modules/
│   ├── vpc/                           # Reusable VPC module
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   └── README.md
│   ├── eks/                           # EKS cluster module
│   ├── rds/                           # RDS with Multi-AZ
│   ├── elasticache/                   # Redis cluster
│   └── iam-roles/                     # Standard role templates
├── accounts/
│   ├── management/                    # AWS Organizations root
│   ├── dev/
│   │   └── terragrunt.hcl
│   ├── staging/
│   │   └── terragrunt.hcl
│   └── prod/
│       └── terragrunt.hcl
├── environments/
│   ├── base.hcl                       # Shared config (provider, state)
│   ├── dev/
│   │   ├── vpc/
│   │   ├── eks/
│   │   └── rds/
│   ├── staging/
│   └── prod/
├── policies/
│   ├── sentinel/
│   │   ├── require-tags.sentinel      # Enforce tagging policy
│   │   ├── restrict-regions.sentinel  # Only allowed regions
│   │   └── cost-limits.sentinel       # Block expensive resources
│   └── opa/
│       └── terraform-policies/
├── scripts/
│   ├── new-environment.sh             # Provision a full env in 1 command
│   └── destroy-environment.sh        # Safe teardown with checks
└── docs/
    ├── account-structure.md
    ├── tagging-strategy.md
    └── cost-allocation.md
```

**VPC design (enterprise-grade):**
```
Production VPC (10.0.0.0/16)
├── Public Subnets (10.0.1.0/24, 10.0.2.0/24, 10.0.3.0/24)
│   └── ALB, NAT Gateways, Bastion (session manager preferred)
├── Private App Subnets (10.0.11.0/24, 10.0.12.0/24, 10.0.13.0/24)
│   └── EKS nodes, ECS tasks, Lambda
└── Private Data Subnets (10.0.21.0/24, 10.0.22.0/24, 10.0.23.0/24)
    └── RDS Multi-AZ, ElastiCache, MSK
```

---

## 📋 Labs

### Week 5 Labs — Docker

**Lab 5.1 — Container from Scratch (Mon evening, 2.5h)**
```bash
# Build a container WITHOUT Docker to understand what Docker does
# Step 1: Create a filesystem
mkdir mycontainer/{bin,lib,lib64,proc,sys}
cp /bin/bash mycontainer/bin/
# Copy bash dependencies
ldd /bin/bash | grep -o '/lib[^ ]*' | xargs -I{} cp {} mycontainer/lib/

# Step 2: Create namespace manually
sudo unshare --pid --net --mount --fork \
  chroot mycontainer /bin/bash

# Inside: you have a new PID namespace, you are PID 1
# This is what Docker does, with many more features

# Lab output: write a 1-page explanation of what you learned
```

**Lab 5.2 — Image Optimisation Challenge (Tue evening)**
```dockerfile
# Start: build a Python Flask app image (typically ~800MB)
FROM python:3.11
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py .
CMD ["python", "app.py"]

# Your challenge: get this below 30MB using multi-stage + distroless
# Hints: python:3.11-slim, gcr.io/distroless/python3, strip unused deps
# Measure: docker image ls | grep myapp
# Document: each step and MB saved

# Target output: <30MB production image with full security scan passing
```

**Lab 5.3 — Security Hardening (Wed evening)**
```bash
# Before: typical vulnerable container setup
docker run -d \
  --privileged \           # NEVER in prod
  -v /:/host \            # NEVER in prod
  -e DATABASE_PASSWORD=prod_password \  # NEVER plain text
  myapp

# After: hardened setup — build this
docker run -d \
  --read-only \
  --tmpfs /tmp \
  --tmpfs /var/run \
  --cap-drop ALL \
  --cap-add NET_BIND_SERVICE \
  --security-opt no-new-privileges \
  --security-opt seccomp=./seccomp-profile.json \
  --user 1000:1000 \
  --memory 256m \
  --cpus 0.5 \
  myapp

# Run Trivy: trivy image myapp
# Fix all CRITICAL and HIGH CVEs
# Document: before/after vulnerability count
```

**Lab 5.4 — Docker Networking Lab (Thu evening)**
```bash
# Build a 3-tier app to understand container networking
# Create: custom bridge networks (not default)
docker network create --driver bridge frontend-net
docker network create --driver bridge backend-net

# Rule: frontend can talk to app. App can talk to db. Frontend CANNOT talk to db.
# Implement this with container network assignments
# Test: docker exec frontend curl http://database  # must fail
# Test: docker exec frontend curl http://app       # must succeed
# Test: docker exec app curl http://database       # must succeed
```

**Lab 5.5 — Private Registry (Fri morning)**
```bash
# Set up Harbor (enterprise registry) locally
# Harbor gives you: vulnerability scanning, RBAC, image signing, replication

docker-compose -f harbor/docker-compose.yml up -d
# Configure: OIDC auth, project RBAC, Trivy scanner
# Push: your hardened image from Lab 5.3
# Set: block policy (block deploy of HIGH+ CVE images)
```

*(Labs for weeks 6–10 in `/labs/week*/` directories)*

---

## 🎤 Interview Prep

### Week 5 — Docker (Top 5)

**Q1. What happens when you run `docker run nginx`?**
```
1. Docker CLI → Docker daemon (dockerd) via REST API
2. dockerd checks: is nginx:latest in local image cache?
3. If not: pull from configured registry (Docker Hub default)
   - Download manifest → download layers in parallel
   - Each layer is a tar archive, stored in overlay2 dir
4. Create container: 
   - Allocate new cgroup (cpu, memory)
   - Create new namespaces (PID, NET, MNT, UTS, IPC)
   - Set up overlay2 filesystem (read-only layers + writable layer)
   - Configure veth pair for networking (connects to docker0 bridge)
5. Execute ENTRYPOINT/CMD (nginx -g 'daemon off;') as PID 1
6. Container is running
```

**Q2. How do you debug a container that keeps crashing?**
```
Step 1: kubectl describe pod <name> → check Events section first
Step 2: kubectl logs <pod> --previous → logs from crashed container
Step 3: Check exit code: 137 = OOMKilled, 1 = application error, 
        139 = SIGSEGV, 143 = SIGTERM
Step 4: If OOMKilled: check memory limits, increase if needed, 
        or find the memory leak
Step 5: kubectl exec -it <pod> -- sh → if it's alive long enough
Step 6: Debug with ephemeral container: 
        kubectl debug -it <pod> --image=busybox --target=mycontainer
Step 7: If image itself broken: docker run -it --entrypoint sh myimage
```

**Q3. Explain Docker layer caching and how to optimise it.**
```
Each instruction in Dockerfile = one layer. Layers are cached by content hash.
If a layer changes, ALL subsequent layers are invalidated.

Anti-pattern (slow builds):
COPY . .                           # Cache busted on ANY file change
RUN pip install -r requirements.txt  # Re-runs even if deps unchanged

Optimised:
COPY requirements.txt .            # Only changes when deps change  
RUN pip install -r requirements.txt  # Cached unless requirements.txt changes
COPY . .                           # Application code (changes frequently)

Rule: Order from least-changing to most-changing.
Further optimisation: BuildKit cache mounts for package managers:
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt
This persists the pip cache between builds without committing to image.
```

**Q4. What is the difference between ENTRYPOINT and CMD?**
```
ENTRYPOINT: the process that runs (hard to override, needs --entrypoint flag)
CMD: default arguments passed to ENTRYPOINT (easily overridden)

exec form (JSON array): doesn't invoke shell, receives signals properly
  ENTRYPOINT ["nginx"]    CMD ["-g", "daemon off;"]
shell form (string): runs via /bin/sh -c, signals go to shell not process
  CMD nginx -g 'daemon off;'     ← BAD: nginx won't receive SIGTERM

Best practice:
ENTRYPOINT ["nginx"]              # The process
CMD ["-g", "daemon off;"]         # Overridable defaults

docker run myimage -g 'daemon on;'   # Replaces CMD only
docker run --entrypoint /bin/sh myimage  # Replaces ENTRYPOINT

Common gotcha: using shell form = containers that don't handle signals.
Result: 30-second SIGKILL wait during every rolling deployment.
```

**Q5. How do you implement zero-downtime deployments for a containerised app?**
```
Multiple layers:
1. Container level: graceful shutdown
   - Handle SIGTERM: finish in-flight requests, then exit
   - Set terminationGracePeriodSeconds appropriately (>0!)
   - Add preStop hook if app needs warning before SIGTERM:
     lifecycle:
       preStop:
         exec:
           command: ["sleep", "5"]

2. Kubernetes level: rolling update
   - strategy: RollingUpdate
     maxSurge: 1           # Add 1 new pod before removing old
     maxUnavailable: 0     # Never remove until new is ready
   - Proper readiness probe (only Ready when actually ready)
   - PodDisruptionBudget: minAvailable: 1

3. Load balancer level:
   - K8s removes pod from Service endpoints BEFORE sending SIGTERM
   - But: existing connections still drain. Set connection draining timeout.

4. Application level:
   - Stateless design (no local state to lose)
   - Idempotent operations (safe to retry)
   - Feature flags for risky changes (decouple deploy from release)
```

*(Full 20 questions for weeks 5–10 in `/interview-prep/` files)*

---

## 🔗 CNCF Tools — Phase 2

| Tool | Graduation Status | Learn By Week | Resource |
|------|-----------------|---------------|----------|
| Kubernetes | Graduated | 6 | kubernetes.io/docs |
| Helm | Graduated | 7 | helm.sh/docs |
| ArgoCD | Graduated | 7 | argo-cd.readthedocs.io |
| Flux | Graduated | 7 | fluxcd.io |
| Harbor | Graduated | 5 | goharbor.io |
| Tekton | Graduated | 8 | tekton.dev |
| Argo Rollouts | Incubating | 8 | argoproj.github.io/argo-rollouts |
| Falco | Graduated | 9 | falco.org |
| OPA | Graduated | 9 | openpolicyagent.org |

---

## 📚 References — Phase 2

| Resource | Focus | Priority |
|----------|-------|----------|
| Kubernetes in Action (Luksa) | K8s fundamentals | Must read |
| Programming Kubernetes | K8s operators + CRDs | Week 6-7 |
| Terraform: Up & Running | IaC patterns | Week 9 |
| Cloud Native Patterns | Distributed systems | Week 10 |
| AWS Well-Architected | Cloud design | Week 10 |
| CNCF Annual Survey | Industry benchmarks | Skim weekly |
