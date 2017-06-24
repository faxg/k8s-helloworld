#!/bin/sh
export NS=hello-world
echo "Using K8S namespace '$NS' ..."


# delete previous deployments
kubectl delete cm/config --namespace="$NS"
kubectl delete cm/redis-config --namespace="$NS"
kubectl delete deployments/web-ui-deployment --namespace="$NS"
kubectl delete deployments/redis-deployment --namespace="$NS"

kubectl delete svc/web-ui --namespace="$NS"
kubectl delete svc/redis-db --namespace="$NS"

# remove namespace
kubectl delete -f ./manifests/namespace.yaml
