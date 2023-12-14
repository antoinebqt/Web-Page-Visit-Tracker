provider "helm" {
  kubernetes {
    config_path = "~/.kube/config"
  }
}

# resource "kubernetes_namespace" "example" {
#   metadata {
#     name = "terraform-example-namespace"
#   }
# }

resource "helm_release" "redis" {
  name            = "redis"
  chart           = "bitnami/redis"
  version         = "10.7.0"
  namespace       = "terraform-example-namespace"
  create_namespace = true

  set {
    name  = "redisPassword"
    value = "ov6D2EYYcb"
  }
}

resource "helm_release" "postgresql" {
  name            = "postgresql"
  chart           = "bitnami/postgresql"
  version         = "10.5.0"
  namespace       = "terraform-example-namespace"
  create_namespace = true

  set {
    name  = "postgresqlPassword"
    value = "cBxkAqQtZR"
  }
}

# resource "kubernetes_manifest" "polymetrie_deployment" {
#   manifest = yamldecode(file("${path.module}/polymetrie-deployment.yaml"))
# }
#
# resource "kubernetes_manifest" "polymetrie_service" {
#   manifest = yamldecode(file("${path.module}/polymetrie-deployment.yaml"))
# }
#
# resource "kubernetes_manifest" "polymetrie_ingress" {
#   manifest = yamldecode(file("${path.module}/polymetrie-deployment.yaml"))
# }