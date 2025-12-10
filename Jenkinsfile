pipeline {
    agent any

    environment {
        IMAGE_NAME      = "mock-api"
        IMAGE_TAG       = "latest"
        DOCKERHUB_USER  = "rozeen123"
        DOCKERHUB_REPO  = "mock-api"
        DOCKER_CREDS_ID = "dockerhub-credentials"   // צריך ליצור ב־Jenkins
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh """
                    echo "📦 Building Docker image..."
                    docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
                """
            }
        }

        stage('Run Container for Tests') {
            steps {
                sh """
                    echo "🚀 Starting test container..."
                    docker run -d --rm -p 8000:8000 --name ${IMAGE_NAME}-test ${IMAGE_NAME}:${IMAGE_TAG}
                    sleep 3
                """
            }
        }

        stage('Run Pytest Inside Container') {
            steps {
                sh """
                    echo "🧪 Running tests..."
                    docker exec ${IMAGE_NAME}-test pytest -v
                """
            }
        }

        stage('Stop Test Container') {
            steps {
                sh """
                    echo "🛑 Stopping test container..."
                    docker stop ${IMAGE_NAME}-test || true
                """
            }
        }

        stage('Docker Login') {
            when {
                anyOf {
                    branch 'main'
                    branch 'master'
                }
            }
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: "${DOCKER_CREDS_ID}",
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )
                ]) {
                    sh """
                        echo "🔐 Logging in to Docker Hub..."
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                    """
                }
            }
        }

        stage('Tag & Push Docker Image') {
            when {
                anyOf {
                    branch 'main'
                    branch 'master'
                }
            }
            steps {
                sh """
                    echo "🏷️ Tagging image..."
                    docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${DOCKERHUB_USER}/${DOCKERHUB_REPO}:${IMAGE_TAG}

                    echo "⬆️ Pushing to Docker Hub..."
                    docker push ${DOCKERHUB_USER}/${DOCKERHUB_REPO}:${IMAGE_TAG}
                """
            }
        }

        stage('Pull & Run Image from Docker Hub') {
            when {
                anyOf {
                    branch 'main'
                    branch 'master'
                }
            }
            steps {
                sh """
                    echo "⬇️ Pulling image from Docker Hub..."
                    docker pull ${DOCKERHUB_USER}/${DOCKERHUB_REPO}:${IMAGE_TAG}

                    echo "🚀 Running pulled image..."
                    docker run -d --rm -p 8000:8000 --name ${IMAGE_NAME}-prod ${DOCKERHUB_USER}/${DOCKERHUB_REPO}:${IMAGE_TAG}
                    sleep 3
                """
            }
        }

    }

    post {
        always {
            sh """
                echo "🧹 Cleaning up containers..."
                docker stop ${IMAGE_NAME}-test || true
                docker stop ${IMAGE_NAME}-prod || true
                docker ps -a
            """
        }
    }
}
