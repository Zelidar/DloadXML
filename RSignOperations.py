# Setting the environment to connect to the RSign API
import json
import requests

# Imports required to handle files i/o
import base64
import os

import xml.etree.ElementTree as ET

# For simulating an API call (taking some time)
import time

# Fetching my RPost API credentials and the RSign API sandbox URL
from GettingRSignAuthToken import GetAuthToken, BaseURL


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
    # Define the payload with the calculated start and end dates,
    # this only to limit the number of envelopes in the response.
    payload = {
        "StartDate": start_date_str,
        "EndDate": end_date_str,
        "Period": 24,
        "MasterEnvelopeID": "",
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


def GetUserData(EnvelopeID, userElements):
    GetEndpointString = '/api/V1/Manage/GetDownloadeDataByCode/' + str(EnvelopeID)
    headers = {'AuthToken': GetAuthToken()}
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
                elements_dict[label].append(text_value)
    else:
        # Handle cases where Base64FileData is not present or empty
        elements_dict = {name: [] for name in userElements}  # Using empty list for consistency
    return elements_dict


def LoadB64dataForRule():
    base_filename = 'DloadXMLb64'  # Common base filename
    docx_template_file = base_filename + '.docx'
    b64_template_file = base_filename + '.b64'

    # This will check is a b64 file is already present,
    # it will otherwise perform a docx to b64 conversion.
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


def GetEnvelopeStatus(EnvelopeID):
    GetEndpointString = '/api/V1/Envelope/GetEnvelopeStatus/' + str(EnvelopeID)
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
    
    TemplateCode = 62651    # This needs to correspond to the below RoleID
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
    TemplateCode = 65581  # This needs to correspond to the below RoleID and ControlId

    EmailSubject = "Contract Document (sent from CRM)"

    data = {
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
                "RoleID": "27a6ea94-5900-45cc-8241-d9ba3e75dfc4",
                "RecipientEmail": email,
                "RecipientName": name,
            },
            {
                "RoleID": "21bcca0b-b8ca-4a3c-bbcb-d43cbb9ca90b",
                "RecipientEmail": "zaid.el-hoiydi@frama.com",
                "RecipientName": "Company Administration"
            }
            ],
            "UpdateControls": [
            {
            "ControlID": "9ecb8bd8-0352-476d-9981-267da1d3f891",
            "IsReadOnly": True,
            "ControlValue": CustomerNbr,
            },
            {
            "ControlID": "4df3b132-577a-4ddc-a067-0bb3ffd01e55",
            "IsReadOnly": True,
            "ControlValue": ContractNbr,
            },
            {
            "ControlID": "8b9f98aa-1cd8-46cf-ad81-bf2cdc28afb1",
            "IsReadOnly": False,
            "ControlValue": CustomerString, # CustLongString1
            },
            {
            "ControlID": "d8e6e3ea-063f-4c0d-bb87-01eff5ae50a2",
            "IsReadOnly": False,
            "ControlValue": "Enter your text here", # CustLongString2
            },
            {
            "ControlID": "30a80604-a4a5-471a-acdd-45cae6790b03",
            "IsReadOnly": False,
            "ControlValue": "Your text here", # CustEntryText1
            },
            {
            "ControlID": "08fed352-a2c1-4d55-998f-34d096ff876f",
            "IsReadOnly": False,
            "ControlValue": "You text here", # CustEntryText2
            },
            {
            "ControlID": "902966d1-f54f-45d1-940a-daef47416b37",
            "IsReadOnly": True,
            "ControlValue": "What do you like?", # DropDownControl
            },
            {
            "ControlID": "c8263488-cbef-41ff-8f15-24fd95ffde6a",
            "IsReadOnly": True,
            "ControlValue": name, # nameControl
            },
            {
            "ControlID": "a0215f88-188f-4692-b774-01c5ef152643",
            "IsReadOnly": True,
            "ControlValue": email, #emailControl
            },
            { # Radio button text
            "ControlID": "28911b85-a2d6-4d8e-98c3-d3b0177cc709",
            "IsReadOnly": True,
            "ControlValue": "Earth - 12'756 km",
            },
            { # Radio button text
            "ControlID": "b54eb008-ad68-4f9b-8ff5-815e62f9f4c7",
            "IsReadOnly": True,
            "ControlValue": "Neptune - 49'526 km",
            },
            { # Radio button text
            "ControlID": "84e07b2e-af93-4824-9fde-f0098e0ca4f6",
            "IsReadOnly": True,
            "ControlValue": "Saturn - 116'464 km",
            },
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
    TemplateCode = 62830  # This needs to correspond to the below RoleID and ControlId

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
