pipeline {
  agent none
  stages {
    stage('UnitTests') {
      agent { dockerfile true }
      steps {
        sh 'pip3 install -r requirements.txt'
        sh 'pytest'
      }
    }
  }
}
