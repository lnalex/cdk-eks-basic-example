from aws_cdk import core
import aws_cdk.aws_eks as eks
import aws_cdk.aws_ec2 as ec2

class EksCdkBasicStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # ============================================
        # Variables
        # ============================================

        # Existing VPC to lookup
        vpc_id = "vpc-123456"
        subnet_ids = ["subnet-XXX", "subnet-XXX", "subnet-XXX"]

        # EKS cluster name
        cluster_name = "my-test-cluster"

        # ============================================
        # Stack resources
        # ============================================

        # Lookup an existing VPC
        # https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_ec2/Vpc.html#aws_cdk.aws_ec2.Vpc.from_lookup
        vpc = ec2.Vpc.from_lookup(self, "VPC", vpc_id=vpc_id)

        # Lookup existing subnets
        # https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_ec2/Subnet.html
        subnets = []
        for i, subnet_id in enumerate(subnet_ids):
            subnets.append(ec2.Subnet.from_subnet_id(self, f"Subnet{i}", subnet_id=subnet_id))

        # Create the EKS cluster
        # https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_eks/Cluster.html
        cluster = eks.Cluster(self, "EKSCluster",
            cluster_name=cluster_name,
            version=eks.KubernetesVersion.V1_20,
            vpc=vpc,
            # Don't add default worker nodes
            default_capacity=0,

            # Private endpoints only
            # https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_eks/EndpointAccess.html#aws_cdk.aws_eks.EndpointAccess
            endpoint_access=eks.EndpointAccess.PRIVATE,

            # Pick specific subnets
            # https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_ec2/SubnetSelection.html#subnetselection
            vpc_subnets=[ec2.SubnetSelection(subnets=subnets)]
        )

        # Create CNI Addon
        # https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_eks/CfnAddon.html
        cni_addon = eks.CfnAddon(self, "CNIAddon", 
            addon_name="vpc-cni",
            addon_version="v1.7.5-eksbuild.2",
            cluster_name=cluster.cluster_name
        )
