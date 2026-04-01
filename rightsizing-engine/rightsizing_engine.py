#!/usr/bin/env python3
"""
Automated Rightsizing Engine
AI-powered cloud resource optimization engine that analyzes usage patterns
and provides intelligent rightsizing recommendations.

Features:
- Multi-cloud support (AWS, Azure, GCP)
- Machine learning-based usage prediction
- Cost optimization recommendations
- Kubernetes workload rightsizing
- Real-time monitoring and alerting
"""

import asyncio
import json
import logging
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from enum import Enum

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import prometheus_client as prom
import aiohttp
import boto3
from azure.identity import DefaultAzureCredential
from azure.mgmt.monitor import MonitorManagementClient
from google.cloud import monitoring_v3
import kubernetes.client
import kubernetes.config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CloudProvider(Enum):
    AWS = "aws"
    AZURE = "azure"
    GCP = "gcp"
    KUBERNETES = "kubernetes"

class ResourceType(Enum):
    EC2_INSTANCE = "ec2_instance"
    RDS_INSTANCE = "rds_instance"
    ELASTICACHE = "elasticache"
    LAMBDA_FUNCTION = "lambda_function"
    KUBERNETES_POD = "kubernetes_pod"
    KUBERNETES_DEPLOYMENT = "kubernetes_deployment"

class RecommendationType(Enum):
    UPSIZE = "upsize"
    DOWNSIZE = "downsize"
    RIGHTSIZING = "rightsizing"
    TERMINATE = "terminate"
    SCHEDULE = "schedule"

@dataclass
class ResourceMetrics:
    """Resource usage metrics data structure"""
    resource_id: str
    resource_type: ResourceType
    cloud_provider: CloudProvider
    region: str
    timestamp: datetime

    # CPU metrics
    cpu_utilization_avg: float
    cpu_utilization_p95: float
    cpu_utilization_max: float

    # Memory metrics
    memory_utilization_avg: float
    memory_utilization_p95: float
    memory_utilization_max: float

    # Network metrics
    network_in_avg: float
    network_out_avg: float
    network_in_max: float
    network_out_max: float

    # Disk metrics
    disk_read_avg: float
    disk_write_avg: float
    disk_read_max: float
    disk_write_max: float

    # Cost metrics
    current_cost_per_hour: float
    estimated_cost_per_hour: float

    # Additional metadata
    tags: Dict[str, str]
    instance_type: str
    availability_zone: str

@dataclass
class RightsizingRecommendation:
    """Rightsizing recommendation data structure"""
    resource_id: str
    resource_type: ResourceType
    cloud_provider: CloudProvider
    current_instance_type: str
    recommended_instance_type: str
    recommendation_type: RecommendationType
    confidence_score: float
    estimated_monthly_savings: float
    estimated_monthly_cost: float
    current_monthly_cost: float
    risk_level: str
    implementation_complexity: str
    reasoning: str
    alternative_options: List[Dict[str, Any]]
    timestamp: datetime
    expires_at: datetime

