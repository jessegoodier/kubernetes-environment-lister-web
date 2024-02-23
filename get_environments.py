import subprocess
import json
import os

ClusterName = os.getenv("CLUSTER_NAME", "null")

def delete_existing_file():
    # If docs/index.md exists, delete it
    if os.path.exists("docs/index.md"):
        os.remove("docs/index.md")

def write_cluster_name():
    with open("docs/index.md", "a") as f:
        f.write(f"\n# {ClusterName}\n")
        print(f"\n# {ClusterName}")

def get_namespaces():
    # Get all namespaces
    namespaces = subprocess.run(["kubectl", "get", "ingress", "--all-namespaces", "-o", "json"], capture_output=True, text=True)
    namespaces = json.loads(namespaces.stdout)
    namespaces = sorted(set(item.get('metadata', {}).get('namespace') for item in namespaces.get('items', [])))
    return namespaces

def write_namespace(ns):
    with open("docs/index.md", "a") as f:
        f.write(f"\n## Namespace: {ns}\n")
        print(f"\n## Namespace: {ns}")

def get_ingress(ns):
    # Get all ingress
    ingress = subprocess.run(["kubectl", "get", "ingress", "-n", ns, "-o", "json"], capture_output=True, text=True)
    ingress = json.loads(ingress.stdout)
    ingress = [(rule.get('host'), path.get('path')) for item in ingress.get('items', []) for rule in item.get('spec', {}).get('rules', []) for path in rule.get('http', {}).get('paths', [])]
    return ingress

def write_ingress(host, path):
    if '(' in path:
        path = path.split('(')[0] + '/' # There will be more clean up to do here for more complex paths
    fqdn = f"\n<https://{host}{path}>\n"
    with open("docs/index.md", "a") as f:
        f.write(fqdn)
        print(fqdn)

def write_pod_container_image_table_open():
    with open("docs/index.md", "a") as f:
        f.write("\n<details><summary>Pods</summary>\n\n")
        f.write("\n| Pod | Container Name | Image |\n")
        print("\n| Pod | Container Name | Image |")
        f.write("| --- | -------------- | ----- |\n")
        print("| --- | -------------- | ----- |")

def write_pod_container_image_table_end():
    with open("docs/index.md", "a") as f:
        f.write("\n</details>\n")
        f.write("<br>\n")

def get_pods(ns):
    # Get all pods
    pods = subprocess.run(["kubectl", "get", "pod", "-n", ns, "-o", "json"], capture_output=True, text=True)
    pods = json.loads(pods.stdout)
    pods = [item.get('metadata', {}).get('name') for item in pods.get('items', [])]
    return pods

def get_container_names(ns, p):
    # Get all container names
    container_names = subprocess.run(["kubectl", "get", "pod", "-n", ns, p, "-o", "json"], capture_output=True, text=True)
    container_names = json.loads(container_names.stdout)
    container_names = [container.get('name') for container in container_names.get('spec', {}).get('containers', [])]
    return container_names

def write_container_images(ns, p, cn):
    # Get all container images
    container_images = subprocess.run(["kubectl", "get", "pod", "-n", ns, p, "-o", "jsonpath={.spec.containers[?(@.name=='" + cn + "')].image}"], capture_output=True, text=True)
    with open("docs/index.md", "a") as f:
        f.write(f"| {p} | {cn} | {container_images.stdout} |\n")
        print(f"| {p} | {cn} | {container_images.stdout} |")

def write_helm_list(ns):
    # Run helm list command
    helm_list = subprocess.run(["helm", "list", "-n", ns, "-o", "json"], capture_output=True, text=True)
    helm_list = json.loads(helm_list.stdout)

    # Write the output to a markdown table
    with open("docs/index.md", "a") as f:
        f.write("\n| Name | Namespace | Revision | Updated | Status | Chart | App Version |\n")
        print("\n| Name | Namespace | Revision | Updated | Status | Chart | App Version |")
        f.write("| --- | --- | --- | --- | --- | --- | --- |\n")
        print("| --- | --- | --- | --- | --- | --- | --- |")
        for release in helm_list:
            f.write(f"| {release['name']} | {release['namespace']} | {release['revision']} | {release['updated']} | {release['status']} | {release['chart']} | {release['app_version']} |\n")
            print(f"| {release['name']} | {release['namespace']} | {release['revision']} | {release['updated']} | {release['status']} | {release['chart']} | {release['app_version']} |")
        f.write("<br>\n")

def write_html_output():
    html_output = subprocess.run(["markdown2", "-x", "tables", "docs/index.md"],capture_output=True, text=True)
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

def manage_configmap():
    delete_cm = subprocess.run(["kubectl", "delete", "configmap", "html", "-n", "environment-lister"])
    create_cm = subprocess.run(["kubectl", "create", "configmap", "html", "-n", "environment-lister", "--from-file", "docs/index.html"])
    restart_pod = subprocess.run(["kubectl", "rollout", "restart", "deployment", "environment-lister-web", "-n", "environment-lister"])

# Call the functions
delete_existing_file()
if ClusterName != "null": write_cluster_name()

namespaces = get_namespaces()

for ns in namespaces:
    pods = get_pods(ns)
    if (len(pods))>0:
        write_namespace(ns)
        ingress = get_ingress(ns)
        for host, path in ingress:
            write_ingress(host, path)
        write_helm_list(ns)
        write_pod_container_image_table_open()
        for p in pods:
            container_names = get_container_names(ns, p)
            for cn in container_names:
                write_container_images(ns, p, cn)
        write_pod_container_image_table_end()

write_html_output()
manage_configmap()