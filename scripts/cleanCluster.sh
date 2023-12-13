kubectl delete deployment polymetrie-app
kubectl delete svc polymetrie-service
kubectl delete ingress polymetrie-ingress
helm delete redis
helm delete postgresql