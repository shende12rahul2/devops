PROJECTS_PART_1 = {
    "project_1_cicd_platform": {
        "title": "Project 1: Multi-cloud CI/CD Platform (GitHub Actions + ArgoCD)",
        "phase": "Core DevOps Stack",
        "enterprise_problem": {
            "statement": "Global SaaS company with 200+ developers deploys to AWS, Azure, and GCP. Deployments manually triggered, inconsistent, slow (4+ hours per deployment). Zero visibility into deployment status. Frequent deployment failures and rollbacks taking hours.",
            "business_context": "Company loses $50k/hour during deployment windows. Failed deployments cause customer outages affecting $2M revenue contracts. Manual process introduces human errors. Compliance requires audit trail of all deployments."
        },
        "current_state": {
            "pain_points": [
                "Manual SSH into servers to deploy",
                "4-hour deployment window with high failure rate (15-20%)",
                "No rollback capability, require manual database migrations",
                "Inconsistent configurations across environments",
                "Zero observability into what was deployed when"
            ],
            "cost_impact": "Failed deployments cost $50k each, happens 2-3 times monthly = $100-150k/month loss"
        },
        "architecture_diagram": """
MULTI-CLOUD CI/CD PLATFORM WITH GITHUB ACTIONS & ARGOCD

┌─────────────────────────────────────────────────────────────────────────────┐
│ DEVELOPER WORKFLOW                                                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Developer writes code → git push → GitHub PR created                       │
│                    ↓                                                         │
│           GitHub Actions triggers                                           │
│                    ↓                                                         │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │ CI PIPELINE (Runs on GitHub Actions)                              │    │
│  │ ┌──────────────┐ ┌──────────────┐ ┌──────────────────────────┐   │    │
│  │ │ Unit Tests   │→│ SAST Scan    │→│ Build Docker Image      │   │    │
│  │ │ (pytest)     │ │ (SonarQube)  │ │ (multi-arch)            │   │    │
│  │ └──────────────┘ └──────────────┘ └──────────────────────────┘   │    │
│  │         ↓             ↓                     ↓                     │    │
│  │  ┌────────────────────────────────────────────────────────────┐  │    │
│  │  │ Image Scanning (Trivy) → Sign (cosign) → Push to Registry │  │    │
│  │  └────────────────────────────────────────────────────────────┘  │    │
│  │         ↓                                                         │    │
│  │  ┌────────────────────────────────────────────────────────────┐  │    │
│  │  │ Deploy to Staging → Run smoke tests → Approval required   │  │    │
│  │  └────────────────────────────────────────────────────────────┘  │    │
│  └────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ CD LAYER - ARGOCD (Declarative GitOps)                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Application Manifest Git Repo (Infrastructure Code)                        │
│  ├── base/                                                                   │
│  │   ├── deployment.yaml (defines desired state)                            │
│  │   ├── service.yaml                                                       │
│  │   └── ingress.yaml                                                       │
│  ├── overlays/                                                              │
│  │   ├── dev/ (kustomization.yaml - image: app:dev)                         │
│  │   ├── staging/ (kustomization.yaml - image: app:staging)                 │
│  │   └── prod/ (kustomization.yaml - image: app:latest)                     │
│                                                                              │
│  ArgoCD watches Git repo ─→ Detects changes ─→ Auto-syncs to cluster       │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ ARGOCD APPLICATION CONTROLLER                                       │   │
│  │ ├── Detect config drift (desired vs. actual state)                  │   │
│  │ ├── Auto-sync or notify admin (policy: automatic/manual)            │   │
│  │ ├── Canary deployment (5% traffic → 25% → 100%)                     │   │
│  │ └── Automatic rollback on failed health checks                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ DEPLOYMENT TARGETS (Multi-Cloud)                                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐             │
│  │ AWS EKS Cluster │  │ Azure AKS       │  │ GCP GKE         │             │
│  │ (prod + staging)│  │ (staging)       │  │ (backup region) │             │
│  │                 │  │                 │  │                 │             │
│  │ ┌─────────────┐ │  │ ┌─────────────┐ │  │ ┌─────────────┐ │             │
│  │ │ ArgoCD App  │ │  │ │ ArgoCD App  │ │  │ │ ArgoCD App  │ │             │
│  │ │ (prod)      │ │  │ │ (staging)   │ │  │ │ (backup)    │ │             │
│  │ └─────────────┘ │  │ └─────────────┘ │  │ └─────────────┘ │             │
│  │                 │  │                 │  │                 │             │
│  │ ┌─────────────┐ │  │ ┌─────────────┐ │  │ ┌─────────────┐ │             │
│  │ │ Pods        │ │  │ │ Pods        │ │  │ │ Pods        │ │             │
│  │ │ Services    │ │  │ │ Services    │ │  │ │ Services    │ │             │
│  │ │ Ingress     │ │  │ │ Ingress     │ │  │ │ Ingress     │ │             │
│  │ └─────────────┘ │  │ └─────────────┘ │  │ └─────────────┘ │             │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘             │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘

DEPLOYMENT FLOW:
Developer → Git Push → GitHub Actions (test, build, scan) → Create ArgoCD commit
                                                                        ↓
                                        ArgoCD detects Git change → sync to clusters
                                                                        ↓
                                        Canary: 5% traffic to new version
                                                                        ↓
                                        Monitor metrics (error rate, latency)
                                                                        ↓
                                        Auto-promote to 100% or rollback on failure
        """,
        "terraform_code": {
            "description": "AWS EKS cluster setup with GitHub Actions integration",
            "files": {
                "main.tf": """
terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.20"
    }
    helm = {
      source  = "hashicorp/helm"
      version = "~> 2.10"
    }
  }
  backend "s3" {
    bucket         = "terraform-state-prod"
    key            = "eks-production/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-lock"
  }
}

provider "aws" {
  region = var.aws_region
}

# EKS Cluster
resource "aws_eks_cluster" "main" {
  name            = "${var.cluster_name}-${var.environment}"
  role_arn        = aws_iam_role.eks_cluster_role.arn
  version         = var.kubernetes_version

  vpc_config {
    subnet_ids              = aws_subnet.private[*].id
    endpoint_private_access = true
    endpoint_public_access  = true
    public_access_cidrs     = ["0.0.0.0/0"]
  }

  depends_on = [
    aws_iam_role_policy_attachment.eks_cluster_policy,
    aws_iam_role_policy_attachment.eks_vpc_resource_controller,
  ]

  tags = {
    Environment = var.environment
    Terraform   = true
  }
}

# EKS Node Group
resource "aws_eks_node_group" "main" {
  cluster_name    = aws_eks_cluster.main.name
  node_group_name = "${var.cluster_name}-node-group-${var.environment}"
  node_role_arn   = aws_iam_role.eks_node_role.arn
  subnet_ids      = aws_subnet.private[*].id

  scaling_config {
    desired_size = var.node_group_desired_size
    max_size     = var.node_group_max_size
    min_size     = var.node_group_min_size
  }

  instance_types = var.node_instance_types

  depends_on = [
    aws_iam_role_policy_attachment.eks_worker_node_policy,
    aws_iam_role_policy_attachment.eks_cni_policy,
    aws_iam_role_policy_attachment.eks_container_registry_policy,
  ]

  tags = {
    Environment = var.environment
  }
}

# OIDC Provider for IRSA (IAM Roles for Service Accounts)
data "tls_certificate" "cluster" {
  url = aws_eks_cluster.main.identity[0].oidc[0].issuer
}

resource "aws_iam_openid_connect_provider" "cluster" {
  client_id_list  = ["sts.amazonaws.com"]
  thumbprint_list = [data.tls_certificate.cluster.certificates[0].sha1_fingerprint]
  url             = aws_eks_cluster.main.identity[0].oidc[0].issuer
}

# Kubernetes Provider Configuration
provider "kubernetes" {
  host                   = aws_eks_cluster.main.endpoint
  cluster_ca_certificate = base64decode(aws_eks_cluster.main.certificate_authority[0].data)
  token                  = data.aws_eks_cluster_auth.cluster.token
}

data "aws_eks_cluster_auth" "cluster" {
  name = aws_eks_cluster.main.name
}

# Helm Provider Configuration
provider "helm" {
  kubernetes {
    host                   = aws_eks_cluster.main.endpoint
    cluster_ca_certificate = base64decode(aws_eks_cluster.main.certificate_authority[0].data)
    token                  = data.aws_eks_cluster_auth.cluster.token
  }
}

# ArgoCD Namespace
resource "kubernetes_namespace" "argocd" {
  metadata {
    name = "argocd"
  }
  depends_on = [aws_eks_cluster.main]
}

# ArgoCD Helm Release
resource "helm_release" "argocd" {
  name             = "argocd"
  repository       = "https://argoproj.github.io/argo-helm"
  chart            = "argo-cd"
  version          = var.argocd_version
  namespace        = kubernetes_namespace.argocd.metadata[0].name
  create_namespace = false

  values = [
    yamlencode({
      server = {
        service = {
          type = "LoadBalancer"
        }
      }
      configs = {
        secret = {
          argocdServerAdminPassword = bcrypt(random_string.argocd_admin_password.result)
        }
      }
    })
  ]

  depends_on = [aws_eks_node_group.main]
}

# GitHub Actions OIDC Integration
resource "aws_iam_openid_connect_provider" "github" {
  url             = "https://token.actions.githubusercontent.com"
  client_id_list  = ["sts.amazonaws.com"]
  thumbprint_list = [var.github_actions_thumbprint]
}

# IAM Role for GitHub Actions
resource "aws_iam_role" "github_actions" {
  name = "${var.cluster_name}-github-actions-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Federated = aws_iam_openid_connect_provider.github.arn
        }
        Action = "sts:AssumeRoleWithWebIdentity"
        Condition = {
          StringEquals = {
            "token.actions.githubusercontent.com:aud" = "sts.amazonaws.com"
            "token.actions.githubusercontent.com:sub" = "repo:${var.github_repo}:ref:refs/heads/main"
          }
        }
      }
    ]
  })
}

# Policy for GitHub Actions to push to ECR
resource "aws_iam_role_policy" "github_actions_ecr" {
  name   = "github-actions-ecr-policy"
  role   = aws_iam_role.github_actions.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "ecr:GetDownloadUrlForLayer",
          "ecr:BatchGetImage",
          "ecr:BatchCheckLayerAvailability",
          "ecr:PutImage",
          "ecr:InitiateLayerUpload",
          "ecr:UploadLayerPart",
          "ecr:CompleteLayerUpload"
        ]
        Resource = aws_ecr_repository.app.arn
      },
      {
        Effect = "Allow"
        Action = [
          "ecr:GetAuthorizationToken"
        ]
        Resource = "*"
      }
    ]
  })
}

# ECR Repository for Docker images
resource "aws_ecr_repository" "app" {
  name                 = "${var.cluster_name}-app"
  image_tag_mutability = "IMMUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  encryption_configuration {
    encryption_type = "KMS"
    kms_key         = aws_kms_key.ecr.id
  }

  tags = {
    Environment = var.environment
  }
}

# CloudWatch Log Group for EKS
resource "aws_cloudwatch_log_group" "eks" {
  name              = "/aws/eks/${var.cluster_name}/cluster"
  retention_in_days = 7

  tags = {
    Environment = var.environment
  }
}

# Random password for ArgoCD admin
resource "random_string" "argocd_admin_password" {
  length  = 32
  special = true
}

# Outputs
output "eks_cluster_endpoint" {
  value       = aws_eks_cluster.main.endpoint
  description = "EKS cluster endpoint"
}

output "eks_cluster_name" {
  value       = aws_eks_cluster.main.name
  description = "EKS cluster name"
}

output "argocd_admin_password" {
  value       = random_string.argocd_admin_password.result
  sensitive   = true
  description = "ArgoCD admin password"
}

output "ecr_repository_url" {
  value       = aws_ecr_repository.app.repository_url
  description = "ECR repository URL for Docker images"
}

output "github_actions_role_arn" {
  value       = aws_iam_role.github_actions.arn
  description = "IAM role ARN for GitHub Actions"
}
""",
                "variables.tf": """
variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "cluster_name" {
  description = "EKS cluster name"
  type        = string
}

variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
}

variable "kubernetes_version" {
  description = "Kubernetes version"
  type        = string
  default     = "1.28"
}

variable "node_group_desired_size" {
  description = "Desired number of worker nodes"
  type        = number
  default     = 3
}

variable "node_group_min_size" {
  description = "Minimum number of worker nodes"
  type        = number
  default     = 2
}

variable "node_group_max_size" {
  description = "Maximum number of worker nodes"
  type        = number
  default     = 10
}

variable "node_instance_types" {
  description = "EC2 instance types for worker nodes"
  type        = list(string)
  default     = ["t3.large"]
}

variable "argocd_version" {
  description = "ArgoCD Helm chart version"
  type        = string
  default     = "5.40.0"
}

variable "github_repo" {
  description = "GitHub repository for OIDC integration (format: owner/repo)"
  type        = string
}

variable "github_actions_thumbprint" {
  description = "GitHub Actions OIDC thumbprint"
  type        = string
  default     = "6938fd4d98bab03faadb97b34396831e3780aea1"
}
"""
            }
        },
        "github_actions_yaml": {
            "description": "Complete GitHub Actions CI/CD workflow",
            "file": ".github/workflows/deploy.yml",
            "content": """
name: CI/CD Pipeline - Build, Test, Deploy

on:
  push:
    branches:
      - main
      - staging
  pull_request:
    branches:
      - main

env:
  REGISTRY: public.ecr.aws
  IMAGE_NAME: devops-app
  AWS_REGION: us-east-1

jobs:
  # Stage 1: Lint & SAST
  security_lint:
    runs-on: ubuntu-latest
    permissions:
      contents: read
    steps:
      - uses: actions/checkout@v4
      
      - name: Run pylint
        run: |
          pip install pylint
          pylint src/ --fail-under=8.0 || true
      
      - name: Run SonarQube scan
        uses: SonarSource/sonarcloud-github-action@master
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}

  # Stage 2: Unit Tests
  unit_tests:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.10', '3.11', '3.12']
    permissions:
      contents: read
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
          cache: 'pip'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov pytest-xdist
      
      - name: Run tests with coverage
        run: |
          pytest tests/ \
            --cov=src \
            --cov-report=xml \
            --cov-report=term \
            -v \
            -n auto
      
      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage.xml
          fail_ci_if_error: true

  # Stage 3: Build & Push Docker Image
  build_push_image:
    needs: [security_lint, unit_tests]
    runs-on: ubuntu-latest
    permissions:
      contents: read
      id-token: write
    outputs:
      image-uri: ${{ steps.image.outputs.uri }}
    steps:
      - uses: actions/checkout@v4
      
      - name: Configure AWS credentials via OIDC
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.AWS_ROLE_ARN }}
          aws-region: ${{ env.AWS_REGION }}
      
      - name: Login to ECR
        run: aws ecr get-login-password --region ${{ env.AWS_REGION }} | docker login --username AWS --password-stdin ${{ env.REGISTRY }}
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2
      
      - name: Build and push multi-arch image
        uses: docker/build-push-action@v4
        with:
          context: .
          platforms: linux/amd64,linux/arm64
          push: true
          tags: |
            ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}
            ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:latest
          cache-from: type=gha
          cache-to: type=gha,mode=max
      
      - name: Output image URI
        id: image
        run: echo "uri=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}" >> $GITHUB_OUTPUT

  # Stage 4: Container Security Scanning
  container_scan:
    needs: build_push_image
    runs-on: ubuntu-latest
    permissions:
      contents: read
    steps:
      - name: Run Trivy vulnerability scan
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: ${{ needs.build_push_image.outputs.image-uri }}
          format: 'sarif'
          output: 'trivy-results.sarif'
          severity: 'CRITICAL,HIGH'
      
      - name: Upload Trivy results to GitHub Security
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: 'trivy-results.sarif'
      
      - name: Fail if critical vulnerabilities found
        run: |
          trivy image --exit-code 1 --severity CRITICAL ${{ needs.build_push_image.outputs.image-uri }}

  # Stage 5: Sign Container Image
  sign_image:
    needs: [build_push_image, container_scan]
    runs-on: ubuntu-latest
    permissions:
      contents: read
      id-token: write
    steps:
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.AWS_ROLE_ARN }}
          aws-region: ${{ env.AWS_REGION }}
      
      - name: Install cosign
        uses: sigstore/cosign-installer@v3
      
      - name: Sign container image
        env:
          COSIGN_EXPERIMENTAL: 1
        run: |
          cosign sign --yes ${{ needs.build_push_image.outputs.image-uri }}

  # Stage 6: Deploy to Staging
  deploy_staging:
    needs: [build_push_image, sign_image]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    permissions:
      contents: read
      id-token: write
    steps:
      - uses: actions/checkout@v4
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.AWS_ROLE_ARN }}
          aws-region: ${{ env.AWS_REGION }}
      
      - name: Update staging deployment via ArgoCD Git
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          
          # Update image tag in ArgoCD overlay
          sed -i "s|image: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:.*|image: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}|" \
            k8s/overlays/staging/kustomization.yaml
          
          git add k8s/overlays/staging/kustomization.yaml
          git commit -m "Deploy staging: ${{ env.IMAGE_NAME }}:${{ github.sha }}"
          git push

  # Stage 7: Smoke Tests on Staging
  smoke_tests:
    needs: deploy_staging
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Wait for deployment
        run: sleep 30
      
      - name: Run smoke tests against staging
        run: |
          pip install requests
          python tests/smoke_tests.py --url https://staging-api.example.com

  # Stage 8: Production Deployment (Manual Approval)
  deploy_production:
    needs: [build_push_image, smoke_tests]
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://api.example.com
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    permissions:
      contents: read
      id-token: write
    steps:
      - uses: actions/checkout@v4
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.AWS_ROLE_ARN }}
          aws-region: ${{ env.AWS_REGION }}
      
      - name: Deploy to production via ArgoCD (canary)
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          
          # Update production overlay with canary strategy
          sed -i "s|image: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:.*|image: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}|" \
            k8s/overlays/prod/kustomization.yaml
          
          # Add canary strategy annotation
          sed -i "/kind: Deployment/a\\  annotations:\\n    deployment.strategy: canary\\n    canary.replicas: 1" \
            k8s/base/deployment.yaml
          
          git add k8s/overlays/prod/kustomization.yaml
          git commit -m "Deploy prod canary: ${{ env.IMAGE_NAME }}:${{ github.sha }}"
          git push
      
      - name: Monitor canary deployment
        run: |
          echo "Canary deployed. Monitoring metrics..."
          # In real scenario, query Prometheus for error rates, latency
          # If metrics look good, promote from 5% → 100%
          sleep 300
          echo "Canary metrics healthy. Auto-promoting to 100%"
"""
        },
        "kubernetes_argocd": {
            "description": "Kubernetes manifests and ArgoCD Application definitions",
            "base_deployment": """
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
  namespace: default
data:
  LOG_LEVEL: "INFO"
  ENABLE_METRICS: "true"

---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: app-sa
  namespace: default

---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: app-reader
rules:
  - apiGroups: [""]
    resources: ["configmaps", "secrets"]
    verbs: ["get", "list", "watch"]

---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: app-reader-binding
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: app-reader
subjects:
  - kind: ServiceAccount
    name: app-sa
    namespace: default

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
  namespace: default
  labels:
    app: app-backend
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: app-backend
  template:
    metadata:
      labels:
        app: app-backend
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "8080"
        prometheus.io/path: "/metrics"
    spec:
      serviceAccountName: app-sa
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsReadOnlyRootFilesystem: true
      containers:
      - name: app
        image: public.ecr.aws/devops-app:latest
        imagePullPolicy: IfNotPresent
        ports:
        - containerPort: 8080
          name: http
        - containerPort: 8081
          name: metrics
        env:
        - name: LOG_LEVEL
          valueFrom:
            configMapKeyRef:
              name: app-config
              key: LOG_LEVEL
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: url
        resources:
          requests:
            cpu: 100m
            memory: 256Mi
          limits:
            cpu: 500m
            memory: 512Mi
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 2
        securityContext:
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
          capabilities:
            drop:
              - ALL
        volumeMounts:
        - name: tmp
          mountPath: /tmp
      volumes:
      - name: tmp
        emptyDir: {}

---
apiVersion: v1
kind: Service
metadata:
  name: app
  namespace: default
  labels:
    app: app-backend
spec:
  type: ClusterIP
  ports:
  - port: 80
    targetPort: 8080
    protocol: TCP
    name: http
  - port: 8081
    targetPort: 8081
    protocol: TCP
    name: metrics
  selector:
    app: app-backend
  sessionAffinity: None

---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: app-hpa
  namespace: default
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: app
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
      - type: Percent
        value: 100
        periodSeconds: 30
      selectPolicy: Max
""",
            "argocd_application": """
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: app-prod
  namespace: argocd
spec:
  project: default
  
  source:
    repoURL: https://github.com/org/infrastructure-repo
    targetRevision: main
    path: k8s/overlays/prod
    plugin:
      name: kustomize
  
  destination:
    server: https://kubernetes.default.svc
    namespace: default
  
  # Auto-sync when Git changes
  syncPolicy:
    automated:
      prune: true      # Delete K8s resources not in Git
      selfHeal: true   # Sync when cluster drifts from Git
      allow:
        empty: false
    retry:
      limit: 5
      backoff:
        duration: 5s
        factor: 2
        maxDuration: 3m
    syncOptions:
    - CreateNamespace=true
    - RespectIgnoreDifferences=true
  
  # Canary deployment strategy
  progressDeadlineSeconds: 600
  
  # Health assessment rules
  ignoreDifferences:
  - group: apps
    kind: Deployment
    jsonPointers:
    - /spec/replicas  # Ignore replica count (HPA controls it)
  
  # Notification settings
  notification:
    enabled: true
"""
        },
        "helm_chart": {
            "description": "Helm chart for application deployment",
            "chart_yaml": """
apiVersion: v2
name: app
description: Production application Helm chart
type: application
version: 1.0.0
appVersion: "1.0.0"

keywords:
  - app
  - microservice
  - kubernetes

maintainers:
  - name: Platform Team
    email: platform@example.com

dependencies: []

annotations:
  category: Backend
  licenses: "Apache-2.0"
""",
            "values_yaml": """
# Default values for Helm chart
replicaCount: 3

image:
  repository: public.ecr.aws/devops-app
  tag: latest
  pullPolicy: IfNotPresent

imagePullSecrets: []
nameOverride: ""
fullnameOverride: ""

serviceAccount:
  create: true
  name: app-sa

service:
  type: ClusterIP
  port: 80
  targetPort: 8080

ingress:
  enabled: true
  className: "nginx"
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
    nginx.ingress.kubernetes.io/rate-limit: "100"
  hosts:
    - host: api.example.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: app-tls
      hosts:
        - api.example.com

resources:
  requests:
    cpu: 100m
    memory: 256Mi
  limits:
    cpu: 500m
    memory: 512Mi

autoscaling:
  enabled: true
  minReplicas: 3
  maxReplicas: 10
  targetCPUUtilizationPercentage: 70
  targetMemoryUtilizationPercentage: 80

config:
  LOG_LEVEL: "INFO"
  ENABLE_METRICS: "true"
""",
            "templates_deployment": """
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "app.fullname" . }}
  labels:
    {{- include "app.labels" . | nindent 4 }}
spec:
  {{- if not .Values.autoscaling.enabled }}
  replicas: {{ .Values.replicaCount }}
  {{- end }}
  selector:
    matchLabels:
      {{- include "app.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      labels:
        {{- include "app.selectorLabels" . | nindent 8 }}
    spec:
      serviceAccountName: {{ include "app.serviceAccountName" . }}
      containers:
      - name: {{ .Chart.Name }}
        image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
        imagePullPolicy: {{ .Values.image.pullPolicy }}
        ports:
        - name: http
          containerPort: 8080
          protocol: TCP
        env:
        {{- range $key, $value := .Values.config }}
        - name: {{ $key }}
          value: {{ $value | quote }}
        {{- end }}
        resources:
          {{- toYaml .Values.resources | nindent 10 }}
        livenessProbe:
          httpGet:
            path: /health
            port: http
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: http
          initialDelaySeconds: 10
          periodSeconds: 5
"""
        },
        "kustomization_overlays": {
            "prod_overlay": """
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

namespace: default

bases:
  - ../../base

replicas:
  - name: app
    count: 5

images:
  - name: public.ecr.aws/devops-app
    newTag: prod-v1.0.0

patches:
  - target:
      kind: Deployment
      name: app
    patch: |-
      - op: replace
        path: /spec/replicas
        value: 5
      - op: add
        path: /spec/template/spec/affinity
        value:
          podAntiAffinity:
            preferredDuringSchedulingIgnoredDuringExecution:
            - weight: 100
              podAffinityTerm:
                labelSelector:
                  matchExpressions:
                  - key: app
                    operator: In
                    values:
                    - app-backend
                topologyKey: kubernetes.io/hostname

configMapGenerator:
  - name: app-config
    behavior: merge
    literals:
      - ENVIRONMENT=production
      - LOG_LEVEL=WARN
      - ENABLE_METRICS=true
"""
        }
    },
    "finops_analysis": {
        "description": "Monthly cost analysis and optimization strategies",
        "monthly_breakdown": {
            "aws_compute": {
                "eks_nodes": {
                    "quantity": 3,
                    "instance_type": "t3.large",
                    "monthly_cost": 450,
                    "notes": "3 nodes × $150/month on-demand"
                },
                "data_transfer": {
                    "egress_gb": 500,
                    "monthly_cost": 50,
                    "notes": "Data transfer out: $0.10/GB"
                },
                "subtotal_compute": 500
            },
            "aws_storage": {
                "ebs_volumes": {
                    "size_gb": 200,
                    "monthly_cost": 20,
                    "notes": "$0.10/GB-month"
                },
                "ecr_storage": {
                    "images_gb": 50,
                    "monthly_cost": 5,
                    "notes": "Docker images in ECR"
                },
                "subtotal_storage": 25
            },
            "aws_networking": {
                "nat_gateway": {
                    "quantity": 3,
                    "monthly_cost": 45,
                    "notes": "3 NAT Gateways × $15/month + data processing"
                },
                "load_balancer": {
                    "quantity": 1,
                    "monthly_cost": 16,
                    "notes": "Classic/ALB: $0.0225/hour"
                },
                "subtotal_networking": 61
            },
            "database": {
                "rds_postgres": {
                    "instance_type": "db.t3.large",
                    "monthly_cost": 200,
                    "notes": "Multi-AZ: $200/month"
                },
                "rds_backup": {
                    "storage_gb": 100,
                    "monthly_cost": 10,
                    "notes": "Automated backups: $0.10/GB"
                },
                "subtotal_database": 210
            },
            "other_services": {
                "cloudwatch_logs": {
                    "gb_ingested": 100,
                    "monthly_cost": 50,
                    "notes": "$0.50/GB ingestion"
                },
                "total_monthly_cost": 846
            }
        },
        "optimization_strategies": [
            {
                "strategy": "1. Reserved Instances (RI) Commitment",
                "description": "Purchase 1-year RIs for predictable workloads (EKS nodes, RDS)",
                "potential_savings": "30-40% cost reduction",
                "implementation": "Convert 3× t3.large to 1-year RI: $450 → $270/month ($180 savings)",
                "payback_period": "Immediate (10 months ROI on commitment)",
                "risk": "Inflexible if workload changes"
            },
            {
                "strategy": "2. Spot Instances for Non-Critical Workloads",
                "description": "Use EC2 Spot instances for dev/staging (up to 90% discount)",
                "potential_savings": "60-70% on non-production compute",
                "implementation": "Dev/staging: Use Spot instances (request interruption: 2-5%). Implement pod disruption budgets",
                "payback_period": "Immediate in dev environment",
                "risk": "Spot instances can be interrupted"
            },
            {
                "strategy": "3. Right-Size Compute Resources",
                "description": "Analyze CloudWatch metrics. Scale down over-provisioned instances",
                "potential_savings": "20-30% compute cost",
                "implementation": "Monitor CPU/memory for 2 weeks. If avg usage < 20%, downsize instance type",
                "payback_period": "Monthly",
                "risk": "Application might need more resources during spikes"
            }
        ],
        "projected_annual_cost": {
            "current": 846 * 12,
            "with_optimization": (846 * 0.6) * 12,
            "annual_savings": (846 * 12) - ((846 * 0.6) * 12)
        }
    },
    "resume_bullets": [
        "Architected and implemented multi-cloud CI/CD platform (GitHub Actions + ArgoCD + Terraform) for 200+ developers, reducing deployment time from 4 hours to 15 minutes (94% improvement) and eliminating manual deployment errors.",
        "Designed GitOps workflow using ArgoCD with automatic reconciliation, enabling zero-downtime deployments via canary strategy (5%→25%→100% traffic shift) with automated rollback on failed health checks.",
        "Implemented GitHub Actions workflows with comprehensive security scanning (SAST, container image, dependency scanning) and policy gates, blocking 95% of vulnerabilities before production deployment.",
        "Deployed highly available AWS EKS clusters across 3 AZs with OIDC federation for GitHub Actions, reducing infrastructure provisioning time from 2 weeks to 30 minutes using Terraform.",
        "Integrated ECR image scanning, cosign signing, and image policy enforcement, reducing supply chain security incidents by 100% (zero container escape attempts in 12 months post-implementation)."
    ]
}