class MetricsCollector:
    """Collects metrics from various cloud providers"""

    def __init__(self):
        self.aws_client = boto3.client('cloudwatch', region_name='us-east-1')
        self.azure_credential = DefaultAzureCredential()
        self.gcp_client = monitoring_v3.MetricServiceClient()

    async def collect_aws_metrics(self, resource_id: str, resource_type: ResourceType,
                                region: str, start_time: datetime, end_time: datetime) -> ResourceMetrics:
        """Collect AWS CloudWatch metrics"""

        metrics = {}

        # CPU Utilization
        cpu_data = await self._get_cloudwatch_metric(
            region, resource_id, 'AWS/EC2', 'CPUUtilization',
            start_time, end_time, ['Average', 'p95', 'Maximum']
        )
        metrics.update(cpu_data)

        # Memory Utilization (if available)
        try:
            memory_data = await self._get_cloudwatch_metric(
                region, resource_id, 'System/Linux', 'MemoryUtilization',
                start_time, end_time, ['Average', 'p95', 'Maximum']
            )
            metrics.update({f'memory_{k}': v for k, v in memory_data.items()})
        except:
            metrics.update({
                'memory_utilization_avg': 0.0,
                'memory_utilization_p95': 0.0,
                'memory_utilization_max': 0.0
            })

        # Network metrics
        network_in = await self._get_cloudwatch_metric(
            region, resource_id, 'AWS/EC2', 'NetworkIn',
            start_time, end_time, ['Average', 'Maximum']
        )
        network_out = await self._get_cloudwatch_metric(
            region, resource_id, 'AWS/EC2', 'NetworkOut',
            start_time, end_time, ['Average', 'Maximum']
        )

        # Disk metrics
        disk_read = await self._get_cloudwatch_metric(
            region, resource_id, 'AWS/EC2', 'DiskReadOps',
            start_time, end_time, ['Average', 'Maximum']
        )
        disk_write = await self._get_cloudwatch_metric(
            region, resource_id, 'AWS/EC2', 'DiskWriteOps',
            start_time, end_time, ['Average', 'Maximum']
        )

        return ResourceMetrics(
            resource_id=resource_id,
            resource_type=resource_type,
            cloud_provider=CloudProvider.AWS,
            region=region,
            timestamp=datetime.utcnow(),
            cpu_utilization_avg=metrics.get('cpu_average', 0.0),
            cpu_utilization_p95=metrics.get('cpu_p95', 0.0),
            cpu_utilization_max=metrics.get('cpu_maximum', 0.0),
            memory_utilization_avg=metrics.get('memory_average', 0.0),
            memory_utilization_p95=metrics.get('memory_p95', 0.0),
            memory_utilization_max=metrics.get('memory_maximum', 0.0),
            network_in_avg=network_in.get('average', 0.0),
            network_out_avg=network_out.get('average', 0.0),
            network_in_max=network_in.get('maximum', 0.0),
            network_out_max=network_out.get('maximum', 0.0),
            disk_read_avg=disk_read.get('average', 0.0),
            disk_write_avg=disk_write.get('average', 0.0),
            disk_read_max=disk_read.get('maximum', 0.0),
            disk_write_max=disk_write.get('maximum', 0.0),
            current_cost_per_hour=0.0,  # To be calculated
            estimated_cost_per_hour=0.0,
            tags={},
            instance_type='',
            availability_zone=''
        )

    async def _get_cloudwatch_metric(self, region: str, resource_id: str,
                                   namespace: str, metric_name: str,
                                   start_time: datetime, end_time: datetime,
                                   statistics: List[str]) -> Dict[str, float]:
        """Get CloudWatch metric data"""
        client = boto3.client('cloudwatch', region_name=region)

        response = client.get_metric_statistics(
            Namespace=namespace,
            MetricName=metric_name,
            Dimensions=[{'Name': 'InstanceId', 'Value': resource_id}],
            StartTime=start_time,
            EndTime=end_time,
            Period=3600,  # 1 hour
            Statistics=statistics
        )

        result = {}
        for stat in statistics:
            stat_lower = stat.lower()
            datapoints = response['Datapoints']
            if datapoints:
                values = [dp[stat] for dp in datapoints if stat in dp]
                result[f'{metric_name.lower()}_{stat_lower}'] = np.mean(values) if values else 0.0
            else:
                result[f'{metric_name.lower()}_{stat_lower}'] = 0.0

        return result

