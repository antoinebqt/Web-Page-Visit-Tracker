## Polymetrie

L'application Polymetrie est un compteur de visite externe pour les sites web.
L'application est déployée sur un cluster Kubernetes.
Il est possible de suivre des métriques utilisateurs et sur le cluster Kubernetes via des dashboard Grafana.
Il est aussi possible de consulter les données de journalisation via Kibana.

### Arboresence
- `ansible` : Contient les playbooks ansible permettant le déploiement automatique de la stack Polymetrie
- `K6-script` : Contient les scripts K6 pour effectuer les tests de charge sur le cluster Kubernetes
- `kubernetes` : Contient les fichiers YAML de déploiement sur Kubernetes
- `scripts` : Contient des scripts sh utile pour divers actions
- `terraform` : Contient les fichiers terraform, ainsi que les informations de l'état du dernier déploiement

### Liens
- Grafana: http://grafana.orch-team-a.pns-projects.fr.eu.org/
- Kibana : https://kibana.orch-team-a.pns-projects.fr.eu.org/
- Argocd : http://argocd.orch-team-a.pns-projects.fr.eu.org/
- Polymetrie : http://polymetrie-service.orch-team-a.pns-projects.fr.eu.org/

### Groupe Team A
- Antoine BUQUET
- Ayoub IMAMI
- Mourad KARRAKCHOU
- Benoit GAUDET
