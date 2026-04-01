# Internal Developer Platform (IDP)

This repository contains the infrastructure-as-code for deploying a comprehensive Internal Developer Platform using Backstage and Crossplane.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    Internal Developer Platform                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   Backstage     │  │   Crossplane    │  │    ArgoCD       │ │
│  │  (Developer     │  │ (Infrastructure │  │  (GitOps)      │ │
│  │   Portal)       │  │   as Code)      │  │                 │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
│           │                       │                   │         │
│           └───────────────────────┼───────────────────┘         │
│                                   │                             │
│                    ┌──────────────┴──────────────┐              │
│                    │     Kubernetes Cluster      │              │
│                    │     (AWS EKS / Azure AKS /  │              │
│                    │      GCP GKE)               │              │
│                    └─────────────────────────────┘              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Components

### Backstage (Developer Portal)
- **Service Catalog**: Centralized catalog of all services, APIs, and resources
- **Software Templates**: Golden path templates for creating new services
- **TechDocs**: Documentation site for all services
- **Cost Insights**: Cloud cost visibility and optimization recommendations
- **Kubernetes Plugin**: Direct access to Kubernetes resources
- **ArgoCD Plugin**: GitOps deployment visibility

### Crossplane (Infrastructure as Code)
- **Multi-Cloud Support**: AWS, Azure, GCP providers
- **Infrastructure Provisioning**: Declarative infrastructure management
- **Policy Enforcement**: Governance and compliance automation
- **Self-Service**: Developer self-provisioning of infrastructure

### ArgoCD (GitOps)
- **Application Delivery**: Declarative application deployment
- **Multi-Environment**: Automated promotion across environments
- **Drift Detection**: Automatic reconciliation of desired vs actual state
- **Rollback Capability**: Instant rollback to previous versions

## Prerequisites

- AWS Account with appropriate permissions
- Route 53 hosted zone
- GitHub organization for catalog and templates
- Docker registry access

## Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-org/idp-platform.git
   cd idp-platform
   ```

2. **Configure variables**
   ```bash
   cp terraform.tfvars.example terraform.tfvars
   # Edit terraform.tfvars with your values
   ```

3. **Deploy the platform**
   ```bash
   terraform init
   terraform plan
   terraform apply
   ```

4. **Access the platform**
   - Backstage: https://idp.yourdomain.com
   - ArgoCD: https://argocd.yourdomain.com

## Configuration

### Backstage Configuration
- Edit `backstage-config.yaml` for application settings
- Configure authentication providers (GitHub OAuth)
- Set up integrations (GitHub, Kubernetes, ArgoCD)

### Crossplane Configuration
- Provider credentials stored in Kubernetes secrets
- IRSA for AWS provider authentication
- Service account keys for Azure/GCP providers

### ArgoCD Configuration
- Admin password stored in Kubernetes secret
- SSO integration with organizational identity provider
- Repository credentials for private Git repositories

## Development Workflow

1. **Service Creation**: Use Backstage software templates
2. **Infrastructure Provisioning**: Create Crossplane resources
3. **Code Deployment**: Push to Git, ArgoCD auto-deploys
4. **Monitoring**: Use Backstage plugins for observability

## Security Considerations

- **Network Security**: VPC isolation, security groups, network policies
- **Access Control**: RBAC, IRSA, service account permissions
- **Secret Management**: AWS Secrets Manager, Kubernetes secrets
- **Compliance**: Audit logging, compliance monitoring

## Cost Optimization

- **Right-sizing**: Automated instance optimization
- **Reserved Instances**: RI recommendations and purchasing
- **Spot Instances**: Interruptible workload optimization
- **Storage Tiering**: Cost-effective data storage

## Monitoring & Observability

- **Platform Monitoring**: Prometheus, Grafana dashboards
- **Application Monitoring**: Distributed tracing, error tracking
- **Cost Monitoring**: Real-time spending visibility
- **Performance Monitoring**: SLO tracking and alerting

## Troubleshooting

### Common Issues

1. **Backstage not accessible**
   - Check ALB health checks
   - Verify SSL certificate status
   - Check application logs

2. **Crossplane provider issues**
   - Verify IRSA role permissions
   - Check provider pod logs
   - Validate credentials

3. **ArgoCD sync failures**
   - Check repository connectivity
   - Verify manifest syntax
   - Review application events

### Logs and Debugging

```bash
# Backstage logs
kubectl logs -n backstage deployment/backstage

# Crossplane logs
kubectl logs -n crossplane-system deployment/crossplane

# ArgoCD logs
kubectl logs -n argocd deployment/argocd-server
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.