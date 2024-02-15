# Setting the environment to connecto to RSign
import json
import requests
# Fetching my RPost test credentials
from GettingRSignAuthToken import GetAuthToken, BaseURL

import base64
import xml.etree.ElementTree as ET

import time
def SimCall(SimCallNumber):
    time.sleep(5)
    return SimCallNumber


def GetTemplateData():
    GetEndpointString = '/api/V1/Template/GetTemplateRuleList'
    headers = {'AuthToken': GetAuthToken()}
    query = BaseURL + GetEndpointString
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


def GetEnvelopeInfo():
    from datetime import datetime, timedelta
    # Get the current date and time
    current_time = datetime.now()
    # Calculate the start date as 2 weeks before the current date
    start_date = current_time - timedelta(weeks=2)
    # Format the dates in the required format (mm/dd/YYYY)
    start_date_str = start_date.strftime("%m/%d/%Y")
    end_date_str = current_time.strftime("%m/%d/%Y")
    # Define the payload with the calculated start and end dates
    payload = {
        "StartDate": start_date_str,
        "EndDate": end_date_str,
        "Period": 24,
        "MasterEnvelopeCode": "",
        "SenderEmail": "zaid.el-hoiydi_tc@frama.com",
        "SignerEmail": "",
        "Status": "Completed;Terminated",
        "DetailOrSummary": "Summary"
    }

    GetEndpointString = '/api/V1/Envelope/GetEnvelopeStatusInfo'
    headers = {'AuthToken': GetAuthToken()}
    query = BaseURL + GetEndpointString
    response = requests.post(query, headers=headers, data=payload)
    myData = response.json()
    return myData


def GetUserData(EnvelopeCode, userElements):
    GetEndpointString = '/api/V1/Manage/GetDownloadeDataByCode/' + str(EnvelopeCode)
    headers = {'AuthToken': GetAuthToken()}  # Ensure GetAuthToken() is defined elsewhere
    query = BaseURL + GetEndpointString
    response = requests.get(query, headers=headers)
    json_data = response.json()
    # Extract the Base64-encoded XML data
    base64_encoded_xml = json_data.get('Base64FileData', '')
    elements_dict = {}
    if base64_encoded_xml:
        # Decode the Base64-encoded XML data
        xml_data = base64.b64decode(base64_encoded_xml).decode('utf-8')
        # Parse the XML data
        root = ET.fromstring(xml_data)
        
        for control in root.iter('Control'):
            label = control.attrib.get('label')
            if label in userElements:
                text_value = control.attrib.get('text')
                if label not in elements_dict:
                    elements_dict[label] = []
                # elements_dict[label].append({'Name': label, 'Text': text_value})
                elements_dict[label].append(text_value)
    else:
        # Handle cases where Base64FileData is not present or empty
        elements_dict = {name: [] for name in userElements}  # Using empty list for consistency
    return elements_dict


def GetTemplateInfo(TemplateCode):
    GetEndpointString = '/api/V1/Template/GetTemplateInfo/' + str(TemplateCode)
    headers = {'AuthToken': GetAuthToken()}
    query = BaseURL + GetEndpointString
    response = requests.get(query, headers=headers)
    myData = response.json()
    return myData


def GetRolesInfo(TemplateCode):
    # Endpoint with the TemplateCode
    GetEndpointString = '/api/V1/Template/GetTemplateInfo/' + str(TemplateCode)
    headers = {'AuthToken': GetAuthToken()}
    query = BaseURL + GetEndpointString
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


# def GetXMLdata(EnvelopeCode):
#     GetEndpointString = '/api/V1/Template/GetDownloadeDataByCode/' + str(EnvelopeCode)
#     headers = {'AuthToken': GetAuthToken()}
#     query = BaseURL + GetEndpointString
#     response = requests.get(query, headers=headers)
#     myData = response.json()

#     return myData


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