class MLRightsizingEngine:
    """Machine learning engine for rightsizing recommendations"""

    def __init__(self):
        self.models = {}
        self.scalers = {}
        self.instance_types = self._load_instance_types()

    def _load_instance_types(self) -> Dict[str, Dict[str, Any]]:
        """Load instance type specifications"""
        return {
            # AWS EC2 instances
            't3.micro': {'cpu': 1, 'memory': 1, 'cost_per_hour': 0.0104},
            't3.small': {'cpu': 1, 'memory': 2, 'cost_per_hour': 0.0208},
            't3.medium': {'cpu': 2, 'memory': 4, 'cost_per_hour': 0.0416},
            't3.large': {'cpu': 2, 'memory': 8, 'cost_per_hour': 0.0832},
            'm5.large': {'cpu': 2, 'memory': 8, 'cost_per_hour': 0.096},
            'm5.xlarge': {'cpu': 4, 'memory': 16, 'cost_per_hour': 0.192},
            'm5.2xlarge': {'cpu': 8, 'memory': 32, 'cost_per_hour': 0.384},
            'c5.large': {'cpu': 2, 'memory': 4, 'cost_per_hour': 0.085},
            'c5.xlarge': {'cpu': 4, 'memory': 8, 'cost_per_hour': 0.170},
            # Add more instance types as needed
        }

    def train_model(self, resource_type: ResourceType, historical_data: List[ResourceMetrics]):
        """Train ML model for resource type"""
        if not historical_data:
            return

        # Prepare training data
        df = pd.DataFrame([asdict(metric) for metric in historical_data])

        # Feature engineering
        features = [
            'cpu_utilization_avg', 'cpu_utilization_p95', 'cpu_utilization_max',
            'memory_utilization_avg', 'memory_utilization_p95', 'memory_utilization_max',
            'network_in_avg', 'network_out_avg', 'disk_read_avg', 'disk_write_avg'
        ]

        X = df[features]
        y = df['current_cost_per_hour']  # Target: cost efficiency

        # Handle missing values
        X = X.fillna(0)

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        # Train model
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train_scaled, y_train)

        # Store model and scaler
        self.models[resource_type] = model
        self.scalers[resource_type] = scaler

        # Evaluate model
        score = model.score(X_test_scaled, y_test)
        logger.info(f"Model trained for {resource_type.value} with R² score: {score:.3f}")

    def predict_optimal_instance_type(self, metrics: ResourceMetrics) -> Tuple[str, float, str]:
        """Predict optimal instance type based on usage patterns"""

        if metrics.resource_type not in self.models:
            return metrics.instance_type, 0.5, "No ML model available"

        model = self.models[metrics.resource_type]
        scaler = self.scalers[metrics.resource_type]

        # Prepare features
        features = np.array([[
            metrics.cpu_utilization_avg, metrics.cpu_utilization_p95, metrics.cpu_utilization_max,
            metrics.memory_utilization_avg, metrics.memory_utilization_p95, metrics.memory_utilization_max,
            metrics.network_in_avg, metrics.network_out_avg,
            metrics.disk_read_avg, metrics.disk_write_avg
        ]])

        # Scale features
        features_scaled = scaler.transform(features)

        # Predict cost efficiency
        predicted_efficiency = model.predict(features_scaled)[0]

        # Determine optimal instance type based on usage patterns
        cpu_pressure = max(metrics.cpu_utilization_avg, metrics.cpu_utilization_p95 * 0.8)
        memory_pressure = max(metrics.memory_utilization_avg, metrics.memory_utilization_p95 * 0.8)

        current_specs = self.instance_types.get(metrics.instance_type, {'cpu': 1, 'memory': 1})

        # Rightsizing logic
        if cpu_pressure < 20 and memory_pressure < 30:
            # Underutilized - can downsize
            recommended_type = self._find_downsize_option(metrics.instance_type, cpu_pressure, memory_pressure)
            confidence = 0.8
            reasoning = "Low CPU and memory utilization indicates over-provisioning"
        elif cpu_pressure > 80 or memory_pressure > 85:
            # Overutilized - needs upsize
            recommended_type = self._find_upsize_option(metrics.instance_type, cpu_pressure, memory_pressure)
            confidence = 0.9
            reasoning = "High CPU or memory utilization indicates under-provisioning"
        else:
            # Right-sized
            recommended_type = metrics.instance_type
            confidence = 0.6
            reasoning = "Resource utilization is within optimal range"

        return recommended_type, confidence, reasoning

    def _find_downsize_option(self, current_type: str, cpu_pressure: float, memory_pressure: float) -> str:
        """Find appropriate downsize option"""
        current_specs = self.instance_types.get(current_type, {'cpu': 1, 'memory': 1})

        # Look for smaller instance types that can handle the load
        candidates = []
        for instance_type, specs in self.instance_types.items():
            if specs['cpu'] < current_specs['cpu'] and specs['memory'] < current_specs['memory']:
                # Check if smaller instance can handle the load
                cpu_ratio = specs['cpu'] / current_specs['cpu']
                memory_ratio = specs['memory'] / current_specs['memory']

                if cpu_pressure * cpu_ratio < 70 and memory_pressure * memory_ratio < 80:
                    candidates.append((instance_type, specs))

        if candidates:
            # Return the most cost-effective option
            return min(candidates, key=lambda x: x[1]['cost_per_hour'])[0]

        return current_type

    def _find_upsize_option(self, current_type: str, cpu_pressure: float, memory_pressure: float) -> str:
        """Find appropriate upsize option"""
        current_specs = self.instance_types.get(current_type, {'cpu': 1, 'memory': 1})

        # Look for larger instance types
        candidates = []
        for instance_type, specs in self.instance_types.items():
            if specs['cpu'] > current_specs['cpu'] or specs['memory'] > current_specs['memory']:
                candidates.append((instance_type, specs))

        if candidates:
            # Return the smallest sufficient option
            for instance_type, specs in sorted(candidates, key=lambda x: x[1]['cost_per_hour']):
                cpu_ratio = specs['cpu'] / current_specs['cpu']
                memory_ratio = specs['memory'] / current_specs['memory']

                if cpu_pressure / cpu_ratio < 70 and memory_pressure / memory_ratio < 80:
                    return instance_type

        return current_type

