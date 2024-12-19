pipeline {
    agent any
    environment {
        DOCKER_IMAGE = "shrikantdandge7/cv-minikube:${BUILD_NUMBER}"
        PATH = "$PATH:/var/lib/jenkins/.local/bin" // Add this line to include the directory in PATH
    }

    stages {
        stage('Clone Repository') {
            steps {
                git url: 'https://github.com/shrikantdandge665/Deploy-CV-on-minikube.git', branch: 'main'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip install --user -r requirements.txt' // Use --user to install in user directory
            }
        }

        stage('Run Tests') {
            steps {
                sh 'python -m unittest discover'
                sh 'coverage run -m unittest discover && coverage xml'
            }
        }

        stage('Static Code Analysis') {
            environment {
                SONAR_URL = "http://localhost:9000"
            }
            steps {
                withCredentials([string(credentialsId: 'sonar', variable: 'SONAR_AUTH_TOKEN')]) {
                    sh '''
                    sonar-scanner \
                    -Dsonar.projectKey=CV-minikube \
                    -Dsonar.projectName=CV-minikube \
                    -Dsonar.sources=. \
                    -Dsonar.python.coverage.reportPaths=coverage.xml \
                    -Dsonar.host.url=${SONAR_URL} \
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
                withDockerRegistry(url: 'https://index.docker.io/v1/', credentialsId: 'docker-cred') {
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
                withDockerRegistry(url: 'https://index.docker.io/v1/', credentialsId: 'docker-cred') {
                    sh "docker push $DOCKER_IMAGE"
                }
            }
        }
    }
}
