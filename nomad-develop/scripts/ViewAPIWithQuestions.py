import requests
import logging
import json
import re

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Define NOMAD API URL and keycloak URL
nomad_url = 'http://localhost/nomad-oasis/api/v1'
keycloak_url = 'https://nomad-lab.eu/fairdi/keycloak/auth'

# Define a function for authentication using requests
def authenticate(username, password):
    """
    Authenticate the user and return the access token.
    """
    token_url = f"{keycloak_url}/realms/fairdi_nomad_prod/protocol/openid-connect/token"
    auth_data = {
        "grant_type": "password",
        "client_id": "nomad_public",
        "username": username,
        "password": password
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(token_url, data=auth_data, headers=headers)
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        logger.error(f"Failed to retrieve access token: {response.text}")
        return None

# Define a function to get upload entries
def get_upload_entries(access_token, upload_id):
    """
    Retrieve the entries of a specific upload.
    """
    entries_url = f"{nomad_url}/uploads/{upload_id}/entries?page_size=10&order=asc"
    headers = {"Authorization": f"Bearer {access_token}", "Accept": "application/json"}
    response = requests.get(entries_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        logger.error(f"Failed to retrieve upload entries: {response.text}")
        return None

# Define a function to get user data
def get_user_data(access_token):
    """
    Retrieve the user data of the authenticated user.
    """
    user_url = f"{nomad_url}/users/me"
    headers = {"Authorization": f"Bearer {access_token}", "Accept": "application/json"}
    response = requests.get(user_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        logger.error(f"Failed to retrieve user data: {response.text}")
        return None

def parse_comment(comment):
    """
    Parse the comment string into a dictionary.
    """
    roles = re.findall(r'(\w+):\s*\[(.*?)\]', comment)
    return {role.strip(): [id.strip() for id in ids.split(',')] for role, ids in roles}

def has_permission(comment_data, user_id, role):
    """
    Check if the user has the specified role in the comment data.
    """
    return user_id in comment_data.get(role, [])


def main():
    while True:
        # Ask for user input
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        upload_id = input("Enter the upload ID: ")

        # Authenticate user and get access token
        access_token = authenticate(username, password)
        if not access_token:
            choice = input("Authentication failed. Do you want to try again? (yes/no): ")
            if choice.lower() != 'yes':
                break
            else:
                continue

        # Get user data
        user_data = get_user_data(access_token)
        if not user_data:
            logger.error("Failed to retrieve user data.")
            choice = input("Do you want to try again? (yes/no): ")
            if choice.lower() != 'yes':
                break
            else:
                continue

        # Extract user id
        user_id = user_data.get("user_id")

        # Get upload entries
        entries_data = get_upload_entries(access_token, upload_id)
        if entries_data:
            entries = entries_data.get("data")
            if entries:
                for entry in entries:
                    comment = entry.get("entry_metadata", {}).get("comment")

                    if comment:
                        # Parse comment and check permissions
                        comment_data = parse_comment(comment)
                        has_permission_flag = False  # Renamed the boolean variable
                        for role in ["Owner", "Reader", "Writer"]:
                            if has_permission(comment_data, user_id, role):
                                print(f"User has {role} role on this upload, data: {json.dumps(entry)}")
                                has_permission_flag = True
                                break

                        if not has_permission_flag:  # Updated the variable reference
                            print("User has no permission to look at this document.")
                    else:
                        print("No comment found for this entry.")
        else:
            print("Failed to retrieve upload entries.")

        choice = input("Do you want to check another upload? (yes/no): ")
        if choice.lower() != 'yes':
            break

if __name__ == "__main__":
    main()
