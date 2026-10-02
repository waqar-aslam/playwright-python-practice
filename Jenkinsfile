// Assumes a "Pipeline script from SCM" job, so Jenkins has already checked out the repo.
pipeline {
    agent any

    options {
        timeout(time: 45, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '20'))
    }

    parameters {
        choice(name: 'BROWSER', choices: ['chromium', 'firefox', 'webkit'], description: 'Browser to run the tests in')
        string(name: 'MARKERS', defaultValue: 'smoke or regression', description: 'pytest -m expression, e.g. "smoke" or "smoke or regression"')
        string(name: 'WORKERS', defaultValue: 'auto', description: 'pytest-xdist worker count (-n)')
    }

    environment {
        VENV_PY = '.venv\\Scripts\\python.exe'
    }

    stages {
        stage('Setup Python Environment') {
            steps {
                bat 'python --version'
                bat 'python -m venv .venv'
                bat '%VENV_PY% -m pip install --upgrade pip'
                bat '%VENV_PY% -m pip install -r requirements.txt'
            }
        }

        stage('Install Playwright Browser') {
            steps {
                bat "%VENV_PY% -m playwright install ${params.BROWSER}"
            }
        }

        stage('Run Playwright Tests') {
            steps {
                // Secret file credential holding the credentials.json contents (see data/credentials.example.json)
                withCredentials([file(credentialsId: 'playwright-test-credentials', variable: 'TEST_CREDENTIALS_FILE')]) {
                    bat "if exist reports rmdir /s /q reports"
                    // --browser drives pytest-playwright's page fixture, --browser_name drives browser_instance
                    bat "%VENV_PY% -m pytest --tb=short -m \"${params.MARKERS}\" -n ${params.WORKERS} --browser ${params.BROWSER} --browser_name ${params.BROWSER}"
                }
            }
        }
    }

    post {
        always {
            junit allowEmptyResults: true, testResults: 'reports/junit.xml'
            archiveArtifacts artifacts: 'reports/**', allowEmptyArchive: true, fingerprint: true
        }
    }
}
