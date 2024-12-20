# Deploy-CV-on-minikube

# Expose argocd service in minkube
 minikube service example-argocd-server

# start ngrok proxy
 ngrok config add-authtoken 2TFLqU65KsLvLLsSZ6l2bU69OHk_2fqw57ZHde28c9fBBAwqS
 ngrok http http://localhost:8080

# Expose Grafana service in minikube
 minikube service grafana -n monitoring

# Expose Application service in minikube
 minikube service cv-minikube-service


