
---

# CV Deployment on Minikube with CI/CD Pipeline

![cv-minikube (2)](https://github.com/user-attachments/assets/0930166d-5c7f-44c1-b0da-c9f4d8d3a8c5)




## Table of Contents

1. [Project Overview](#project-overview)
2. [Technologies Used](#technologies-used)
3. [Prerequisites](#prerequisites)
4. [Project Structure](#project-structure)
5. [Setting up the Project](#setting-up-the-project)
6. [Jenkins Pipeline](#jenkins-pipeline)
7. [Kubernetes Deployment](#kubernetes-deployment)
8. [Metrics Monitoring](#metrics-monitoring)
9. [Exposing Services](#exposing-services)
10. [Troubleshooting](#troubleshooting)


---

## Project Overview

This project demonstrates a Continuous Integration and Continuous Deployment (CI/CD) pipeline for deploying a **Flask-based CV application** on a **Kubernetes cluster** (Minikube). The pipeline is automated using **Jenkins**, and the application is containerized using **Docker**. The setup also includes monitoring the Kubernetes cluster using **Prometheus** and **Grafana**.

---

## Technologies Used

- **Python**: Flask framework for the application.
- **Docker**: Containerization of the application.
- **Kubernetes**: Deployment and orchestration of the application.
- **Minikube**: Local Kubernetes cluster for testing.
- **Jenkins**: CI/CD pipeline.
- **Prometheus & Grafana**: Metrics and monitoring.
- **SonarQube**: Static code analysis.
- **Trivy**: Docker image vulnerability scanning.
- **OWASP Dependency Check**: Dependency vulnerability scanning.

---

## Prerequisites

Ensure you have the following tools installed and configured:
1. **Minikube**: [Installation Guide](https://minikube.sigs.k8s.io/docs/start/)
2. **Docker**: [Installation Guide](https://docs.docker.com/get-docker/)
3. **Jenkins**: [Installation Guide](https://www.jenkins.io/doc/book/installing/)
4. **Helm**: [Installation Guide](https://helm.sh/docs/intro/install/)
5. **kubectl**: [Installation Guide](https://kubernetes.io/docs/tasks/tools/)
6. **Python 3.10 or later**
7. **Ngrok**: For GitHub webhook integration.

---


## Project Structure

```plaintext
DEPLOY CV ON MINIKUBE/
├── __pycache__/                 # Compiled Python files
├── manifests/                   # Kubernetes deployment manifests
│   ├── deployment.yml           # Deployment configuration for Kubernetes
│   ├── service.yml              # Service configuration for Kubernetes
├── static/                      # Static files for the Flask app
│   ├── style.css                # CSS for the application UI
├── templates/                   # HTML templates for the Flask app
│   ├── index.html               # Main HTML template
├── .gitignore                   # Git ignore file for untracked files
├── app.py                       # Main Flask application code
├── docker-compose.yml           # Docker Compose file for multi-container setup
├── Dockerfile                   # Dockerfile for containerizing the application
├── Jenkinsfile                  # Jenkins pipeline configuration
├── README.md                    # Project documentation
├── requirements.txt             # Python dependencies
├── sonar-project.properties     # SonarQube configuration
├── test_app.py                  # Unit tests for the Flask application
```

### Description of Key Components:
1. **`manifests/`**:
   - **`deployment.yml`**: Defines the Kubernetes Deployment resource to deploy the application pods.
   - **`service.yml`**: Defines the Kubernetes Service resource to expose the application pods.

2. **`static/`**:
   - Contains static assets like stylesheets and images required for the Flask app.

3. **`templates/`**:
   - Contains HTML templates for the Flask app's frontend.

4. **`.gitignore`**:
   - Lists files and directories to be ignored by Git version control.

5. **`app.py`**:
   - The main Python file containing the Flask application logic.

6. **`docker-compose.yml`**:
   - Defines multi-container Docker applications for local development and testing.

7. **`Dockerfile`**:
   - Specifies the instructions for building a Docker image for the Flask app.

8. **`Jenkinsfile`**:
   - Automates CI/CD processes like building, testing, and deploying the application.

9. **`requirements.txt`**:
   - Lists all the Python dependencies required by the Flask application.

10. **`sonar-project.properties`**:
    - Configures SonarQube for static code analysis.

11. **`test_app.py`**:
    - Contains unit tests for the Flask app to ensure code functionality.

---

## Setting up the Project

### 1. Clone the Repository
```bash
git clone https://github.com/shrikantdandge665/Deploy-CV-on-minikube.git
cd Deploy-CV-on-minikube
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Start Minikube
```bash
minikube start
```

### 4. Build Docker Image
```bash
docker build -t shrikantdandge7/cv-minikube:1.0 .
```

---

## Jenkins Pipeline

The **Jenkins pipeline** automates the process of building, testing, analyzing, and deploying the application.

### Pipeline Stages:
1. **Clone Repository**: Clones the GitHub repository.
2. **Install Dependencies**: Installs Python dependencies.
3. **Run Tests**: Executes unit tests.
4. **Static Code Analysis**: Scans the code using SonarQube.
5. **OWASP Dependency Check**: Scans dependencies for vulnerabilities.
6. **Build Docker Image**: Builds the Docker image.
7. **Trivy Scan**: Scans the Docker image for vulnerabilities.
8. **Docker Image Push**: Pushes the image to Docker Hub.
9. **Update Deployment File**: Updates the Kubernetes deployment YAML with the latest image.
10. **Cleanup Workspace**: Cleans up the Jenkins workspace.

---

## Kubernetes Deployment

### Deploy the Application:
1. Update the `deployment.yml` file with the correct Docker image tag:
   ```yaml
   image: shrikantdandge7/cv-minikube:1.0
   ```
2. Apply the Kubernetes manifests:
   ```bash
   kubectl apply -f manifests/deployment.yml
   kubectl apply -f manifests/service.yml
   ```

---

## Metrics Monitoring

### Install Node Exporter and Prometheus using Helm:
1. Add Helm repositories:
   ```bash
   helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
   helm repo update
   ```

2. Install Node Exporter:
   ```bash
   helm install node-exporter prometheus-community/prometheus-node-exporter
   ```

3. Install Prometheus and Grafana:
   ```bash
   helm install prometheus prometheus-community/kube-prometheus-stack
   ```

4. Access Grafana Dashboard:
   ```bash
   kubectl port-forward svc/prometheus-grafana 3000:80
   ```
   Open `http://localhost:3000` in your browser. Default credentials:
   - Username: `admin`
   - Password: `admin`

---

## Exposing Services

### Expose ArgoCD Service
```bash
minikube service example-argocd-server
```

### Start Ngrok Proxy
```bash
ngrok config add-authtoken 2TFLqU65KsLvLLsSZ6l2bU69OHk_2fqw57ZHde28c9fBBAwqS
ngrok http http://localhost:8080
```

### Expose Grafana Service
```bash
minikube service grafana -n monitoring
```

### Expose Application Service
```bash
minikube service cv-minikube-service
```

---

## Troubleshooting

### Common Issues:
1. **Minikube Not Starting**:
   - Verify virtualization is enabled on your system.
   - Restart your Minikube cluster: `minikube delete && minikube start`.

2. **Jenkins Builds Failing**:
   - Check logs in Jenkins: `Build > Console Output`.
   - Ensure the required Jenkins plugins are installed.

3. **Metrics Not Displayed**:
   - Verify Prometheus and Grafana pods are running:
     ```bash
     kubectl get pods -n kube-system
     ```

---

