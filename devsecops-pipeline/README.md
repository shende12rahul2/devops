# DevSecOps Pipeline with OPA Admission Control

This DevSecOps pipeline implements comprehensive security automation with Open Policy Agent (OPA) for Kubernetes admission control, ensuring zero-trust deployment practices across the entire software delivery lifecycle.

## Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Source Code   │───▶│  Security Scan  │───▶│   Build & Test  │
│                 │    │                 │    │                 │
│ • SAST          │    │ • SonarQube     │    │ • Unit Tests    │
│ • SCA           │    │ • Dependency    │    │ • Integration   │
│ • Secret Scan   │    │   Check         │    │ • Coverage      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│Container Security│───▶│ Policy Check   │───▶│Infrastructure   │
│                 │    │                 │    │                 │
│ • Trivy         │    │ • OPA Validation│    │ • Terraform     │
│ • Dockle        │    │ • Compliance    │    │ • Terratest     │
│ • Image Signing │    │ • Admission Ctrl│    │ • Validation    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Staging Deploy │───▶│Prod Deployment │───▶│  Compliance     │
│                 │    │                 │    │                 │
│ • Smoke Tests   │    │ • ArgoCD        │    │ • SBOM          │
│ • DAST          │    │ • Canary        │    │ • Audit Report  │
│ • Validation    │    │ • Rollback      │    │ • Notifications │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Key Components

### 1. Security Scanning
- **SAST**: Static Application Security Testing using SonarQube
- **SCA**: Software Composition Analysis with OWASP Dependency Check
- **Secret Scanning**: TruffleHog for detecting exposed secrets
- **Container Security**: Trivy and Dockle for vulnerability scanning
- **DAST**: Dynamic Application Security Testing with OWASP ZAP

### 2. Policy Enforcement
- **OPA Admission Controller**: Kubernetes admission control with Rego policies
- **Infrastructure Compliance**: Terraform plan validation against security policies
- **Container Image Policies**: Image signing and vulnerability checks
- **RBAC Policies**: Least privilege access control validation

### 3. Infrastructure as Code
- **Terraform Validation**: Format checking and security policy validation
- **Terratest**: Infrastructure testing framework
- **Compliance Checks**: Automated compliance validation for PCI-DSS, HIPAA, GDPR

### 4. Deployment Automation
- **ArgoCD**: GitOps deployment with progressive delivery
- **Canary Deployments**: Risk-free production releases
- **Automated Rollbacks**: Failure detection and automatic recovery
- **Health Checks**: Comprehensive application validation

## OPA Policies

### Kubernetes Security Policies (`policy/kubernetes-security.rego`)
- Privileged container prevention
- Root user restrictions
- Host access controls
- Resource limit enforcement
- Image security validation
- Network policy requirements
- Compliance labeling

### Infrastructure Policies (`policy/terraform-compliance.rego`)
- Cloud resource security
- Encryption requirements
- Access control validation
- Cost optimization rules
- Compliance tagging
- Multi-region requirements

## Prerequisites

### Required Tools
- Docker & Docker Compose
- Kubernetes cluster (v1.24+)
- Helm 3.x
- Terraform 1.5+
- GitHub CLI
- Open Policy Agent (OPA)

### Required Secrets
Set these in your GitHub repository secrets:
```
SONAR_TOKEN
SONAR_HOST_URL
SLACK_WEBHOOK_URL
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
COSIGN_PRIVATE_KEY
COSIGN_PASSWORD
DEPENDENCY_TRACK_URL
DEPENDENCY_TRACK_API_KEY
```

## Installation

### 1. Deploy OPA Admission Controller

```bash
# Deploy OPA to Kubernetes
kubectl apply -f k8s/opa-admission-controller.yaml

# Verify deployment
kubectl get pods -n opa
kubectl get validatingwebhookconfigurations
```

### 2. Configure GitHub Actions

The pipeline is defined in `.github/workflows/devsecops-pipeline.yml`. Ensure all required secrets are configured in your repository settings.

### 3. Setup Monitoring

```bash
# Deploy Prometheus and Grafana for monitoring
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install prometheus prometheus-community/prometheus

# Access Grafana
kubectl port-forward svc/prometheus-grafana 3000:80
# Default credentials: admin/prom-operator
```

## Usage

### Running the Pipeline

1. **Push to develop branch**: Triggers security scanning and staging deployment
2. **Create pull request**: Runs full security validation
3. **Merge to main**: Executes production deployment with compliance checks

### Policy Validation

```bash
# Test OPA policies locally
opa eval --data policy/ --input k8s/sample-deployment.yaml data.main.deny

# Validate Terraform plans
terraform plan -out=tfplan.binary
terraform show -json tfplan.binary > tfplan.json
opa eval --data policy/ --input tfplan.json data.terraform.deny
```

### Monitoring and Alerts

The pipeline integrates with:
- **Prometheus**: Metrics collection and alerting
- **Grafana**: Dashboard visualization
- **Slack**: Real-time notifications
- **Dependency Track**: SBOM management and vulnerability tracking

## Security Policies

### Container Security
- Non-root user execution
- Read-only root filesystem
- Minimal capabilities
- Resource limits and requests
- Image vulnerability scanning
- Image signing verification

### Network Security
- Network policies for all namespaces
- Service mesh integration
- Encrypted communications
- Firewall rules validation

### Access Control
- RBAC policy validation
- Service account restrictions
- Secret management policies
- Least privilege enforcement

### Compliance Requirements
- PCI-DSS labeling and validation
- HIPAA compliance checks
- GDPR data protection rules
- SOX audit trail requirements

## Troubleshooting

### Common Issues

1. **OPA Admission Controller Denies Deployment**
   ```bash
   # Check OPA logs
   kubectl logs -n opa deployment/opa

   # Test policy evaluation
   opa eval --data policy/ --input <your-manifest.yaml> data.main.deny
   ```

2. **Pipeline Security Scan Failures**
   - Check SonarQube configuration
   - Verify secret scanning exclusions
   - Review dependency vulnerabilities

3. **Container Image Issues**
   ```bash
   # Scan image manually
   trivy image <your-image>

   # Check image signing
   cosign verify <your-image>
   ```

### Debugging Commands

```bash
# Check webhook status
kubectl get validatingwebhookconfigurations

# View admission controller logs
kubectl logs -n opa -l app=opa

# Test policy against manifest
kubectl apply --dry-run=server -f <manifest.yaml>

# Check pipeline status
gh run list --workflow=devsecops-pipeline.yml
```

## Integration with Rightsizing Engine

This DevSecOps pipeline integrates with the Automated Rightsizing Engine for cost-optimized deployments:

```yaml
# Example: Cost-aware deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  annotations:
    rightsizing-engine/cost-optimization: "enabled"
    rightsizing-engine/max-cost-per-month: "500"
spec:
  template:
    metadata:
      annotations:
        rightsizing-engine/recommendation: "accepted"
```

## Compliance Reporting

The pipeline generates comprehensive compliance reports including:
- Security scan results
- Policy validation outcomes
- Infrastructure compliance status
- SBOM (Software Bill of Materials)
- Audit trails and evidence

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new policies
4. Update documentation
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue in the repository
- Check the troubleshooting guide
- Review OPA policy documentation
- Consult the security team for policy exceptions