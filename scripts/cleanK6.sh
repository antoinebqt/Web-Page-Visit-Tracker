printf "\n\033[1;31m## Deleting K6 deployment in default namespace\033[0m\n"
kubectl delete deployment k6-deployment
kubectl delete svc k6-service