# Projet IoT ESP32 – Organisation du GitHub

> ## Projet étudiant – IoT / MicroPython / ESP32
> Objectif : organiser proprement le dépôt GitHub pour un développement clair, structuré et collaboratif.

---

## 1. Structure des branches
1. main – Branche principale (stable)

Contient uniquement du code totalement fonctionnel et testé

Aucun push direct autorisé

Les mises à jour passent uniquement par une Pull Request depuis Dev

---

## 2. Dev – Branche de développement

Branche fille de main

Sert d’environnement d’intégration

Toutes les fonctionnalités validées sont fusionnées ici avant d’aller dans main

---

## 3. Branches fonctionnelles (feature branches)

Exemples :

Car_manual

Tout ajout futur (ex : wifi_module, sensor_system, etc.)

Caractéristiques :

Créées depuis Dev

Ne doivent contenir qu’une seule fonctionnalité

Fusion vers Dev via Pull Request uniquement

🔁 Workflow Git
[Feature Branch] → Pull Request → [Dev] → Pull Request → [main]


Créer une branche depuis Dev

Développer et tester la fonctionnalité

Ouvrir une PR vers Dev

Quand tout fonctionne dans Dev, ouvrir une PR vers main
