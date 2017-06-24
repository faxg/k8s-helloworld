#!/bin/sh
export NS=hello-world
echo "Using K8S namespace '$NS' ..."

POD=web-ui-deployment-1307918463-jcsf4

# ssh into container:
kubectl --namespace="$NS" exec -it $POD -- /bin/sh
