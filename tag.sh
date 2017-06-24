
IMG=faxg/hello-world-web:$1
echo "Tagging and push: $IMG"
docker tag faxg/hello-world-web:latest $IMG
docker push $IMG
