pipeline {
    agent any

    environment {
        DOCKERHUB_USER = "rozeen123"
        IMAGE_NAME     = "mock-api"
        IMAGE_TAG      = "${env.BUILD_NUMBER}"
        FULL_IMAGE     = "${DOCKERHUB_USER}/${IMAGE_NAME}:${IMAGE_TAG}"
        FULL_LATEST    = "${DOCKERHUB_USER}/${IMAGE_NAME}:latest"
        CONTAINER_NAME = "mock-api-ci"
        PORT           = "8000"
        BASE_URL       = "http://localhost:${PORT}"
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
                  docker build -t ${FULL_IMAGE} -t ${FULL_LATEST} .
                """
            }
        }

        stage('Run Container') {
            steps {
                sh """
                  docker rm -f ${CONTAINER_NAME} || true
                  docker run -d --name ${CONTAINER_NAME} -p ${PORT}:8000 ${FULL_IMAGE}
                """
            }
        }

        stage('Wait for Service') {
            steps {
                sh """
                  for i in \$(seq 1 30); do
                    if curl -fsS ${BASE_URL}/health > /dev/null; then
                      exit 0
                    fi
                    sleep 1
                  done
                  echo "Service did not become ready in time"
                  docker logs ${CONTAINER_NAME} || true
                  exit 1
                """
            }
        }

        stage('Pytest') {
            steps {
                sh """
                  pip install --no-cache-dir -r requirements.txt
                  pytest -v
                """
            }
        }

        stage('Docker Login + Push (only if tests passed)') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DH_USER', passwordVariable: 'DH_PASS')]) {
                    sh """
                      echo "\$DH_PASS" | docker login -u "\$DH_USER" --password-stdin
                      docker push ${FULL_IMAGE}
                      docker push ${FULL_LATEST}
                      docker logout
                    """
                }
            }
        }

        stage('Pull + Run Latest (verification)') {
            steps {
                sh """
                  docker rm -f ${CONTAINER_NAME} || true
                  docker pull ${FULL_LATEST}
                  docker run -d --name ${CONTAINER_NAME} -p ${PORT}:8000 ${FULL_LATEST}
                  for i in \$(seq 1 30); do
                    if curl -fsS ${BASE_URL}/health > /dev/null; then
                      exit 0
                    fi
                    sleep 1
                  done
                  echo "Pulled image did not become ready"
                  docker logs ${CONTAINER_NAME} || true
                  exit 1
                """
            }
        }
    }

    post {
        always {
            sh """
              docker logs ${CONTAINER_NAME} || true
              docker rm -f ${CONTAINER_NAME} || true
            """
        }
        cleanup {
            sh """
              docker image prune -f || true
            """
        }
    }
}
