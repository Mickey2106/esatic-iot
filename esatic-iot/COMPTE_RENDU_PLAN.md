# Compte rendu – Station de mesure connectée (plan à compléter)

**Groupe :** … **Date :** 20/10/2026

## 1. Introduction
- Contexte : surveillance à distance de la température et de l'humidité des locaux de l'ESATIC.
- Objectif et livrables (GitHub, Docker Hub, URL dashboard).

## 2. Architecture
- Schéma de la chaîne : capteur → broker MQTT (AWS) → dashboard.
- Flux de données : topic `esatic/<salle>/mesures`, format JSON.

## 3. Choix techniques et justifications
| Choix | Pourquoi ? | Alternatives écartées |
|---|---|---|
| **MQTT** | Protocole léger, publish/subscribe, conçu pour l'IoT, faible consommation | HTTP/REST (plus lourd, pas de push), CoAP |
| **Mosquitto** | Broker open source léger, tourne sur une `t2.micro` | EMQX, HiveMQ, AWS IoT Core (plus complet mais plus complexe/coûteux) |
| **AWS EC2** | Contrôle total, free tier, exigé par le sujet | AWS IoT Core, Lightsail |
| **Docker / Compose** | Portabilité, déploiement identique en local et sur AWS, un conteneur par composant | Installation manuelle |
| **Dashboard web (nginx + MQTT.js + Chart.js)** | Temps réel via WebSocket, aucune base de données, très léger | Node-RED, Grafana + InfluxDB (historisation, mais plus lourd) |
| **Python pour le capteur** | Simple, bibliothèque paho-mqtt | Node.js |

## 4. Mise en œuvre
- Capteur simulé (marche aléatoire, plages réalistes).
- Configuration du broker (ports 1883 / 9001).
- Dashboard.
- Dockerisation et docker-compose.
- Déploiement AWS : instance, Security Group, Elastic IP (captures d'écran).
- Publication Docker Hub / GitHub.

## 5. Sécurité
- Security Group (ports minimaux, SSH limité à votre IP).
- Authentification MQTT, TLS (réalisé ou perspectives).
- Limites de la version actuelle.

## 6. Difficultés rencontrées et solutions

## 7. Améliorations possibles
- Historisation (InfluxDB + Grafana), alertes (seuil de température), vrai capteur ESP32 + DHT22, TLS, plusieurs salles.

## 8. Conclusion

## Annexes
- Liens : GitHub, Docker Hub, URL du dashboard.
- Captures d'écran.
