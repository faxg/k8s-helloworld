#!/bin/sh
export NS=hello-world
echo "Using K8S namespace '$NS' ..."

# make sure namespace exists
kubectl apply -f ./manifests/namespace.yaml --record

# create configMaps, db backend (redis) and web-ui deployment
kubectl apply -f ./manifests/config.yaml --namespace="$NS" --record
kubectl apply -f ./manifests/deploy-webui.yaml --namespace="$NS" --record
kubectl apply -f ./manifests/deploy-db.yaml --namespace="$NS" --record



# ssh into container: kubectl --namespace=hello-world exec -it web-ui-deployment-1287265622-qvtrl -- /bin/sh

# kubectl rollout status deploy/web-ui-deployment --namespace="hello-world"
# kubectl rollout history deploy/web-ui-deployment --namespace="hello-world"
# kubectl rollout history deploy/web-ui-deployment --revision=2 --namespace="hello-world"
# kubectl rollout undo deploy/web-ui-deployment --to-revision=1 --namespace="hello-world"
# kubectl set image deploy/web-ui-deployment web-ui=faxg/hello-world-web:1.0.0 --namespace="hello-world"
# kubectl set image deploy/web-ui-deployment web-ui=faxg/hello-world-web:1.0.1 --namespace="hello-world"
