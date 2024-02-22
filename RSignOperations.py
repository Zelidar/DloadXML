# Setting the environment to connecto to RSign
import json
import requests
# Fetching RPost API credentials and URL
from GettingRSignAuthToken import GetAuthToken, BaseURL

import base64
import os
import xml.etree.ElementTree as ET

import time
def SimCall(SimCallNumber):
    time.sleep(3)
    print(f"A RSign call was simulated returning: {SimCallNumber}")
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
    return response.json()


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


def LoadB64dataForRule():
    base_filename = 'DloadXMLb64'  # Common base filename
    docx_template_file = base_filename + '.docx'
    b64_template_file = base_filename + '.b64'

    if os.path.exists(b64_template_file):
        print(f"Loading B64 template from {b64_template_file}")
        with open(b64_template_file, 'r') as file:
            return file.read()

    elif os.path.exists(docx_template_file):
        print(f"Converting DOCX template to B64...")
        with open(docx_template_file, 'rb') as file:  # Open in binary mode
            binary_data = file.read()
            encoded_data = base64.b64encode(binary_data)

        with open(b64_template_file, 'wb') as file:
            file.write(encoded_data) 

        return encoded_data.decode('utf-8')  
    
    else:
        print(f"Error! Template file {docx_template_file} not found.")
        return None


def GetTemplateInfo(TemplateCode):
    GetEndpointString = '/api/V1/Template/GetTemplateInfo/' + str(TemplateCode)
    headers = {'AuthToken': GetAuthToken()}
    query = BaseURL + GetEndpointString
    response = requests.get(query, headers=headers)
    return response.json()


def GetEnvelopeStatus(EnvelopeCode):
    GetEndpointString = '/api/V1/Envelope/GetEnvelopeStatus/' + str(EnvelopeCode)
    headers = {'AuthToken': GetAuthToken()}
    query = BaseURL + GetEndpointString
    response = requests.get(query, headers=headers)
    return response.json()


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


def SendEnvelopeFromTemplate(email, name):
    query = BaseURL + '/api/V1/Envelope/SendEnvelopeFromTemplate'
    headers = {
        'AuthToken': GetAuthToken(),
        'Content-Type': 'application/json'
    }
    # The TemplateCode and the RoleID can be obtained using respectively
    # GetTemplateData() and GetTemplateInfo() implemented above.
    
    TemplateCode = 62651
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


def SendEnvelopeFromRule(email, name, CustomerNbr, ContractNbr, CustomerString):
    query = BaseURL + '/api/V1/Envelope/SendEnvelopeFromRule'
    headers = {
        'AuthToken': GetAuthToken(),
        'Content-Type': 'application/json'
    }
    TemplateCode = 62673  # This needs to correspond to the below RoleName and ControlId

    EmailSubject = "Contract Document (sent from CRM)"

    data = { # To be updated accordingly
        "TemplateCode": TemplateCode,
        "Subject": EmailSubject,
        "SigningMethod": 0,
        "Documents": [
            {
                "Name": "DloadXMLb64.docx",
                "DocumentBase64Data": LoadB64dataForRule(),
            }
        ],
        "TemplateRoleRecipientMapping": [
            {
                "RoleID": "8ec6a891-0f10-4aca-8183-4d22db911801",
                "RecipientEmail": email,
                "RecipientName": name,
            },
            {
                "RoleID": "1bc66b98-50a4-452c-872b-ed19c44f8adf",
                "RecipientEmail": "zaid.el-hoiydi@frama.com",
                "RecipientName": "Company Administration"
            }
            ],
            "UpdateControls": [
            {
            "ControlID": "4348e7e5-9b71-4861-aea7-eeb5cb03cdd1",
            "IsReadOnly": True,
            "ControlValue": CustomerNbr,
            },
            {
            "ControlID": "2fd8505b-9fbf-4ec4-896c-212b3d5a22a3",
            "IsReadOnly": True,
            "ControlValue": ContractNbr,
            },
            {
            "ControlID": "73e44240-c5f0-4b78-bd74-c7a2247d3974",
            "IsReadOnly": False,
            "ControlValue": CustomerString,
            } 
        ]
    }

    response = requests.post(query, headers=headers, data=json.dumps(data))
    
    if response.status_code == 200:
        print("The envelope was successfully sent (rule).")
        return response.json()
    else:
        return f"Failed to send envelope (rule). Status code: {response.status_code}, Response: {response.text}"


def SendDynEnvelope(email, name, CustomerNbr, ContractNbr, CustomerString):
    SendEnvelopeFromTemplate = '/api/V1/Envelope/SendDynamicEnvelopeFromTemplate'
    query = BaseURL + SendEnvelopeFromTemplate
    headers = {
        'AuthToken': GetAuthToken(),
        'Content-Type': 'application/json'
    }
    TemplateCode = 62673  # This needs to correspond to the below RoleID

    # Section for the signer
    EmailSubject = "Here is a Health History Form (sent from CRM)"
    RecipientRoleID = "8ec6a891-0f10-4aca-8183-4d22db911801"

    # Section for the company owning the CRM
    CompanyRoleID = "1bc66b98-50a4-452c-872b-ed19c44f8adf"
    CompanyEmail = "zaid.el-hoiydi@frama.com"
    CompanyName = "Company Administration"

    data = {
        "TemplateCode": TemplateCode,
        "Subject": EmailSubject,
        "PostSigningUrl": "https://www.frama.com/en/digital-products/electronic-signature/",
        "IsSingleSigningURL": "False",
        "SigningMethod": 0,
        "TemplateRoleRecipientMapping": [
            {
                "RecipientID": RecipientRoleID,
                "RecipientEmail": email,
                "RecipientName": name,
            },
            {
                "RecipientID": CompanyRoleID,
                "RecipientEmail": CompanyEmail,
                "RecipientName": CompanyName,
            }
        ],
        "UpdateControls": [ # To be updated according to the template
            {
            "ControlID": "e2936ae9-e3ee-4b27-b5a0-572b7305d736",
            "IsReadOnly": True,
            "ControlValue": CustomerNbr,
            },
            {
            "ControlID": "fc6686ea-1e29-4767-b050-6fe491f9fa88",
            "IsReadOnly": True,
            "ControlValue": ContractNbr,
            },
            {
            "ControlID": "192aaab0-a4fb-45bf-a941-45ae2be84538",
            "IsReadOnly": False,
            "ControlValue": CustomerString,
            } 
        ]
    }

    response = requests.post(query, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        print(f"The envelope was successfully prefilled then sent: {response.status_code}, Response: {response.text}")
        return response.json()
    else:
        print(f"Failed to send dynamic envelope. Status code: {response.status_code}, Response: {response.text}")
        return None


# Write the formatted JSON string to a text file
def write_to_file(content, filename):
    with open(filename, 'w') as f:
        f.write(content)
