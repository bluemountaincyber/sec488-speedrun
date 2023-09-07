import boto3
from common import *

def challenge_3():
    """Create policy for permissions boundary"""
    client = boto3.client('iam')
    print("Removing current permissions boundaries...")
    try:
        for user in ["cloudsecurity", "cloudtools"]:
            userInfo = client.get_user(UserName=user)
            if 'PermissionsBoundary' in userInfo['User'].keys():
                client.delete_user_permissions_boundary(UserName=user)
                print(success("Removed permissions boundary for " + user))
            else:
                print(warning("No permissions boundary for " + user))
    except:
        print(failure("Could not remove permissions boundaries for " + user))
        return None

    print("Creating CDCAStrictRegions policy...")
    try:
        response = client.list_policies(Scope='Local')
    except:
        print(failure("Cannot list policies"))
        return None
    for policy in response['Policies']:
        if policy['PolicyName'] == "CDCAStrictRegions":
            print(warning("CDCAStrictRegions already exists—recreating"))
            try:
                client.delete_policy(PolicyArn=policy['Arn'])
                print(success("CDCAStrictRegions policy deleted"))
            except:
                print(failure("Could not delete CDCAStrictRegions policy"))
                return None
    policy_document = """{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowAllTheThings",
      "Action": "*",
      "Effect": "Allow",
      "Resource": "*"
    },
    {
      "Sid": "RestrictRegions",
      "Action": "*",
      "Effect": "Deny",
      "Resource": "*",
      "Condition": {
        "StringNotEquals": {
          "aws:RequestedRegion": [
            "us-east-1",
            "us-east-2",
            "us-west-1",
            "us-west-2",
            "ca-central-1",
            "eu-west-1",
            "eu-west-2",
            "ap-southeast-1",
            "ap-southeast-2"
          ]
        }
      }
    }
  ]
}"""
    try:
        response = client.create_policy(
            PolicyName="CDCAStrictRegions",
            PolicyDocument=policy_document
        )
        policyArn=response['Policy']['Arn']
        print(success("Created CDCAStrictRegions"))
        return policyArn
    except:
        print(failure("Could not create CDCAStrictRegions"))
        return None

def challenge_4(policyArn):
    """Puts permissions boundary in place for cloudtools and cloudsecurity user"""
    print("Setting permissions boundary for cloudsecurity and cloudtools...")
    client = boto3.client('iam')
    for user in ["cloudsecurity", "cloudtools"]:
        try:
            client.put_user_permissions_boundary(
                UserName=user,
                PermissionsBoundary=policyArn
            )
            print(success("Permissions boundary added to " + user))
        except:
            print(failure("Could not assign permissions boundary to " + user))
            return

def challenge_5():
    """Checks if permissions boundary is working for current user"""
    print("Attempting access to unapproved region (ap-northeast-2/Seoul)...")
    client = boto3.client('ec2', region_name='ap-northeast-2')
    try:
        client.describe_instances()
        print(failure("Can still access unapproved region"))
        return
    except:
        print(success("No access to unapproved region"))

policyArn = challenge_3()
if policyArn is not None:
    challenge_4(policyArn)
    challenge_5()