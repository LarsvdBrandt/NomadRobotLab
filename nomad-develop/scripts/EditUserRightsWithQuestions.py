# TODO: Add and remove coauthors and reviewers accordingly to  writer and reader.

import requests
import logging

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

# Define a function to update metadata with new comment
def update_metadata(access_token, upload_id, new_comment):
    """
    Update metadata of the upload with a new comment.
    """
    edit_url = f"{nomad_url}/uploads/{upload_id}/edit"

    # Extract readers and writers from the comment
    metadata = {"comment": new_comment}
    viewers = parse_viewers_roles(new_comment)
    writers = parse_writers_roles(new_comment)
    if viewers:
        metadata["reviewers"] = viewers
    if writers:
        metadata["coauthors"] = writers

        print(metadata)

        payload = {"metadata": metadata}
        headers = {"Authorization": f"Bearer {access_token}", "Accept": "application/json", "Content-Type": "application/json"}
        response = requests.post(edit_url, headers=headers, json=payload)
        if response.status_code == 200:
            print("Metadata updated successfully.")
            return True
        else:
            logger.error(f"Failed to update metadata: {response.text}")
            return False

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


def add_user_to_role(comment, role, user_id):
    """
    Add a user ID to the specified role in the comment metadata.
    """
    # Find the role entry in the comment
    role_start = comment.find(role)
    if role_start != -1:
        # Role exists, find the end of the role entry
        role_end = comment.find("]", role_start)
        # Extract the existing role entry
        existing_role_entry = comment[role_start:role_end+1]
        # Extract user IDs from the existing role entry
        existing_user_ids = existing_role_entry.split("[")[1].split("]")[0].split(", ")
        # Append the new user ID if it's not already in the list
        if user_id not in existing_user_ids:
            existing_user_ids.append(user_id)
        # Join the user IDs and update the existing role entry
        updated_role_entry = f"{role}: [{', '.join(existing_user_ids)}]"
        # Replace the existing role entry with the updated one
        comment = comment.replace(existing_role_entry, updated_role_entry)
    else:
        # Role doesn't exist, create a new role entry
        new_role_entry = f", {role}: [{user_id}]"
        # Check if there are existing roles, if not, add the role at the beginning
        roles_start = comment.find("Owner")
        if roles_start != -1:
            roles_end = comment.find("]", roles_start)
            comment = comment[:roles_end] + new_role_entry + comment[roles_end:]
        else:
            comment += new_role_entry
    return comment



# Define a function to remove a user ID from a role
def remove_user_from_role(comment, role, user_id):
    """
    Remove a user ID from the specified role in the comment metadata.
    """
    role_start = comment.find(role)
    if role_start != -1:
        role_end = comment.find("]", role_start)
        existing_role_entry = comment[role_start:role_end+1]
        existing_user_ids = existing_role_entry.split("[")[1].split("]")[0].split(", ")

        # Check if the user ID to be removed is an owner and if there's more than one owner
        if role == "Owner" and user_id in existing_user_ids and len(existing_user_ids) == 1:
            print("Cannot remove the only owner. There must always be at least one owner.")
            return comment

        new_role_entry = existing_role_entry.replace(f", {user_id}", "").replace(f"{user_id}, ", "").replace(user_id, "").strip(", ")
        comment = comment.replace(existing_role_entry, new_role_entry)
    return comment

def is_user_owner(comment, user_id):
    """
    Check if the user is one of the owners of the document.
    """
    owners_start = comment.find("Owner")
    if owners_start != -1:
        owners_end = comment.find("]", owners_start)
        owner_ids = comment[owners_start:owners_end+1].split("[")[1].split("]")[0].split(", ")
        return user_id in owner_ids
    return False

def parse_viewers_roles(comment):
  """
  Check all viewers and return a comma-separated string of their IDs.
  """
  viewers_start = comment.find("Reader")
  if viewers_start != -1:
    owners_end = comment.find("]", viewers_start)
    owner_ids = comment[viewers_start:owners_end+1].split("[")[1].split("]")[0].split(", ")
    # filter out empty ids
    owner_ids = [id for id in owner_ids if id]
    return ", ".join(owner_ids)  # join the list with commas
  return ""

def parse_writers_roles(comment):
  """
  Check all writers and return a comma-separated string of their IDs.
  """
  viewers_start = comment.find("Writer")
  if viewers_start != -1:
    owners_end = comment.find("]", viewers_start)
    owner_ids = comment[viewers_start:owners_end+1].split("[")[1].split("]")[0].split(", ")
    # filter out empty ids
    owner_ids = [id for id in owner_ids if id]
    return ", ".join(owner_ids)  # join the list with commas
  return ""

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

        # Get upload entries
        entries_data = get_upload_entries(access_token, upload_id)
        if not entries_data:
            choice = input("Failed to retrieve upload entries. Do you want to try again? (yes/no): ")
            if choice.lower() != 'yes':
                break
            else:
                continue

        entries = entries_data.get("data")
        if not entries:
            print("No entries found for the upload.")
            choice = input("Do you want to try again? (yes/no): ")
            if choice.lower() != 'yes':
                break
            else:
                continue

        for entry in entries:
            comment = entry.get("entry_metadata", {}).get("comment")
            if comment:
                # Extract user id
                user_id = user_data.get("user_id")
                print("Comment:", comment)
                print("User id:", user_id)

                # Check if the user is the owner
                if is_user_owner(comment, user_id):
                    action = input("Do you want to add or remove a user? (add/remove): ")
                    role = input("Enter the role (Owner/Writer/Reader): ")
                    new_user_id = input("Enter the user ID to add/remove: ")

                    if action.lower() == "add":
                        comment = add_user_to_role(comment, role, new_user_id)
                    elif action.lower() == "remove":
                        comment = remove_user_from_role(comment, role, new_user_id)
                    else:
                        print("Invalid action.")
                        continue

                    # Update metadata with new comment
                    if update_metadata(access_token, upload_id, comment):
                        choice = input("Metadata updated successfully. Do you want to update another document? (yes/no): ")
                        if choice.lower() != 'yes':
                            break
                    else:
                        choice = input("Metadata update failed. Do you want to try again? (yes/no): ")
                        if choice.lower() != 'yes':
                            break

                else:
                    print("User is not the owner of this document.")
            else:
                print("No comment found for this document.")

if __name__ == "__main__":
    main()
