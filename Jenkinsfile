pipeline {
    agent any
    environment {
        DOCKER_IMAGE = "shrikantdandge7/cv-minikube:${BUILD_NUMBER}"
        PATH = "$PATH:/var/lib/jenkins/.local/bin"
        SCANNER_HOME = tool 'sonar-scanner'
        SONAR_URL = "http://localhost:9000"
        GIT_REPO_NAME = "Deploy-CV-on-minikube"
        GIT_USER_NAME = "shrikantdandge665"
        GIT_USER_EMAIL = "shrikantdandge665@gmail.com"
    }

    stages {
        stage('Clone Repository') {
            steps {
                git url: 'https://github.com/shrikantdandge665/Deploy-CV-on-minikube.git', branch: 'main'
            }
        }

        stage('Skip Jenkins-triggered Builds') {
            steps {
                script {
                    def authorEmail = sh(
                        script: "git log -1 --pretty=format:'%ae'",
                        returnStdout: true
                    ).trim()
                    if (authorEmail == "${GIT_USER_EMAIL}") {
                        echo "Build skipped because it was triggered by Jenkins bot."
                        currentBuild.result = 'SUCCESS'
                        error("Stopping the pipeline because the commit was made by Jenkins bot.")
                    }
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip install --user -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'python -m unittest discover'
                sh 'coverage run -m unittest discover'
                sh 'coverage xml -o ./coverage.xml'
            }
        }

        stage('Static Code Analysis') {
            steps {
                withSonarQubeEnv('sonar-server') {
                    sh '''
                    $SCANNER_HOME/bin/sonar-scanner \
                    -Dsonar.projectKey=CV-minikube \
                    -Dsonar.projectName=CV-minikube \
                    -Dsonar.sources=. \
                    -Dsonar.python.coverage.reportPaths=coverage.xml \
                    -Dsonar.tests= \
                    -Dsonar.host.url=${SONAR_URL} \
                    -X
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

        stage('Update Deployment File') {
            steps {
                withCredentials([string(credentialsId: 'github', variable: 'GITHUB_TOKEN')]) {
                    sh '''
                    git config user.email "${GIT_USER_EMAIL}"
                    git config user.name "${GIT_USER_NAME}"
                    sed -i "s|image: .*|image: ${DOCKER_IMAGE}|" manifests/deployment.yml
                    git add manifests/deployment.yml
                    git commit -m "Update deployment image to version ${BUILD_NUMBER}"
                    git push https://${GITHUB_TOKEN}@github.com/${GIT_USER_NAME}/${GIT_REPO_NAME} HEAD:main
                    '''
                }
            }
        }

        stage('Cleanup Workspace') {
            steps {
                deleteDir()
            }
        }
    }
}
