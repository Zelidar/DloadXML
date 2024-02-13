import os
import requests
from myTestCompany import ReferenceKey, EmailId, Password

BaseURL = 'https://api3.use.rsign.com'  # RSign Sandbox
AuthenticateIUser = '/api/V1/Authentication/AuthenticateIUser'

def GetAuthToken():
    auth_token_file = 'MyAuthToken.txt'

    # Check if the AuthToken file exists. If no longer valid,
    # delete it, the following code will create a fresh one.
    if os.path.exists(auth_token_file):
        print(f"A {auth_token_file} file was found. The token will be read from there.")
        with open(auth_token_file, 'r') as file:
            AuthToken = file.read()
    else:
        # If file doesn't exist, make API call to get a new token.
        print(f"No token file available. Getting a new one ...")
        payload = {'ReferenceKey': ReferenceKey, 'EmailID': EmailId, 'Password': Password}
        query = BaseURL + AuthenticateIUser
        AuthResponse = requests.post(query, data=payload)

        print(AuthResponse.json()['AuthMessage'])
        print(AuthResponse.json()['EmailId'])

        AuthToken = AuthResponse.json()['AuthToken']
        print(AuthToken)

        # Optionally save the AuthToken to a file for future use
        with open(auth_token_file, 'w') as file:
            file.write(AuthToken)

    return AuthToken