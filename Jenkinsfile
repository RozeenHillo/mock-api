pipeline {
    agent any

    environment {
        DOCKERHUB_USER = "rozeen123"
        IMAGE_NAME     = "mock-api"
        IMAGE_TAG      = "latest"
        FULL_IMAGE     = "${DOCKERHUB_USER}/${IMAGE_NAME}:${IMAGE_TAG}"
        CONTAINER_NAME = "mock-api-ci"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t mock-api:local .'
            }
        }

        stage('Run Container (CI mode)') {
            steps {
                sh '''
                  docker rm -f ${CONTAINER_NAME} || true
                  docker run -d --name ${CONTAINER_NAME} mock-api:local
                '''
            }
        }

        stage('Wait for Service') {
    steps {
        sh '''
          for i in {1..20}; do
            if docker exec mock-api-ci curl -sf http://localhost:8000/health; then
              echo "Service is ready"
              exit 0
            fi
            echo "Waiting for service..."
            sleep 2
          done
          echo "Service did not become ready"
          exit 1
        '''
    }
}


        stage('Run Pytest') {
            steps {
                sh '''
                  pip install --no-cache-dir -r requirements.txt
                  pytest -v
                '''
            }
        }

        stage('Docker Login & Push') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'Docker_cred',
                    usernameVariable: 'DH_USER',
                    passwordVariable: 'DH_PASS'
                )]) {
                    sh '''
                      echo "$DH_PASS" | docker login -u "$DH_USER" --password-stdin
                      docker tag mock-api:local ${FULL_IMAGE}
                      docker push ${FULL_IMAGE}
                    '''
                }
            }
        }

        stage('Pull & Run From Docker Hub (Verification)') {
            steps {
                sh '''
                  docker rm -f ${CONTAINER_NAME} || true
                  docker pull ${FULL_IMAGE}
                  docker run -d --name ${CONTAINER_NAME} ${FULL_IMAGE}
                  docker exec ${CONTAINER_NAME} curl -s http://localhost:8000/health
                '''
            }
        }
    }

    post {
        always {
            sh 'docker logs ${CONTAINER_NAME} || true'
            sh 'docker rm -f ${CONTAINER_NAME} || true'
        }
    }
}

