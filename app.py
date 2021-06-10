#!/usr/bin/env python3

from aws_cdk import core

from eks_cdk_basic.eks_cdk_basic_stack import EksCdkBasicStack


app = core.App()
EksCdkBasicStack(app, "eks-cdk-basic")

app.synth()
