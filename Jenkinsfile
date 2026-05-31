pipeline {

// Use any available Jenkins agent/node
// Jenkins will run this pipeline on any machine
// connected to Jenkins that is available
agent any

// Global environment variables used by all stages
environment {

    // Enables Docker CLI-based builds
    // Required for modern Docker Compose + Buildx
    COMPOSE_DOCKER_CLI_BUILD = '1'

    // Enables Docker BuildKit
    // BuildKit provides faster and more efficient builds
    DOCKER_BUILDKIT = '1'
}

// All pipeline stages are defined here
stages {

    // ==========================================
    // STAGE 1 - Checkout source code
    // ==========================================
    stage('Checkout Code') {

        steps {

            // Pull latest source code from Git repository
            // Uses repository configured in Jenkins job
            checkout scm
        }
    }

    // ==========================================
    // STAGE 2 - Verify Docker installation
    // ==========================================
    stage('Verify Docker Setup') {

        steps {

            // Show installed Docker version
            // Useful for debugging build environment
            sh 'docker --version'

            // Show Docker Buildx version
            // Ensures required Buildx plugin exists
            sh 'docker buildx version'

            // Show Docker Compose plugin version
            // Confirms docker compose command works
            sh 'docker compose version'
        }
    }

    // ==========================================
    // STAGE 3 - Build backend Docker image
    // ==========================================
    stage('Build Backend Image') {

        steps {

            // Build backend image using backend.Dockerfile
            //
            // -f backend.Dockerfile
            // tells Docker which Dockerfile to use
            //
            // -t crud-backend
            // assigns image name/tag
            //
            // . means current directory as build context
            sh 'docker build -f backend.Dockerfile -t crud-backend .'
        }
    }

    // ==========================================
    // STAGE 4 - Stop old containers
    // ==========================================
    stage('Stop Existing Containers') {

        steps {

            // Stop and remove old running containers
            //
            // Prevents:
            // - port conflicts
            // - duplicate containers
            // - stale deployments
            //
            // || true prevents pipeline failure
            // if no containers currently exist
            sh 'docker compose down || true'
        }
    }

    // ==========================================
    // STAGE 5 - Start application services
    // ==========================================
    stage('Start Services') {

        steps {

            // Start all services defined in docker-compose.yml
            //
            // -d runs containers in detached/background mode
            //
            // --build forces rebuild before startup
            // ensuring latest code changes are used
            sh 'docker compose up -d --build'
        }
    }

    // ==========================================
    // STAGE 6 - Verify deployment health
    // ==========================================
    stage('Verify Deployment') {

        steps {

            // Wait for containers to fully initialize
            // Prevents health check from running too early
            sh 'sleep 10'

            // Display running containers
            // Useful for troubleshooting deployments
            sh 'docker ps'

            // Perform simple HTTP health check
            //
            // curl -f:
            // fails if HTTP status is 4xx or 5xx
            //
            // exit 1:
            // explicitly fails Jenkins stage if app unreachable
            sh 'curl -f http://localhost || exit 1'
        }
    }

    // ==========================================
    // STAGE 7 - Success notification
    // ==========================================
    stage('Deployment Success') {

        steps {

            // Display success message in Jenkins console
            echo 'Deployment completed successfully!'
        }
    }
}

// ==========================================
// POST ACTIONS
// Runs after pipeline finishes
// ==========================================
post {

    // Executes only if pipeline fails
    failure {

        // Display failure message
        echo 'Deployment failed!'

        // Show container logs for debugging
        //
        // Helps identify:
        // - application startup issues
        // - nginx errors
        // - database connection failures
        //
        // || true prevents secondary failure
        // if containers are missing
        sh 'docker compose logs || true'
    }
}


}
