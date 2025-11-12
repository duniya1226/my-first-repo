#Ass1setA1
# Variables
PROJECT_NAME="vprofile-project"
BUILD_ID=$BUILD_NUMBER
TIMESTAMP=$(date +%Y%m%d%H%M%S)
VERSIONED_WAR="${PROJECT_NAME}-${BUILD_ID}-${TIMESTAMP}.war"
VERSIONS_DIR="versions"

# Create versions directory if not exists
mkdir -p $VERSIONS_DIR

# Copy and rename WAR
cp target/*.war ${VERSIONS_DIR}/${VERSIONED_WAR}
echo "Versioned WAR created: ${VERSIONS_DIR}/${VERSIONED_WAR}"

#q2
PROJECT_NAME="vprofile-project"
BUILD_ID=$BUILD_NUMBER               # Jenkins build number
TIMESTAMP=$(date +%Y%m%d%H%M%S)     # Current timestamp
VERSIONED_WAR="${PROJECT_NAME}-${BUILD_ID}-${TIMESTAMP}.war"
VERSIONS_DIR="versions"

# Step 1: Build the Maven project
echo "Building the project with Maven..."
mvn clean install

mkdir -p $VERSIONS_DIR

WAR_FILE="target/${PROJECT_NAME}.war"

if [ -f "$WAR_FILE" ]; then
    cp "$WAR_FILE" "${VERSIONS_DIR}/${VERSIONED_WAR}"
    echo "WAR file versioned and stored as ${VERSIONS_DIR}/${VERSIONED_WAR}"
else
    echo "Error: WAR file not found at ${WAR_FILE}"
  
 #Ass2setAq1 
  pipeline {
    agent { label 'builtinubuntu' }

    tools {
        // Use Maven and JDK configured in Jenkins global tool configuration
        maven 'maven 3.9.10'
        jdk 'openjdk 21.0.7'
    }

    stages {
        stage('Fetch Code') {
            steps {
                echo 'Cloning Git repository...'
                git branch: 'main', url: 'https://github.com/hkhcoder/vprofile-project.git'
            }
        }

        stage('Unit Test') {
            steps {
                echo 'Running unit tests...'
                sh 'mvn test'
            }
        }

        stage('Build Code') {
            steps {
                echo 'Packaging application (skip tests)...'
                sh 'mvn package -DskipTests'
            }
        }

        stage('Archive Artifact') {
            steps {
                echo 'Archiving WAR files...'
                archiveArtifacts artifacts: '**/*.war', allowEmptyArchive: false
            }
        }

        stage('Deploy to Staging') {
            when {
                expression { currentBuild.currentResult == 'SUCCESS' }
            }
            steps {
                echo 'Deploying artifact to staging server.'
            }
        }
    }

    post {
        failure {
            echo 'Build failed. Notifying the development team.'
        }
    }
}
#q4
pipeline {
    agent { label 'aws-ec2-cloud-agent' }

    tools {
        maven 'Maven-3.9.10'      // Maven version configured in Jenkins global tools
        jdk 'openjdk 21.0.7'      // JDK version configured in Jenkins global tools
    }

    environment {
        PROJECT_NAME = "vprofile-v2"
        VERSIONS_DIR = "versions"
        BUILD_TIMESTAMP = "${new Date().format('yyyyMMddHHmmss')}"
    }

    stages {
        stage('Fetch Source Code') {
            steps {
                echo 'Cloning Git repository...'
                git branch: 'main', url: 'https://github.com/hkhcoder/vprofile-project.git'
            }
        }

        stage('Build Project') {
            steps {
                echo 'Building project using Maven...'
                sh 'mvn clean package -DskipTests'
            }
        }

        stage('Version WAR File') {
            steps {
                echo "Creating versions directory if it does not exist..."
                sh "mkdir -p ${VERSIONS_DIR}"

                echo "Copying WAR file to versions directory with versioned filename..."
                sh """
                cp target/${PROJECT_NAME}.war ${VERSIONS_DIR}/${PROJECT_NAME}-${BUILD_NUMBER}-${BUILD_TIMESTAMP}.war
                """
            }
        }

        stage('Run Unit Tests') {
            steps {
                echo 'Running unit tests...'
                sh 'mvn test'
            }
        }
    }

    post {
        success {
            echo "Build completed successfully. WAR file is stored in ${VERSIONS_DIR}."
            archiveArtifacts artifacts: 'versions/*.war', allowEmptyArchive: false
        }
        failure {
            echo 'Build failed. Check Jenkins console output for details.'
        }
    }
}

        
