import streamlit as st
import pandas as pd


def explain_info_optimize_operate():
    """Returns a multi-paragraph explanation of the Inform-Optimize-Operate FinOps framework."""
    return """
Inform-Optimize-Operate is the FinOps lifecycle used to manage cloud spend with product- and engineering-led accountability.

1) Inform: make cost and usage visible in the context of business metrics.
   - Collect granular usage data (cloud billing, metrics, tags, labels).
   - Attach to products, teams, and sprints. Example checkpoints: COGS per feature, cost per customer.
   - Drive informed decision-making with dashboards, budgets, and anomaly alerts.

2) Optimize: find and execute savings opportunities without degrading reliability.
   - Rightsize CPU/memory; buy reserved/savings plans; use spot/preemptible nodes.
   - Identify idle resources (orphaned disks, stale envs, underutilized VMs) and reclaim.
   - Align architecture: use managed services for variable workloads (serverless, autoscaling clusters).

3) Operate: embed cost awareness in SDLC and ops process.
   - implement guardrails for spend and enforce using policy-as-code (OPA, Terraform Cloud policies).
   - Operationalize runbooks: budget burn rate, incident triage for cost spikes, acceptance criteria for infra changes.
   - Maintain continuous feedback loops via reviews, runbooks, and SLOs tied to FinOps KPIs.

In production this becomes a standing discipline:
- daily/weekly cost forecasts and anomaly alerts (Inform)
- prioritized savings cycles (Optimize)
- repeated validation, policy checks, and culture (Operate)
"""


rightsizing_kql = {
    'AKS': [
        {
            'name': 'AKS underutilized VMScaleSet instances',
            'query': """
Resources
| where type =~ 'microsoft.compute/virtualmachinescalesets'
| extend capacity = toint(properties.sku.capacity), allocated = todouble(properties.overprovisioningPolicy? 1 : 0)
| join kind=inner (
    resources
    | where type =~ 'microsoft.compute/virtualmachines'
    | summarize avgCpu = avg(properties.hardwareProfile.vmSize), avgMem = avg(properties.hardwareProfile.memoryInGB) by tostring(properties.vmScaleSetId)
) on $left.id == $right.properties.vmScaleSetId
| where avgCpu < 0.4 and avgMem < 0.4
| project id, name, resourceGroup, avgCpu, avgMem
"""
        },
        {
            'name': 'AKS pod requests vs limits skew',
            'query': """
KubernetesPodInventory
| where ClusterName == '<<CLUSTER>>'
| summarize totalRequestsCpu = sum(todouble(CpuRequests)), totalLimitCpu = sum(todouble(CpuLimits)), totalRequestsMem = sum(todouble(MemRequests)), totalLimitMem = sum(todouble(MemLimits)) by Namespace
| extend cpuRatio = totalRequestsCpu / totalLimitCpu, memRatio = totalRequestsMem / totalLimitMem
| where cpuRatio < 0.5 or memRatio < 0.5
"""
        }
    ],
    'EKS': [
        {
            'name': 'EKS underutilized managed node groups',
            'query': """
Resources
| where type =~ 'AWS::AutoScaling::AutoScalingGroup'
| where tags['eks:cluster-name'] == '<<CLUSTER>>'
| extend desired = toint(desiredCapacity), instances = toint(instances)
| join kind=inner (
    Perf
    | where ObjectName == 'AWS/EKS'
    | where CounterName == 'CPUUtilization'
    | summarize avgCpu = avg(CounterValue) by ResourceId
) on tags['aws:autoscaling:groupName'] == ResourceId
| where avgCpu < 30
| project name, resourceGroup, desired, avgCpu
"""
        },
        {
            'name': 'EKS idle Elastic Load Balancers',
            'query': """
Resources
| where type =~ 'AWS::ElasticLoadBalancingV2::LoadBalancer'
| where tags['kubernetes.io/cluster/<<CLUSTER>>'] == 'owned'
| join kind=leftouter (
    Perf
    | where ObjectName == 'AWS/ELB'
    | where CounterName == 'RequestCount'
    | summarize avgRequests=avg(CounterValue) by ResourceId
) on $left.id == $right.ResourceId
| where avgRequests < 5
| project name, id, avgRequests
"""
        }
    ],
    'GKE': [
        {
            'name': 'GKE node pool low CPU utilization',
            'query': """
Resources
| where type =~ 'GCP.Container.NodePool'
| where labels['kubernetes.io/cluster-name'] == '<<CLUSTER>>'
| join kind=inner (
    Perf
    | where ObjectName =~ 'k8s_node'
    | where CounterName =~ 'cpu/utilization'
    | summarize avgCpu = avg(CounterValue) by ResourceId
) on $left.id == $right.ResourceId
| where avgCpu < 0.3
| project name, location, avgCpu
"""
        },
        {
            'name': 'GKE preemptible instance churn',
            'query': """
Resources
| where type =~ 'GCP.Compute.Instance'
| where tags['k8s-io-cluster'] == '<<CLUSTER>>' and tags['preemptible'] == 'true'
| where properties.status == 'TERMINATED'
| where properties.lastStartTimestamp > ago(1d)
| project name, zone, properties.lastStartTimestamp
"""
        }
    ]
}


