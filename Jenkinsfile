pipeline {
    agent any
    environment {

		MY_TELEGRAM_BOT_TOKEN = credentials('books_api_tg_bot_token')

		DOCKER_IMAGE = 'yuriirybak/kursova'
    }
    stages {
        stage('Start') {
            steps {
                echo 'Cursova_Bot:'
            }
        }

        stage('Build Bot services') {
            steps {
                sh 'export MY_TELEGRAM_BOT_TOKEN=$MY_TELEGRAM_BOT_TOKEN'
                dir("Telegram_bot")
				{
					sh 'docker-compose build'
				}
				sh 'docker tag books_api:latest $DOCKER_IMAGE:kursova_bot-latest'
                sh 'docker tag books_api:latest $DOCKER_IMAGE:kursova_bot-$BUILD_NUMBER'
            }
            post{
                failure {
                    script {
                    // Send Telegram notification on success
                        telegramSend message: "Job Name: ${env.JOB_NAME}\n Branch: ${env.GIT_BRANCH}\nBuild #${env.BUILD_NUMBER}: ${currentBuild.currentResult}\n Failure stage: '${env.STAGE_NAME}'"
                    }
                }
            }
        }

        stage('Test Bot services') {
            steps {
                echo 'Pass'
            }
            post{
                failure {
                    script {
                    // Send Telegram notification on success
                        telegramSend message: "Job Name: ${env.JOB_NAME}\nBranch: ${env.GIT_BRANCH}\nBuild #${env.BUILD_NUMBER}: ${currentBuild.currentResult}\nFailure stage: '${env.STAGE_NAME}'"
                    }
                }
            }
        }

		stage('Push to registry') {
            steps {
                withDockerRegistry([ credentialsId: "dockerhub_token", url: "" ])
                {
                    sh "docker push $DOCKER_IMAGE:kursova_bot-latest"
                    sh "docker push $DOCKER_IMAGE:kursova_bot-$BUILD_NUMBER"
                }
            }
            post{
                failure {
                    script {
                    // Send Telegram notification on success
                        telegramSend message: "Job Name: ${env.JOB_NAME}\nBranch: ${env.GIT_BRANCH}\nBuild #${env.BUILD_NUMBER}: ${currentBuild.currentResult}\nFailure stage: '${env.STAGE_NAME}'"
                    }
                }
            }
        }

        stage('Deploy Bot services') {
            steps {
				dir("Telegram_bot"){
					sh "docker-compose down -v"
                	sh "docker container prune --force"
                	sh "docker image prune --force"
                	sh "docker-compose up -d --build"
				}
            }
            post{
                failure {
                    script {
                    // Send Telegram notification on success
                        telegramSend message: "Job Name: ${env.JOB_NAME}\nBranch: ${env.GIT_BRANCH}\nBuild #${env.BUILD_NUMBER}: ${currentBuild.currentResult}\nFailure stage: '${env.STAGE_NAME}'"
                    }
                }
            }
        }
    }

    post {
        success {
            script {
                // Send Telegram notification on success
                telegramSend message: "Job Name: ${env.JOB_NAME}\n Branch: ${env.GIT_BRANCH}\nBuild #${env.BUILD_NUMBER}: ${currentBuild.currentResult}"
            }
        }
    }
}