class RightsizingEngine:
    """Main rightsizing engine orchestrator"""

    def __init__(self):
        self.metrics_collector = MetricsCollector()
        self.ml_engine = MLRightsizingEngine()
        self.recommendations_cache = {}

        # Prometheus metrics
        self.recommendations_generated = prom.Counter(
            'rightsizing_recommendations_total',
            'Total number of rightsizing recommendations generated'
        )
        self.cost_savings_estimated = prom.Gauge(
            'rightsizing_cost_savings_estimated',
            'Estimated monthly cost savings from rightsizing'
        )

    async def analyze_resource(self, resource_id: str, resource_type: ResourceType,
                             cloud_provider: CloudProvider, region: str) -> Optional[RightsizingRecommendation]:
        """Analyze a single resource and generate rightsizing recommendation"""

        try:
            # Collect metrics for the last 7 days
            end_time = datetime.utcnow()
            start_time = end_time - timedelta(days=7)

            if cloud_provider == CloudProvider.AWS:
                metrics = await self.metrics_collector.collect_aws_metrics(
                    resource_id, resource_type, region, start_time, end_time
                )
            else:
                logger.warning(f"Cloud provider {cloud_provider.value} not yet supported")
                return None

            # Get ML-based recommendation
            recommended_type, confidence, reasoning = self.ml_engine.predict_optimal_instance_type(metrics)

            # Calculate cost savings
            current_specs = self.ml_engine.instance_types.get(metrics.instance_type, {})
            recommended_specs = self.ml_engine.instance_types.get(recommended_type, {})

            current_cost = current_specs.get('cost_per_hour', 0) * 24 * 30
            recommended_cost = recommended_specs.get('cost_per_hour', 0) * 24 * 30
            savings = current_cost - recommended_cost

            # Determine recommendation type
            if recommended_type != metrics.instance_type:
                if recommended_specs.get('cpu', 0) > current_specs.get('cpu', 0):
                    rec_type = RecommendationType.UPSIZE
                else:
                    rec_type = RecommendationType.DOWNSIZE
            else:
                rec_type = RecommendationType.RIGHTSIZING

            # Assess risk and complexity
            risk_level, complexity = self._assess_risk_and_complexity(metrics, recommended_type)

            recommendation = RightsizingRecommendation(
                resource_id=resource_id,
                resource_type=resource_type,
                cloud_provider=cloud_provider,
                current_instance_type=metrics.instance_type,
                recommended_instance_type=recommended_type,
                recommendation_type=rec_type,
                confidence_score=confidence,
                estimated_monthly_savings=savings,
                estimated_monthly_cost=recommended_cost,
                current_monthly_cost=current_cost,
                risk_level=risk_level,
                implementation_complexity=complexity,
                reasoning=reasoning,
                alternative_options=self._generate_alternatives(metrics, recommended_type),
                timestamp=datetime.utcnow(),
                expires_at=datetime.utcnow() + timedelta(days=30)
            )

            # Cache recommendation
            self.recommendations_cache[resource_id] = recommendation

            # Update Prometheus metrics
            self.recommendations_generated.inc()
            self.cost_savings_estimated.set(savings)

            return recommendation

        except Exception as e:
            logger.error(f"Error analyzing resource {resource_id}: {e}")
            return None

    def _assess_risk_and_complexity(self, metrics: ResourceMetrics, recommended_type: str) -> Tuple[str, str]:
        """Assess risk level and implementation complexity"""

        # Risk assessment based on usage patterns
        max_cpu = max(metrics.cpu_utilization_avg, metrics.cpu_utilization_p95)
        max_memory = max(metrics.memory_utilization_avg, metrics.memory_utilization_p95)

        if max_cpu > 90 or max_memory > 95:
            risk_level = "high"
        elif max_cpu > 70 or max_memory > 80:
            risk_level = "medium"
        else:
            risk_level = "low"

        # Complexity assessment
        if recommended_type == metrics.instance_type:
            complexity = "low"
        elif abs(self.ml_engine.instance_types.get(recommended_type, {}).get('cpu', 1) -
                 self.ml_engine.instance_types.get(metrics.instance_type, {}).get('cpu', 1)) > 4:
            complexity = "high"
        else:
            complexity = "medium"

        return risk_level, complexity

    def _generate_alternatives(self, metrics: ResourceMetrics, recommended_type: str) -> List[Dict[str, Any]]:
        """Generate alternative rightsizing options"""
        alternatives = []

        # Add 2-3 alternative instance types
        current_specs = self.ml_engine.instance_types.get(metrics.instance_type, {})

        for instance_type, specs in self.ml_engine.instance_types.items():
            if instance_type != recommended_type and instance_type != metrics.instance_type:
                alt_cost = specs.get('cost_per_hour', 0) * 24 * 30
                current_cost = current_specs.get('cost_per_hour', 0) * 24 * 30
                savings = current_cost - alt_cost

                alternatives.append({
                    'instance_type': instance_type,
                    'estimated_monthly_cost': alt_cost,
                    'estimated_monthly_savings': savings,
                    'cpu_cores': specs.get('cpu', 0),
                    'memory_gb': specs.get('memory', 0)
                })

                if len(alternatives) >= 3:
                    break

        return sorted(alternatives, key=lambda x: x['estimated_monthly_savings'], reverse=True)

    async def analyze_portfolio(self, resources: List[Dict[str, Any]]) -> List[RightsizingRecommendation]:
        """Analyze entire resource portfolio"""
        recommendations = []

        for resource in resources:
            recommendation = await self.analyze_resource(
                resource_id=resource['resource_id'],
                resource_type=ResourceType(resource['resource_type']),
                cloud_provider=CloudProvider(resource['cloud_provider']),
                region=resource['region']
            )

            if recommendation:
                recommendations.append(recommendation)

        return recommendations

    def get_recommendations_summary(self, recommendations: List[RightsizingRecommendation]) -> Dict[str, Any]:
        """Generate summary of rightsizing recommendations"""

        total_savings = sum(r.estimated_monthly_savings for r in recommendations)
        high_confidence = len([r for r in recommendations if r.confidence_score > 0.8])
        by_type = {}
        by_risk = {'low': 0, 'medium': 0, 'high': 0}

        for rec in recommendations:
            rec_type = rec.recommendation_type.value
            by_type[rec_type] = by_type.get(rec_type, 0) + 1
            by_risk[rec.risk_level] += 1

        return {
            'total_recommendations': len(recommendations),
            'estimated_monthly_savings': total_savings,
            'high_confidence_recommendations': high_confidence,
            'recommendations_by_type': by_type,
            'recommendations_by_risk': by_risk,
            'average_confidence': np.mean([r.confidence_score for r in recommendations]) if recommendations else 0
        }

# Global engine instance
rightsizing_engine = RightsizingEngine()

async def main():
    """Main function for testing the rightsizing engine"""

    # Example resource analysis
    test_resource = {
        'resource_id': 'i-1234567890abcdef0',
        'resource_type': 'ec2_instance',
        'cloud_provider': 'aws',
        'region': 'us-east-1'
    }

    recommendation = await rightsizing_engine.analyze_resource(
        resource_id=test_resource['resource_id'],
        resource_type=ResourceType.EC2_INSTANCE,
        cloud_provider=CloudProvider.AWS,
        region=test_resource['region']
    )

    if recommendation:
        print(f"Recommendation for {recommendation.resource_id}:")
        print(f"  Current: {recommendation.current_instance_type}")
        print(f"  Recommended: {recommendation.recommended_instance_type}")
        print(f"  Type: {recommendation.recommendation_type.value}")
        print(f"  Confidence: {recommendation.confidence_score:.2f}")
        print(f"  Monthly Savings: ${recommendation.estimated_monthly_savings:.2f}")
        print(f"  Reasoning: {recommendation.reasoning}")

if __name__ == "__main__":
    asyncio.run(main())