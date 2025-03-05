# Pipeline de Détection de Mentions de Médicaments

Ce projet est une pipeline de données qui détecte les mentions de médicaments dans les publications scientifiques et les essais cliniques. Il extrait les données depuis des fichiers CSV et JSON, identifie les mentions de médicaments dans les titres de publications, construit une structure de graphe représentant ces relations, et génère le résultat sous forme de fichier JSON.

## Structure du Projet

```
drug_mentions_pipeline/
├── pyproject.toml        # Configuration Poetry
├── README.md             # Documentation du projet
├── drug_mentions_pipeline/
│   ├── config.py         # Paramètres de configuration
│   ├── main.py           # Point d'entrée principal
│   ├── extract/          # Modules d'extraction de données
│   ├── transform/        # Modules de transformation de données
│   └── utils/            # Fonctions utilitaires
├── data/
│   ├── input/            # Répertoire pour les données d'entrée
│   └── output/           # Répertoire pour les données de sortie
└── tests/                # Répertoire de tests
```

## Installation

### Option 1 : Utiliser Poetry (Recommandé)

1. Assurez-vous que Poetry est installé sur votre système :
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

2. Clonez le dépôt :
   ```bash
   git clone https://github.com/votre-nom-utilisateur/drug-mentions-pipeline.git
   cd drug-mentions-pipeline
   ```

3. Installez les dépendances :
   ```bash
   poetry install
   ```

### Option 2 : Utiliser pip

1. Clonez le dépôt :
   ```bash
   git clone https://github.com/votre-nom-utilisateur/drug-mentions-pipeline.git
   cd drug-mentions-pipeline
   ```

2. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

## Utilisation

### Préparation des données

Placez vos fichiers d'entrée dans le répertoire `data/input/` :
- `drugs.csv` : Liste des médicaments
- `pubmed.csv` : Publications PubMed au format CSV
- `pubmed.json` : Publications PubMed au format JSON
- `clinical_trials.csv` : Données d'essais cliniques

### Exécution de la pipeline

Avec Poetry :
```bash
# Depuis le répertoire racine du projet (où se trouve pyproject.toml)
poetry run run-pipeline
```

Ou directement avec Python :
```bash
# Depuis le répertoire racine du projet
python -m drug_mentions_pipeline.main
```
### Analyse des journaux scientifiques

Après avoir exécuté la pipeline, vous pouvez analyser les données pour identifier le journal scientifique qui mentionne le plus de médicaments différents :

```bash
# Depuis le répertoire racine du projet
poetry run analyze-journals
```

Cette commande analyse le fichier JSON généré par la pipeline et affiche :
- Le nom du journal qui mentionne le plus de médicaments différents
- Le nombre total de médicaments différents mentionnés
- La liste complète des médicaments mentionnés par ce journal

Vous pouvez également analyser un fichier JSON spécifique en le passant en paramètre à la commande d'analyse :

```bash
# Pour analyser un fichier JSON spécifique
python -m drug_mentions_pipeline.main analyze_top_journal chemin/vers/fichier.json
```

### Résultat

La pipeline génère un fichier JSON (`data/output/drug_graph.json`) qui contient la structure en graphe des médicaments et leurs mentions dans les publications et essais cliniques.

## Configuration

Vous pouvez personnaliser la pipeline en modifiant les paramètres dans `drug_mentions_pipeline/config.py`. Cela vous permet de :
- Changer les chemins des fichiers d'entrée/sortie
- Configurer la journalisation
- Ajuster d'autres paramètres de la pipeline

## Exécution des Tests

### Exécuter tous les tests
```bash
# Depuis le répertoire racine du projet
poetry run pytest
```

### Exécuter une catégorie spécifique de tests
```bash
# Tests unitaires
poetry run pytest tests/unit/

# Tests d'intégration
poetry run pytest tests/integration/
```

### Vérifier la couverture des tests
```bash
# Installer d'abord pytest-cov
poetry add pytest-cov --dev

# Exécuter les tests avec couverture
poetry run pytest --cov=drug_mentions_pipeline
```

### Exécuter un script de vérification fonctionnelle
```bash
# Depuis le répertoire racine du projet
python test_functionality.py
```

## Environnement de Développement

### Mise en place de l'environnement de développement
```bash
# Créer et activer un shell virtuel Poetry
poetry shell

# Installer les dépendances de développement supplémentaires
poetry add black flake8 pytest-cov --dev
```

### Vérification du style de code
```bash
# Formater le code avec Black
poetry run black drug_mentions_pipeline tests

# Vérifier le code avec Flake8
poetry run flake8 drug_mentions_pipeline tests
```

## Fonctionnalités du Projet

1. **Extraction de Données** : Lecture des données sur les médicaments, publications et essais cliniques depuis des sources CSV et JSON.
2. **Détection de Mentions de Médicaments** : Identification des noms de médicaments dans les titres de publications.
3. **Construction de Graphe** : Création d'une structure de graphe reliant les médicaments à leurs mentions.
4. **Journalisation Propre** : Journalisation complète tout au long de la pipeline.
5. **Configuration Facile** : Configuration centralisée pour tous les chemins de fichiers et paramètres.

## Contribution au Projet

Pour contribuer à ce projet :

1. Créez une nouvelle branche pour votre fonctionnalité ou correction de bug
2. Effectuez vos modifications
3. Exécutez les tests pour garantir le bon fonctionnement
4. Soumettez une pull request

Le formatage du code suit le guide de style Black.
