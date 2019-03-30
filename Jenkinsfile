pipeline {
  agent any
  stages {
    stage('UnitTests') {
      steps {
        sh 'apt-get install python'
        sh 'apt-get install python-pip'
        sh 'pip install pipenv pyenv'
        sh 'pipenv install'
        sh 'pytest'
      }
    }
  }
}
