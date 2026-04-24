pipeline {
    agent any  // run on any available Jenkins node

    stages {

        stage('Checkout Code') {
            steps {
                // Pull latest code from repository
                checkout scm
            }
        }

        stage('Build Backend Image') {
            steps {
                // Build Docker image for backend service
                // -f specifies Dockerfile
                sh 'docker build -f backend.Dockerfile -t crud-backend .'
            }
        }

        stage('Stop Existing Containers') {
            steps {
                // Stop old running containers (if any)
                // prevents port conflicts
                sh 'docker-compose down || true'
            }
        }

        stage('Start Services') {
            steps {
                // Start backend + nginx containers
                // -d runs in background
                sh 'docker-compose up -d'
            }
        }

        stage('Verify Deployment') {
            steps {
                // Simple health check
                sh 'sleep 5'
                sh 'curl -f http://localhost || exit 1'
            }
        }
    }
}
