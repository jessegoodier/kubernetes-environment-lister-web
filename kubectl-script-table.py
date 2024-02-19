import subprocess
import json
import os

ClusterName = "kc-integration-test"

# If docs/index.md exists, delete it
if os.path.exists("docs/index.md"):
    os.remove("docs/index.md")

with open("docs/index.md", "a") as f:
    f.write(f"\n# {ClusterName}\n")
    print(f"\n# {ClusterName}")

# Get all namespaces
namespaces = subprocess.run(["kubectl", "get", "ingress", "--all-namespaces", "-o", "json"], capture_output=True, text=True)
namespaces = json.loads(namespaces.stdout)
namespaces = sorted(set(item.get('metadata', {}).get('namespace') for item in namespaces.get('items', [])))

for ns in namespaces:
    with open("docs/index.md", "a") as f:
        f.write(f"\n## Namespace: {ns}\n")
        print(f"\n## Namespace: {ns}")

    # Get all ingress
    ingress = subprocess.run(["kubectl", "get", "ingress", "-n", ns, "-o", "json"], capture_output=True, text=True)
    ingress = json.loads(ingress.stdout)
    ingress = [rule.get('host') for item in ingress.get('items', []) for rule in item.get('spec', {}).get('rules', [])]

    for i in ingress:
        fqdn = f"\n<https://{i}>\n"
        with open("docs/index.md", "a") as f:
            f.write(fqdn)
            print(fqdn)

    with open("docs/index.md", "a") as f:
        f.write("\n| Pod | Container Name | Image |\n")
        f.write("| --- | -------------- | ----- |\n")

    # Get all pods
    pods = subprocess.run(["kubectl", "get", "pod", "-n", ns, "-o", "json"], capture_output=True, text=True)
    pods = json.loads(pods.stdout)
    pods = [item.get('metadata', {}).get('name') for item in pods.get('items', [])]

    for p in pods:
        # Get all container names
        container_names = subprocess.run(["kubectl", "get", "pod", "-n", ns, p, "-o", "json"], capture_output=True, text=True)
        container_names = json.loads(container_names.stdout)
        container_names = [container.get('name') for container in container_names.get('spec', {}).get('containers', [])]

        for cn in container_names:
            # Get all container images
            container_images = subprocess.run(["kubectl", "get", "pod", "-n", ns, p, "-o", "jsonpath={.spec.containers[?(@.name=='" + cn + "')].image}"], capture_output=True, text=True)
            with open("docs/index.md", "a") as f:
                f.write(f"| {p} | {cn} | {container_images.stdout} |\n")
                print(f"| {p} | {cn} | {container_images.stdout} |")

import subprocess
html_output = subprocess.run(["markdown2", "-x", "tables", "docs/index.md"],capture_output=True, text=True)

# output = html_output.stdout
# Write the output to a file
# with open('output.txt', 'w') as file:
#     file.write(output)

# Print the file
# with open("docs/index.md", "r") as f:
#     print(f.read())

header = f"""
<!DOCTYPE html>
<html>
<head>
    <title>envs on {ClusterName}</title>
    <link rel="icon" href="https://raw.githubusercontent.com/jessegoodier/kubernetes-environment-lister-web/main/docs/favicon.ico" type="image/x-icon">
    <link rel="stylesheet" type="text/css" href="css/styles.css">
</head><body>
"""

with open("docs/index.html", "w") as f:
    f.write(f"{header}\n")
    f.write(f"{html_output.stdout}")
    f.write(f"\n</body></html>\n")

delete_cm = subprocess.run(["kubectl", "delete", "configmap", "html", "-n", "environment-lister"])
create_cm = subprocess.run(["kubectl", "create", "configmap", "html", "-n", "environment-lister", "--from-file", "docs/index.html"])

