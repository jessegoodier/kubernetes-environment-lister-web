# kubernetes-web-environment-lister

Find all the namespaces with ingresses and list the pods/containers/images

## Usage

Clone this repo:

```sh
gh repo clone jessegoodier/kubernetes-web-environment-lister
```

Edit the manifests to fit your needs and:

```sh
kubectl create configmap environment-script -n environment-lister --from-file kubectl-script-table.py
kubectl apply -f ./manifests -n environment-lister
```
