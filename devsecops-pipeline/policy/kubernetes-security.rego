package main

import data.kubernetes

# Deny privileged containers
deny_privileged[msg] {
    input.kind == "Pod"
    container := input.spec.containers[_]
    container.securityContext.privileged == true
    msg := sprintf("Privileged container not allowed: %s", [container.name])
}

# Deny containers running as root
deny_root_user[msg] {
    input.kind == "Pod"
    container := input.spec.containers[_]
    not container.securityContext.runAsNonRoot == true
    not container.securityContext.runAsUser >= 1000
    msg := sprintf("Container must not run as root: %s", [container.name])
}

# Deny containers with host network access
deny_host_network[msg] {
    input.kind == "Pod"
    input.spec.hostNetwork == true
    msg := "Host network access not allowed"
}

# Deny containers with host PID access
deny_host_pid[msg] {
    input.kind == "Pod"
    input.spec.hostPID == true
    msg := "Host PID access not allowed"
}

# Deny containers with host IPC access
deny_host_ipc[msg] {
    input.kind == "Pod"
    input.spec.hostIPC == true
    msg := "Host IPC access not allowed"
}

# Deny containers with dangerous capabilities
deny_dangerous_capabilities[msg] {
    input.kind == "Pod"
    container := input.spec.containers[_]
    capability := container.securityContext.capabilities.add[_]
    dangerous_caps := {"NET_ADMIN", "SYS_ADMIN", "SYS_PTRACE", "SYS_MODULE"}
    dangerous_caps[capability]
    msg := sprintf("Dangerous capability not allowed: %s in container %s", [capability, container.name])
}

# Require resource limits
require_resource_limits[msg] {
    input.kind == "Pod"
    container := input.spec.containers[_]
    not container.resources.limits
    msg := sprintf("Resource limits required for container: %s", [container.name])
}

# Require resource requests
require_resource_requests[msg] {
    input.kind == "Pod"
    container := input.spec.containers[_]
    not container.resources.requests
    msg := sprintf("Resource requests required for container: %s", [container.name])
}

# Deny latest tag usage
deny_latest_tag[msg] {
    input.kind == "Pod"
    container := input.spec.containers[_]
    endswith(container.image, ":latest")
    msg := sprintf("Latest tag not allowed: %s", [container.image])
}

# Require image pull policy
require_image_pull_policy[msg] {
    input.kind == "Pod"
    container := input.spec.containers[_]
    not container.imagePullPolicy
    msg := sprintf("Image pull policy required for container: %s", [container.name])
}

# Deny hostPath volumes
deny_hostpath_volumes[msg] {
    input.kind == "Pod"
    volume := input.spec.volumes[_]
    volume.hostPath
    msg := sprintf("HostPath volumes not allowed: %s", [volume.name])
}

# Require probes for production workloads
require_probes[msg] {
    input.kind == "Pod"
    input.metadata.namespace == "production"
    container := input.spec.containers[_]
    not container.livenessProbe
    msg := sprintf("Liveness probe required for production container: %s", [container.name])
}

# Require probes for production workloads (readiness)
require_readiness_probes[msg] {
    input.kind == "Pod"
    input.metadata.namespace == "production"
    container := input.spec.containers[_]
    not container.readinessProbe
    msg := sprintf("Readiness probe required for production container: %s", [container.name])
}

# Deny secrets in environment variables
deny_env_secrets[msg] {
    input.kind == "Pod"
    container := input.spec.containers[_]
    env := container.env[_]
    env.valueFrom.secretKeyRef
    msg := sprintf("Secrets should not be exposed as environment variables: %s in container %s", [env.name, container.name])
}

# Require labels for organization
require_labels[msg] {
    input.kind == "Pod"
    required_labels := {"app", "version", "environment"}
    label := required_labels[_]
    not input.metadata.labels[label]
    msg := sprintf("Required label missing: %s", [label])
}

# Require annotations for tracking
require_annotations[msg] {
    input.kind == "Pod"
    required_annotations := {"deployment.kubernetes.io/revision", "kubectl.kubernetes.io/restartedAt"}
    annotation := required_annotations[_]
    not input.metadata.annotations[annotation]
    msg := sprintf("Required annotation missing: %s", [annotation])
}

