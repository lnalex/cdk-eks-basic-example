# Basic CDK EKS Application

## Usage

1. Configure account and region variables in `app.py`
2. Configure other variables in `eks_cdk_basic_stack.py`
3. Deploy toolkit stack to env
```
cdk bootstrap aws://<ACCOUNT_ID>/<REGION>
```
4. Deploy the stack
```
cdk deploy
```