pipeline {
    agent any
    environment {
        // ubah 'rifkilaroyba/komputasi' dengan nama kamu dan repo proyek kamu
        IMAGE_NAME = 'rifkilaroyba/komputasi'
        // ubah 'dockerhub-credentials' dengan credential yang sudah kamu buat 
        REGISTRY_CREDENTIALS = 'dockerhub-credentials'
    }
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Build') {
            steps {
                // Install semua library yang dibutuhkan dari requirements.txt
                bat 'pip install -r requirements.txt'
            }
        }
        stage('Unit Test') {
            steps {
                // Jalankan pytest. Pipeline akan berhenti jika ada tes yang gagal.
                bat 'pytest'
            }
        }
        stage('Build Docker Image') {
            steps {
                bat """docker build -t ${env.IMAGE_NAME}:${env.BUILD_NUMBER} ."""
            }
        }
        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: env.REGISTRY_CREDENTIALS, usernameVariable: 'USER', passwordVariable: 'PASS')]) {
                    bat """docker login -u %USER% -p %PASS%"""
                    bat """docker push ${env.IMAGE_NAME}:${env.BUILD_NUMBER}"""
                    bat """docker tag ${env.IMAGE_NAME}:${env.BUILD_NUMBER} ${env.IMAGE_NAME}:latest"""
                    bat """docker push ${env.IMAGE_NAME}:latest"""
                }
            }
        }
    }
}
