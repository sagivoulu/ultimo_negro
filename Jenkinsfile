pipeline {
  agent any
  stages {
    stage('run pytest') {
      steps {
        powershell(script: 'pytest', returnStdout: true, returnStatus: true)
      }
    }
  }
}