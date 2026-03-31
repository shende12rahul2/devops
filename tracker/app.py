import streamlit as st
import json
import os
from datetime import datetime, date, timedelta
from pathlib import Path
import random

# ─── Config ───────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="DevOps Mastery Tracker",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

DATA_FILE = Path(__file__).parent / "progress.json"

# ─── Data Schema ──────────────────────────────────────────────────────────────
DEFAULT_DATA = {
    "profile": {
        "name": "Rahul Shende",
        "start_date": str(date.today()),
        "target_role": "Senior/Staff DevOps Engineer",
        "current_week": 1,
        "streak_days": 0,
        "last_activity": str(date.today()),
        "total_hours_logged": 0.0,
        "github_url": "https://github.com/shende12rahul2/devops"
    },
    "phases": {
        "phase_1": {
            "name": "Foundations & Mindset",
            "weeks": "1-4",
            "total_hours": 160,
            "color": "#4F46E5",
            "weeks_data": {
                "week_1": {
                    "topic": "Linux Deep Dive",
                    "hours_target": 40,
                    "hours_logged": 0,
                    "labs": {
                        "1.1 Permission hardening audit script": False,
                        "1.2 Systemd service creation": False,
                        "1.3 Production bash script (error handling)": False,
                        "1.4 Network troubleshooting toolkit": False,
                        "1.5 Kernel parameter tuning": False
                    },
                    "project": {
                        "name": "Enterprise Linux Sysadmin Toolkit v1.0",
                        "completed": False,
                        "github_url": "",
                        "business_impact": ""
                    },
                    "interview_prep": {
                        "Q1 99% CPU diagnosis walkthrough": False,
                        "Q2 Hard link vs soft link": False,
                        "Q3 Linux process scheduler (CFS)": False,
                        "Q4 cgroups v2 + Kubernetes connection": False,
                        "Q5 Disk full — exact steps": False,
                        "Q6 File descriptors + 'too many open files'": False,
                        "Q7 SIGTERM vs SIGKILL + graceful shutdown": False,
                        "Q8 Virtual memory + swap strategy": False,
                        "Q9 Nice values + real-time scheduling": False,
                        "Q10 SELinux/AppArmor in production": False,
                        "Q11 Behavioral: production incident STAR": False,
                        "Q12 Performance tuning methodology": False,
                        "Q13 'Everything is a file' explanation": False,
                        "Q14 New server provisioning walkthrough": False,
                        "Q15 inode exhaustion diagnosis": False,
                        "Q16 Memory leak identification": False,
                        "Q17 Boot process (BIOS to shell)": False,
                        "Q18 Process vs thread": False,
                        "Q19 Kernel scheduling deep dive": False,
                        "Q20 STAR: time I improved system performance": False
                    },
                    "morning_sessions": 0,
                    "evening_sessions": 0,
                    "notes": "",
                    "week_rating": 0,
                    "completed": False
                },
                "week_2": {
                    "topic": "Networking Mastery",
                    "hours_target": 40,
                    "hours_logged": 0,
                    "labs": {
                        "2.1 TCP/IP deep dive with tcpdump": False,
                        "2.2 DNS resolution tracing + health checker": False,
                        "2.3 HAProxy load balancer setup": False,
                        "2.4 iptables firewall ruleset": False,
                        "2.5 WireGuard VPN server": False
                    },
                    "project": {
                        "name": "Network Diagnostic & Monitoring Suite",
                        "completed": False,
                        "github_url": "",
                        "business_impact": ""
                    },
                    "interview_prep": {
                        "Q1 google.com in browser — full technical": False,
                        "Q2 TCP 3-way handshake + TIME_WAIT": False,
                        "Q3 HTTPS/TLS handshake deep dive": False,
                        "Q4 L4 vs L7 load balancing": False,
                        "Q5 DNS authoritative vs recursive": False,
                        "Q6 BGP basics (enterprise networking)": False,
                        "Q7 CDN how it works": False,
                        "Q8 TCP vs UDP — when to use each": False,
                        "Q9 Network packet loss diagnosis": False,
                        "Q10 VPN protocols comparison": False,
                        "Q11 VLAN and network segmentation": False,
                        "Q12 HTTP/2 vs HTTP/3 differences": False,
                        "Q13 NAT types and implications": False,
                        "Q14 BEHAVIORAL: network incident I led": False,
                        "Q15 Zero-downtime DNS cutover": False,
                        "Q16 Rate limiting strategies": False,
                        "Q17 WebSocket vs HTTP connection": False,
                        "Q18 Firewall rules — design approach": False,
                        "Q19 Network monitoring golden signals": False,
                        "Q20 STAR: time I prevented network incident": False
                    },
                    "morning_sessions": 0,
                    "evening_sessions": 0,
                    "notes": "",
                    "week_rating": 0,
                    "completed": False
                },
                "week_3": {
                    "topic": "Git & Collaboration at Scale",
                    "hours_target": 40,
                    "hours_logged": 0,
                    "labs": {
                        "3.1 Git internals — objects, trees, commits": False,
                        "3.2 Advanced merge strategies + conflict resolution": False,
                        "3.3 Git hooks for automated quality gates": False,
                        "3.4 Trunk-based development workflow": False,
                        "3.5 GitOps repo structure design": False
                    },
                    "project": {
                        "name": "Enterprise Git Workflow System",
                        "completed": False,
                        "github_url": "",
                        "business_impact": ""
                    },
                    "interview_prep": {
                        "Q1 git rebase vs merge — when to use each": False,
                        "Q2 git bisect for bug hunting": False,
                        "Q3 git reflog — recover lost commits": False,
                        "Q4 Branching strategies comparison": False,
                        "Q5 Trunk-based development trade-offs": False,
                        "Q6 Conventional commits + semantic versioning": False,
                        "Q7 Git hooks — what you use in prod": False,
                        "Q8 Monorepo vs polyrepo strategy": False,
                        "Q9 BEHAVIORAL: secrets in git history incident": False,
                        "Q10 Code review best practices": False,
                        "Q11 Git submodules vs subtrees": False,
                        "Q12 Large file storage (Git LFS)": False,
                        "Q13 GitOps vs traditional deployment": False,
                        "Q14 STAR: improved team git workflow": False,
                        "Q15 Squash merge strategy": False
                    },
                    "morning_sessions": 0,
                    "evening_sessions": 0,
                    "notes": "",
                    "week_rating": 0,
                    "completed": False
                },
                "week_4": {
                    "topic": "Communication & Python Automation",
                    "hours_target": 40,
                    "hours_logged": 0,
                    "labs": {
                        "4.1 Python sysadmin automation scripts": False,
                        "4.2 REST API interaction + error handling": False,
                        "4.3 JSON/YAML parsing + manipulation": False,
                        "4.4 Cron job automation with alerting": False,
                        "4.5 Documentation-as-code with diagrams": False
                    },
                    "project": {
                        "name": "Infrastructure Automation Suite v1.0",
                        "completed": False,
                        "github_url": "",
                        "business_impact": ""
                    },
                    "interview_prep": {
                        "Q1 Production bash script standards": False,
                        "Q2 Python vs bash — when to use each": False,
                        "Q3 API rate limiting + retry strategies": False,
                        "Q4 YAML anchors + aliases": False,
                        "Q5 Idempotency in automation scripts": False,
                        "Q6 STAR: automated a manual process — ROI": False,
                        "Q7 Error handling patterns": False,
                        "Q8 Structured logging standards": False,
                        "Q9 Script security — injection prevention": False,
                        "Q10 Testing infrastructure code": False,
                        "Q11 Documentation as code tools": False,
                        "Q12 Explain tech to non-technical audience": False,
                        "Q13 On-call runbook writing": False,
                        "Q14 STAR: communication improved a project": False,
                        "Q15 10 STAR stories prepared": False
                    },
                    "morning_sessions": 0,
                    "evening_sessions": 0,
                    "notes": "",
                    "week_rating": 0,
                    "completed": False
                }
            }
        },
        "phase_2": {
            "name": "Core DevOps Stack",
            "weeks": "5-10",
            "total_hours": 240,
            "color": "#0891B2",
            "weeks_data": {
                "week_5": {"topic": "Docker & Container Internals", "hours_target": 40, "hours_logged": 0, "labs": {"5.1 Container from scratch (namespaces)": False, "5.2 Multi-stage build optimisation (1GB → 50MB)": False, "5.3 Container security hardening + Trivy": False, "5.4 Docker networking (bridge, overlay, host)": False, "5.5 Private registry (Harbor) setup": False}, "project": {"name": "Production Containerised Microservices Platform", "completed": False, "github_url": "", "business_impact": ""}, "interview_prep": {"Q1 docker run nginx — what happens": False, "Q2 Debug crashing container": False, "Q3 Layer caching optimisation": False, "Q4 ENTRYPOINT vs CMD": False, "Q5 Zero-downtime container deployment": False, "Q6 Container namespaces deep dive": False, "Q7 cgroups in containers": False, "Q8 Docker networking modes": False, "Q9 Image security scanning": False, "Q10 Multi-stage build strategy": False, "Q11 Docker registry — pull/push mechanics": False, "Q12 Container runtime (containerd)": False, "Q13 OCI spec": False, "Q14 STAR: containerisation project impact": False, "Q15 Rootless containers": False}, "morning_sessions": 0, "evening_sessions": 0, "notes": "", "week_rating": 0, "completed": False},
                "week_6": {"topic": "Kubernetes Core Architecture", "hours_target": 40, "hours_logged": 0, "labs": {"6.1 kubeadm cluster from scratch": False, "6.2 Pod scheduling — affinity, taints, tolerations": False, "6.3 ConfigMaps, Secrets, ServiceAccounts": False, "6.4 Services — all 4 types": False, "6.5 PVs, StorageClasses, dynamic provisioning": False}, "project": {"name": "Multi-tier Production App on Kubernetes", "completed": False, "github_url": "", "business_impact": ""}, "interview_prep": {"Q1 kubectl apply — full internal flow": False, "Q2 Pod stuck in CrashLoopBackOff": False, "Q3 Pod stuck in Pending": False, "Q4 etcd role + backup strategy": False, "Q5 Scheduler decision algorithm": False, "Q6 kubelet responsibilities": False, "Q7 kube-proxy modes (iptables vs IPVS)": False, "Q8 CoreDNS in Kubernetes": False, "Q9 Service types and use cases": False, "Q10 StatefulSet vs Deployment": False, "Q11 DaemonSet use cases": False, "Q12 Resource requests vs limits": False, "Q13 QoS classes (Guaranteed, Burstable, BestEffort)": False, "Q14 STAR: K8s migration project": False, "Q15 Rolling update with zero downtime": False}, "morning_sessions": 0, "evening_sessions": 0, "notes": "", "week_rating": 0, "completed": False},
                "week_7": {"topic": "K8s Security + ArgoCD GitOps", "hours_target": 40, "hours_logged": 0, "labs": {"7.1 RBAC full implementation": False, "7.2 Network Policies — zero-trust": False, "7.3 HPA, VPA, Cluster Autoscaler": False, "7.4 Helm chart authoring from scratch": False, "7.5 ArgoCD GitOps pipeline": False}, "project": {"name": "Secure Auto-scaling K8s Cluster", "completed": False, "github_url": "", "business_impact": ""}, "interview_prep": {"Q1 Kubernetes RBAC design": False, "Q2 Secrets management (ESO + Vault)": False, "Q3 Network Policy implementation": False, "Q4 Pod Security Standards": False, "Q5 HPA vs VPA — when to use": False, "Q6 Cluster Autoscaler vs Karpenter": False, "Q7 Helm chart architecture": False, "Q8 GitOps principles (Argo vs Flux)": False, "Q9 OPA/Gatekeeper policies": False, "Q10 Admission webhooks": False, "Q11 Multi-tenant cluster design": False, "Q12 RBAC least privilege implementation": False, "Q13 K8s audit logging": False, "Q14 STAR: security hardening impact": False, "Q15 Supply chain security in K8s": False}, "morning_sessions": 0, "evening_sessions": 0, "notes": "", "week_rating": 0, "completed": False},
                "week_8": {"topic": "CI/CD Pipeline Engineering", "hours_target": 40, "hours_logged": 0, "labs": {"8.1 GitHub Actions reusable workflows": False, "8.2 Full pipeline: test→scan→build→sign→deploy": False, "8.3 Canary deployment with auto-rollback": False, "8.4 Feature flags (Flagsmith)": False, "8.5 Pipeline caching and parallelism": False}, "project": {"name": "Enterprise CI/CD Platform", "completed": False, "github_url": "", "business_impact": ""}, "interview_prep": {"Q1 CI/CD pipeline design for 500 devs": False, "Q2 Deployment strategies comparison": False, "Q3 Pipeline security (SLSA, SBOM, cosign)": False, "Q4 Build time optimisation": False, "Q5 Rollback strategy": False, "Q6 Feature flags — implementation": False, "Q7 Trunk-based dev + CI": False, "Q8 Secrets in pipelines": False, "Q9 Matrix builds": False, "Q10 Pipeline observability": False, "Q11 GitOps vs push-based deploy": False, "Q12 DORA metrics and how to improve": False, "Q13 Pipeline testing (testing the CI)": False, "Q14 STAR: pipeline improvement impact": False, "Q15 Multi-cloud deploy strategy": False}, "morning_sessions": 0, "evening_sessions": 0, "notes": "", "week_rating": 0, "completed": False},
                "week_9": {"topic": "Terraform + IaC at Scale", "hours_target": 40, "hours_logged": 0, "labs": {"9.1 Terraform modules (reusable, versioned)": False, "9.2 Remote state with S3 + DynamoDB locking": False, "9.3 Terragrunt multi-env IaC": False, "9.4 Ansible roles with molecule testing": False, "9.5 Policy as Code (Sentinel/OPA)": False}, "project": {"name": "Multi-environment AWS Infrastructure Platform", "completed": False, "github_url": "", "business_impact": ""}, "interview_prep": {"Q1 Terraform state management": False, "Q2 Terraform module design": False, "Q3 terraform import — existing resources": False, "Q4 Terragrunt vs Terraform workspaces": False, "Q5 IaC testing strategies": False, "Q6 Drift detection and remediation": False, "Q7 Policy as Code implementation": False, "Q8 Ansible idempotency": False, "Q9 Pulumi vs Terraform": False, "Q10 CDK for Terraform (CDKTF)": False, "Q11 Managing secrets in IaC": False, "Q12 Multi-account AWS strategy": False, "Q13 IaC review process": False, "Q14 STAR: IaC transformation project": False, "Q15 Disaster recovery via IaC": False}, "morning_sessions": 0, "evening_sessions": 0, "notes": "", "week_rating": 0, "completed": False},
                "week_10": {"topic": "Cloud Architecture — AWS Deep Dive", "hours_target": 40, "hours_logged": 0, "labs": {"10.1 VPC design (multi-AZ, private/public)": False, "10.2 IAM — roles, SCPs, permission boundaries": False, "10.3 EKS with Karpenter autoscaler": False, "10.4 CloudWatch → Prometheus federation": False, "10.5 AWS Well-Architected review": False}, "project": {"name": "Production AWS Multi-Account Architecture", "completed": False, "github_url": "", "business_impact": ""}, "interview_prep": {"Q1 AWS VPC design (enterprise)": False, "Q2 IAM least privilege + SCPs": False, "Q3 EKS vs self-managed K8s": False, "Q4 AWS networking (Transit Gateway, PrivateLink)": False, "Q5 Multi-account strategy (AWS Organizations)": False, "Q6 Cost optimisation strategies": False, "Q7 Well-Architected 6 pillars": False, "Q8 Spot instances + Karpenter": False, "Q9 RDS vs Aurora + HA strategy": False, "Q10 S3 + lifecycle policies": False, "Q11 CloudFront + WAF": False, "Q12 Route53 routing policies": False, "Q13 Service limits + quota management": False, "Q14 STAR: cloud cost reduction": False, "Q15 Multi-region architecture": False}, "morning_sessions": 0, "evening_sessions": 0, "notes": "", "week_rating": 0, "completed": False}
            }
        },
        "phase_3": {
            "name": "Enterprise Practices",
            "weeks": "11-18",
            "total_hours": 320,
            "color": "#D97706",
            "weeks_data": {
                "week_11": {"topic": "DevSecOps — Shift Left Security", "hours_target": 40, "hours_logged": 0, "labs": {}, "project": {"name": "Secure CI/CD Pipeline with Policy Gates", "completed": False, "github_url": "", "business_impact": ""}, "interview_prep": {}, "morning_sessions": 0, "evening_sessions": 0, "notes": "", "week_rating": 0, "completed": False},
                "week_12": {"topic": "Secrets Management (Vault)", "hours_target": 40, "hours_logged": 0, "labs": {}, "project": {"name": "Enterprise Secrets Management Platform", "completed": False, "github_url": "", "business_impact": ""}, "interview_prep": {}, "morning_sessions": 0, "evening_sessions": 0, "notes": "", "week_rating": 0, "completed": False},
                "week_13": {"topic": "Service Mesh (Istio/Linkerd)", "hours_target": 40, "hours_logged": 0, "labs": {}, "project": {"name": "Zero-Trust Service Mesh Implementation", "completed": False, "github_url": "", "business_impact": ""}, "interview_prep": {}, "morning_sessions": 0, "evening_sessions": 0, "notes": "", "week_rating": 0, "completed": False},
                "week_14": {"topic": "Observability Stack (Prometheus+Grafana+OTel)", "hours_target": 40, "hours_logged": 0, "labs": {}, "project": {"name": "Full Observability Platform", "completed": False, "github_url": "", "business_impact": ""}, "interview_prep": {}, "morning_sessions": 0, "evening_sessions": 0, "notes": "", "week_rating": 0, "completed": False},
                "week_15": {"topic": "SRE — SLOs, Error Budgets, Incidents", "hours_target": 40, "hours_logged": 0, "labs": {}, "project": {"name": "SLO-based Alerting + Error Budget Dashboard", "completed": False, "github_url": "", "business_impact": ""}, "interview_prep": {}, "morning_sessions": 0, "evening_sessions": 0, "notes": "", "week_rating": 0, "completed": False},
                "week_16": {"topic": "Chaos Engineering", "hours_target": 40, "hours_logged": 0, "labs": {}, "project": {"name": "GameDay Chaos Engineering Program", "completed": False, "github_url": "", "business_impact": ""}, "interview_prep": {}, "morning_sessions": 0, "evening_sessions": 0, "notes": "", "week_rating": 0, "completed": False},
                "week_17": {"topic": "FinOps + Cloud Cost Engineering", "hours_target": 40, "hours_logged": 0, "labs": {}, "project": {"name": "Cloud Cost Optimisation Platform", "completed": False, "github_url": "", "business_impact": ""}, "interview_prep": {}, "morning_sessions": 0, "evening_sessions": 0, "notes": "", "week_rating": 0, "completed": False},
                "week_18": {"topic": "Compliance as Code + Audit", "hours_target": 40, "hours_logged": 0, "labs": {}, "project": {"name": "SOC2 Evidence Collection Automation", "completed": False, "github_url": "", "business_impact": ""}, "interview_prep": {}, "morning_sessions": 0, "evening_sessions": 0, "notes": "", "week_rating": 0, "completed": False}
            }
        },
        "phase_4": {
            "name": "Architectural Thinking",
            "weeks": "19-26",
            "total_hours": 320,
            "color": "#16A34A",
            "weeks_data": {
                "week_19": {"topic": "System Design for DevOps", "hours_target": 40, "hours_logged": 0, "labs": {}, "project": {"name": "Design: CI/CD for 1000-person Org", "completed": False, "github_url": "", "business_impact": ""}, "interview_prep": {}, "morning_sessions": 0, "evening_sessions": 0, "notes": "", "week_rating": 0, "completed": False},
                "week_20": {"topic": "Multi-region HA Architecture", "hours_target": 40, "hours_logged": 0, "labs": {}, "project": {"name": "Multi-region Active-Active Deployment", "completed": False, "github_url": "", "business_impact": ""}, "interview_prep": {}, "morning_sessions": 0, "evening_sessions": 0, "notes": "", "week_rating": 0, "completed": False},
                "week_21": {"topic": "Platform Engineering + Backstage", "hours_target": 40, "hours_logged": 0, "labs": {}, "project": {"name": "Internal Developer Platform (IDP)", "completed": False, "github_url": "", "business_impact": ""}, "interview_prep": {}, "morning_sessions": 0, "evening_sessions": 0, "notes": "", "week_rating": 0, "completed": False},
                "week_22": {"topic": "Microservices Patterns + Event-Driven", "hours_target": 40, "hours_logged": 0, "labs": {}, "project": {"name": "Event-Driven Microservices on K8s", "completed": False, "github_url": "", "business_impact": ""}, "interview_prep": {}, "morning_sessions": 0, "evening_sessions": 0, "notes": "", "week_rating": 0, "completed": False},
                "week_23": {"topic": "Kubernetes Operators + CRDs", "hours_target": 40, "hours_logged": 0, "labs": {}, "project": {"name": "Custom Kubernetes Operator", "completed": False, "github_url": "", "business_impact": ""}, "interview_prep": {}, "morning_sessions": 0, "evening_sessions": 0, "notes": "", "week_rating": 0, "completed": False},
                "week_24": {"topic": "Database Reliability Engineering", "hours_target": 40, "hours_logged": 0, "labs": {}, "project": {"name": "Database HA + Backup Automation", "completed": False, "github_url": "", "business_impact": ""}, "interview_prep": {}, "morning_sessions": 0, "evening_sessions": 0, "notes": "", "week_rating": 0, "completed": False},
                "week_25": {"topic": "AI/ML Infrastructure (MLOps)", "hours_target": 40, "hours_logged": 0, "labs": {}, "project": {"name": "ML Pipeline on Kubernetes (Kubeflow)", "completed": False, "github_url": "", "business_impact": ""}, "interview_prep": {}, "morning_sessions": 0, "evening_sessions": 0, "notes": "", "week_rating": 0, "completed": False},
                "week_26": {"topic": "Architecture Review + Portfolio", "hours_target": 40, "hours_logged": 0, "labs": {}, "project": {"name": "Architecture Decision Records (ADR) Portfolio", "completed": False, "github_url": "", "business_impact": ""}, "interview_prep": {}, "morning_sessions": 0, "evening_sessions": 0, "notes": "", "week_rating": 0, "completed": False}
            }
        },
        "phase_5": {
            "name": "Leadership & Communication",
            "weeks": "27-36",
            "total_hours": 400,
            "color": "#DC2626",
            "weeks_data": {
                "week_27": {"topic": "Engineering Leadership Fundamentals", "hours_target": 40, "hours_logged": 0, "labs": {}, "project": {"name": "Team Health Framework", "completed": False, "github_url": "", "business_impact": ""}, "interview_prep": {}, "morning_sessions": 0, "evening_sessions": 0, "notes": "", "week_rating": 0, "completed": False},
                "week_28": {"topic": "Mentoring + Technical Bar-Raising", "hours_target": 40, "hours_logged": 0, "labs": {}, "project": {"name": "Mentoring Framework + Interview Rubric", "completed": False, "github_url": "", "business_impact": ""}, "interview_prep": {}, "morning_sessions": 0, "evening_sessions": 0, "notes": "", "week_rating": 0, "completed": False},
                "week_29": {"topic": "Executive Communication", "hours_target": 40, "hours_logged": 0, "labs": {}, "project": {"name": "Quarterly Platform Review Presentation", "completed": False, "github_url": "", "business_impact": ""}, "interview_prep": {}, "morning_sessions": 0, "evening_sessions": 0, "notes": "", "week_rating": 0, "completed": False},
                "week_30": {"topic": "DevOps Culture + Change Management", "hours_target": 40, "hours_logged": 0, "labs": {}, "project": {"name": "DevOps Transformation Roadmap", "completed": False, "github_url": "", "business_impact": ""}, "interview_prep": {}, "morning_sessions": 0, "evening_sessions": 0, "notes": "", "week_rating": 0, "completed": False},
                "week_31": {"topic": "DORA Metrics + Engineering Effectiveness", "hours_target": 40, "hours_logged": 0, "labs": {}, "project": {"name": "DORA Metrics Dashboard", "completed": False, "github_url": "", "business_impact": ""}, "interview_prep": {}, "morning_sessions": 0, "evening_sessions": 0, "notes": "", "week_rating": 0, "completed": False},
                "week_32": {"topic": "On-Call + Incident Management Culture", "hours_target": 40, "hours_logged": 0, "labs": {}, "project": {"name": "On-Call Programme Design", "completed": False, "github_url": "", "business_impact": ""}, "interview_prep": {}, "morning_sessions": 0, "evening_sessions": 0, "notes": "", "week_rating": 0, "completed": False},
                "week_33": {"topic": "Open Source + Community", "hours_target": 40, "hours_logged": 0, "labs": {}, "project": {"name": "First OSS Contribution Merged", "completed": False, "github_url": "", "business_impact": ""}, "interview_prep": {}, "morning_sessions": 0, "evening_sessions": 0, "notes": "", "week_rating": 0, "completed": False},
                "week_34": {"topic": "Interview Intensive — Mock Rounds", "hours_target": 40, "hours_logged": 0, "labs": {}, "project": {"name": "10 Mock Interviews Completed", "completed": False, "github_url": "", "business_impact": ""}, "interview_prep": {}, "morning_sessions": 0, "evening_sessions": 0, "notes": "", "week_rating": 0, "completed": False},
                "week_35": {"topic": "Portfolio Polish + LinkedIn", "hours_target": 40, "hours_logged": 0, "labs": {}, "project": {"name": "Portfolio Blog + LinkedIn Optimised", "completed": False, "github_url": "", "business_impact": ""}, "interview_prep": {}, "morning_sessions": 0, "evening_sessions": 0, "notes": "", "week_rating": 0, "completed": False},
                "week_36": {"topic": "Final Review + Job Application Sprint", "hours_target": 40, "hours_logged": 0, "labs": {}, "project": {"name": "30 Applications Submitted", "completed": False, "github_url": "", "business_impact": ""}, "interview_prep": {}, "morning_sessions": 0, "evening_sessions": 0, "notes": "", "week_rating": 0, "completed": False}
            }
        }
    },
    "certifications": {
        "CKA": {"status": "not_started", "target_date": "", "score": "", "notes": ""},
        "CKAD": {"status": "not_started", "target_date": "", "score": "", "notes": ""},
        "CKS": {"status": "not_started", "target_date": "", "score": "", "notes": ""},
        "AWS_SAP": {"status": "not_started", "target_date": "", "score": "", "notes": ""},
        "Terraform_Associate": {"status": "not_started", "target_date": "", "score": "", "notes": ""},
        "Vault_Associate": {"status": "not_started", "target_date": "", "score": "", "notes": ""}
    },
    "daily_logs": [],
    "interview_sessions": [],
    "consultant_journal": []
}

