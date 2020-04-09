def github_id = 'rudihinds'

// DO NOT CHANGE THE VARIBLES BELOW THIS LINE 

def image_name = "sepractices/${github_id}-transaction-service"

def namespace = github_id.toLowerCase()

def cluster_name = "prod-ak-k8s-cluster"

def git_repository = "https://github.com/${github_id}/transaction-service.git"

def kaniko_image = 'gcr.io/kaniko-project/executor:debug-b0e7c0e8cd07ef3ad2b7181e0779af9fcb312f0b'
def kubectl_image = 'sepractices/jenkins-eks-kubectl-deployer:0.1.0'

def git_commit = ''

def label = "build-${UUID.randomUUID().toString()}"
def build_pod_template = """
kind: Pod
metadata:
  name: build-pod
spec:
  containers:
  - name: kaniko
    image: ${kaniko_image}
    imagePullPolicy: Always
    command:
    - /busybox/cat
    tty: true
    volumeMounts:
      - name: jenkins-docker-cfg
        mountPath: /root/.docker

  - name: kubectl
    image: ${kubectl_image}
    imagePullPolicy: Always
    tty: true

  - name: python-test
    image: sepractices/pg-python:0.1.0
    tty: true

  volumes:
  - name: jenkins-docker-cfg
    projected:
      sources:
      - secret:
          name: regcred
          items:
            - key: dockerconfigjson
              path: config.json
"""

podTemplate(name: 'transaction-service-build', label: label, yaml: build_pod_template) {
  node(label) {
    git git_repository

    stage('Test') {
        container(name: 'python-test', shell: '/bin/sh') {
            sh 'pipenv install --dev'
            sh 'bin/run_tests.sh'
        }
    }

    stage('Build Image') {
      git_commit = sh (
        script: 'git rev-parse HEAD',
        returnStdout: true
      ).trim()
      image_name += ":${git_commit}"
      echo "Building image ${image_name}"
      container(name: 'kaniko', shell: '/busybox/sh') {
        withEnv(['PATH+EXTRA=/busybox:/kaniko']) {
          sh """#!/busybox/sh
          /kaniko/executor -f `pwd`/Dockerfile -c `pwd` --skip-tls-verify --cache=true --destination=${image_name}
          """
        }
      }
    }

    stage('Deploy to Kubernetes') {
      withCredentials([
        string(credentialsId: 'AWS_ACCESS_KEY_ID', variable: 'AWS_ACCESS_KEY_ID'),
        string(credentialsId: 'AWS_SECRET_ACCESS_KEY', variable: 'AWS_SECRET_ACCESS_KEY'),
        string(credentialsId: 'KUBERNETES_SERVER', variable: 'KUBERNETES_SERVER'),
        file(credentialsId: 'KUBERNETES_CA', variable: 'KUBERNETES_CA')
      ]) {
        container(name: 'kubectl', shell: '/bin/sh') {
          sh '''kubectl config \
              set-cluster kubernetes \
              --server=$KUBERNETES_SERVER \
              --certificate-authority=$KUBERNETES_CA
          '''
          sh """
            kubectl config \
              set-credentials aws \
              --exec-arg=token \
              --exec-arg=-i \
              --exec-arg="${cluster_name}"
          """
          sh "yq w -i kubernetes/deployment.yml 'spec.template.spec.containers[0].image' ${image_name}"
          sh "kubectl create namespace ${namespace} || true"
          sh "kubectl apply -n ${namespace} -f kubernetes/"
        }
      }
    }
  }
}
