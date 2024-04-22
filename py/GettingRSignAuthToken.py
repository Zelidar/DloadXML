import os
import requests
from py.myTestCompany import ReferenceKey, EmailId, Password

BaseURL = 'https://api3.use.rsign.com'  # RSign Sandbox
AuthenticateIUser = '/api/V1/Authentication/AuthenticateIUser'

auth_token_file = 'MyAuthToken.txt'

def GetAuthToken():
    # Check if the AuthToken file exists. If no longer valid,
    # delete it, the following code will create a fresh one.
    if os.path.exists(auth_token_file):
        print(f"A {auth_token_file} file was found. The token will be read from there.")
        with open(auth_token_file, 'r') as file:
            AuthToken = file.read()
    else:
        # If file doesn't exist, make an API call to get a new token.
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


def RefreshAuthToken():
    # Delete the auth_token_file if it exists to ensure GetAuthToken generates a new token
    if os.path.exists(auth_token_file):
        os.remove(auth_token_file)
        print(f"{auth_token_file} deleted successfully.")
    else:
        print(f"No {auth_token_file} file to delete.")
    # Call GetAuthToken to get a new token
    return GetAuthToken()
