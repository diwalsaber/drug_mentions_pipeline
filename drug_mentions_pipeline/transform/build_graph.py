import logging
import polars as pl
from typing import List, Dict, Any

logger = logging.getLogger(__name__)


def build_drug_graph(
        df_mentions_pubmed: pl.DataFrame,
        df_mentions_clinical: pl.DataFrame
) -> list:
    """
    Construit la structure de graphe par drug, sous forme d'une liste Python
    (qu'on convertira ensuite en JSON).

    Args:
        df_mentions_pubmed (pl.DataFrame): colonnes [publication_id, drug, journal, date]
        df_mentions_clinical (pl.DataFrame): mêmes colonnes que df_mentions_pubmed

    Returns:
        list: chaque élément est un dict représentant 1 drug avec la clé 'drug' et 'mentions'.
    """
    logger.info("Construction de la structure graphe des médicaments...")

    # Ajouter la colonne source_type à chaque DataFrame
    df_pubmed = df_mentions_pubmed.clone()
    df_pubmed = df_pubmed.with_columns(pl.lit("pubmed").alias("source_type"))

    df_clinical = df_mentions_clinical.clone()
    df_clinical = df_clinical.with_columns(pl.lit("clinical_trial").alias("source_type"))

    # Concaténer les DataFrames
    df_all = pl.concat([df_pubmed, df_clinical], how="vertical")

    # Grouper par médicament
    results = []

    # Obtenir la liste unique des médicaments
    unique_drugs = df_all.select("drug").unique().to_series().to_list()

    for drug_name in unique_drugs:
        # Filtrer les mentions pour ce médicament
        drug_mentions = df_all.filter(pl.col("drug") == drug_name)

        # Convertir les mentions en liste de dictionnaires
        mentions_list = []
        for row in drug_mentions.rows(named=True):
            mentions_list.append({
                "source_type": row["source_type"],
                "publication_id": row["publication_id"],
                "journal": row["journal"],
                "date": row["date"]
            })

        # Ajouter l'entrée pour ce médicament
        results.append({
            "drug": drug_name,
            "mentions": mentions_list
        })

    logger.info(f"Graphe construit avec {len(results)} médicaments et leurs mentions")
    return results
