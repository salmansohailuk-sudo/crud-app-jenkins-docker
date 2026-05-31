pipeline {
    agent any

    environment {
        COMPOSE_DOCKER_CLI_BUILD = '1'
        DOCKER_BUILDKIT = '1'
    }

    stages {

        stage('Checkout Code') {
            steps {
                // Pull latest code from repository
                checkout scm
            }
        }

        stage('Verify Docker Setup') {
            steps {
                sh 'docker --version'
                sh 'docker buildx version'
                sh 'docker compose version'
            }
        }

        stage('Build Backend Image') {
            steps {
                // Build backend Docker image
                sh 'docker build -f backend.Dockerfile -t crud-backend .'
            }
        }

        stage('Stop Existing Containers') {
            steps {
                // Stop and remove old containers
                sh 'docker compose down || true'
            }
        }

        stage('Start Services') {
            steps {
                // Start all services in detached mode
                sh 'docker compose up -d --build'
            }
        }

        stage('Verify Deployment') {
            steps {
                // Wait for containers to initialize
                sh 'sleep 10'

                // Check running containers
                sh 'docker ps'

                // Health check
                sh 'curl -f http://localhost || exit 1'
            }
        }
    }

    post {
        success {
            echo 'Deployment completed successfully!'
        }

        failure {
            echo 'Deployment failed!'

            // Show container logs for debugging
            sh 'docker compose logs || true'
        }
    }
}
```
