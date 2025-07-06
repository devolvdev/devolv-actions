#!/usr/bin/env python3

import json
import time
import argparse

import boto3
from botocore.exceptions import ClientError

OIDC_URL = "https://token.actions.githubusercontent.com"
OIDC_AUDIENCE = "sts.amazonaws.com"
THUMBPRINT = "6938fd4d98bab03faadb97b34396831e3780aea1"

def wait_for_role(iam_client, role_name, max_attempts=10, delay=2):
    waiter = iam_client.get_waiter('role_exists')
    try:
        waiter.wait(RoleName=role_name, WaiterConfig={'Delay': delay, 'MaxAttempts': max_attempts})
        return True
    except ClientError as e:
        print(f"Error waiting for role: {e}")
        return False

def wait_for_policy(iam_client, policy_arn, max_attempts=10, delay=2):
    for _ in range(max_attempts):
        try:
            iam_client.get_policy(PolicyArn=policy_arn)
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchEntity':
                time.sleep(delay)
                continue
            raise
    return False

def ensure_github_oidc_provider_exists(iam_client, account_id, org_name):
    provider_arn = f"arn:aws:iam::{account_id}:oidc-provider/token.actions.githubusercontent.com"
    try:
        existing_providers = iam_client.list_open_id_connect_providers()['OpenIDConnectProviderList']
        if any(p['Arn'] == provider_arn for p in existing_providers):
            print(f"✅ OIDC provider for GitHub already exists (used for {org_name})")
            return
        print(f"🔧 Creating GitHub OIDC provider for {org_name}...")
        iam_client.create_open_id_connect_provider(
            Url=OIDC_URL,
            ClientIDList=[OIDC_AUDIENCE],
            ThumbprintList=[THUMBPRINT]
        )
        print(f"✅ GitHub OIDC provider created (used for {org_name})")
    except ClientError as e:
        print(f"❌ Failed to ensure GitHub OIDC provider: {e}")
        raise

def main():
    parser = argparse.ArgumentParser(description="Set up GitHub OIDC role + policy")
    parser.add_argument("--github-org", required=True, help="GitHub organization name")
    args = parser.parse_args()

    org_name = args.github_org
    role_name = f"{org_name}-DevolvRole"
    policy_name = f"{org_name}-DevolvPolicy"

    iam_client = boto3.client('iam')
    sts_client = boto3.client('sts')

    try:
        account_id = sts_client.get_caller_identity()['Account']
    except ClientError as e:
        print(f"❌ Error getting account ID: {e}")
        return

    ensure_github_oidc_provider_exists(iam_client, account_id, org_name)

    trust_policy = {
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": {
                "Federated": f"arn:aws:iam::{account_id}:oidc-provider/token.actions.githubusercontent.com"
            },
            "Action": "sts:AssumeRoleWithWebIdentity",
            "Condition": {
                "StringEquals": {
                    "token.actions.githubusercontent.com:aud": OIDC_AUDIENCE
                },
                "StringLike": {
                    "token.actions.githubusercontent.com:sub": f"repo:{org_name}/*"
                }
            }
        }]
    }

    try:
        iam_client.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps(trust_policy)
        )
        if wait_for_role(iam_client, role_name):
            print(f"✅ Role created: {role_name}")
        else:
            print("❌ Failed to confirm role creation")
            return
    except ClientError as e:
        if e.response['Error']['Code'] == 'EntityAlreadyExists':
            print(f"ℹ️ Role {role_name} already exists")
        else:
            print(f"❌ Error creating role: {e}")
            return

    policy_document = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "AllowIAMPolicyDriftActions",
                "Effect": "Allow",
                "Action": [
                    "iam:GetPolicy",
                    "iam:GetPolicyVersion",
                    "iam:ListPolicyVersions",
                    "iam:CreatePolicyVersion",
                    "iam:DeletePolicyVersion"
                ],
                "Resource": "*"
            },
            {
                "Sid": "AllowSTSAssumeRoleForDevolvCIRole",
                "Effect": "Allow",
                "Action": [
                    "sts:AssumeRole",
                    "sts:TagSession"
                ],
                "Resource": f"arn:aws:iam::{account_id}:role/{role_name}"
            }
        ]
    }

    try:
        response = iam_client.create_policy(
            PolicyName=policy_name,
            PolicyDocument=json.dumps(policy_document)
        )
        policy_arn = response['Policy']['Arn']
        if wait_for_policy(iam_client, policy_arn):
            print(f"✅ Policy created: {policy_name}")
        else:
            print("❌ Failed to confirm policy creation")
            return
    except ClientError as e:
        if e.response['Error']['Code'] == 'EntityAlreadyExists':
            policy_arn = f"arn:aws:iam::{account_id}:policy/{policy_name}"
            print(f"ℹ️ Policy {policy_name} already exists")
        else:
            print(f"❌ Error creating policy: {e}")
            return

    try:
        iam_client.attach_role_policy(RoleName=role_name, PolicyArn=policy_arn)
        print(f"✅ Policy attached to role: {role_name}")
    except ClientError as e:
        print(f"❌ Error attaching policy to role: {e}")
        return

    print("\n🎉 Setup complete!")
    print(f"🔑 Role: arn:aws:iam::{account_id}:role/{role_name}")
    print(f"🔑 Policy: arn:aws:iam::{account_id}:policy/{policy_name}")
    print(f"🔑 OIDC provider: token.actions.githubusercontent.com (used for {org_name})")
    print("\n👉 Add this to your GitHub Actions workflow:\n")
    print("permissions:")
    print("  contents: write")
    print("  issues: write")
    print("  pull-requests: write\n")
    print("- uses: aws-actions/configure-aws-credentials@v2")
    print("  with:")
    print(f"    role-to-assume: arn:aws:iam::{account_id}:role/{role_name}")
    print("    aws-region: <your-region>  # Replace with your AWS region (e.g. us-east-1)")

if __name__ == "__main__":
    main()
