provider "helm" {
  kubernetes {
    config_path = "~/.kube/config"  # Update with the path to your kubeconfig
  }
}

resource "helm_release" "postgresql" {
  name            = "my-postgresql"
  repository      = "https://charts.bitnami.com/bitnami"
  chart           = "postgresql"
  version         = "13.2.24"
  namespace       = "default"
  create_namespace = true

  set {
    name  = "postgresqlPassword"
    value = "cBxkAqQtZR"
  }
}

resource "helm_release" "redis" {
  name            = "my-redis"
  repository      = "https://charts.bitnami.com/bitnami"
  chart           = "redis"
  version         = "18.5.0"
  namespace       = "default"
  create_namespace = true
}
