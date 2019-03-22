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
    failure {
        mail to: 'sagiv.oulu@gmail.com',
             subject: "Failed Pipeline: ${currentBuild.fullDisplayName}",
             body: "Something is wrong with ${env.BUILD_URL}"
    }
    always {
      archiveArtifacts artifacts: 'assets/*.css,*.html', fingerprint: true
    }
  }
}