# Internal Developer Platform - Backstage + Crossplane
# Terraform configuration for deploying IDP infrastructure

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
    kubectl = {
      source  = "gavinbunney/kubectl"
      version = "~> 1.14"
    }
  }

  backend "s3" {
    bucket         = "idp-terraform-state"
    key            = "idp-platform/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "idp-terraform-lock"
  }
}

provider "aws" {
  region = var.aws_region
}

provider "kubernetes" {
  host                   = module.eks.cluster_endpoint
  cluster_ca_certificate = base64decode(module.eks.cluster_certificate_authority_data)
  token                  = data.aws_eks_cluster_auth.cluster.token
}

provider "helm" {
  kubernetes {
    host                   = module.eks.cluster_endpoint
    cluster_ca_certificate = base64decode(module.eks.cluster_certificate_authority_data)
    token                  = data.aws_eks_cluster_auth.cluster.token
  }
}

provider "kubectl" {
  host                   = module.eks.cluster_endpoint
  cluster_ca_certificate = base64decode(module.eks.cluster_certificate_authority_data)
  token                  = data.aws_eks_cluster_auth.cluster.token
  load_config_file       = false
}

data "aws_eks_cluster_auth" "cluster" {
  name = module.eks.cluster_name
}

# VPC Configuration
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"

  name = "idp-vpc"
  cidr = "10.0.0.0/16"

  azs             = ["${var.aws_region}a", "${var.aws_region}b", "${var.aws_region}c"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]

  enable_nat_gateway   = true
  single_nat_gateway   = true
  enable_dns_hostnames = true

  public_subnet_tags = {
    "kubernetes.io/cluster/${local.cluster_name}" = "shared"
    "kubernetes.io/role/elb"                      = "1"
  }

  private_subnet_tags = {
    "kubernetes.io/cluster/${local.cluster_name}" = "shared"
    "kubernetes.io/role/internal-elb"             = "1"
  }

  tags = local.common_tags
}

# EKS Cluster
module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 19.0"

  cluster_name    = local.cluster_name
  cluster_version = "1.28"

  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets

  # EKS Managed Node Group
  eks_managed_node_groups = {
    idp_nodes = {
      min_size     = 3
      max_size     = 10
      desired_size = 3

      instance_types = ["t3.large"]
      capacity_type  = "ON_DEMAND"

      tags = merge(local.common_tags, {
        "k8s.io/cluster-autoscaler/enabled" = "true"
      })
    }
  }

  # Cluster access entry
  enable_cluster_creator_admin_permissions = true

  tags = local.common_tags
}

# IRSA for Crossplane
module "crossplane_irsa" {
  source  = "terraform-aws-modules/iam/aws//modules/iam-role-for-service-accounts-eks"
  version = "~> 5.0"

  role_name = "crossplane-controller"

  attach_crossplane_controller_policy = true

  oidc_providers = {
    main = {
      provider_arn               = module.eks.oidc_provider_arn
      namespace_service_accounts = ["crossplane-system:crossplane"]
    }
  }

  tags = local.common_tags
}

# IRSA for External DNS
module "external_dns_irsa" {
  source  = "terraform-aws-modules/iam/aws//modules/iam-role-for-service-accounts-eks"
  version = "~> 5.0"

  role_name = "external-dns"

  attach_external_dns_policy = true

  oidc_providers = {
    main = {
      provider_arn               = module.eks.oidc_provider_arn
      namespace_service_accounts = ["external-dns:external-dns"]
    }
  }

  tags = local.common_tags
}

# IRSA for Cert Manager
module "cert_manager_irsa" {
  source  = "terraform-aws-modules/iam/aws//modules/iam-role-for-service-accounts-eks"
  version = "~> 5.0"

  role_name = "cert-manager"

  attach_cert_manager_policy = true

  oidc_providers = {
    main = {
      provider_arn               = module.eks.oidc_provider_arn
      namespace_service_accounts = ["cert-manager:cert-manager"]
    }
  }

  tags = local.common_tags
}

# RDS for Backstage Database
resource "aws_db_subnet_group" "backstage" {
  name       = "backstage-db-subnet"
  subnet_ids = module.vpc.private_subnets

  tags = local.common_tags
}