# ─── Data I/O ─────────────────────────────────────────────────────────────────
def load_data():
    if DATA_FILE.exists():
        with open(DATA_FILE) as f:
            data = json.load(f)
        if data and "profile" in data:
            return data
    return DEFAULT_DATA

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

# ─── Helpers ──────────────────────────────────────────────────────────────────
MOTIVATIONAL_QUOTES = [
    "The best time to plant a tree was 20 years ago. The second best time is now.",
    "A consultant doesn't just fix problems — they build systems that prevent them.",
    "Every expert was once a beginner. Every pro was once an amateur.",
    "Your GitHub commit graph is your resume in progress.",
    "Think in business impact. Speak in STAR. Build in prod-grade.",
    "The people who get hired are the ones who can explain WHY, not just HOW.",
    "Consistency over intensity. 40 hours every week beats 100 hours one week.",
    "Build it. Break it. Fix it. Document it. That's how you learn.",
]

def get_phase_for_week(week_num):
    if week_num <= 4: return "phase_1"
    if week_num <= 10: return "phase_2"
    if week_num <= 18: return "phase_3"
    if week_num <= 26: return "phase_4"
    return "phase_5"

def calc_overall_progress(data):
    total_items = 0
    done_items = 0
    total_hours_target = 1440
    hours_logged = 0
    for phase in data["phases"].values():
        for week in phase["weeks_data"].values():
            hours_logged += week.get("hours_logged", 0)
            for lab_done in week.get("labs", {}).values():
                total_items += 1
                if lab_done: done_items += 1
            for q_done in week.get("interview_prep", {}).values():
                total_items += 1
                if q_done: done_items += 1
            if week.get("project", {}).get("completed", False):
                total_items += 1
                done_items += 1
    pct = (done_items / total_items * 100) if total_items > 0 else 0
    hours_pct = (hours_logged / total_hours_target * 100)
    return pct, done_items, total_items, hours_logged, hours_pct

