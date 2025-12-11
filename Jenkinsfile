pipeline {
    agent any

    environment {
        IMAGE_NAME      = "mock-api"
        IMAGE_TAG       = "latest"
        DOCKERHUB_USER  = "rozeen123"
        DOCKERHUB_REPO  = "mock-api"
        DOCKER_CREDS_ID = "dockerhub-credentials"   // השם המדויק מג'נקינס
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
                    echo "🐳 Building Docker image..."
                    docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
                """
            }
        }

        stage('Run Container for Tests') {
            steps {
                sh """
                    echo "🚀 Starting test container..."
                    docker stop ${IMAGE_NAME}-test || true
                    docker rm ${IMAGE_NAME}-test || true
                    docker run -d --name ${IMAGE_NAME}-test -p 8000:8000 ${IMAGE_NAME}:${IMAGE_TAG}
                """
            }
        }

        stage('Run Pytest') {
            steps {
                sh """
                    echo "🧪 Running tests..."
                    sleep 3
                    pytest test_app.py
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
                withCredentials([usernamePassword(
                    credentialsId: "${DOCKER_CREDS_ID}",
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh """
                        echo "🔑 Logging in to Docker Hub..."
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

                    echo "📤 Pushing image to Docker Hub..."
                    docker push ${DOCKERHUB_USER}/${DOCKERHUB_REPO}:${IMAGE_TAG}
                """
            }
        }
    }
}
