# Dashboard KPI - TP DataViz

Dashboard interactif pour l'analyse de données et le calcul des KPI (Indicateurs Clés de Performance).

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Dash](https://img.shields.io/badge/Dash-2.18-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## Description

Ce projet contient deux dashboards interactifs créés avec Python Dash :

1. **Exercice 1** : Dashboard KPI avec analyse détaillée de 6 indicateurs clés
2. **Exercice 2** : Dashboard interactif avec filtres dynamiques pour l'analyse des ventes

## Fonctionnalités

### Dashboard KPI (Exercice 1)
-  **6 KPI détaillés** : Valeur moyenne, Répartition catégories, Taux de récurrence, Modes de paiement, CLV, Performance
- **Graphiques interactifs** : Camemberts, barres, histogrammes
-  **Top 5 clients** avec classement
-  **Design moderne** avec animations

### Dashboard Interactif (Exercice 2)
-  **Filtres dynamiques** : Magasin, Catégorie, Mode de paiement, Période
- **5 sections d'analyse** : Vue d'ensemble, Magasins, Catégories, Paiements, Satisfaction
-  **KPI en temps réel** : Total ventes, Transactions, Montant moyen, Satisfaction
-  **Interface moderne** avec gradient et animations

##  Installation

### Prérequis
- Python 3.8 ou supérieur
- pip

### Installation locale

1. Clonez le repository :
```bash
git clone https://github.com/votre-username/dashboard-kpi.git
cd dashboard-kpi
```

2. Installez les dépendances :
```bash
pip install -r requirements.txt
```

3. Lancez le dashboard :
```bash
# Dashboard KPI (Exercice 1)
python exercice1_dashboard_kpi.py

# OU Dashboard Interactif (Exercice 2)
python exercice2_dashboard_style.py
```

4. Ouvrez votre navigateur :
```
http://127.0.0.1:8050/
```

## Structure du projet

```
dashboard-kpi/
├── exercice1_dashboard_kpi.py      # Dashboard KPI
├── exercice2_dashboard_style.py    # Dashboard interactif
├── data_kpi.xlsx                   # Données Exercice 1
├── data_dashboard_large.xlsx       # Données Exercice 2
├── requirements.txt                # Dépendances Python
├── Procfile                        # Configuration déploiement
├── .gitignore                      # Fichiers à ignorer
└── README.md                       # Ce fichier
```

##  Technologies utilisées

- **Python 3.x** - Langage de programmation
- **Dash** - Framework pour dashboards web
- **Plotly** - Bibliothèque de graphiques interactifs
- **Pandas** - Manipulation de données
- **Openpyxl** - Lecture de fichiers Excel

## Aperçu des KPI

### Exercice 1 - 6 KPI calculés
1. **Valeur moyenne des transactions** : 263.60 €
2. **Répartition des catégories** : Électronique (36.73%), Vêtements (31.20%), etc.
3. **Taux de récurrence** : 77.22% des clients reviennent
4. **Mode de paiement le plus utilisé** : Carte bancaire (62.60%)
5. **CLV moyenne** : 729.28 €
6. **Catégorie la plus performante** : Électronique

## Déploiement

Ce projet peut être déployé gratuitement sur :
- **Render** (recommandé)
- **Heroku**
- **PythonAnywhere**

### Déploiement sur Render

1. Créez un compte sur [Render.com](https://render.com)
2. Créez un nouveau "Web Service"
3. Connectez votre repository GitHub
4. Render détectera automatiquement le Procfile
5. Déployez !

## Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## Auteur

Créé dans le cadre du TP DataViz - Analyse Décisionnelle

##  Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou une pull request.

## Contact

Pour toute question ou suggestion, ouvrez une issue sur GitHub.

---

N'oubliez pas de mettre une étoile si ce projet vous a été utile !
