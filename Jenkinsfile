pipeline {
  agent none
  stages {
    stage('UnitTests') {
      agent {
        docker {
          image 'python:3.7'
        }
      }
      steps {
        sh 'pytest ./tests/unit_tests--html=unit_tests.html'
      }
    }
    stage('Build') {
      agent {
        docker {
          image 'python:3.7'
        }
      }
      steps {
        bat 'pyinstaller --onefile ultimo_negro.py'
      }
      post {
        success  {
          archiveArtifacts artifacts: 'dist/*', fingerprint: true
        }
      }
    }
  }
}