import logging
import pandas as pd

logger = logging.getLogger(__name__)


def detect_drug_mentions(
        df_publications: pd.DataFrame,
        df_drugs: pd.DataFrame,
        title_col: str
) -> pd.DataFrame:
    """
    Détecte pour chaque ligne de df_publications si un drug est mentionné 
    dans title_col.
    Retourne un DataFrame avec colonnes:
      [id_publication, drug, journal, date]

    Args:
        df_publications (pd.DataFrame): 
        Contient au minimum: [id, journal, date, <title_col>].
        df_drugs (pd.DataFrame): Contient au minimum: [drug].
        title_col (str): Nom de la colonne du titre dans df_publications 
        (ex. "title" ou "scientific_title").

    Returns:
        pd.DataFrame
    """
    results = []
    # Conversion en minuscule avant comparaison
    df_drugs["drug_lower"] = df_drugs["drug"].str.lower()

    df_publications["title_lower"] = df_publications[title_col].str.lower()

    for _, pub_row in df_publications.iterrows():
        title_text = pub_row["title_lower"]
        publication_id = pub_row["id"]
        journal_name = pub_row["journal"]
        pub_date = pub_row["date"]

        for _, drug_row in df_drugs.iterrows():
            drug_name = drug_row["drug"]
            drug_lower = drug_row["drug_lower"]

            if drug_lower in title_text:
                results.append({
                    "publication_id": publication_id,
                    "drug": drug_name,
                    "journal": journal_name,
                    "date": pub_date
                })

    return pd.DataFrame(results)
