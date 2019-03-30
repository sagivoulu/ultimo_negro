pipeline {
  agent any
  stages {
    stage('UnitTests') {
      steps {
        sh 'apt-get install python -y'
        sh 'apt-get install python-pip -y'
        sh 'pip install pipenv pyenv'
        sh 'pipenv install'
        sh 'pytest'
      }
    }
  }
}
