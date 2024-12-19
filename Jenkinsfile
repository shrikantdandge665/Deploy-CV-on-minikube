pipeline {
    agent {
        docker {
            image 'shrikantdandge7/flask-cv-agent:latest'
            args '--user root -v /var/run/docker.sock:/var/run/docker.sock' // Mount Docker socket
        }
    }

    environment {
        DOCKER_IMAGE = "shrikantdandge7/cv-minikube:${BUILD_NUMBER}"
    }

    stages {
        stage('Clone Repository') {
            steps {
                git url: 'https://github.com/shrikantdandge665/Deploy-CV-on-minikube.git', branch: 'main'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'python -m unittest discover'
                sh 'coverage run -m unittest discover && coverage xml'
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('sonar-server') { // Replace 'sonar-server' with your SonarQube server name
                    sh '''
                    sonar-scanner \
                    -Dsonar.projectKey=CV-minikube \
                    -Dsonar.projectName=CV-minikube \
                    -Dsonar.sources=. \
                    -Dsonar.python.coverage.reportPaths=coverage.xml \
                    -Dsonar.host.url=$SONAR_HOST_URL \
                    -Dsonar.login=$SONAR_AUTH_TOKEN
                    '''
                }
            }
        }

        stage('OWASP Dependency Check') {
            steps {
                dependencyCheck additionalArguments: '--scan ./', odcInstallation: 'DC'
                dependencyCheckPublisher pattern: '**/dependency-check-report.xml'
            }
        }

        stage('Build Docker Image') {
            steps {
                withDockerRegistry(credentialsId: 'docker-cred') { // Replace 'docker-cred' with your Docker Hub credentials ID
                    sh "docker build -t $DOCKER_IMAGE ."
                }
            }
        }

        stage('Trivy Scan') {
            steps {
                sh "trivy image --format table -o trivy-report.html $DOCKER_IMAGE"
            }
        }

        stage('Docker Image Push') {
            steps {
                withDockerRegistry(credentialsId: 'docker-cred') {
                    sh "docker push $DOCKER_IMAGE"
                }
            }
        }
    }
}
