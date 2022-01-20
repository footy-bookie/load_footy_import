import requests


def get_vm_custom_envs(meta_key: str):
    response = requests.get(
        "http://metadata.google.internal/computeMetadata/v1/instance/attributes/{}".format(meta_key),
        headers={'Metadata-Flavor': 'Google'},
    )

    data = response.text

    return data
