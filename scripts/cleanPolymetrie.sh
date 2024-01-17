printf "\n\033[1;31m## Deleting content of default namespace and Helm ressources\033[0m\n"
kubectl delete deployment polymetrie-app
kubectl delete svc polymetrie-service
kubectl delete ingress polymetrie-ingress
kubectl delete hpa polymetrie-hpa
helm delete redis
helm delete postgresql
helm repo remove bitnami