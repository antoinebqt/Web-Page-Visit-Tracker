# provider "kubernetes" {
#   config_path = "~/.kube/config"
# }


################################################################################################################################

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

################################################################################################################################

# provider "kubernetes" {
#   config_path = "~/.kube/config"
# }
#
# resource "kubernetes_namespace" "terraform-test" {
#   metadata {
#     name = "terraform_test"
#   }
# }
#
# resource "kubernetes_deployment" "polymetrie" {
#   metadata {
#     name      = "polymetrie"
# 	namespace = kubernetes_namespace.terraform_test.metadata.0.name
#   }
#
#   spec {
#     replicas = 1
#     selector {
#       match_labels = {
#         app = "polymetrie"
#       }
#     }
#     template {
#       metadata {
#         labels = {
#           app = "polymetrie"
#         }
#       }
#       spec {
#         container {
#           name  = "polymetrie"
#           image = "leolebossducloud/polymetrie:latest"
#           port {
#             container_port = 80
#           }
#         }
#       }
#     }
#   }
# }
#
# resource "kubernetes_service" "polymetrie-service" {
#   metadata {
#     name      = "polymetrie-service"
# 	namespace = kubernetes_namespace.terraform_test.metadata.0.name
#   }
#
#   spec {
#     selector = {
#       app = kubernetes_deployment.polymetrie.spec.0.template.0.metadata.0.labels.app
#     }
#     port {
#       protocol    = "TCP"
#       port        = 80
#       target_port = 5000
#     }
#   }
# }
#
# resource "kubernetes_ingress" "polymetrie-ingress" {
#   metadata {
#     name      = "polymetrie-ingress"
# 	namespace = kubernetes_namespace.terraform_test.metadata.0.name
#   }
#
#   spec {
#     rules {
# 	  host = "polymetrie.com"
# 	  http {
# 		paths {
# 		  path = "/"
# 		  pathType = "Prefix"
# 		  backend {
# 		    service {
# 			  name = kubernetes_deployment.polymetrie.spec.0.template.0.metadata.0.labels.app
# 			  port {
# 			    number = 80
# 			  }
# 			}
# 		  }
# 		}
# 	  }
#   }
# }