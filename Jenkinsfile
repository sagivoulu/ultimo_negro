pipeline {
  agent any
  stages {
    stage('UnitTests') {
      steps {
        sh 'apt-get install python'
        sh 'pip install pipenv pyenv'
        sh 'pipenv install'
        sh 'pytest'
      }
    }
  }
}
