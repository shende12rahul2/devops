package terraform

import input as tfplan

# Deny public S3 buckets
deny_public_s3[msg] {
    resource := tfplan.resource_changes[_]
    resource.type == "aws_s3_bucket_public_access_block"
    resource.change.after.block_public_acls == false
    msg := sprintf("S3 bucket must not be public: %s", [resource.address])
}

# Require encryption for S3 buckets
require_s3_encryption[msg] {
    resource := tfplan.resource_changes[_]
    resource.type == "aws_s3_bucket"
    not has_encryption_configuration(resource)
    msg := sprintf("S3 bucket must have encryption enabled: %s", [resource.address])
}

# Deny unencrypted RDS instances
deny_unencrypted_rds[msg] {
    resource := tfplan.resource_changes[_]
    resource.type == "aws_db_instance"
    resource.change.after.storage_encrypted == false
    msg := sprintf("RDS instance must be encrypted: %s", [resource.address])
}

# Require multi-AZ for production RDS
require_rds_multi_az[msg] {
    resource := tfplan.resource_changes[_]
    resource.type == "aws_db_instance"
    resource.change.after.multi_az == false
    has_production_tag(resource)
    msg := sprintf("RDS instance must be multi-AZ in production: %s", [resource.address])
}

# Require backup retention for RDS
require_rds_backup_retention[msg] {
    resource := tfplan.resource_changes[_]
    resource.type == "aws_db_instance"
    resource.change.after.backup_retention_period < 7
    msg := sprintf("RDS backup retention must be at least 7 days: %s", [resource.address])
}

# Deny security groups with wide-open rules
deny_wide_open_sg[msg] {
    resource := tfplan.resource_changes[_]
    resource.type == "aws_security_group"
    rule := resource.change.after.ingress[_]
    rule.cidr_blocks[_] == "0.0.0.0/0"
    rule.from_port == 0
    rule.to_port == 65535
    msg := sprintf("Security group has wide-open ingress rule: %s", [resource.address])
}

# Require VPC flow logs
require_vpc_flow_logs[msg] {
    resource := tfplan.resource_changes[_]
    resource.type == "aws_vpc"
    not has_flow_logs(resource.address)
    msg := sprintf("VPC must have flow logs enabled: %s", [resource.address])
}

# Deny unencrypted EBS volumes
deny_unencrypted_ebs[msg] {
    resource := tfplan.resource_changes[_]
    resource.type == "aws_ebs_volume"
    resource.change.after.encrypted == false
    msg := sprintf("EBS volume must be encrypted: %s", [resource.address])
}

# Require CloudTrail for all regions
require_cloudtrail[msg] {
    not has_cloudtrail
    msg := "CloudTrail must be enabled for all regions"
}

# Deny IAM users without MFA
deny_iam_users_without_mfa[msg] {
    resource := tfplan.resource_changes[_]
    resource.type == "aws_iam_user"
    not has_mfa_device(resource.address)
    msg := sprintf("IAM user must have MFA enabled: %s", [resource.address])
}

# Require least privilege for IAM policies
require_least_privilege[msg] {
    resource := tfplan.resource_changes[_]
    resource.type == "aws_iam_policy"
    policy := json.unmarshal(resource.change.after.policy)
    has_wildcard_permissions(policy)
    msg := sprintf("IAM policy should not use wildcard permissions: %s", [resource.address])
}

# Deny public EC2 instances
deny_public_ec2[msg] {
    resource := tfplan.resource_changes[_]
    resource.type == "aws_instance"
    resource.change.after.associate_public_ip_address == true
    not has_production_tag(resource)
    msg := sprintf("EC2 instance should not have public IP in non-production: %s", [resource.address])
}

# Require monitoring for EC2 instances
require_ec2_monitoring[msg] {
    resource := tfplan.resource_changes[_]
    resource.type == "aws_instance"
    resource.change.after.monitoring == false
    msg := sprintf("EC2 instance must have detailed monitoring enabled: %s", [resource.address])
}

# Require tags for cost allocation
require_cost_allocation_tags[msg] {
    resource := tfplan.resource_changes[_]
    required_tags := {"Environment", "Project", "Owner", "Cost-Center"}
    tag := required_tags[_]
    not resource.change.after.tags[tag]
    msg := sprintf("Required cost allocation tag missing: %s on %s", [tag, resource.address])
}

# Deny deprecated instance types
deny_deprecated_instances[msg] {
    resource := tfplan.resource_changes[_]
    resource.type == "aws_instance"
    deprecated_types := {"t2.micro", "t2.small", "t2.medium"}
    deprecated_types[_] == resource.change.after.instance_type
    msg := sprintf("Deprecated instance type not allowed: %s on %s", [resource.change.after.instance_type, resource.address])
}

# Require ELB access logging
require_elb_access_logs[msg] {
    resource := tfplan.resource_changes[_]
    resource.type == "aws_lb"
    resource.change.after.access_logs[0].enabled == false
    msg := sprintf("ELB must have access logs enabled: %s", [resource.address])
}

# Deny unencrypted Lambda environment variables
deny_unencrypted_lambda_env[msg] {
    resource := tfplan.resource_changes[_]
    resource.type == "aws_lambda_function"
    env_vars := resource.change.after.environment.variables
    has_sensitive_data(env_vars)
    not resource.change.after.kms_key_arn
    msg := sprintf("Lambda environment variables must be encrypted: %s", [resource.address])
}

# Require WAF for public ALBs
require_waf_for_alb[msg] {
    resource := tfplan.resource_changes[_]
    resource.type == "aws_lb"
    resource.change.after.load_balancer_type == "application"
    resource.change.after.scheme == "internet-facing"
    not has_waf_association(resource.address)
    msg := sprintf("Public ALB must have WAF associated: %s", [resource.address])
}

# Helper functions
has_encryption_configuration(resource) {
    resource.change.after.server_side_encryption_configuration
}

has_production_tag(resource) {
    resource.change.after.tags.Environment == "production"
}

has_flow_logs(vpc_address) {
    flow_log := tfplan.resource_changes[_]
    flow_log.type == "aws_flow_log"
    flow_log.change.after.vpc_id == vpc_address
}

has_cloudtrail {
    trail := tfplan.resource_changes[_]
    trail.type == "aws_cloudtrail"
    trail.change.after.is_multi_region_trail == true
}

has_mfa_device(user_address) {
    mfa := tfplan.resource_changes[_]
    mfa.type == "aws_iam_user_login_profile"
    mfa.address == user_address
}

has_wildcard_permissions(policy) {
    statement := policy.Statement[_]
    permission := statement.Action[_]
    contains(permission, "*")
}

has_sensitive_data(env_vars) {
    sensitive_keys := {"password", "secret", "key", "token"}
    key := sensitive_keys[_]
    env_vars[key]
}

has_waf_association(alb_address) {
    waf := tfplan.resource_changes[_]
    waf.type == "aws_wafv2_web_acl_association"
    waf.change.after.resource_arn == alb_address
}