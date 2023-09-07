import boto3
from common import *

def challenge_1():
    """Checks and, if necessary, adjusts AWS Account password policy"""
    print("Creating/adjusting password policy")
    client = boto3.client('iam')
    try:
        response = client.get_account_password_policy()
    except:
        print(warning("No password policy found"))
    count = 0
    if response['PasswordPolicy']['MinimumPasswordLength'] < 14:
        print(warning("Minimum password length too short"))
        count += 1
    if response['PasswordPolicy']['RequireSymbols'] == False:
        print(warning("Symbols are not required"))
        count += 1
    if response['PasswordPolicy']['RequireNumbers'] == False:
        print(warning("Numbers are not required"))
        count += 1
    if response['PasswordPolicy']['RequireUppercaseCharacters'] == False:
        print(warning("Uppercase characters are not required"))
        count += 1
    if response['PasswordPolicy']['RequireLowercaseCharacters'] == False:
        print(warning("Lowercase characters are not required"))
        count += 1
    if response['PasswordPolicy']['ExpirePasswords'] == False:
        print(warning("Password expiry not set"))
        count += 1
    if response['PasswordPolicy']['MaxPasswordAge'] < 90:
        print(warning("Max password age too short"))
        count += 1
    if response['PasswordPolicy']['PasswordReusePrevention'] < 24:
        print(warning("Password reuse threshold too low"))
        count += 1
    if count > 0:
        print(info("Adjusting password policy"))
        try:
            client.update_account_password_policy(
                MinimumPasswordLength=14,
                RequireSymbols=True,
                RequireNumbers=True,
                RequireUppercaseCharacters=True,
                RequireLowercaseCharacters=True,
                AllowUsersToChangePassword=True,
                MaxPasswordAge=90,
                PasswordReusePrevention=24,
                HardExpiry=False
            )
            print(success("Account password policy set"))
        except:
            print(failure("Error setting account password policy"))
            return
    else:
        print(warning("Password policy is already set correctly"))
        return
    
def challenge_3():
    """Checks and, if necessary creates the cloudtools user and adds to Admins group"""
    print("Generating cloudtools user")
    client = boto3.client('iam')
    try:
        response = client.list_users()
    except:
        print(failure("Could not list users"))
        return
    found = False
    for user in response['Users']:
        if user['UserName'] == "cloudtools":
            found = True
    if not found:
        print(info("cloudtools not found—creating..."))
        try:
            client.create_user(UserName="cloudtools")
            print(success("cloudtools user created"))
        except:
            print(failure("Could not create cloudtools user"))
            return
    else:
        warning("cloudtools user already created")
    
    print("Adding cloudtools user to Admins group")
    try:
        response = client.list_groups_for_user(UserName='cloudtools')
    except:
        print(failure("Could not list groups for cloudtools user"))
    found = False
    for group in response['Groups']:
        if group['GroupName'] == "Admins":
            found = True
    if not found:
        try:
            client.add_user_to_group(
                GroupName='Admins',
                UserName='cloudtools'
            )
            print(success("Added cloudtools user to Admins group"))
        except:
            print(failure("Failed to add cloudtools to Admins group"))
    else:
        warning("cloudtools user already added to Admins group")

    print("Creating access key for cloudtools user")
    try:
        response = client.list_access_keys(UserName='cloudtools')
    except:
        print(failure("Could not list access keys for cloudtools user"))
    if len(response['AccessKeyMetadata']) >= 2:
        print(warning("Two access keys already exist for cloudtools user—deleting existing keys"))
        try:
            for access_key in response['AccessKeyMetadata']:
                client.delete_access_key(
                    UserName='cloudtools',
                    AccessKeyId=access_key['AccessKeyId']
                )
            print(success("cloudtools user's access keys deleted"))
        except:
            print(failure("Could not delete access keys for cloudtools user"))
    try:
        response = client.create_access_key(UserName='cloudtools')
        output =  "Access key generated (SAVE THIS SOMEWHERE SAFE!): \n"
        output += "      AWS_ACCESS_KEY_ID=" + response['AccessKey']['AccessKeyId'] + "\n"
        output += "      AWS_SECRET_ACCESS_KEY=" + response['AccessKey']['SecretAccessKey']
        print(success(output))
    except:
        print(failure("Could not generate access key for cloudtools user"))

challenge_1()
challenge_3()
