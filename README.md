## Team A
### Authors
- [Antoine BUQUET](https://github.com/antoinebqt)
- [Benoit GAUDET](https://github.com/BenoitGAUDET38)
- [Ayoub IMAMI](https://github.com/AyoubIMAMI)
- [Mourad KARRAKCHOU](https://github.com/MouradKarrakchou)

---

## Polymetrie

L'application Polymetrie est un compteur de visite de page externe destiné à des sites web.
L'application est déployée sur un cluster Kubernetes.
Il est possible de monitorer l'application via des métriques exportées pour Prometheus et visible grâce à un dashboard Grafana.
Il est aussi possible de consulter les données de journalisation via Kibana.

---

### Arboresence
- `ansible` : Contient les playbooks Ansible permettant le déploiement automatique de notre application Polymetrie et d'autres stack (Prometheus/Grafana)
- `K6-script` : Contient le script K6 pour effectuer les tests de charge sur l'application
- `kubernetes` : Contient les fichiers YAML des ressources à déployer sur Kubernetes
- `scripts` : Contient des scripts sh utile pour divers actions (déployer, nettoyer un namespace, etc.)
- `terraform` : Contient les fichiers Terraform, ainsi que les informations de l'état du dernier déploiement

---

### Liens
- Grafana: http://grafana.orch-team-a.pns-projects.fr.eu.org/ (user: admin, password: benochan)
- Kibana : https://kibana.orch-team-a.pns-projects.fr.eu.org/
- Argocd : http://argocd.orch-team-a.pns-projects.fr.eu.org/ (user: admin, password: 9y6LAsY5vbF-1Bhq)
- Polymetrie : http://polymetrie-service.orch-team-a.pns-projects.fr.eu.org/
