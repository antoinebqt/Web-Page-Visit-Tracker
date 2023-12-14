echo "Delete Kubernetes Dashboard Namespace"
kubectl delete ns kubernetes-dashboard
echo "Clean Default Namespace"
./scripts/cleanDefaultNS.sh
./cleanDefaultNS.sh