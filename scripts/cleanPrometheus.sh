printf "\n\033[1;31m## Deleting Prometheus namespace and Helm ressources\033[0m\n"
helm delete prometheus -n prometheus
helm repo remove prometheus-community
kubectl delete ns prometheus