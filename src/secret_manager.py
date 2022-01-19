# run pip install google-cloud-secret-manager to install secretmanager
from google.cloud import secretmanager
from helpers import get_vm_custom_envs

footy_key_name = get_vm_custom_envs("FOOTY_KEY_NAME")

def access_secret_version(project_id):
    """
    Access the payload for the given secret version if one exists. The version
    can be a version number as a string (e.g. "5") or an alias (e.g. "latest").
    """
    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the secret version.
    name = f"projects/{project_id}/secrets/{footy_key_name}/versions/latest"

    # Access the secret version.
    response = client.access_secret_version(request={"name": name})
    payload = response.payload.data.decode("UTF-8")

    return payload
