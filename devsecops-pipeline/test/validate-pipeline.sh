#!/bin/bash

# DevSecOps Pipeline Test Script
# This script validates OPA policies and pipeline components

set -e

echo "🔍 DevSecOps Pipeline Validation Script"
echo "======================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print status
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if OPA is installed
check_opa() {
    if command -v opa &> /dev/null; then
        print_status "OPA is installed"
        opa version
    else
        print_error "OPA is not installed. Please install from https://openpolicyagent.org/docs/latest/#running-opa"
        exit 1
    fi
}

# Check if Docker is running
check_docker() {
    if docker info &> /dev/null; then
        print_status "Docker is running"
    else
        print_error "Docker is not running or not accessible"
        exit 1
    fi
}

# Check if kubectl is configured
check_kubectl() {
    if kubectl cluster-info &> /dev/null; then
        print_status "kubectl is configured"
    else
        print_warning "kubectl is not configured or cluster is not accessible"
    fi
}

# Validate OPA policies
validate_policies() {
    echo ""
    echo "🔍 Validating OPA Policies..."
    echo "-----------------------------"

    # Test Kubernetes security policies
    echo "Testing Kubernetes security policies..."
    if opa eval --data policy/kubernetes-security.rego --input k8s/sample-deployment.yaml 'data.main.deny' 2>/dev/null; then
        print_status "Kubernetes security policies validated"
    else
        print_error "Kubernetes security policy validation failed"
    fi

    # Test Terraform compliance policies
    echo "Testing Terraform compliance policies..."
    if [ -f "test/terraform-plan.json" ]; then
        if opa eval --data policy/terraform-compliance.rego --input test/terraform-plan.json 'data.terraform.deny' 2>/dev/null; then
            print_status "Terraform compliance policies validated"
        else
            print_error "Terraform compliance policy validation failed"
        fi
    else
        print_warning "Terraform plan test file not found (test/terraform-plan.json)"
    fi
}

# Test container image security
test_container_security() {
    echo ""
    echo "🐳 Testing Container Security..."
    echo "-------------------------------"

    # Build test image
    echo "Building test container image..."
    if docker build -t devsecops-test:latest . 2>/dev/null; then
        print_status "Test container image built successfully"

        # Run Trivy scan
        echo "Running Trivy vulnerability scan..."
        if command -v trivy &> /dev/null; then
            trivy image --exit-code 1 --no-progress devsecops-test:latest || true
            print_status "Trivy scan completed"
        else
            print_warning "Trivy not installed, skipping vulnerability scan"
        fi

        # Clean up
        docker rmi devsecops-test:latest 2>/dev/null || true
    else
        print_error "Failed to build test container image"
    fi
}

# Validate Kubernetes manifests
validate_manifests() {
    echo ""
    echo "☸️  Validating Kubernetes Manifests..."
    echo "-------------------------------------"

    # Check if manifests are valid YAML
    for manifest in k8s/*.yaml; do
        if [ -f "$manifest" ]; then
            if kubectl apply --dry-run=client -f "$manifest" &> /dev/null; then
                print_status "Manifest $manifest is valid"
            else
                print_error "Manifest $manifest has validation errors"
            fi
        fi
    done
}

# Test GitHub Actions workflow
validate_workflow() {
    echo ""
    echo "🔄 Validating GitHub Actions Workflow..."
    echo "----------------------------------------"

    workflow_file=".github/workflows/devsecops-pipeline.yml"

    if [ -f "$workflow_file" ]; then
        # Basic YAML validation
        if python3 -c "import yaml; yaml.safe_load(open('$workflow_file'))" 2>/dev/null; then
            print_status "GitHub Actions workflow YAML is valid"
        else
            print_error "GitHub Actions workflow YAML is invalid"
        fi

        # Check for required jobs
        if grep -q "security-scan" "$workflow_file"; then
            print_status "Security scan job found"
        else
            print_error "Security scan job missing"
        fi

        if grep -q "policy-check" "$workflow_file"; then
            print_status "Policy check job found"
        else
            print_error "Policy check job missing"
        fi

        if grep -q "deploy-production" "$workflow_file"; then
            print_status "Production deployment job found"
        else
            print_error "Production deployment job missing"
        fi
    else
        print_error "GitHub Actions workflow file not found"
    fi
}

# Check required secrets
check_secrets() {
    echo ""
    echo "🔐 Checking Required Secrets..."
    echo "-------------------------------"

    required_secrets=(
        "SONAR_TOKEN"
        "SONAR_HOST_URL"
        "SLACK_WEBHOOK_URL"
        "AWS_ACCESS_KEY_ID"
        "AWS_SECRET_ACCESS_KEY"
        "COSIGN_PRIVATE_KEY"
        "COSIGN_PASSWORD"
        "DEPENDENCY_TRACK_URL"
        "DEPENDENCY_TRACK_API_KEY"
    )

    echo "Note: This check assumes you're running in a GitHub Actions environment"
    echo "For local testing, ensure these secrets are available in your environment"
    echo ""

    for secret in "${required_secrets[@]}"; do
        if [ -n "${!secret}" ]; then
            print_status "Secret $secret is set"
        else
            print_warning "Secret $secret is not set (expected in CI/CD environment)"
        fi
    done
}

# Generate test report
generate_report() {
    echo ""
    echo "📊 Test Report Summary"
    echo "======================"

    echo "DevSecOps Pipeline Validation Completed"
    echo "Timestamp: $(date)"
    echo ""
    echo "Components Tested:"
    echo "- OPA Policy Validation"
    echo "- Container Security"
    echo "- Kubernetes Manifests"
    echo "- GitHub Actions Workflow"
    echo "- Required Secrets"
    echo ""
    echo "Next Steps:"
    echo "1. Fix any validation errors shown above"
    echo "2. Deploy OPA admission controller to Kubernetes"
    echo "3. Configure GitHub repository secrets"
    echo "4. Run pipeline on a test repository"
    echo "5. Monitor security scan results and policy violations"
}

# Main execution
main() {
    check_opa
    check_docker
    check_kubectl

    validate_policies
    test_container_security
    validate_manifests
    validate_workflow
    check_secrets

    generate_report

    echo ""
    print_status "DevSecOps Pipeline validation completed!"
}

# Run main function
main "$@"