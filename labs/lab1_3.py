import os
import json
import getpass
from azure.identity import AzureCliCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.resource.resources.models import DeploymentMode

def challenge_1():
    """Launch CDCA-MGMT VM"""
    password = getpass.getpass(prompt="Enter a password for this VM: ")
    credential = AzureCliCredential()
    subscription_id = os.environ["ACC_USER_SUBSCRIPTION"]
    resource_client = ResourceManagementClient(credential, subscription_id)
    with open("arm-templates/cdca-mgmt/template.json", "r") as template_file:
        template_body = json.load(template_file)
    rg_deployment_result = resource_client.deployments.begin_create_or_update(
        "CDCA-RG",
        "CDCA-MGMT",
        {
            "properties": {
                "template": template_body,
                "parameters": {
                    "location": {
                    "value": "eastus"
                },
                "networkInterfaceName": {
                    "value": "cdca-mgmt753"
                },
                "networkSecurityGroupName": {
                    "value": "CDCA-MGMT-nsg"
                },
                "networkSecurityGroupRules": {
                    "value": [
                        {
                            "name": "SSH",
                            "properties": {
                                "priority": 300,
                                "protocol": "TCP",
                                "access": "Allow",
                                "direction": "Inbound",
                                "sourceAddressPrefix": "*",
                                "sourcePortRange": "*",
                                "destinationAddressPrefix": "*",
                                "destinationPortRange": "22"
                            }
                        }
                    ]
                },
                "subnetName": {
                    "value": "default"
                },
                "virtualNetworkName": {
                    "value": "CDCA-MGMT-vnet"
                },
                "addressPrefixes": {
                    "value": [
                        "10.0.0.0/16"
                    ]
                },
                "subnets": {
                    "value": [
                        {
                            "name": "default",
                            "properties": {
                                "addressPrefix": "10.0.0.0/24"
                            }
                        }
                    ]
                },
                "publicIpAddressName": {
                    "value": "CDCA-MGMT-ip"
                },
                "publicIpAddressType": {
                    "value": "Static"
                },
                "publicIpAddressSku": {
                    "value": "Standard"
                },
                "pipDeleteOption": {
                    "value": "Detach"
                },
                "virtualMachineName": {
                    "value": "CDCA-MGMT"
                },
                "virtualMachineComputerName": {
                    "value": "CDCA-MGMT"
                },
                "virtualMachineRG": {
                    "value": "CDCA-RG"
                },
                "osDiskType": {
                    "value": "Premium_LRS"
                },
                "osDiskDeleteOption": {
                    "value": "Delete"
                },
                "virtualMachineSize": {
                    "value": "Standard_B1ms"
                },
                "nicDeleteOption": {
                    "value": "Detach"
                },
                "adminUsername": {
                    "value": "student"
                },
                "adminPassword": {
                    "value": password
                },
                "securityType": {
                    "value": "TrustedLaunch"
                },
                "secureBoot": {
                    "value": True
                },
                "vTPM": {
                    "value": True
                }
                }
            }
        }
    )

challenge_1()