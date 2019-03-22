pipeline {
  agent any
  stages {
    stage('Test') {
      steps {
        bat 'pytest --html=report.html'
      }
    }
  }
  post {
    always {
      archiveArtifacts artifacts: '*.css,*.html', fingerprint: true
    }
  }
}