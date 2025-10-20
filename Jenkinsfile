pipeline {
  agent any

  environment {
    IMAGE_NAME = 'awanmh/simple-app'              // Ganti 'awanmh' dengan username Docker Hub kalian
    REGISTRY_CREDENTIALS = 'dockerhub-credentials'
  }

  stages {

    stage('Checkout') {
      steps {
        echo 'Checkout source code...'
        checkout scm
      }
    }

    stage('Build') {
      steps {
        bat 'echo "Mulai build aplikasi (Windows)"'
      }
    }

    stage('Build Docker Image') {
      steps {
        withCredentials([usernamePassword(credentialsId: env.REGISTRY_CREDENTIALS, usernameVariable: 'USER', passwordVariable: 'PASS')]) {
          bat """
            echo Login Docker sebelum build...
            docker login -u %USER% -p %PASS%
            docker build -t ${env.IMAGE_NAME}:${env.BUILD_NUMBER} .
            docker logout
          """
        }
      }
    }

    stage('Push Docker Image') {
      steps {
        withCredentials([usernamePassword(credentialsId: env.REGISTRY_CREDENTIALS, usernameVariable: 'USER', passwordVariable: 'PASS')]) {
          bat """
            echo Login Docker untuk push...
            docker login -u %USER% -p %PASS%
            docker push ${env.IMAGE_NAME}:${env.BUILD_NUMBER}
            docker tag ${env.IMAGE_NAME}:${env.BUILD_NUMBER} ${env.IMAGE_NAME}:latest
            docker push ${env.IMAGE_NAME}:latest
            docker logout
          """
        }
      }
    }
  }

  post {
    always {
      echo 'Selesai build pipeline.'
    }
  }
}