resource "aws_security_group" "backstage_db" {
  name   = "backstage-db"
  vpc_id = module.vpc.vpc_id

  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.backstage_app.id]
  }

  tags = local.common_tags
}

resource "aws_db_instance" "backstage" {
  identifier = "backstage-db"

  engine         = "postgres"
  engine_version = "15.4"
  instance_class = "db.t3.micro"

  db_name  = "backstage"
  username = "backstage"
  password = random_password.backstage_db_password.result

  db_subnet_group_name   = aws_db_subnet_group.backstage.name
  vpc_security_group_ids = [aws_security_group.backstage_db.id]

  allocated_storage     = 20
  max_allocated_storage = 100
  storage_encrypted     = true

  backup_retention_period = 7
  skip_final_snapshot     = true

  tags = local.common_tags
}

resource "random_password" "backstage_db_password" {
  length  = 32
  special = true
}

# S3 Bucket for Backstage TechDocs
resource "aws_s3_bucket" "backstage_techdocs" {
  bucket = "idp-backstage-techdocs-${random_string.bucket_suffix.result}"

  tags = local.common_tags
}

resource "aws_s3_bucket_versioning" "backstage_techdocs" {
  bucket = aws_s3_bucket.backstage_techdocs.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "backstage_techdocs" {
  bucket = aws_s3_bucket.backstage_techdocs.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "random_string" "bucket_suffix" {
  length  = 8
  lower   = true
  upper   = false
  numeric = true
  special = false
}

# Security Group for Backstage Application
resource "aws_security_group" "backstage_app" {
  name   = "backstage-app"
  vpc_id = module.vpc.vpc_id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = local.common_tags
}

# ACM Certificate for HTTPS
resource "aws_acm_certificate" "backstage" {
  domain_name       = var.backstage_domain
  validation_method = "DNS"

  tags = local.common_tags
}

# Route 53 Zone (assuming it exists)
data "aws_route53_zone" "backstage" {
  name = var.route53_zone_name
}

resource "aws_route53_record" "backstage_cert_validation" {
  for_each = {
    for dvo in aws_acm_certificate.backstage.domain_validation_options : dvo.domain_name => {
      name   = dvo.resource_record_name
      record = dvo.resource_record_value
      type   = dvo.resource_record_type
    }
  }

  allow_overwrite = true
  name            = each.value.name
  records         = [each.value.record]
  ttl             = 60
  type            = each.value.type
  zone_id         = data.aws_route53_zone.backstage.zone_id
}

resource "aws_acm_certificate_validation" "backstage" {
  certificate_arn         = aws_acm_certificate.backstage.arn
  validation_record_fqdns = [for record in aws_route53_record.backstage_cert_validation : record.fqdn]
}

# Crossplane Installation
resource "helm_release" "crossplane" {
  name             = "crossplane"
  repository       = "https://charts.crossplane.io/stable"
  chart            = "crossplane"
  version          = "1.14.0"
  namespace        = "crossplane-system"
  create_namespace = true

  set {
    name  = "args"
    value = "{--enable-external-secret-stores}"
  }

  set {
    name  = "serviceAccount.name"
    value = "crossplane"
  }

  depends_on = [module.eks]
}

# Crossplane AWS Provider
resource "helm_release" "crossplane_aws_provider" {
  name             = "crossplane-aws-provider"
  repository       = "https://charts.crossplane.io/stable"
  chart            = "provider-aws"
  version          = "0.44.0"
  namespace        = "crossplane-system"

  depends_on = [helm_release.crossplane]
}

# Crossplane Azure Provider
resource "helm_release" "crossplane_azure_provider" {
  name             = "crossplane-azure-provider"
  repository       = "https://charts.crossplane.io/stable"
  chart            = "provider-azure"
  version          = "0.40.0"
  namespace        = "crossplane-system"

  depends_on = [helm_release.crossplane]
}

# Crossplane GCP Provider
resource "helm_release" "crossplane_gcp_provider" {
  name             = "crossplane-gcp-provider"
  repository       = "https://charts.crossplane.io/stable"
  chart            = "provider-gcp"
  version          = "0.40.0"
  namespace        = "crossplane-system"

  depends_on = [helm_release.crossplane]
}

# Cert Manager
resource "helm_release" "cert_manager" {
  name             = "cert-manager"
  repository       = "https://charts.jetstack.io"
  chart            = "cert-manager"
  version          = "v1.13.2"
  namespace        = "cert-manager"
  create_namespace = true

  set {
    name  = "installCRDs"
    value = "true"
  }

  set {
    name  = "serviceAccount.name"
    value = "cert-manager"
  }

  depends_on = [module.eks]
}

# External DNS
resource "helm_release" "external_dns" {
  name             = "external-dns"
  repository       = "https://kubernetes-sigs.github.io/external-dns"
  chart            = "external-dns"
  version          = "1.13.1"
  namespace        = "external-dns"
  create_namespace = true

  set {
    name  = "serviceAccount.name"
    value = "external-dns"
  }

  set {
    name  = "domainFilters[0]"
    value = var.route53_zone_name
  }

  set {
    name  = "policy"
    value = "sync"
  }

  set {
    name  = "txtOwnerId"
    value = "idp-platform"
  }

  depends_on = [module.eks]
}

# ArgoCD for GitOps
resource "helm_release" "argocd" {
  name             = "argocd"
  repository       = "https://argoproj.github.io/argo-helm"
  chart            = "argo-cd"
  version          = "5.51.6"
  namespace        = "argocd"
  create_namespace = true

  values = [
    yamlencode({
      server = {
        service = {
          type = "LoadBalancer"
        }
        ingress = {
          enabled = true
          annotations = {
            "kubernetes.io/ingress.class"                    = "alb"
            "alb.ingress.kubernetes.io/scheme"               = "internet-facing"
            "alb.ingress.kubernetes.io/target-type"          = "ip"
            "alb.ingress.kubernetes.io/certificate-arn"      = aws_acm_certificate.backstage.arn
            "alb.ingress.kubernetes.io/listen-ports"         = "[{\"HTTPS\":443}]"
            "alb.ingress.kubernetes.io/ssl-redirect"         = "443"
          }
          hosts = [
            {
              host = "argocd.${var.backstage_domain}"
              paths = ["/"]
            }
          ]
        }
      }
    })
  ]

  depends_on = [module.eks]
}

# Backstage Application
resource "helm_release" "backstage" {
  name             = "backstage"
  repository       = "https://backstage.github.io/charts"
  chart            = "backstage"
  version          = "1.14.0"
  namespace        = "backstage"
  create_namespace = true

  values = [
    yamlencode({
      backstage = {
        image = {
          registry = "docker.io"
          repository = "backstage/backstage"
          tag = "latest"
        }
        command = ["node", "packages/backend", "--config", "app-config.yaml"]
        extraEnvVars = [
          {
            name = "POSTGRES_HOST"
            value = aws_db_instance.backstage.address
          },
          {
            name = "POSTGRES_PORT"
            value = "5432"
          },
          {
            name = "POSTGRES_USER"
            value = aws_db_instance.backstage.username
          },
          {
            name = "POSTGRES_PASSWORD"
            valueFrom = {
              secretKeyRef = {
                name = "backstage-db-secret"
                key = "password"
              }
            }
          },
          {
            name = "TECHDOCS_S3_BUCKET_NAME"
            value = aws_s3_bucket.backstage_techdocs.bucket
          }
        ]
        extraVolumeMounts = [
          {
            name = "backstage-config"
            mountPath = "/app/app-config.yaml"
            subPath = "app-config.yaml"
          }
        ]
        extraVolumes = [
          {
            name = "backstage-config"
            configMap = {
              name = "backstage-config"
            }
          }
        ]
      }
      service = {
        type = "ClusterIP"
        port = 7007
      }
      ingress = {
        enabled = true
        className = "alb"
        annotations = {
          "kubernetes.io/ingress.class"                    = "alb"
          "alb.ingress.kubernetes.io/scheme"               = "internet-facing"
          "alb.ingress.kubernetes.io/target-type"          = "ip"
          "alb.ingress.kubernetes.io/certificate-arn"      = aws_acm_certificate.backstage.arn
          "alb.ingress.kubernetes.io/listen-ports"         = "[{\"HTTPS\":443}]"
          "alb.ingress.kubernetes.io/ssl-redirect"         = "443"
        }
        hosts = [
          {
            host = var.backstage_domain
            paths = [
              {
                path = "/"
                pathType = "Prefix"
              }
            ]
          }
        ]
      }
    })
  ]

  depends_on = [module.eks, aws_db_instance.backstage]
}

# Backstage Configuration
resource "kubernetes_config_map" "backstage_config" {
  metadata {
    name      = "backstage-config"
    namespace = "backstage"
  }

  data = {
    "app-config.yaml" = yamlencode({
      app = {
        title = "Internal Developer Platform"
        baseUrl = "https://${var.backstage_domain}"
      }
      backend = {
        baseUrl = "https://${var.backstage_domain}"
        listen = {
          port = 7007
        }
        database = {
          client = "pg"
          connection = {
            host = "$${POSTGRES_HOST}"
            port = "$${POSTGRES_PORT}"
            user = "$${POSTGRES_USER}"
            password = "$${POSTGRES_PASSWORD}"
          }
        }
      }
      techdocs = {
        builder = "external"
        generator = {
          runIn = "docker"
        }
        publisher = {
          type = "awsS3"
          awsS3 = {
            bucketName = "$${TECHDOCS_S3_BUCKET_NAME}"
            region = var.aws_region
          }
        }
      }
      auth = {
        environment = "production"
        providers = {
          github = {
            development = {
              clientId = "$${AUTH_GITHUB_CLIENT_ID}"
              clientSecret = "$${AUTH_GITHUB_CLIENT_SECRET}"
            }
          }
        }
      }
      catalog = {
        locations = [
          {
            type = "url"
            target = "https://github.com/${var.github_org}/backstage-catalog/blob/main/catalog-info.yaml"
          }
        ]
      }
      integrations = {
        github = [
          {
            host = "github.com"
            token = "$${GITHUB_TOKEN}"
          }
        ]
      }
    })
  }

  depends_on = [helm_release.backstage]
}

# Backstage Database Secret
resource "kubernetes_secret" "backstage_db_secret" {
  metadata {
    name      = "backstage-db-secret"
    namespace = "backstage"
  }

  data = {
    password = random_password.backstage_db_password.result
  }

  type = "Opaque"

  depends_on = [helm_release.backstage]
}

# Crossplane Providers Configuration
resource "kubectl_manifest" "aws_provider_config" {
  yaml_body = yamlencode({
    apiVersion = "aws.crossplane.io/v1beta1"
    kind       = "ProviderConfig"
    metadata = {
      name = "aws-provider"
    }
    spec = {
      credentials = {
        source = "IRSA"
        irsa = {
          roleArn = module.crossplane_irsa.iam_role_arn
        }
      }
    }
  })

  depends_on = [helm_release.crossplane_aws_provider]
}

# Route 53 Record for Backstage
resource "aws_route53_record" "backstage" {
  zone_id = data.aws_route53_zone.backstage.zone_id
  name    = var.backstage_domain
  type    = "A"

  alias {
    name                   = data.kubernetes_ingress_v1.backstage.status.0.load_balancer.0.ingress.0.hostname
    zone_id                = "Z1D633PJN98FT9"  # ALB zone ID for us-east-1
    evaluate_target_health = true
  }

  depends_on = [helm_release.backstage]
}

data "kubernetes_ingress_v1" "backstage" {
  metadata {
    name      = "backstage"
    namespace = "backstage"
  }

  depends_on = [helm_release.backstage]
}

# Outputs
output "backstage_url" {
  description = "URL of the Backstage IDP"
  value       = "https://${var.backstage_domain}"
}

output "argocd_url" {
  description = "URL of the ArgoCD dashboard"
  value       = "https://argocd.${var.backstage_domain}"
}

output "cluster_name" {
  description = "EKS cluster name"
  value       = module.eks.cluster_name
}

output "crossplane_version" {
  description = "Crossplane version"
  value       = helm_release.crossplane.version
}

# Locals
locals {
  cluster_name = "idp-platform"
  common_tags = {
    Environment = "production"
    Project     = "IDP"
    ManagedBy   = "Terraform"
  }
}