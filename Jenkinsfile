pipeline {
  agent any
  stages {
    stage('UnitTests') {
      steps {
        bat 'pytest tests\unit_tests --html=unit_tests.html'
      }
    }
  }
}
