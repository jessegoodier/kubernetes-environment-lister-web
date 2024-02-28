import subprocess
import json
import os

ClusterName = os.getenv("CLUSTER_NAME", "null")

output = {"ClusterName": ClusterName, "Namespaces": []}

def get_namespaces():
    # Get all namespaces
    namespaces = subprocess.run(["kubectl", "get", "ingress", "--all-namespaces", "-o", "json"], capture_output=True, text=True)
    namespaces = json.loads(namespaces.stdout)
    namespaces = sorted(set(item.get('metadata', {}).get('namespace') for item in namespaces.get('items', [])))
    return namespaces

def get_ingress(ns):
    # Get all ingress
    ingress = subprocess.run(["kubectl", "get", "ingress", "-n", ns, "-o", "json"], capture_output=True, text=True)
    ingress = json.loads(ingress.stdout)
    ingress = [(rule.get('host'), path.get('path')) for item in ingress.get('items', []) for rule in item.get('spec', {}).get('rules', []) for path in rule.get('http', {}).get('paths', [])]
    return ingress

def get_pods(ns):
    # Get all pods
    pods = subprocess.run(["kubectl", "get", "pod", "-n", ns, "-o", "json"], capture_output=True, text=True)
    pods = json.loads(pods.stdout)
    pods = [item.get('metadata', {}).get('name') for item in pods.get('items', [])]
    return pods

def get_container_names_and_status(ns, p):
    # Get all container names and their status
    pod_info = subprocess.run(["kubectl", "get", "pod", "-n", ns, p, "-o", "json"], capture_output=True, text=True)
    pod_info = json.loads(pod_info.stdout)
    containers = pod_info.get('spec', {}).get('containers', [])
    statuses = pod_info.get('status', {}).get('containerStatuses', [])
    container_names_and_status = []
    for container, status in zip(containers, statuses):
        container_names_and_status.append({
            'name': container.get('name'),
            'status': status.get('state')
        })
    return container_names_and_status

def get_container_images(ns, p, cn):
    # Get all container images
    container_images = subprocess.run(["kubectl", "get", "pod", "-n", ns, p, "-o", "jsonpath={.spec.containers[?(@.name=='" + cn + "')].image}"], capture_output=True, text=True)
    return container_images.stdout

namespaces = get_namespaces()

for ns in namespaces:
    namespace_data = {"Namespace": ns, "Ingress": [], "Pods": []}
    ingress = get_ingress(ns)
    print(ns)
    for host, path in ingress:
        namespace_data["Ingress"].append({"Host": host, "Path": path})
    pods = get_pods(ns)
    for p in pods:
        pod_data = {"Pod": p, "Containers": []}
        print(p)
        container_info = get_container_names_and_status(ns, p)
        for info in container_info:
            container_image = get_container_images(ns, p, info['name'])
            print(info['name'], container_image, info['status'])
            pod_data["Containers"].append({"ContainerName": info['name'], "Image": container_image, "Status": info['status']})
        namespace_data["Pods"].append(pod_data)
    output["Namespaces"].append(namespace_data)

with open("docs/index.json", "w") as f:
    f.write(json.dumps(output, indent=2))