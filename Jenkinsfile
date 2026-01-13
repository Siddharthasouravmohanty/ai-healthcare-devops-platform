pipeline {
    agent any

    environment {
        IMAGE_NAME = "siddhu7978/ai-healthcare-devops-platform"
        IMAGE_TAG  = "v1"
        CONTAINER_NAME = "ai-healthcare-app"
    }

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/Siddharthasouravmohanty/ai-healthcare-devops-platform.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $IMAGE_NAME:$IMAGE_TAG .'
            }
        }

        stage('Push Image to Docker Hub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh '''
                    echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                    docker push $IMAGE_NAME:$IMAGE_TAG
                    '''
                }
            }
        }

        stage('Deploy to EC2') {
            steps {
                sh '''
                echo "Stopping old container if it exists..."
                docker stop $CONTAINER_NAME || true
                docker rm $CONTAINER_NAME || true

                echo "Pulling latest image..."
                docker pull $IMAGE_NAME:$IMAGE_TAG

                echo "Starting new container..."
                docker run -d \
                  --name $CONTAINER_NAME \
                  -p 80:5000 \
                  $IMAGE_NAME:$IMAGE_TAG
                '''
            }
        }
    }
}
