kubectl delete deployment polymetrie
kubectl delete svc polymetrie-service
kubectl delete ingress polymetrie-ingress
helm delete redis
helm delete postgresql