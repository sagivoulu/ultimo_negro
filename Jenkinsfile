pipeline {
  agent any
  stages {
    stage('UnitTests') {
      steps {
        sg 'pip3 install -r requirements.txt'
        sh 'pytest'
      }
    }
  }
}
