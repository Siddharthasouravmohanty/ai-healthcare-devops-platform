pipeline {
    agent any

    environment {
        IMAGE_NAME = "siddhu7978/ai-healthcare-devops-platform"
    }

    stages {

        stage('Checkout Code') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/Siddharthasouravmohanty/ai-healthcare-devops-platform.git'
            }
        }

        stage('Generate Version') {
            steps {
                script {
                    env.VERSION = sh(
                        script: "git rev-parse --short HEAD",
                        returnStdout: true
                    ).trim()
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh "docker build -t $IMAGE_NAME:v-${VERSION} ."
            }
        }

        stage('Push Image') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh '''
                    echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                    docker push $IMAGE_NAME:v-${VERSION}
                    '''
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh """
                kubectl set image deployment/ai-healthcare-app \
                ai-healthcare=$IMAGE_NAME:v-${VERSION}

                kubectl rollout status deployment/ai-healthcare-app
                """
            }
        }
    }
}