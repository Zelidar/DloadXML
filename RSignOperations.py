# Setting the environment to connecto to RSign
import json
import requests
# Fetching my RPost test credentials
from GettingRSignAuthToken import GetAuthToken, BaseURL

import time
def SimCall(SimCallNumber):
    time.sleep(5)
    return SimCallNumber

def GetTemplateData():
    GetTemplateRuleList = '/api/V1/Template/GetTemplateRuleList'
    
    headers = {'AuthToken': GetAuthToken()}
    query = BaseURL + GetTemplateRuleList
    AuthResponse = requests.get(query, headers=headers)
    myData = AuthResponse.json()

    filtered_data = []
    for template in myData.get("TemplateList", []):
        filtered_template = {
            "TemplateName": template.get("TemplateName"),
            "TemplateCode": template.get("TemplateCode"),
            "TypeName": template.get("TypeName"),
            "TemplateId": template.get("TemplateId"),
            "CreatedDate": template.get("CreatedDate"),
            "UserEmail": template.get("UserEmail"),
        }
        filtered_data.append(filtered_template)

    pretty_json = json.dumps(filtered_data, indent=4)
    return pretty_json


def GetTemplateInfo(TemplateCode):
    GetTemplateInfoEndpoint = '/api/V1/Template/GetTemplateInfo/' + str(TemplateCode)

    headers = {'AuthToken': GetAuthToken()}
    query = BaseURL + GetTemplateInfoEndpoint
    response = requests.get(query, headers=headers)
    myData = response.json()

    return myData


def GetRolesInfo(TemplateCode):
    # Endpoint with the TemplateCode
    GetTemplateInfoEndpoint = '/api/V1/Template/GetTemplateInfo/' + str(TemplateCode)

    headers = {'AuthToken': GetAuthToken()}
    query = BaseURL + GetTemplateInfoEndpoint
    response = requests.get(query, headers=headers)
    myData = response.json()

    # Initialize an empty list to store RoleIDs
    roles_info = []

    # Access the TemplateBasicInfo and then the TemplateRoleList
    template_basic_info = myData.get("TemplateBasicInfo", {})
    template_role_list = template_basic_info.get("TemplateRoleList", [])

    # Iterate through the TemplateRoleList to extract RoleID and RoleName
    for role in template_role_list:
        role_id = role.get("RoleID")
        role_name = role.get("RoleName")
        if role_id and role_name:
            roles_info.append({"RoleID": role_id, "RoleName": role_name})

    # Returning the list of RoleIDs
    return roles_info


def SendEnvelope(email, name):
    SendEnvelopeFromTemplate = '/api/V1/Envelope/SendEnvelopeFromTemplate'
    query = BaseURL + SendEnvelopeFromTemplate
    headers = {
        'AuthToken': GetAuthToken(),
        'Content-Type': 'application/json'  # Add this line
    }
    # The TemplateCode and the RoleID can be obtained using respectively
    # GetTemplateData() and GetTemplateInfo() implemented above.
    
    TemplateCode = 60592
    EmailSubject = "Here is your membership application"
    RecipientRoleID = "e15f5faa-a6c3-46ff-bb57-dc11276ef5b9"

    data = {
        "TemplateCode": TemplateCode,
        "Subject": EmailSubject,
        "SigningMethod": 0,
        "TemplateRoleRecipientMapping": [
            {
                "RoleID": RecipientRoleID,
                "RecipientEmail": email,
                "RecipientName": name
            }
        ]
    }

    response = requests.post(query, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        return "The envelope was successfully sent."
    else:
        return f"Failed to send envelope. Status code: {response.status_code}, Response: {response.text}"


def SendDynEnvelope(email, name, CustomerNbr, ContractNbr, CustomerString):
    SendEnvelopeFromTemplate = '/api/V1/Envelope/SendDynamicEnvelopeFromTemplate'
    query = BaseURL + SendEnvelopeFromTemplate
    headers = {
        'AuthToken': GetAuthToken(),
        'Content-Type': 'application/json'
    }
    TemplateCode = 62651  # To be updated
    EmailSubject = "Here is your rental contract (from app)"
    RecipientRoleID = "5d52c9a7-a310-4914-bb21-31573728c978"

    data = {
        "TemplateCode": TemplateCode,
        "Subject": EmailSubject,
        "PostSigningUrl": "https://itmx.de",
        "IsSingleSigningURL": "True",
        "SigningMethod": 0,
        "TemplateRoleRecipientMapping": [
            {
                "RecipientID": RecipientRoleID,
                "RecipientEmail": email,
                "RecipientName": name
            }
        ],
        "UpdateControls": [ # To be updated according to the template
            {
            "ControlID": "27ced1eb-2142-4520-bec7-7645be1fc5a5",
            "IsReadOnly": True,
            "ControlValue": CustomerNbr,
            },
            {
            "ControlID": "5cf8eb4e-fab4-4c9a-80ec-aa5327453a1c",
            "IsReadOnly": True,
            "ControlValue": ContractNbr,
            },
            {
            "ControlID": "0b813678-1e63-4fd8-970f-1821e0fca1a1",
            "IsReadOnly": False,
            "ControlValue": CustomerString,
            } 
        ]
    }

    response = requests.post(query, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        return "The envelope was successfully updated then sent."
    else:
        return f"Failed to send dynamic envelope. Status code: {response.status_code}, Response: {response.text}"


# Write the formatted JSON string to a text file
def write_to_file(content, filename):
    with open(filename, 'w') as f:
        f.write(content)
