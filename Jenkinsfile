pipeline {
  agent any
  stages {
    stage('Test') {
      steps {
        bat 'pip3 install -r requirements.txt',
        bat 'pytest --html=report.html'
      }
    }
  }
  post {
    always {
      archiveArtifacts artifacts: 'report.html', fingerprint: true
    }
  }
}