pipeline {
    agent any

    stages {
        stage('Verify Environment') {
    steps {
        bat '''
        echo ===== USER =====
        whoamiss

        echo.
        echo ===== PYTHON =====
        where python

        echo.
        python --version

        echo.
        pip --version
        '''
    }
}
        stage('Checkout Code') {
            steps {
                echo '📦 Cloning repository from GitHub...'
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: '*/main']],
                    userRemoteConfigs: [[
                        url: 'https://github.com/waqar-aslam/playwright-python-practice.git',
                        credentialsId: 'github-token'
                    ]]
                ])
                echo '✅ Repository cloned successfully!'
            }
        }

        stage('Setup Python Environment') {
            steps {
                echo '🐍 Setting up Python environment...'
                bat 'python --version'
                bat 'python -m pip install --upgrade pip'
                bat 'python -m pip install -r requirements.txt'
                echo '✅ Dependencies installed!'
            }
        }

        stage('Install Playwright Browsers') {
            steps {
                echo '🌐 Installing Playwright browsers...'
                bat 'python -m playwright install'
                echo '✅ Playwright browsers installed!'
            }
        }

        stage('Run Playwright Tests') {
            steps {
                echo '🧪 Running Playwright tests...'
                bat 'python -m pytest --tb=short'
                echo '✅ Tests completed!'
            }
            post {
                always {
                    // Archive test reports if they exist
                    archiveArtifacts artifacts: 'report.html', fingerprint: true
                    echo '📊 Test report archived!'
                }
            }
        }
    }

    post {
        success {
            echo '🎉 All Playwright tests passed! Build successful!'
        }
        failure {
            echo '❌ Some Playwright tests failed! Check the logs.'
        }
        always {
            echo '🏁 Pipeline execution completed.'
        }
    }
}