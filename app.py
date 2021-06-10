#!/usr/bin/env python3

from aws_cdk import core

from eks_cdk_basic.eks_cdk_basic_stack import EksCdkBasicStack

env = core.Environment(account="XXXXXXXXXX", region="us-east-1")

app = core.App()
EksCdkBasicStack(app, "eks-cdk-basic", env=env)

app.synth()
