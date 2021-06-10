from aws_cdk import core
import aws_cdk.aws_eks as eks
import aws_cdk.aws_ec2 as ec2

class EksCdkBasicStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Variables
        vpc_id = "vpc-123456"
        cluster_name = "my-test-cluster"

        # The code that defines your stack goes here

        # Lookup an existing VPC
        # https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_ec2/Vpc.html#aws_cdk.aws_ec2.Vpc.from_lookup
        vpc = ec2.Vpc.from_lookup(self, "VPC", vpc_id=vpc_id)

        # Create the EKS cluster
        # https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_eks/Cluster.html
        cluster = eks.Cluster(self, "EKSCluster",
            cluster_name=cluster_name,
            version=eks.KubernetesVersion.V1_20,
            vpc=vpc,

            # Private endpoints only
            # https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_eks/EndpointAccess.html#aws_cdk.aws_eks.EndpointAccess
            endpoint_access=eks.EndpointAccess.PRIVATE,

            # Pick one private subnet from each AZ
            # https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_ec2/SubnetSelection.html#subnetselection
            vpc_subnets=[ec2.SubnetSelection(
                one_per_az=True,
                subnet_type=ec2.SubnetType.PRIVATE
            )]
        )

        # Add tagging
        # https://docs.aws.amazon.com/cdk/latest/guide/tagging.html
        # https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.core/Tags.html
        core.Tags.of(cluster).add("environment", "dev")