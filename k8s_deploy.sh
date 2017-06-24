#!/bin/sh
export NS=hello-world
echo "Using K8S namespace '$NS' ..."

# make sure namespace exists
kubectl apply -f ./manifests/namespace.yaml

# create configMaps, db backend (redis) and web-ui deployment
kubectl apply -f ./manifests/config.yaml --namespace="$NS"
kubectl apply -f ./manifests/deploy-webui.yaml --namespace="$NS"
kubectl apply -f ./manifests/deploy-db.yaml --namespace="$NS"



# ssh into container: kubectl --namespace=hello-world exec -it web-ui-deployment-1287265622-qvtrl -- /bin/sh
