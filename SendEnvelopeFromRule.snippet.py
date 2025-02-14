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