def render_dashboard():
    """Render the main dashboard with key metrics and skill heatmap."""
    st.header("📊 DevOps Command Center Dashboard")

    # Key metrics section
    st.subheader("🎯 Key Performance Metrics")

    # Calculate metrics from session state
    weeks_completed = len([week for week in st.session_state.get('week_details', {}).values() if week.get('completed', False)])
    finops_projects = sum(1 for project in st.session_state.get('project_status', {}).values() if project.get('completed', False))

    # Create three columns for metrics
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="Interview Readiness",
            value=f"{(st.session_state.get('current_question', 1) - 1) / 3:.0f}%",
            delta="Target: 300 questions"
        )

    with col2:
        st.metric(
            label="FinOps Mastery",
            value=f"{finops_projects}/12",
            delta=f"{finops_projects/12*100:.0f}% complete"
        )

    with col3:
        st.metric(
            label="Architect Maturity",
            value=f"{weeks_completed}/48",
            delta=f"{weeks_completed/48*100:.0f}% roadmap"
        )

    # Skill heatmap section
    st.subheader("🔥 Skill Proficiency Heatmap")

    # Sample skill data - in real implementation, this would come from progress tracking
    skills = [
        "Linux/Unix", "Networking", "Git", "Python", "AWS/GCP",
        "Docker/K8s", "Terraform", "Monitoring", "Security", "CI/CD"
    ]

    # Generate sample proficiency data (0-100)
    import numpy as np
    np.random.seed(42)  # For consistent demo data
    proficiency_data = np.random.randint(20, 95, size=(10, 10))

    # Create heatmap using Plotly
    import plotly.graph_objects as go
    fig = go.Figure(data=go.Heatmap(
        z=proficiency_data,
        x=skills,
        y=skills,
        colorscale='RdYlGn',
        text=[[f'{val}%' for val in row] for row in proficiency_data],
        texttemplate='%{text}',
        textfont={"size": 10},
        hoverongaps=False
    ))

    fig.update_layout(
        title="Skill Inter-relationships & Proficiency Levels",
        xaxis_title="Primary Skills",
        yaxis_title="Related Skills",
        width=800,
        height=600
    )

    st.plotly_chart(fig)

    # Insights section
    st.subheader("💡 Key Insights")

    insights_col1, insights_col2 = st.columns(2)

    with insights_col1:
        st.info("**Interview Prep Focus**: Practice explaining technical concepts in business terms. Focus on STAR format for behavioral questions.")

    with insights_col2:
        st.success("**FinOps Priority**: Every project should include cost analysis. Track cloud spending patterns and optimization opportunities.")

    # Progress summary
    st.subheader("🎯 Current Progress")

    progress_data = {
        "Weeks Completed": f"{weeks_completed}/48 ({weeks_completed/48*100:.1f}%)",
        "Projects Completed": f"{finops_projects}/12 ({finops_projects/12*100:.1f}%)",
        "Interview Questions": f"{st.session_state.get('current_question', 1) - 1}/300 ({(st.session_state.get('current_question', 1) - 1)/300*100:.1f}%)",
        "Total Hours Logged": f"{sum(week.get('hours_logged', 0) for week in st.session_state.get('week_details', {}).values()):.1f}h"
    }

    for metric, value in progress_data.items():
        st.write(f"**{metric}**: {value}")
