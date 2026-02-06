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
        withCredentials([string(
            credentialsId: 'OPENAI_API_KEY',
            variable: 'OPENAI_KEY'
        )]) {
            sh '''
            mkdir -p $STATE_DIR

            if [ -f "$STATE_DIR/current.txt" ]; then
                cp $STATE_DIR/current.txt $STATE_DIR/previous.txt
            fi

            echo "v-${VERSION}" > $STATE_DIR/current.txt

            echo "Stopping old container..."
            docker stop $CONTAINER_NAME || true
            docker rm $CONTAINER_NAME || true

            echo "Pulling image $IMAGE_NAME:v-${VERSION}"
            docker pull $IMAGE_NAME:v-${VERSION}

            echo "Starting new container..."
            docker run -d \
              --restart unless-stopped \
              --name $CONTAINER_NAME \
              -p 80:5000 \
              -e OPENAI_API_KEY=$OPENAI_KEY \
              $IMAGE_NAME:v-${VERSION}
            '''
        }
    }
}

