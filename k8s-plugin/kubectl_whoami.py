# kubectl_whoami.py

import os
from kubernetes import client, config

def get_current_user():
    config.load_kube_config(os.getenv("KUBECONFIG"))

    kube_client = client.CoreV1Api()

    user = kube_client.read_user()

    return user

def main():
    try:
        # Get current user information
        user = get_current_user()

        # Display user information
        print("Current Kubernetes User:")
        print("  Username:", user.username)
        print("  Groups:", user.groups)
        print("  Authentication Method:", user.auth_method)
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
