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


1. Install Prometheus and Grafana Using Helm
Helm is a package manager for Kubernetes that simplifies the deployment of Prometheus and Grafana.

Step 1: Add Helm Repositories
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update

Step 2: Install Prometheus
Deploy Prometheus using Helm:
helm install prometheus prometheus-community/prometheus --namespace monitoring --create-namespace

Step 3: Install Grafana
Deploy Grafana using Helm:
helm install grafana grafana/grafana --namespace monitoring

2. Install Node Exporter
Node Exporter is used to collect metrics from Kubernetes nodes (e.g., CPU, memory, disk usage).

# Install Node Exporter
helm install node-exporter prometheus-community/prometheus-node-exporter --namespace monitoring
3. Verify Installation
# Check Pods

kubectl get pods -n monitoring
You should see pods for Prometheus, Grafana, and Node Exporter.

# Access Prometheus UI
Forward Prometheus service port:

kubectl port-forward -n monitoring svc/prometheus-server 9090:80
Access Prometheus UI at http://localhost:9090.
# Access Grafana UI
Forward Grafana service port:

kubectl port-forward -n monitoring svc/grafana 3000:80
Access Grafana UI at http://localhost:3000.
Login to Grafana using the default credentials:
Username: admin
Password: Retrieve password with:
kubectl get secret --namespace monitoring grafana -o jsonpath="{.data.admin-password}" | base64 --decode
4. Configure Prometheus as a Data Source in Grafana
Log in to Grafana.
Navigate to Configuration > Data Sources > Add data source.
Select Prometheus and enter the following:
URL: http://prometheus-server.monitoring.svc.cluster.local
Click Save & Test.
5. Import Prebuilt Dashboards in Grafana
Grafana has prebuilt dashboards for Kubernetes and Node Exporter metrics.

Navigate to Dashboard > Import.
Use the following dashboard IDs for import:
Kubernetes Cluster Monitoring: 6417
Node Exporter Full: 1860
Once imported, Grafana will display the dashboards with data from Prometheus.
6. Optional: Expose Grafana and Prometheus Externally
To expose Grafana and Prometheus for external access, use an Ingress Controller or a LoadBalancer service.

Example: Expose Grafana
Modify the Grafana service:

yaml
Copy code
kubectl edit svc grafana -n monitoring
Change the type to LoadBalancer:

spec:
  type: LoadBalancer
Get the External IP

kubectl get svc -n monitoring
7. Node Exporter Metrics Monitored
Node Exporter will collect metrics such as:

CPU usage
Memory usage
Disk I/O
Network traffic
8. Verify and Test
Ensure all components are running:
kubectl get pods -n monitoring
Access Grafana dashboards to view metrics.
Use Prometheus queries to verify data collection:
Example: node_cpu_seconds_total, node_memory_Active_bytes.