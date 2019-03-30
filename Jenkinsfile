pipeline {
  agent any
  stages {
    stage('UnitTests') {
      steps {
        sh 'apt-get install python -y'
        sh 'apt-get install python-pip -y'
        sh 'curl https://pyenv.run | bash'
        sh 'pip install pipenv'
        sh 'pipenv install'
        sh 'pytest'
      }
    }
  }
}
