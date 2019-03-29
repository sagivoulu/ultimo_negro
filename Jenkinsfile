pipeline {
  agent any
  stages {
    stage('UnitTests') {
      steps {
        sh 'pip3 install -r requirements.txt'
        sh 'pytest'
      }
    }
  }
}
