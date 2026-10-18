"""Capteur simulé : publie température et humidité de plusieurs salles sur un broker MQTT."""
import json
import os
import random
import time
from datetime import datetime, timezone

import paho.mqtt.client as mqtt

MQTT_HOST = os.getenv("MQTT_HOST", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
MQTT_USER = os.getenv("MQTT_USER")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")
# Liste de salles séparées par des virgules (SALLE, au singulier, reste accepté)
SALLES = [
    s.strip()
    for s in os.getenv("SALLES", os.getenv("SALLE", "salle1,salle2,salle3")).split(",")
    if s.strip()
]
INTERVAL = float(os.getenv("INTERVAL", "3"))


def on_connect(client, userdata, flags, reason_code, properties=None):
    print(f"[capteur] connecté à {MQTT_HOST}:{MQTT_PORT} (code={reason_code})", flush=True)


def main():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    if MQTT_USER:
        client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    client.on_connect = on_connect
    client.reconnect_delay_set(min_delay=1, max_delay=30)

    while True:
        try:
            client.connect(MQTT_HOST, MQTT_PORT, keepalive=60)
            break
        except OSError as e:
            print(f"[capteur] broker injoignable ({e}), nouvel essai dans 5 s", flush=True)
            time.sleep(5)

    client.loop_start()

    # Chaque salle a sa propre marche aléatoire : les valeurs évoluent doucement,
    # comme un vrai capteur, avec des points de départ différents.
    etat = {
        salle: {
            "temperature": random.uniform(24.0, 31.0),
            "humidite": random.uniform(50.0, 70.0),
        }
        for salle in SALLES
    }

    while True:
        for salle, e in etat.items():
            e["temperature"] = min(36.0, max(20.0, e["temperature"] + random.uniform(-0.5, 0.5)))
            e["humidite"] = min(85.0, max(40.0, e["humidite"] + random.uniform(-1.2, 1.2)))
            payload = {
                "salle": salle,
                "temperature": round(e["temperature"], 1),
                "humidite": round(e["humidite"], 1),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
            topic = f"esatic/{salle}/mesures"
            client.publish(topic, json.dumps(payload), qos=1)
            print(f"[capteur] {topic} -> {payload}", flush=True)
        time.sleep(INTERVAL)


if __name__ == "__main__":
    main()
