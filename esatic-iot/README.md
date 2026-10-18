# Station de mesure connectée – ESATIC

Chaîne IoT complète : **capteur simulé → broker MQTT (AWS) → tableau de bord web**, le tout dans des conteneurs Docker.

```
┌──────────────┐  MQTT 1883   ┌───────────────┐  WebSocket 9001  ┌──────────────────┐
│ sensor       │ ───────────▶ │ mosquitto     │ ◀─────────────── │ navigateur       │
│ (Python)     │              │ (broker MQTT) │                  │ (page du         │
└──────────────┘              └───────────────┘                  │  dashboard :80)  │
                                                                 └──────────────────┘
```

| Composant | Technologie | Rôle |
|---|---|---|
| `sensor/` | Python + paho-mqtt | Publie température/humidité toutes les 3 s sur `esatic/<salle>/mesures` |
| `mosquitto/` | Eclipse Mosquitto 2 | Broker MQTT (port 1883) + WebSocket (9001) |
| `dashboard/` | nginx + MQTT.js + Chart.js | Page web qui s'abonne au broker et trace les courbes |

## 1. Test en local

```bash
docker compose up --build
```
Ouvrir http://localhost : les valeurs et les courbes doivent bouger toutes les 3 secondes.

Vérifier les messages en ligne de commande :
```bash
docker exec -it mosquitto mosquitto_sub -t "esatic/#" -v
```

## 2. Publier l'image du capteur sur Docker Hub

```bash
docker login
docker build -t VOTRE_USER/esatic-sensor:latest ./sensor
docker push VOTRE_USER/esatic-sensor:latest
```
Lien à rendre : `https://hub.docker.com/r/VOTRE_USER/esatic-sensor`

## 3. Déploiement sur AWS (EC2)

1. **Lancer une instance EC2** : Ubuntu 22.04/24.04, type `t2.micro` ou `t3.micro` (free tier).
2. **Security Group** (règles entrantes) :

   | Port | Usage | Source |
   |---|---|---|
   | 22 | SSH | Votre IP |
   | 80 | Dashboard | 0.0.0.0/0 |
   | 1883 | MQTT | 0.0.0.0/0 (ou votre IP) |
   | 9001 | MQTT WebSocket | 0.0.0.0/0 |

3. **Installer Docker** sur l'instance :
   ```bash
   sudo apt update && sudo apt install -y docker.io docker-compose-v2 git
   sudo usermod -aG docker ubuntu && newgrp docker
   ```
4. **Récupérer le projet et lancer** :
   ```bash
   git clone https://github.com/VOTRE_USER/esatic-iot.git
   cd esatic-iot
   echo "DOCKERHUB_USER=VOTRE_USER" > .env
   docker compose up -d --build
   ```
5. **Tableau de bord** : `http://<IP_PUBLIQUE_EC2>` (à fournir comme URL du dashboard).
6. *(Conseil)* Associer une **Elastic IP** pour que l'adresse ne change pas après un redémarrage.

> Variante « capteur à distance » : lancer le capteur sur votre PC pour prouver que les mesures transitent bien par AWS :
> `docker run --rm -e MQTT_HOST=<IP_PUBLIQUE_EC2> VOTRE_USER/esatic-sensor:latest`

## 4. Sécurité (à justifier dans le compte rendu)

Par défaut le broker accepte les connexions anonymes (pratique pour la démo). Pour l'authentifier :
```bash
docker exec -it mosquitto mosquitto_passwd -c /mosquitto/config/passwd capteur
```
puis dans `mosquitto.conf` : `allow_anonymous false` et `password_file /mosquitto/config/passwd`, et passer `MQTT_USER` / `MQTT_PASSWORD` au capteur. Pour aller plus loin : TLS (port 8883), Security Group restreint.

## 5. Dépannage

| Symptôme | Cause probable |
|---|---|
| Dashboard « Déconnecté » | Port 9001 non ouvert dans le Security Group |
| Page inaccessible | Port 80 non ouvert, ou utilisation de `https://` au lieu de `http://` |
| Pas de courbes | Le capteur ne tourne pas : `docker compose logs sensor` |

## Membres du groupe
- Nom 1
- Nom 2
- Nom 3