# Deny deprecated API versions
deny_deprecated_api[msg] {
    deprecated_apis := {
        "extensions/v1beta1",
        "apps/v1beta1",
        "apps/v1beta2"
    }
    deprecated_apis[input.apiVersion]
    msg := sprintf("Deprecated API version not allowed: %s", [input.apiVersion])
}

# Require network policies
require_network_policy[msg] {
    input.kind == "Pod"
    input.metadata.namespace == "production"
    not data.kubernetes.networkpolicies[input.metadata.namespace]
    msg := sprintf("Network policy required for production namespace: %s", [input.metadata.namespace])
}

# Deny privileged service accounts
deny_privileged_service_account[msg] {
    input.kind == "Pod"
    input.spec.serviceAccountName
    service_account := data.kubernetes.serviceaccounts[input.spec.serviceAccountName]
    service_account.automountServiceAccountToken == true
    msg := sprintf("Privileged service account not allowed: %s", [input.spec.serviceAccountName])
}

# Require pod disruption budget for production
require_pdb[msg] {
    input.kind == "Pod"
    input.metadata.namespace == "production"
    not data.kubernetes.poddisruptionbudgets[input.metadata.name]
    msg := sprintf("Pod disruption budget required for production workload: %s", [input.metadata.name])
}

# Deny containers with writable root filesystem
deny_writable_rootfs[msg] {
    input.kind == "Pod"
    container := input.spec.containers[_]
    container.securityContext.readOnlyRootFilesystem == false
    msg := sprintf("Read-only root filesystem required for container: %s", [container.name])
}

# Require security context at pod level
require_pod_security_context[msg] {
    input.kind == "Pod"
    not input.spec.securityContext
    msg := "Pod security context required"
}

# Deny containers with allowPrivilegeEscalation
deny_privilege_escalation[msg] {
    input.kind == "Pod"
    container := input.spec.containers[_]
    container.securityContext.allowPrivilegeEscalation == true
    msg := sprintf("Privilege escalation not allowed for container: %s", [container.name])
}

# Require CPU and memory limits within bounds
validate_resource_limits[msg] {
    input.kind == "Pod"
    container := input.spec.containers[_]
    limits := container.resources.limits

    # CPU limit validation (max 4 cores)
    cpu_limit := to_number(limits.cpu)
    cpu_limit > 4

    msg := sprintf("CPU limit too high for container %s: %v cores (max 4)", [container.name, cpu_limit])
}

validate_memory_limits[msg] {
    input.kind == "Pod"
    container := input.spec.containers[_]
    limits := container.resources.limits

    # Memory limit validation (max 8Gi)
    memory_limit := to_number(limits.memory)
    memory_limit > 8 * 1024 * 1024 * 1024  # 8Gi in bytes

    msg := sprintf("Memory limit too high for container %s: %v bytes (max 8Gi)", [container.name, memory_limit])
}

# Require image scanning results
require_image_scan[msg] {
    input.kind == "Pod"
    container := input.spec.containers[_]
    not data.vulnerability.scans[container.image]
    msg := sprintf("Image must be scanned for vulnerabilities: %s", [container.image])
}

# Deny high-severity vulnerabilities
deny_high_severity_vulns[msg] {
    input.kind == "Pod"
    container := input.spec.containers[_]
    scan := data.vulnerability.scans[container.image]
    vuln := scan.vulnerabilities[_]
    vuln.severity == "CRITICAL"
    msg := sprintf("Critical vulnerability found in image %s: %s", [container.image, vuln.id])
}

# Require compliance labels
require_compliance_labels[msg] {
    input.kind == "Pod"
    input.metadata.namespace == "production"
    required_compliance_labels := {"compliance/pci-dss", "compliance/hipaa", "compliance/gdpr"}
    compliance_label := required_compliance_labels[_]
    not input.metadata.labels[compliance_label]
    msg := sprintf("Compliance label required for production: %s", [compliance_label])
}

# Deny non-compliant registries
deny_non_compliant_registries[msg] {
    input.kind == "Pod"
    container := input.spec.containers[_]
    approved_registries := {"ghcr.io", "docker.io/library", "registry.k8s.io"}
    not startswith_any(container.image, approved_registries)
    msg := sprintf("Image from non-approved registry: %s", [container.image])
}

# Helper function to check if string starts with any of the prefixes
startswith_any(str, prefixes) {
    prefix := prefixes[_]
    startswith(str, prefix)
}