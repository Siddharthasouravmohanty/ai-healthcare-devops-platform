pipeline {
    agent any

    environment {
        IMAGE_NAME = "siddhu7978/ai-healthcare-devops-platform"
        CONTAINER_NAME = "ai-healthcare-app"
        STATE_DIR = "/var/lib/jenkins/deploy-state"
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
                    echo "Deploying version: v-${env.VERSION}"
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${IMAGE_NAME}:v-${VERSION} ."
            }
        }

        stage('Push Image to Docker Hub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh """
                    echo "${DOCKER_PASS}" | docker login -u "${DOCKER_USER}" --password-stdin
                    docker push ${IMAGE_NAME}:v-${VERSION}
                    """
                }
            }
        }

        stage('Deploy to EC2') {
            steps {
                withCredentials([string(
                   credentialsId: 'openai-api-key',
                    variable: 'OPENAI_KEY'
                )]) {
                    sh """
                    mkdir -p ${STATE_DIR}

                    if [ -f "${STATE_DIR}/current.txt" ]; then
                        cp ${STATE_DIR}/current.txt ${STATE_DIR}/previous.txt
                    fi

                    echo "v-${VERSION}" > ${STATE_DIR}/current.txt

                    echo "Stopping old container..."
                    docker stop ${CONTAINER_NAME} || true
                    docker rm ${CONTAINER_NAME} || true

                    echo "Pulling image..."
                    docker pull ${IMAGE_NAME}:v-${VERSION}

                    echo "Starting new container..."
                    docker run -d \
                      --restart unless-stopped \
                      --name ${CONTAINER_NAME} \
                      -p 80:5000 \
                      -e OPENAI_API_KEY=${OPENAI_KEY} \
                      ${IMAGE_NAME}:v-${VERSION}
                    """
                }
            }
        }
    }
}
