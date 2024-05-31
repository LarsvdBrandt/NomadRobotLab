import requests
import json
import time
import logging
import sys

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Define a function for authentication using requests
def get_access_token(url, username, password):
    """
    This function retrieves an access token using username and password for basic auth.
    """
    token_url = f"{url}/realms/fairdi_nomad_prod/protocol/openid-connect/token"
    auth_data = {
        "grant_type": "password",
        "client_id": "nomad_public",
        "username": username,
        "password": password
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(token_url, auth=(username, password), data=auth_data, headers=headers)
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        logger.error(f"Failed to retrieve access token: {response.text}")
        return None

def upload_file_with_metadata(username, password, upload_file, readers, writers):
    # Define NOMAD API URL and user credentials
    nomad_url = 'http://localhost/nomad-oasis/api/v1'
    url = 'https://nomad-lab.eu/fairdi/keycloak/auth'

    # Get access token
    access_token = get_access_token(url, username, password)
    if not access_token:
        return

    # Define headers with authorization
    headers = {"Authorization": f"Bearer {access_token}",
               "Accept": "application/json"}

    # Upload the file
    try:
        with open(upload_file, 'rb') as f:
            url = f"{nomad_url}/uploads"
            files = {"file": (upload_file, f)}
            response = requests.post(url, headers=headers, files=files)
            if response.status_code == 200:
                upload_data = response.json()
            else:
                logger.error(f"Error uploading file: {response.text}")
                return False
    except Exception as e:
        logger.error(f"Error opening or uploading file: {e}")
        return False

    # Check upload status and handle different scenarios
    upload_id = upload_data["upload_id"]
    while True:
        try:
            url = f"{nomad_url}/uploads/{upload_id}"
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                upload_data = response.json()
                # Check for 'process_running' as before
                if upload_data['data']['process_running']:
                    time.sleep(5)
                    print('Processing: %s, Status: %s' % (upload_data['data']['current_process'], upload_data['data']['process_status']))
                # If processing is complete, break the loop
                elif upload_data['data']['process_status'] == 'SUCCESS':
                    print('Processing: %s, Status: %s' % (upload_data['data']['current_process'], upload_data['data']['process_status']))
                    print(upload_data['data'])
                    break
                # If processing failed, log error and exit
                elif upload_data['data']['process_status'] == 'FAILED':
                    logger.error("Upload processing failed.")
                    logger.error(f"Errors: {upload_data['errors']}")
                    return False
                # Handle unexpected status (optional)
                else:
                    logger.warning(f"Unexpected process status: {upload_data['data']['process_status']}")
            else:
                logger.error(f"Error getting upload status: {response.text}")
                return False
        except Exception as e:
            logger.error(f"Error getting upload status: {e}")
            return False

    # Check if upload was successful
    if upload_data["data"]["process_status"] != 'SUCCESS':
        logger.error("Something went wrong during upload processing.")
        logger.error(f"Errors: {upload_data['errors']}")
        return False

    # Edit the metadata
    upload_id = upload_data["data"]["upload_id"]
    url = f"{nomad_url}/uploads/{upload_id}/edit"

    # Define metadata to update
    upload_user_id = upload_data["data"]["main_author"]

    # Define metadata to update
    metadata = {
        "comment": f"Owner: [{upload_user_id}], Reader: [{readers}], Writer: [{writers}]",
    }

    # Add readers to reviewers if readers exist
    if readers:
        metadata["reviewers"] = readers

    # Add writers to coauthors if writers exist
    if writers:
        metadata["coauthors"] = writers

    # Prepare request body
    payload = {
        "metadata": metadata,
    }

    headers = {"Authorization": f"Bearer {access_token}",
               "Accept": "application/json",
               "Content-Type": "application/json"}  # Set Content-Type for JSON

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            print("Upload successful and metadata updated.")
            return True
        else:
            logger.error(f"Error editing upload metadata: {response.text}")
            return False
    except Exception as e:
        logger.error(f"Error editing upload metadata: {e}")
        return False

def main():
    while True:
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        upload_file = input("Enter the path of the file to upload: ")
        readers = input("Enter the IDs of readers (separated by commas): ")
        writers = input("Enter the IDs of writers (separated by commas): ")

        if upload_file_with_metadata(username, password, upload_file, readers, writers):
            choice = input("Upload successful. Do you want to make another upload? (yes/no): ")
            if choice.lower() != 'yes':
                break
        else:
            choice = input("Upload failed. Do you want to try again? (yes/no): ")
            if choice.lower() != 'yes':
                break

if __name__ == "__main__":
    main()
