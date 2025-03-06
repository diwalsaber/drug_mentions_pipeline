import logging
import polars as pl

logger = logging.getLogger(__name__)

def detect_drug_mentions(
        df_publications: pl.DataFrame,
        df_drugs: pl.DataFrame,
        title_col: str
) -> pl.DataFrame:
    """
    Détecte les mentions de médicaments dans les publications et retourne un DataFrame
    avec les colonnes [publication_id, drug, journal, date].
    
    Optimisé avec des opérations Polars vectorisées pour une meilleure performance.
    """
    # Normalisation en minuscules
    drugs_normalized = df_drugs.with_columns(
        pl.col("drug").str.to_lowercase().alias("drug_term")
    )
    
    publications_normalized = df_publications.with_columns(
        pl.col(title_col).str.to_lowercase().alias("title_processed")
    )

    # Jointure croisée, filtrage des mentions et sélection des colonnes
    return (
        publications_normalized
        .join(drugs_normalized, how="cross")
        .filter(
            pl.col("title_processed").str.contains(pl.col("drug_term"))
        )
        .select(
            pl.col("id").alias("publication_id"),
            pl.col("drug"),  # Nom original du médicament
            "journal",
            "date"
        )
        .unique()  # Élimine les doublons potentiels
    )
