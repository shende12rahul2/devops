variable "aws_region" {
  description = "AWS region for the IDP platform"
  type        = string
  default     = "us-east-1"
}

variable "backstage_domain" {
  description = "Domain name for Backstage IDP"
  type        = string
  default     = "idp.example.com"
}

variable "route53_zone_name" {
  description = "Route 53 hosted zone name"
  type        = string
  default     = "example.com"
}

variable "github_org" {
  description = "GitHub organization for Backstage catalog"
  type        = string
  default     = "my-org"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "production"
}

variable "cluster_name" {
  description = "EKS cluster name"
  type        = string
  default     = "idp-platform"
}

variable "kubernetes_version" {
  description = "Kubernetes version for EKS"
  type        = string
  default     = "1.28"
}

variable "node_group_desired_size" {
  description = "Desired number of nodes in the node group"
  type        = number
  default     = 3
}

variable "node_group_max_size" {
  description = "Maximum number of nodes in the node group"
  type        = number
  default     = 10
}

variable "node_group_min_size" {
  description = "Minimum number of nodes in the node group"
  type        = number
  default     = 3
}

variable "node_instance_types" {
  description = "Instance types for EKS nodes"
  type        = list(string)
  default     = ["t3.large"]
}