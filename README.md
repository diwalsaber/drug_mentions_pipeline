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
3. **Construction du Graphe** : Création d'une structure de graphe reliant les médicaments à leurs mentions.
4. **Journalisation** : Journalisation complète tout au long de la pipeline.
5. **Configuration** : Configuration centralisée pour tous les chemins de fichiers et paramètres.

## Utilisation avec Docker

Ce projet peut être exécuté dans un conteneur Docker, ce qui simplifie l'installation et garantit un environnement d'exécution cohérent.

### Prérequis

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Exécution avec Docker Compose

Pour exécuter la pipeline complète :
```bash
docker-compose up pipeline
```

Pour analyser les journaux qui mentionnent le plus de médicaments :
```bash
docker-compose up analyze
```

Les résultats seront générés dans le répertoire `data/output/` de votre machine locale.

Pour plus de détails sur l'utilisation avec Docker, consultez la [Documentation Docker](Documentation-Docker.md).

## Contribution au Projet

Pour contribuer à ce projet :

1. Créez une nouvelle branche pour votre fonctionnalité ou correction de bug
2. Effectuez vos modifications
3. Exécutez les tests pour garantir le bon fonctionnement
4. Soumettez une pull request

Le formatage du code suit le guide de style Black.

# Gestion de grandes volumétries de données

## 1. Éléments à considérer pour gérer de grosses volumétries

Avec notre migration vers Polars, nous avons déjà accompli un premier pas important vers la gestion de grandes volumétries de données. Cependant, pour traiter efficacement des fichiers de plusieurs To ou des millions de fichiers, plusieurs éléments clés doivent être considérés:

### 1.1 Traitement par lots (Chunking)

Pour les jeux de données massifs, charger toutes les données en mémoire n'est pas viable. Le traitement par lots permet de diviser les données en segments gérables:

```python
import polars as pl

def process_large_csv(file_path, batch_size=100_000):
    for batch in pl.read_csv_batched(file_path, batch_size=batch_size):
        # Traiter chaque lot
        process_batch(batch)
```

### 1.2 Formats de fichiers optimisés

Dans la mesure du possible, et suivant les contraintes métier et techniques on pourrait avant ou pendant l'ingestion convertir les CSV ou JSON vers du Parquet. Format colonne beaucoup plus efficace pour les grandes volumétries et "Spark-ready":

```python
# Conversion des données en format Parquet
pl.read_csv("large_file.csv").write_parquet("optimized_file.parquet")

# Lecture sélective de colonnes
df = pl.read_parquet("optimized_file.parquet", columns=["id", "drug"])
```

### 1.3 Parallélisation et multiprocessing

Polars utilise déjà un traitement parallèle interne, mais pour traiter des millions de fichiers il pourrait être pertinent d'utiliser le multiprocessing.


## 2. Modifications pour supporter les grandes volumétries

### 2.1 Refonte de l'extraction des données

Le module d'extraction actuel doit être modifié pour prendre en charge le traitement par lots et les formats optimisés.

```python
def extract_large_csv(file_path, batch_size=100_000):
    # Traiter le CSV par lots et convertir en Parquet
```

### 2.3 Intégration avec des systèmes distribuées

L'accès aux fichiers peut devenir un goulot d'étranglement avec des millions de fichiers. Donc pour des volumétries vraiment massives, l'intégration avec des frameworks distribués comme Spark devient nécessaire.

### 2.4 Architecture modulaire et extensible

Pour gérer efficacement des millions de fichiers, une architecture plus orienté objet avec => "une tâche = un module"

## Conclusion

L'architecture globale et les stratégies de traitement doivent être adaptées vers une approche distribuée et une architecture modulaire pour gérer efficacement des données à l'échelle du téraoctet ou des millions de fichiers.


# SQL
## Première partie

```SQL
SELECT 
    date AS date,
    SUM(prod_price * prod_qty) AS ventes
FROM 
    TRANSACTIONS
WHERE 
    date BETWEEN '2019-01-01' AND '2019-12-31'
GROUP BY 
    date
ORDER BY 
    date;
```

## Deuxième partie

```SQL
SELECT
    t.client_id AS client_id,
    SUM(CASE WHEN pn.product_type = 'MEUBLE' THEN t.prod_price * t.prod_qty ELSE 0 END) AS ventes_meuble,
    SUM(CASE WHEN pn.product_type = 'DECO' THEN t.prod_price * t.prod_qty ELSE 0 END) AS ventes_deco
FROM
    TRANSACTIONS t
JOIN
    PRODUCT_NOMENCLATURE pn ON t.prod_id = pn.product_id
WHERE
    t.date BETWEEN '2019-01-01' AND '2019-12-31'
GROUP BY
    t.client_id
ORDER BY
    t.client_id;
```