def calc_phase_progress(phase_data):
    total = done = 0
    hours = 0
    for week in phase_data["weeks_data"].values():
        hours += week.get("hours_logged", 0)
        for v in week.get("labs", {}).values():
            total += 1
            if v: done += 1
        for v in week.get("interview_prep", {}).values():
            total += 1
            if v: done += 1
        if week.get("project", {}).get("completed"):
            total += 1
            done += 1
    return (done/total*100) if total > 0 else 0, done, total, hours

# ─── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
.metric-card {
    background: #f8fafc; border-radius: 12px; padding: 1rem 1.25rem;
    border: 1px solid #e2e8f0; margin-bottom: 0.5rem;
}
.phase-card {
    border-radius: 12px; padding: 1rem 1.25rem; margin-bottom: 0.75rem;
    border: 1px solid #e2e8f0;
}
.quote-box {
    background: #f0f9ff; border-left: 4px solid #0891B2;
    padding: 0.75rem 1rem; border-radius: 0 8px 8px 0;
    font-style: italic; font-size: 0.9rem; color: #0c4a6e; margin: 1rem 0;
}
.consultant-tip {
    background: #fefce8; border-left: 4px solid #D97706;
    padding: 0.75rem 1rem; border-radius: 0 8px 8px 0;
    font-size: 0.85rem; color: #78350f; margin: 0.5rem 0;
}
.impact-box {
    background: #f0fdf4; border: 1px solid #bbf7d0;
    border-radius: 8px; padding: 0.75rem 1rem; margin-top: 0.5rem;
}
</style>
""", unsafe_allow_html=True)

# ─── Load data ────────────────────────────────────────────────────────────────
if "data" not in st.session_state:
    st.session_state.data = load_data()

data = st.session_state.data

# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"### 🚀 DevOps Mastery")
    st.markdown(f"**{data['profile']['name']}**")
    st.markdown(f"*{data['profile']['target_role']}*")
    st.divider()

    overall_pct, done, total, hours_logged, hours_pct = calc_overall_progress(data)
    st.markdown("**Overall Progress**")
    st.progress(overall_pct / 100)
    st.caption(f"{overall_pct:.1f}% complete · {done}/{total} items")
    st.markdown(f"**Hours:** {hours_logged:.1f} / 1440h")
    st.progress(min(hours_pct / 100, 1.0))
    st.divider()

    # ── Session Timer ─────────────────────────────────
    st.divider()
    st.markdown("**⏱️ Session Timer**")

    if "timer_running" not in st.session_state:
        st.session_state.timer_running = False
    if "timer_start" not in st.session_state:
        st.session_state.timer_start = None

    if not st.session_state.timer_running:
        if st.button("▶️ Start Session", use_container_width=True):
            st.session_state.timer_running = True
            st.session_state.timer_start = datetime.now().isoformat()
            st.rerun()
        if st.session_state.get("timer_elapsed_hours"):
            st.info(f"Last session: **{st.session_state.timer_elapsed_hours:.2f}h** — go to Daily Log to save it")
    else:
        start_dt = datetime.fromisoformat(st.session_state.timer_start)
        elapsed = datetime.now() - start_dt
        mins = int(elapsed.total_seconds() // 60)
        secs = int(elapsed.total_seconds() % 60)
        st.markdown(f"🟢 **{mins:02d}:{secs:02d} elapsed**")
        st.caption(f"Started at {start_dt.strftime('%H:%M:%S')}")
        if st.button("⏹️ Stop & Log", use_container_width=True, type="primary"):
            hours = elapsed.total_seconds() / 3600
            st.session_state.timer_running = False
            st.session_state.timer_elapsed_hours = round(hours * 4) / 4  # round to nearest 0.25h
            st.session_state.timer_start = None
            st.rerun()
        if st.button("✕ Cancel Timer", use_container_width=True):
            st.session_state.timer_running = False
            st.session_state.timer_start = None
            st.rerun()

    st.divider()
    page = st.selectbox("Navigate", [
        "🏠 Dashboard",
        "📅 Week Tracker",
        "🎤 Interview Prep",
        "🏗️ Projects",
        "🎓 Certifications",
        "📓 Daily Log",
        "🧠 Consultant Journal",
        "⚙️ Settings"
    ])

# ─── Dashboard ────────────────────────────────────────────────────────────────
if page == "🏠 Dashboard":
    st.title("🚀 DevOps Mastery — Command Center")
    st.markdown(f'<div class="quote-box">"{random.choice(MOTIVATIONAL_QUOTES)}"</div>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    start = datetime.strptime(data["profile"]["start_date"], "%Y-%m-%d").date()
    days_elapsed = (date.today() - start).days
    current_week = min(max(days_elapsed // 7 + 1, 1), 36)
    with col1:
        st.metric("Current Week", f"Week {current_week}", f"of 36")
    with col2:
        st.metric("Hours Logged", f"{hours_logged:.0f}h", f"{1440-hours_logged:.0f}h remaining")
    with col3:
        st.metric("Items Done", f"{done}", f"of {total} total")
    with col4:
        days_left = max(0, 252 - days_elapsed)
        st.metric("Days Left", days_left, "in programme")

    st.divider()
    st.subheader("Phase Overview")

    phase_colors = {"phase_1": "#4F46E5", "phase_2": "#0891B2", "phase_3": "#D97706",
                    "phase_4": "#16A34A", "phase_5": "#DC2626"}

    for phase_key, phase in data["phases"].items():
        pct, pdone, ptotal, phours = calc_phase_progress(phase)
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**{phase['name']}** (Weeks {phase['weeks']})")
            st.progress(pct / 100)
            st.caption(f"{pct:.0f}% · {pdone}/{ptotal} items · {phours:.1f}h logged")
        with col2:
            st.metric("Target", f"{phase['total_hours']}h", f"{phours:.0f}h done")

    st.divider()
    st.subheader("📊 This Week's Targets")
    current_phase = get_phase_for_week(current_week)
    week_key = f"week_{current_week}"
    if week_key in data["phases"][current_phase]["weeks_data"]:
        wk = data["phases"][current_phase]["weeks_data"][week_key]
        c1, c2, c3 = st.columns(3)
        labs_done = sum(wk.get("labs", {}).values())
        labs_total = len(wk.get("labs", {}))
        qs_done = sum(wk.get("interview_prep", {}).values())
        qs_total = len(wk.get("interview_prep", {}))
        with c1: st.metric("Labs", f"{labs_done}/{labs_total}")
        with c2: st.metric("Interview Qs", f"{qs_done}/{qs_total}")
        with c3: st.metric("Hours", f"{wk.get('hours_logged', 0):.1f}/{wk['hours_target']}h")

        st.markdown(f'<div class="consultant-tip">🎯 This week\'s topic: <strong>{wk["topic"]}</strong><br>Project: {wk.get("project", {}).get("name", "TBD")}</div>', unsafe_allow_html=True)

# ─── Week Tracker ─────────────────────────────────────────────────────────────
elif page == "📅 Week Tracker":
    st.title("📅 Week-by-Week Tracker")

    phase_names = {
        "phase_1": "Phase 1: Foundations (Weeks 1–4)",
        "phase_2": "Phase 2: Core DevOps (Weeks 5–10)",
        "phase_3": "Phase 3: Enterprise (Weeks 11–18)",
        "phase_4": "Phase 4: Architecture (Weeks 19–26)",
        "phase_5": "Phase 5: Leadership (Weeks 27–36)"
    }
    selected_phase = st.selectbox("Select Phase", list(phase_names.keys()), format_func=lambda x: phase_names[x])
    phase = data["phases"][selected_phase]

    week_options = list(phase["weeks_data"].keys())
    selected_week = st.selectbox("Select Week", week_options,
        format_func=lambda w: f"Week {w.split('_')[1]} — {phase['weeks_data'][w]['topic']}")

    wk = phase["weeks_data"][selected_week]
    week_num = int(selected_week.split("_")[1])

    st.subheader(f"Week {week_num}: {wk['topic']}")

    # Hours logging
    col1, col2, col3 = st.columns(3)
    with col1:
        new_hours = st.number_input("Hours logged this week", 0.0, 80.0,
                                     float(wk.get("hours_logged", 0)), 0.5)
        if new_hours != wk.get("hours_logged", 0):
            data["phases"][selected_phase]["weeks_data"][selected_week]["hours_logged"] = new_hours
            save_data(data)
    with col2:
        morning = st.number_input("Morning sessions completed", 0, 7,
                                    wk.get("morning_sessions", 0))
        if morning != wk.get("morning_sessions", 0):
            data["phases"][selected_phase]["weeks_data"][selected_week]["morning_sessions"] = morning
            save_data(data)
    with col3:
        evening = st.number_input("Evening sessions completed", 0, 7,
                                    wk.get("evening_sessions", 0))
        if evening != wk.get("evening_sessions", 0):
            data["phases"][selected_phase]["weeks_data"][selected_week]["evening_sessions"] = evening
            save_data(data)

    hours_pct = min(new_hours / wk["hours_target"] * 100, 100)
    st.progress(hours_pct / 100)
    st.caption(f"{new_hours:.1f} / {wk['hours_target']}h ({hours_pct:.0f}%)")
    st.divider()

    # Labs
    if wk.get("labs"):
        st.subheader("🔬 Labs")
        labs = wk["labs"]
        done_count = sum(labs.values())
        st.caption(f"{done_count}/{len(labs)} completed")
        for lab_name, done in labs.items():
            new_val = st.checkbox(lab_name, value=done, key=f"lab_{selected_week}_{lab_name}")
            if new_val != done:
                data["phases"][selected_phase]["weeks_data"][selected_week]["labs"][lab_name] = new_val
                save_data(data)
        st.divider()

    # Project
    if wk.get("project"):
        st.subheader("🏗️ Enterprise Project")
        proj = wk["project"]
        st.markdown(f"**{proj['name']}**")
        proj_done = st.checkbox("Project completed", value=proj.get("completed", False),
                                 key=f"proj_{selected_week}")
        if proj_done != proj.get("completed", False):
            data["phases"][selected_phase]["weeks_data"][selected_week]["project"]["completed"] = proj_done
            save_data(data)

        github_url = st.text_input("GitHub URL", value=proj.get("github_url", ""),
                                    key=f"gh_{selected_week}", placeholder="https://github.com/you/project")
        if github_url != proj.get("github_url", ""):
            data["phases"][selected_phase]["weeks_data"][selected_week]["project"]["github_url"] = github_url
            save_data(data)

        st.markdown('<div class="consultant-tip">📌 Business Impact (required — quantify the value)</div>', unsafe_allow_html=True)
        impact = st.text_area("Business Impact", value=proj.get("business_impact", ""),
                              key=f"impact_{selected_week}",
                              placeholder="e.g. Reduced deployment time from 2 days to 15 minutes. Enabled 3 teams to self-serve environment provisioning.")
        if impact != proj.get("business_impact", ""):
            data["phases"][selected_phase]["weeks_data"][selected_week]["project"]["business_impact"] = impact
            save_data(data)
        st.divider()

    # Notes
    st.subheader("📝 Week Notes")
    notes = st.text_area("Notes, gaps found, follow-ups", value=wk.get("notes", ""),
                          key=f"notes_{selected_week}", height=100)
    if notes != wk.get("notes", ""):
        data["phases"][selected_phase]["weeks_data"][selected_week]["notes"] = notes
        save_data(data)

    rating = st.slider("Week self-rating (1–5)", 1, 5, max(wk.get("week_rating", 3), 1),
                        key=f"rating_{selected_week}")
    if rating != wk.get("week_rating", 0):
        data["phases"][selected_phase]["weeks_data"][selected_week]["week_rating"] = rating
        save_data(data)

# ─── Interview Prep ───────────────────────────────────────────────────────────
elif page == "🎤 Interview Prep":
    st.title("🎤 Interview Preparation Tracker")
    st.markdown('<div class="consultant-tip">Rule: Don\'t just read the answers. Say them out loud. Record yourself. Review. Each answer should flow in 90–120 seconds.</div>', unsafe_allow_html=True)

    phase_names = {
        "phase_1": "Phase 1: Foundations", "phase_2": "Phase 2: Core DevOps",
        "phase_3": "Phase 3: Enterprise", "phase_4": "Phase 4: Architecture",
        "phase_5": "Phase 5: Leadership"
    }
    sel_phase = st.selectbox("Phase", list(phase_names.keys()), format_func=lambda x: phase_names[x])
    phase = data["phases"][sel_phase]

    week_options = [w for w in phase["weeks_data"] if phase["weeks_data"][w].get("interview_prep")]
    if not week_options:
        st.info("Interview prep for this phase will be populated as you progress.")
    else:
        sel_week = st.selectbox("Week", week_options,
            format_func=lambda w: f"Week {w.split('_')[1]} — {phase['weeks_data'][w]['topic']}")
        wk = phase["weeks_data"][sel_week]
        qs = wk.get("interview_prep", {})

        done = sum(qs.values())
        st.caption(f"{done}/{len(qs)} questions practiced")
        st.progress(done / len(qs) if qs else 0)

        col_all, col_pending = st.columns(2)
        with col_all:
            show_all = st.checkbox("Show all", value=True)
        with col_pending:
            show_pending_only = st.checkbox("Pending only", value=False)

        for q_name, q_done in qs.items():
            if show_pending_only and q_done:
                continue
            new_val = st.checkbox(q_name, value=q_done, key=f"iq_{sel_week}_{q_name}")
            if new_val != q_done:
                data["phases"][sel_phase]["weeks_data"][sel_week]["interview_prep"][q_name] = new_val
                save_data(data)

    st.divider()
    st.subheader("📊 Interview Prep Summary")
    for pk, pv in data["phases"].items():
        total_qs = sum_qs = 0
        for wv in pv["weeks_data"].values():
            qs = wv.get("interview_prep", {})
            total_qs += len(qs)
            sum_qs += sum(qs.values())
        if total_qs > 0:
            pct = sum_qs / total_qs * 100
            st.markdown(f"**{pv['name']}**: {sum_qs}/{total_qs} ({pct:.0f}%)")
            st.progress(pct / 100)

# ─── Projects ─────────────────────────────────────────────────────────────────
elif page == "🏗️ Projects":
    st.title("🏗️ Enterprise Projects Portfolio")
    st.markdown('<div class="consultant-tip">Every project must have a Business Impact section. "I built X" → "I built X which reduced Y by Z% saving the business $N/month"</div>', unsafe_allow_html=True)

    # Build full project list with lab/Q stats
    all_projects = []
    for pk, pv in data["phases"].items():
        for wk_key, wv in pv["weeks_data"].items():
            proj = wv.get("project", {})
            if proj.get("name"):
                labs_total = len(wv.get("labs", {}))
                labs_done = sum(1 for v in wv.get("labs", {}).values() if v)
                qs_total = len(wv.get("interview_prep", {}))
                qs_done = sum(1 for v in wv.get("interview_prep", {}).values() if v)
                all_projects.append({
                    "phase": pv["name"],
                    "phase_key": pk,
                    "phase_color": pv.get("color", "#888"),
                    "week": wk_key.replace("_", " ").title(),
                    "week_key": wk_key,
                    "week_num": int(wk_key.split("_")[1]),
                    "topic": wv["topic"],
                    "name": proj["name"],
                    "completed": proj.get("completed", False),
                    "github_url": proj.get("github_url", ""),
                    "business_impact": proj.get("business_impact", ""),
                    "hours_logged": wv.get("hours_logged", 0),
                    "hours_target": wv.get("hours_target", 40),
                    "labs_done": labs_done,
                    "labs_total": labs_total,
                    "qs_done": qs_done,
                    "qs_total": qs_total,
                    "notes": wv.get("notes", ""),
                    "week_rating": wv.get("week_rating", 0),
                })

    # Filter controls
    fcol1, fcol2, fcol3 = st.columns(3)
    with fcol1:
        phase_options = ["All Phases"] + [data["phases"][pk]["name"] for pk in data["phases"]]
        filter_phase = st.selectbox("Phase", phase_options, key="proj_filter_phase")
    with fcol2:
        filter_status = st.selectbox("Status", ["All", "Completed", "Pending"], key="proj_filter_status")
    with fcol3:
        filter_impact = st.selectbox("Impact Written", ["All", "With Impact", "Missing Impact"], key="proj_filter_impact")

    filtered = all_projects
    if filter_phase != "All Phases":
        filtered = [p for p in filtered if p["phase"] == filter_phase]
    if filter_status == "Completed":
        filtered = [p for p in filtered if p["completed"]]
    elif filter_status == "Pending":
        filtered = [p for p in filtered if not p["completed"]]
    if filter_impact == "With Impact":
        filtered = [p for p in filtered if p["business_impact"]]
    elif filter_impact == "Missing Impact":
        filtered = [p for p in filtered if not p["business_impact"]]

    # Summary metrics
    done_count = sum(1 for p in all_projects if p["completed"])
    impact_count = sum(1 for p in all_projects if p["business_impact"])
    pct = done_count / len(all_projects) * 100 if all_projects else 0

    mc1, mc2, mc3, mc4 = st.columns(4)
    with mc1: st.metric("Total Projects", len(all_projects))
    with mc2: st.metric("Completed", done_count)
    with mc3: st.metric("Completion Rate", f"{pct:.0f}%")
    with mc4: st.metric("Impact Written", f"{impact_count}/{len(all_projects)}")
    st.progress(pct / 100)
    st.divider()

    st.caption(f"Showing {len(filtered)} of {len(all_projects)} projects")

    for proj in filtered:
        status_icon = "✅" if proj["completed"] else "⏳"
        star_rating = "⭐" * proj["week_rating"] if proj["week_rating"] > 0 else ""
        label = f"{status_icon} **Week {proj['week_num']}** — {proj['name']}"

        with st.expander(label, expanded=proj["completed"]):
            # Info row
            info_c1, info_c2, info_c3, info_c4 = st.columns([3, 1, 1, 1])
            with info_c1:
                st.caption(f"📁 {proj['phase']}  ·  🏷️ {proj['topic']}")
            with info_c2:
                st.caption(f"🔬 Labs: **{proj['labs_done']}/{proj['labs_total']}**")
            with info_c3:
                st.caption(f"🎤 Qs: **{proj['qs_done']}/{proj['qs_total']}**")
            with info_c4:
                if star_rating:
                    st.caption(f"Rating: {star_rating}")

            # Hours progress bar
            if proj["hours_target"] > 0:
                h_pct = min(proj["hours_logged"] / proj["hours_target"], 1.0)
                st.progress(h_pct)
                st.caption(f"⏱️ Hours: {proj['hours_logged']:.1f} / {proj['hours_target']}h  ({h_pct*100:.0f}%)")

            st.divider()

            # Editable fields
            edit_c1, edit_c2 = st.columns([1, 2])
            with edit_c1:
                new_completed = st.checkbox(
                    "Mark as completed",
                    value=proj["completed"],
                    key=f"proj_completed_{proj['week_key']}"
                )
                if new_completed != proj["completed"]:
                    data["phases"][proj["phase_key"]]["weeks_data"][proj["week_key"]]["project"]["completed"] = new_completed
                    save_data(data)
                    st.rerun()

            with edit_c2:
                new_github = st.text_input(
                    "GitHub Repository URL",
                    value=proj["github_url"],
                    key=f"proj_gh_{proj['week_key']}",
                    placeholder="https://github.com/you/project-name"
                )
                if new_github != proj["github_url"]:
                    data["phases"][proj["phase_key"]]["weeks_data"][proj["week_key"]]["project"]["github_url"] = new_github
                    save_data(data)

            if proj["github_url"]:
                st.markdown(f"🔗 [View on GitHub]({proj['github_url']})")

            st.markdown('<div class="consultant-tip">📌 <strong>Business Impact</strong> — quantify: time saved, cost reduced, reliability improved, scale enabled, incidents prevented</div>', unsafe_allow_html=True)
            new_impact = st.text_area(
                "Business Impact Statement",
                value=proj["business_impact"],
                key=f"proj_impact_{proj['week_key']}",
                height=100,
                placeholder="e.g. Reduced deployment time from 2 hours to 8 minutes (93% reduction). Enabled team to deploy 3× daily vs weekly. Eliminated weekend outages saving ~$15k/incident."
            )
            if new_impact != proj["business_impact"]:
                data["phases"][proj["phase_key"]]["weeks_data"][proj["week_key"]]["project"]["business_impact"] = new_impact
                save_data(data)

            if new_impact:
                st.markdown(f'<div class="impact-box">✅ <strong>Impact:</strong> {new_impact}</div>', unsafe_allow_html=True)

            if proj["notes"]:
                with st.expander("📝 Week Notes"):
                    st.markdown(proj["notes"])

# ─── Certifications ───────────────────────────────────────────────────────────
elif page == "🎓 Certifications":
    st.title("🎓 Certification Tracker")

    cert_info = {
        "CKA": {"full": "Certified Kubernetes Administrator", "priority": "1 — Must Have", "timeline": "Month 2"},
        "CKAD": {"full": "Certified Kubernetes Application Developer", "priority": "2 — Must Have", "timeline": "Month 3"},
        "CKS": {"full": "Certified Kubernetes Security Specialist", "priority": "3 — Must Have", "timeline": "Month 4"},
        "AWS_SAP": {"full": "AWS Solutions Architect Professional", "priority": "4 — High Value", "timeline": "Month 5"},
        "Terraform_Associate": {"full": "HashiCorp Terraform Associate", "priority": "5 — Good to Have", "timeline": "Month 5"},
        "Vault_Associate": {"full": "HashiCorp Vault Associate", "priority": "6 — Good to Have", "timeline": "Month 6"}
    }

    status_options = ["not_started", "in_progress", "completed", "scheduled"]
    status_display = {"not_started": "⬜ Not started", "in_progress": "🟡 In progress",
                      "completed": "✅ Completed", "scheduled": "📅 Scheduled"}

    for cert_key, cert in data["certifications"].items():
        info = cert_info.get(cert_key, {})
        with st.expander(f"{status_display.get(cert.get('status', 'not_started'), '⬜')} {cert_key} — {info.get('full', cert_key)}"):
            st.caption(f"Priority: {info.get('priority', '')} · Target: {info.get('timeline', '')}")
            col1, col2 = st.columns(2)
            with col1:
                new_status = st.selectbox("Status", status_options,
                    index=status_options.index(cert.get("status", "not_started")),
                    format_func=lambda x: status_display[x],
                    key=f"cert_status_{cert_key}")
            with col2:
                target_date = st.text_input("Target date", value=cert.get("target_date", ""),
                    placeholder="YYYY-MM-DD", key=f"cert_date_{cert_key}")
            notes = st.text_area("Study notes", value=cert.get("notes", ""),
                key=f"cert_notes_{cert_key}", height=80)
            if st.button("Save", key=f"cert_save_{cert_key}"):
                data["certifications"][cert_key]["status"] = new_status
                data["certifications"][cert_key]["target_date"] = target_date
                data["certifications"][cert_key]["notes"] = notes
                save_data(data)
                st.success("Saved!")

# ─── Daily Log ────────────────────────────────────────────────────────────────
elif page == "📓 Daily Log":
    st.title("📓 Daily Learning Log")
    st.markdown("*Log every study session. This becomes evidence of your discipline.*")

    # Show timer result banner if timer was just stopped
    timer_hours = st.session_state.get("timer_elapsed_hours", 0.0)
    if timer_hours:
        st.success(f"⏱️ Timer stopped — **{timer_hours:.2f}h** pre-filled below. Fill in the details and submit.")

    with st.form("daily_log_form"):
        col1, col2 = st.columns(2)
        with col1:
            log_date = st.date_input("Date", date.today())
            session_type = st.selectbox("Session", ["Morning (Theory)", "Evening (Lab)", "Saturday (Project)", "Sunday (Review)", "Interview Prep"])
        with col2:
            default_hours = float(timer_hours) if timer_hours else 1.5
            hours = st.number_input("Hours", 0.0, 8.0, default_hours, 0.25)
            week_num = st.number_input("Week #", 1, 36, data["profile"].get("current_week", 1))

        topic = st.text_input("Topic covered", placeholder="e.g. Linux namespaces, cgroups, container internals")
        what_built = st.text_area("What I built / completed", height=80,
            placeholder="e.g. Lab 5.1: Created container from scratch using unshare, chroot. Wrote 500 words on what I learned.")
        stuck_on = st.text_area("What I'm stuck on / questions", height=60,
            placeholder="e.g. Confused about overlay2 vs aufs. Need to re-read.")
        key_insight = st.text_input("One key insight", placeholder="e.g. Containers are just Linux processes with namespaces — that's it.")

        submitted = st.form_submit_button("Log Session ✅")
        if submitted and topic:
            entry = {
                "date": str(log_date),
                "session_type": session_type,
                "hours": hours,
                "week": week_num,
                "topic": topic,
                "what_built": what_built,
                "stuck_on": stuck_on,
                "key_insight": key_insight,
                "timestamp": datetime.now().isoformat()
            }
            data["daily_logs"].append(entry)
            # Update hours in week
            phase_key = get_phase_for_week(week_num)
            week_key = f"week_{week_num}"
            if week_key in data["phases"][phase_key]["weeks_data"]:
                current_hours = data["phases"][phase_key]["weeks_data"][week_key].get("hours_logged", 0)
                data["phases"][phase_key]["weeks_data"][week_key]["hours_logged"] = current_hours + hours
            save_data(data)
            st.session_state.timer_elapsed_hours = None  # clear timer after logging
            st.success(f"Logged {hours}h for {topic}!")

    st.divider()
    st.subheader("Recent Sessions")
    recent = sorted(data["daily_logs"], key=lambda x: x["date"], reverse=True)[:10]
    for entry in recent:
        with st.expander(f"{entry['date']} · {entry['session_type']} · {entry['hours']}h · {entry['topic']}"):
            if entry.get("what_built"): st.markdown(f"**Built:** {entry['what_built']}")
            if entry.get("key_insight"): st.markdown(f"**Insight:** {entry['key_insight']}")
            if entry.get("stuck_on"): st.markdown(f"**Stuck on:** {entry['stuck_on']}")

# ─── Consultant Journal ────────────────────────────────────────────────────────
elif page == "🧠 Consultant Journal":
    st.title("🧠 Consultant Mindset Journal")
    st.markdown('<div class="consultant-tip">Write weekly. This builds the "business impact" narrative you\'ll use in every interview. Think: what problem did I solve? What would it have cost NOT to solve it?</div>', unsafe_allow_html=True)

    with st.form("journal_form"):
        week_num = st.number_input("Week #", 1, 36, 1)
        st.markdown("**Answer these questions every week:**")
        q1 = st.text_area("1. What problem did I solve this week? (in business terms)", height=80)
        q2 = st.text_area("2. What would this have cost the business if NOT solved?", height=80)
        q3 = st.text_area("3. How would I explain this week's work to a CEO in 2 minutes?", height=80)
        q4 = st.text_area("4. What STAR story can I extract from this week?", height=100)
        q5 = st.text_area("5. What would a consultant charge for this work? (think in value)", height=60)

        if st.form_submit_button("Save Journal Entry"):
            entry = {
                "week": week_num,
                "date": str(date.today()),
                "problem_solved": q1,
                "business_cost_if_not": q2,
                "ceo_explanation": q3,
                "star_story": q4,
                "consultant_value": q5
            }
            data["consultant_journal"].append(entry)
            save_data(data)
            st.success("Journal entry saved!")

    st.divider()
    st.subheader("Past Entries")
    for entry in reversed(data.get("consultant_journal", [])[-5:]):
        with st.expander(f"Week {entry.get('week')} — {entry.get('date')}"):
            if entry.get("problem_solved"): st.markdown(f"**Problem:** {entry['problem_solved']}")
            if entry.get("star_story"): st.markdown(f"**STAR Story:** {entry['star_story']}")

# ─── Settings ─────────────────────────────────────────────────────────────────
elif page == "⚙️ Settings":
    st.title("⚙️ Settings")

    with st.form("profile_form"):
        name = st.text_input("Name", value=data["profile"]["name"])
        start_date = st.date_input("Programme start date",
            value=datetime.strptime(data["profile"]["start_date"], "%Y-%m-%d").date())
        target_role = st.text_input("Target role", value=data["profile"]["target_role"])
        github_url = st.text_input("GitHub URL", value=data["profile"].get("github_url", ""))

        if st.form_submit_button("Save Profile"):
            data["profile"]["name"] = name
            data["profile"]["start_date"] = str(start_date)
            data["profile"]["target_role"] = target_role
            data["profile"]["github_url"] = github_url
            save_data(data)
            st.success("Profile saved!")

    st.divider()
    st.subheader("Data Management")
    col1, col2 = st.columns(2)
    with col1:
        if st.download_button("Download progress.json",
                data=json.dumps(data, indent=2), file_name="progress.json", mime="application/json"):
            st.success("Downloaded!")
    with col2:
        uploaded = st.file_uploader("Restore from backup", type=["json"])
        if uploaded:
            restored = json.load(uploaded)
            save_data(restored)
            st.session_state.data = restored
            st.success("Restored!")
            st.rerun()