cncf_tool_mastery = [
    {
        'tool': 'Kubernetes',
        'why': 'The control plane for container orchestration and the baseline for cloud-native SRE practices.',
        'cli': 'kubectl get nodes; kubectl apply -f deployment.yaml; kubectl rollout status deployment/app'
    },
    {
        'tool': 'Istio',
        'why': 'Service mesh providing traffic management, mTLS, and observability in zero-trust clusters.',
        'cli': 'istioctl install --set profile=demo; kubectl label namespace default istio-injection=enabled; istioctl proxy-status'
    },
    {
        'tool': 'Crossplane',
        'why': 'GitOps infrastructure provisioning to treat cloud resources as Kubernetes API objects.',
        'cli': 'kubectl apply -f provider-aws.yaml; kubectl apply -f mysql-instance.yaml; kubectl get managed'
    },
    {
        'tool': 'Prometheus',
        'why': 'Metric collection and alerting core for SRE reliability and cost telemetry.',
        'cli': 'kubectl apply -f prometheus-operator.yaml; kubectl port-forward svc/prometheus 9090; curl localhost:9090/-/ready'
    },
    {
        'tool': 'Grafana',
        'why': 'Visualize FinOps and SRE performance data through dashboards; multi-tenant reporting.',
        'cli': 'kubectl apply -f grafana.yaml; kubectl port-forward svc/grafana 3000:80; grafana-cli plugins install grafana-piechart-panel'
    },
    {
        'tool': 'OPA/Gatekeeper',
        'why': 'Policy-as-code for admission controls and continuous compliance in Kubernetes.',
        'cli': 'kubectl apply -f gatekeeper.yaml; kubectl apply -f constraint-template.yaml; kubectl get k8sconstraints'
    },
    {
        'tool': 'Argo CD',
        'why': 'GitOps deployment with sync status and drift detection, critical for safe FinOps operations.',
        'cli': 'kubectl create namespace argocd; kubectl apply -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml; argocd app create myapp --repo REPO --path ./app --dest-server https://kubernetes.default.svc --dest-namespace default'
    },
    {
        'tool': 'Fluentd/Fluent Bit',
        'why': 'Flexible log routing from cluster to observability and security stores for incident and cost analysis.',
        'cli': 'kubectl apply -f fluentbit-configmap.yaml; kubectl logs ds/fluent-bit -n kube-system'
    },
    {
        'tool': 'Linkerd',
        'why': 'Lightweight service mesh alternative for low-overhead, secure microservice communication.',
        'cli': 'linkerd install | kubectl apply -f -; linkerd check; linkerd inject deploy.yaml | kubectl apply -f -'
    },
    {
        'tool': 'k9s',
        'why': 'Terminal dashboard for rapid cluster troubleshooting in production incidents.',
        'cli': 'k9s -n default; :pods; :nodes; :deploy; /<search-term>'
    }
]


def render_finops_module():
    st.title('FinOps Deep Dive: Inform-Optimize-Operate + Rightsizing + CNCF Tool Mastery')

    st.header('1. Inform-Optimize-Operate Framework')
    st.markdown(explain_info_optimize_operate())

    st.header('2. Rightsizing Playbook (Azure Resource Graph / KQL)')
    st.write('Use these KQL snippets in Azure Resource Graph Explorer to identify rightsizing opportunities.')
    for platform, queries in rightsizing_kql.items():
        st.subheader(platform)
        for q in queries:
            st.markdown(f"**{q['name']}**")
            st.code(q['query'], language='kql')

    st.header('3. Pricing Comparison: AKS vs EKS vs GKE')
    pricing_df = pd.DataFrame([
        {'cloud': 'Azure', 'managed_k8s': 'AKS', 'control_plane': 'free', 'Linux_node': '~$0.096/hr for Standard_D4s_v3 (4 vCPU, 16 GiB)', 'spot': '~$0.03/hr', 'reserved_1yr': '~0.065/hr (save 30%)', 'network_out': '~$0.087/GB'},
        {'cloud': 'AWS', 'managed_k8s': 'EKS', 'control_plane': '$0.10/hr per cluster', 'Linux_node': '~$0.094/hr for m5.xlarge', 'spot': '~$0.026/hr', 'reserved_1yr': '~0.065/hr (save 30%)', 'network_out': '~$0.09/GB'},
        {'cloud': 'GCP', 'managed_k8s': 'GKE', 'control_plane': 'free (Autopilot) or $0.10/hr (standard)', 'Linux_node': '~$0.111/hr for n1-standard-4', 'spot': '~$0.03/hr', 'reserved_1yr': '~0.075/hr (save 30%)', 'network_out': '~$0.085/GB'}
    ])
    st.table(pricing_df)

    st.header('4. CNCF Tool Mastery (10 entries)')
    st.write('Tool, why it matters, quick-start commands')

    for item in cncf_tool_mastery:
        st.subheader(item['tool'])
        st.markdown(f"**Why it matters:** {item['why']}")
        st.markdown(f"**Quick-start CLI commands:** `{item['cli']}`")


if __name__ == '__main__':
    render_finops_module()
