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
        // Build Backend Image
        // ==========================================
        stage('Build Backend Image') {
            steps {
                sh 'docker build -f backend.Dockerfile -t crud-backend .'
            }
        }

        // ==========================================
        // Build Nginx Image (copies frontend files)
        // ==========================================
        stage('Build Frontend (Nginx Image)') {
            steps {
                sh 'docker build -f nginx.Dockerfile -t crud-nginx .'
            }
        }

        stage('Stop Existing Containers') {
            steps {
                sh 'docker compose down || true'
            }
        }

        stage('Start Services') {
            steps {
                sh 'docker compose up -d --build'
            }
        }

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
