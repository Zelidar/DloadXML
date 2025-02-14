# Setting the environment to connect to the RSign API
import json
import requests

# Fetching my RPost API credentials and the RSign API sandbox URL
from ToolKit.GettingRSignAuthToken import GetAuthToken
from ToolKit.myAccessData import BaseURL, TemplateCode
# Imports required to handle files i/o
import base64
import os

import xml.etree.ElementTree as ET

# For simulating an API call (taking some time)
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
    
    EmailSubject = "Here is your application form to fill and sign"
    # The below IDs must correspond to the selected template
    RecipientRoleID = "64b87822-9730-431b-9bdc-61a4dda48e0d"

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
    # The below IDs must correspond to the selected template
    EmailSubject = "Here is your application form to fill and sign"
    # The below IDs must correspond to the selected template
    RecipientRoleID = "64b87822-9730-431b-9bdc-61a4dda48e0d"

    data = {
        "TemplateCode": TemplateCode,
        "Subject": EmailSubject,
        "PostSigningUrl": "https://www.frama.com/en/thank-you-page-esign/",
        "SigningMethod": 0,
        "Documents": [
            {
                "Name": "DloadXMLb64.docx",
                "DocumentBase64Data": LoadB64dataForRule(),
            }
        ],
        "TemplateRoleRecipientMapping": [
            {
                "RoleID": RecipientRoleID,
                "RecipientEmail": email,
                "RecipientName": name,
            },
            {
                "RoleID": "57098f46-b072-482c-b57d-f101e93ca461",
                "RecipientEmail": "zaid.el-hoiydi@frama.com",
                "RecipientName": "Company Administration"
            }
            ],
            "UpdateControls": [
            { # textControl
            "ControlID": "73e28e4d-4a21-4c1b-9b5a-20145392a78b",
            "IsReadOnly": True,
            "ControlValue": CustomerNbr,
            },
            { # textControl
            "ControlID": "d4d9eb82-1d47-4da4-8b03-d8a6533abcd8",
            "IsReadOnly": True,
            "ControlValue": ContractNbr,
            },
            { # textControl
            "ControlID": "e9e78dc0-1c46-4ec2-882c-6c83c66a8923",
            "IsReadOnly": False,
            "ControlValue": CustomerString, # CustLongString1
            },
            { # textControl
            "ControlID": "932fb5d4-1e49-4cb0-9115-26bb88ca8da6",
            "IsReadOnly": False,
            "ControlValue": "Enter your long text here", # CustLongString2
            },
            { # textControl
            "ControlID": "f996e5fe-b61b-4a4c-a5b2-84ed152ef766",
            "IsReadOnly": False,
            "ControlValue": "Enter your text 1 here", # CustEntryText1
            },
            { # textControl
            "ControlID": "455b6343-63d6-4d70-8482-2b12f82a0025",
            "IsReadOnly": False,
            "ControlValue": "Enter your text 2 here", # CustEntryText2
            },
            { # nameControl
            "ControlID": "58c00f2a-133a-4ac3-8cf3-8521af492bfa",
            "IsReadOnly": False,
            "ControlValue": name,
            },
            { #emailControl
            "ControlID": "ad72a5a4-7d6c-426d-89b2-9ce51c49bf09",
            "IsReadOnly": True,
            "ControlValue": email,
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
