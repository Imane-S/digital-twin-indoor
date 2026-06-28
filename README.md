# 📊 Digital Twin Indoor — Prototype de Jumeau Numérique Temps Réel

Ce projet a été réalisé dans le cadre du stage de fin de **Licence 3 MIASHS (Parcours Informatique)** à l'**Université Toulouse - Jean Jaurès**. 
Il propose un prototype fonctionnel de jumeau numérique d'intérieur capable de capter l'occupation physique de zones définies (bureau d'essai) via une caméra et d'en projeter dynamiquement l'état sur une interface web réactive.

## Binôme de Développement
* **Imane Saci** 
* **Susana Granados** 

---

## Architecture Globale du Système

Le système est découpé en trois couches indépendantes et interconnectées :
1. **Captation & Edge Computing (Raspberry Pi 4) :** Extraction des flux vidéo par OpenCV, détection de présence humaine/objets par le modèle IA **YOLOv8n**, application d'une matrice d'**homographie** pour convertir les pixels en centimètres réels, et publication des états en **MQTT**.
2. **Cœur Transactionnel Backend (FastAPI Server) :** Écoute du broker MQTT, validation des structures de données via **Pydantic**, et stratégie de stockage hybride :
   * **Redis :** Stockage en mémoire RAM du tout dernier état pour des lectures instantanées (microsecondes).
   * **PostgreSQL :** Historisation persistante sur disque pour l'analyse à long terme.
3. **Restitution Frontend (React App) :** Interface utilisant **Leaflet** en coordonnées 2D plates (CRS Simple) pour colorer dynamiquement les zones (Rouge = Occupé, Vert = Vide) et affichage de l'historique transactionnel par *Polling* HTTP (fréquence : 1s).

---

## Technologies Utilisées

* **Edge / IA :** Python 3.10, OpenCV, Ultralytics YOLOv8
* **Communication :** MQTT (Mosquitto Broker), Paho-MQTT, Gmqtt
* **Backend API :** FastAPI, Uvicorn, Pydantic
* **Bases de Données :** PostgreSQL 16, Redis 7
* **Frontend UI :** React.js, React-Leaflet
* **DevOps & QA :** Docker, Docker Compose, Pytest, GitHub Actions (CI/CD)

---

## Installation et Lancement Rapide (Mode DevOps)

Grâce à la conteneurisation complète de l'application, l'intégralité de l'infrastructure (Backend, Frontend, Bases de données, Broker) se lance en une seule commande sur n'importe quel environnement hôte disposant de Docker.

### Prérequis
* Docker (v20.10+)
* Docker Compose (v2.0+)

### Démarrage des services
À la racine du projet, exécutez la commande suivante :
```bash
docker-compose up --build