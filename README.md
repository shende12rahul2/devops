# 🚀 DevOps Mastery — From Practitioner to Consultant

> **Goal:** Crack senior/staff-level DevOps/SRE/Platform Engineering roles at top-tier companies  
> **Duration:** 36 weeks · 40 hrs/week · 1440 total hours  
> **Approach:** Consultant mindset from Week 1 — every lab produces a deliverable, every project solves a real business problem

---

## 📐 Repository Structure

```
devops-mastery/
├── phase-01-foundations/          # Weeks 1–4: Linux, Networking, Git, Communication
│   ├── labs/                      # Daily 45-min hands-on labs
│   ├── projects/                  # Enterprise-grade projects
│   ├── interview-prep/            # Weekly Q&A with model answers
│   └── notes/                     # Concept summaries + references
├── phase-02-core-devops/          # Weeks 5–10: Docker, K8s, CI/CD, IaC, Cloud
├── phase-03-enterprise/           # Weeks 11–18: Security, Observability, SRE, FinOps
├── phase-04-architecture/         # Weeks 19–26: System Design, Platform Eng, MLOps
├── phase-05-leadership/           # Weeks 27–36: Team Mgmt, Communication, Culture
├── resources/
│   ├── cncf-tools/                # CNCF landscape tools — what to learn & why
│   ├── references/                # Books, papers, RFCs, post-mortems
│   └── cheatsheets/               # Quick-reference cards for every tool
├── tracker/                       # Streamlit progress tracker app
├── scripts/                       # Automation scripts for labs & setup
└── docs/                          # Architecture diagrams & design docs
```

---

## 🗺️ Roadmap at a Glance

| Phase | Weeks | Hours | Focus | Milestone |
|-------|-------|-------|-------|-----------|
| 1 · Foundations | 1–4 | 160h | Linux, Networking, Git, Mindset | Sysadmin toolkit on GitHub |
| 2 · Core DevOps | 5–10 | 240h | Docker, K8s, CI/CD, IaC, Cloud | Production-grade app deployed |
| 3 · Enterprise | 11–18 | 320h | DevSecOps, Observability, SRE, FinOps | Secure pipeline + SLO dashboard |
| 4 · Architecture | 19–26 | 320h | System Design, Platform Eng, MLOps | Internal Developer Platform |
| 5 · Leadership | 27–36 | 400h | Team Mgmt, Communication, Culture | Conference talk draft + blog series |

**Total: 1440 hours of focused, deliberate practice**

---

## 🧠 The Consultant Mindset (Start Week 1)

Every single thing you build should answer: **"What business problem does this solve?"**

| Engineer Thinks | Consultant Thinks |
|-----------------|-------------------|
| "I set up monitoring" | "I reduced MTTR from 45min to 8min, saving $12k/month in incident cost" |
| "I containerised the app" | "I reduced deployment failures by 70% and cut environment setup from 2 days to 15 minutes" |
| "I wrote Terraform" | "I enabled 3 teams to self-serve infrastructure, freeing the platform team for higher-leverage work" |
| "I set up RBAC" | "I reduced the attack surface by eliminating 40 over-privileged service accounts" |

**Rule:** Every project README must contain a "Business Impact" section. No exceptions.

---

## 📅 Weekly Schedule (40 hrs/week)

```
Monday–Friday:
  06:00–07:30  Theory + reading (1.5h)
  07:30–09:00  Work prep / commute
  [Work Day]
  20:00–22:30  Hands-on lab / project (2.5h)

Saturday:
  08:00–14:00  Deep project work (6h)
  15:00–17:00  Interview prep + mock answers (2h)
  18:00–19:00  Review + planning (1h)

Sunday:
  09:00–11:00  Weekly review + blog/LinkedIn post (2h)
  11:00–12:00  Next-week planning (1h)

Total: (1.5+2.5)×5 + 9 + 3 = 32 weekday + 12 weekend = ~40 hrs
```

---

## 🛠️ CNCF Tool Stack (Learn These — In Order)

### Tier 1 — Must Know (Interviews will test these)
- **Kubernetes** (CKA/CKAD/CKS certified)
- **Prometheus + Alertmanager** (metrics)
- **Grafana** (dashboards)
- **Helm** (package management)
- **ArgoCD / Flux** (GitOps)
- **Istio / Linkerd** (service mesh)
- **Open Policy Agent (OPA)** (policy as code)

### Tier 2 — Differentiators (Senior+ roles)
- **OpenTelemetry** (unified observability)
- **Falco** (runtime security)
- **Crossplane** (infrastructure as code via K8s)
- **KEDA** (event-driven autoscaling)
- **Cilium** (eBPF networking)
- **Backstage** (Internal Developer Portal)
- **Tekton** (K8s-native CI/CD)

### Tier 3 — Emerging (Future-proof)
- **KubeVirt** (VMs in Kubernetes)
- **Kubeflow** (ML pipelines)
- **OpenCost / Kubecost** (cloud cost)
- **SPIFFE/SPIRE** (workload identity)

See `resources/cncf-tools/` for deep dives on each.

---

## 📊 Progress Tracking

Run the Streamlit tracker locally:

```bash
cd tracker/
pip install -r requirements.txt
streamlit run app.py
```

Opens at `http://localhost:8501`

---

## 🎯 Interview Preparation

Each phase has a dedicated `interview-prep/` folder with:
- 20+ questions per week with full model answers
- System design problems with worked solutions
- Behavioral questions with STAR-format answers
- Live scenario walkthroughs (incidents, postmortems)

---

## 📚 Core References

| Type | Resource | Why |
|------|----------|-----|
| Book | The Phoenix Project | DevOps culture foundation |
| Book | Site Reliability Engineering (Google) | SRE principles — free online |
| Book | The DevOps Handbook | Process & measurement |
| Book | Designing Distributed Systems | Patterns every senior needs |
| Book | The Manager's Path | Leadership ladder |
| Paper | Google SRE Workbook | Practical implementation |
| RFC | RFC 793 (TCP) | You'll be asked |
| Postmortem | GitHub's 2018 outage | Real incident analysis |
| Postmortem | Cloudflare's BGP incident | Networking depth |

---

## 🏆 Certification Path

```
Month 1-2:  CKA (Certified Kubernetes Administrator)
Month 2-3:  CKAD (Certified Kubernetes Application Developer)  
Month 3-4:  CKS (Certified Kubernetes Security Specialist)
Month 4-5:  AWS Solutions Architect Professional (or GCP DevOps Engineer)
Month 5-6:  HashiCorp Terraform Associate + Vault Associate
```

---

## 🤝 Contributing / Tracking Progress

Each completed lab/project: add `[x]` to the checklist in the relevant phase README.  
Each completed week: update `tracker/progress.json` or use the Streamlit app.  
Each interview answer you've practiced: mark in `interview-prep/` files.

---

*Built for: Rahul Shende | 8 years DevOps experience | Target: Senior/Staff/Principal roles*  
*Philosophy: Learn in public. Build real things. Think like a consultant.*
