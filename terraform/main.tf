provider "helm" {
  kubernetes {
    config_path = "~/.kube/config"  # Update with the path to your kubeconfig
  }
}

provider "kubernetes" {
  config_path = "~/.kube/config"
}

variable "terraform_namespace" {
  type    = string
  default = "default"
}

resource "helm_release" "postgresql" {
  name            = "postgresql"
  repository      = "https://charts.bitnami.com/bitnami"
  chart           = "postgresql"
  version         = "13.2.24"
  namespace       = var.terraform_namespace
  create_namespace = true

  values = [
      file("../kubernetes/postgresql-values.yaml"),
    ]

}

resource "helm_release" "redis" {
  name            = "redis"
  repository      = "https://charts.bitnami.com/bitnami"
  chart           = "redis"
  version         = "18.5.0"
  namespace       = var.terraform_namespace
  create_namespace = true
}

resource "kubernetes_manifest" "polymetrie_deployment" {
  manifest = yamldecode(file("../kubernetes/polymetrie-deployment.yaml"))
}

resource "kubernetes_manifest" "polymetrie_service" {
  manifest = yamldecode(file("../kubernetes/polymetrie-service.yaml"))
}

resource "kubernetes_manifest" "polymetrie_ingress" {
  manifest = yamldecode(file("../kubernetes/polymetrie-ingress.yaml"))
}