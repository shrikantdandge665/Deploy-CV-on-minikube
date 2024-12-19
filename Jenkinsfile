pipeline {
    agent {
        docker {
            image 'shrikantdandge7/flask-cv-agent:latest'
             args '--user root -v /var/run/docker.sock:/var/run/docker.sock' // mount Docker socket to access the host's Docker daemon
        }
    }


    environment {
        SCANNER_HOME = tool 'sonar-scanner'
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
                script {
                    // Run Python unittests and generate a coverage report
                    sh 'python -m unittest discover'
                    sh 'coverage run -m unittest discover && coverage xml'
                }
            }
        }

        stage('SonarQube Analysis') {
            steps {
                script {
                    withSonarQubeEnv('sonar-server') { // Replace 'sonar-server' with your configured SonarQube server name
                        sh '''
                        $SCANNER_HOME/bin/sonar-scanner \
                        -Dsonar.projectKey=CV-minikube \
                        -Dsonar.projectName=CV-minkube \
                        -Dsonar.sources=./ \
                        -Dsonar.python.coverage.reportPaths=coverage.xml
                        '''
                    }
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
                script {
                    withDockerRegistry(credentialsId: 'docker-cred') { // Replace 'docker-cred' with your Jenkins Docker Hub credentials ID
                        sh "docker build -t $DOCKER_IMAGE ."
                    }
                }
            }
        }

        stage('Trivy Scan') {
            steps {
                script {
                    // Perform Trivy scan on the built Docker image and save output as HTML
                    sh "trivy image --format table -o trivy-report.html $DOCKER_IMAGE"
                }
            }
        }

        stage('Docker Image Push') {
            steps {
                script {
                    withDockerRegistry(credentialsId: 'docker-cred') {
                        sh "docker push $DOCKER_IMAGE"
                    }
                }
            }
        }
    }

}
