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
        stage('Filter Relevant Changes') {
            steps {
                script {
                    def changes = sh(script: 'git diff --name-only HEAD~1', returnStdout: true).trim()
                    if (!changes.contains('index.html') && !changes.contains('manifests/deployment.yml') && !changes.contains('Dockerfile')) {
                        echo "No relevant changes detected. Skipping build."
                        currentBuild.result = 'NOT_BUILT'
                        error('Exiting pipeline since no relevant changes were detected.')
                    } else {
                        echo "Relevant changes detected. Proceeding with the build."
                    }
                }
            }
        }

        stage('Clone Repository') {
            steps {
                git url: 'https://github.com/shrikantdandge665/Deploy-CV-on-minikube.git', branch: 'main'
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
                    script {
                        def changes = sh(script: 'git diff --name-only HEAD~1', returnStdout: true).trim()
                        if (changes.contains('manifests/deployment.yml')) {
                            sh '''
                            # Set Git configuration
                            git config user.email "${GIT_USER_EMAIL}"
                            git config user.name "${GIT_USER_NAME}"
                            
                            # Update deployment.yml with the new image tag
                            sed -i "s|image: .*|image: ${DOCKER_IMAGE}|" manifests/deployment.yml
                            
                            # Commit and push changes
                            git add manifests/deployment.yml
                            git commit -m "Update deployment image to version ${BUILD_NUMBER} [ci skip]"
                            git push https://${GITHUB_TOKEN}@github.com/${GIT_USER_NAME}/${GIT_REPO_NAME} HEAD:main
                            '''
                        } else {
                            echo "No deployment file changes detected. Skipping update."
                        }
                    }
                }
            }
        }

        stage('Cleanup Workspace') {
            steps {
                deleteDir() // This cleans up the workspace
            }
        }
    }
}
