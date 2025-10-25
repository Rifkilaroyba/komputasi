pipeline {
  agent any

  environment {
    // Ganti 'username' dengan username Docker Hub kamu sendiri
    IMAGE_NAME = 'username/simple-flask-app'
    // ID credentials Docker Hub di Jenkins (buat via Manage Jenkins > Credentials)
    REGISTRY_CREDENTIALS = 'dockerhub-credentials'
  }

  stages {

    stage('Checkout') {
      steps {
        echo '==> Checkout source code dari GitHub...'
        checkout scm
      }
    }

    stage('Build Info') {
      steps {
        echo '==> Mengecek versi Docker dan memulai proses build...'
        bat 'docker --version'
      }
    }

    stage('Build Docker Image') {
      steps {
        //BAGIAN BARU: login ke Docker Hub + build image dari Dockerfile Flask kamu
        withCredentials([usernamePassword(credentialsId: env.REGISTRY_CREDENTIALS, usernameVariable: 'USER', passwordVariable: 'PASS')]) {
          bat """
            echo == Login ke Docker Hub...
            docker login -u %USER% -p %PASS%

            echo == Membuat image Docker dari Dockerfile...
            docker build -t ${env.IMAGE_NAME}:${env.BUILD_NUMBER} .

            echo == Logout dari Docker Hub...
            docker logout
          """
        }
      }
    }

    stage('Run Container Test') {
      steps {
        //BAGIAN BARU: Tahap pengujian container Flask — memastikan app bisa diakses di port 5000
        echo '==> Menjalankan container untuk memastikan app dapat diakses...'
        bat """
          echo Jalankan container Flask di background...
          docker run -d -p 5000:5000 --name test_container ${env.IMAGE_NAME}:${env.BUILD_NUMBER}

          // Beri waktu 10 detik agar container siap
          timeout /t 10

          echo Cek apakah container berjalan...
          docker ps

          // Tes akses endpoint utama Flask
          echo Tes akses ke endpoint utama...
          curl http://localhost:5000 || exit /b 1

          echo Stop dan hapus container setelah tes selesai...
          docker stop test_container
          docker rm test_container
        """
      }
    }

    stage('Push Docker Image') {
      when {
        expression { currentBuild.resultIsBetterOrEqualTo('SUCCESS') }
      }
      steps {
        //BAGIAN BARU: Push image hasil build ke Docker Hub
        withCredentials([usernamePassword(credentialsId: env.REGISTRY_CREDENTIALS, usernameVariable: 'USER', passwordVariable: 'PASS')]) {
          bat """
            echo == Login ke Docker Hub untuk push...
            docker login -u %USER% -p %PASS%

            echo == Push image versi build ke Docker Hub...
            docker push ${env.IMAGE_NAME}:${env.BUILD_NUMBER}

            echo == Tag image sebagai latest dan push ulang...
            docker tag ${env.IMAGE_NAME}:${env.BUILD_NUMBER} ${env.IMAGE_NAME}:latest
            docker push ${env.IMAGE_NAME}:latest

            echo == Logout dari Docker Hub...
            docker logout
          """
        }
      }
    }

    stage('Verify Image') {
      steps {
        // Menampilkan daftar image Docker yang ada di host
        bat """
          echo == Menampilkan daftar image di host...
          docker images
        """
      }
    }
  }

  post {
    success {
      //  Pesan muncul kalau semua stage berhasil
      echo 'PIPELINE SUKSES — Image Flask berhasil dibangun, dites, dan dipush ke Docker Hub!'
    }
    failure {
      //  Pesan muncul kalau ada error di salah satu tahap
      echo 'PIPELINE GAGAL — Periksa error di tahapan sebelumnya.'
    }
    always {
      // Pesan yang selalu muncul di akhir
      echo 'Pipeline selesai dijalankan.'
    }
  }
}
