pipeline {

    agent any

    environment {
        COMPOSE_DOCKER_CLI_BUILD = '1'
        DOCKER_BUILDKIT = '1'
    }

    stages {

        stage('Checkout Code') {
            steps {
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

        // ==========================================
        // Validate docker-compose.yml BEFORE deploy
        // ==========================================
        stage('Validate Compose File') {
            steps {
                sh 'docker compose config'
            }
        }

        // ==========================================
        // Build Backend Image
        // ==========================================
        stage('Build Backend Image') {
            steps {
                sh 'docker build -f backend.Dockerfile -t crud-backend .'
            }
        }

        // ==========================================
        // Build Frontend (Nginx) Image
        // ==========================================
        stage('Build Frontend (Nginx Image)') {
            steps {
                sh 'docker build -f frontend.Dockerfile -t crud-nginx .'
            }
        }

        // ==========================================
        // Stop old containers
        // ==========================================
        stage('Stop Existing Containers') {
            steps {
                sh 'docker compose down || true'
            }
        }

        // ==========================================
        // Start new containers (NO build here)
        // ==========================================
        stage('Start Services') {
            steps {
                sh 'docker compose up -d'
            }
        }

        // ==========================================
        // Verify Deployment
        // ==========================================
        stage('Verify Deployment') {
            steps {
                sh 'sleep 10'
                sh 'docker ps'
                sh 'curl -f http://localhost || exit 1'
            }
        }

        stage('Deployment Success') {
            steps {
                echo 'Deployment completed successfully!'
            }
        }
    }

    post {
        failure {
            echo 'Deployment failed!'
            sh 'docker compose logs || true'
        }
    }
}
