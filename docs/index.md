# qa-eks
## Namespace: environment-lister

<https://envs.qa-eks.kubecost.io/>

| Name | Namespace | Revision | Updated | Status | Chart | App Version |
| --- | --- | --- | --- | --- | --- | --- |
| oauth2-proxy | environment-lister | 1 | 2024-02-20 10:22:09.638462734 -0500 -0500 | deployed | oauth2-proxy-6.24.1 | 7.6.0 |
<br>

<details><summary>Pods</summary>


| Pod | Container Name | Image |
| --- | -------------- | ----- |
| environment-lister-web-f44bb7965-cwphk | environment-lister | nginxinc/nginx-unprivileged |
| environment-lister-web-f44bb7965-s8qs8 | environment-lister | nginxinc/nginx-unprivileged |
| get-environments-28479699-xk9b2 | get-environments | jgoodier/markdown2-kubectl:0.0.4 |
| oauth2-proxy-6b79859857-9hpf4 | oauth2-proxy | quay.io/oauth2-proxy/oauth2-proxy:v7.6.0 |

</details>
<br>

## Namespace: kubecost-single-cluster

<https://standalone.qa-eks.kubecost.io/>

| Name | Namespace | Revision | Updated | Status | Chart | App Version |
| --- | --- | --- | --- | --- | --- | --- |
| kubecost-single-cluster | kubecost-single-cluster | 17 | 2024-02-24 09:30:57.921076 -0400 AST | deployed | cost-analyzer-v0.0.1708762629 | v0.0.1708762629 |
<br>

<details><summary>Pods</summary>


| Pod | Container Name | Image |
| --- | -------------- | ----- |
