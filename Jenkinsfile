pipeline {
  agent any
  stages {
    stage('UnitTests') {
      steps {
        bat 'pytest .\tests\unit_tests --html=unit_tests.html'
      }
      post {
        always {
          archiveArtifacts artifacts: 'assets\*.css,*.html', fingerprint: true
        }
      }
    }
    stage('Build') {
      steps {
        bat 'pyinstaller --onefile ultimo_negro.py'
      }
      post {
        success  {
          archiveArtifacts artifacts: 'dist\*', fingerprint: true
        }
      }
    }
  }
}