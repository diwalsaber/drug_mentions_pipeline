import pandas as pd


def build_drug_graph(
        df_mentions_pubmed: pd.DataFrame,
        df_mentions_clinical: pd.DataFrame
) -> list:
    """
    Construit la structure de graphe par drug, sous forme d'une liste Python
    (qu'on convertira ensuite en JSON).

    Args:
        df_mentions_pubmed (pd.DataFrame): colonnes [publication_id, drug, journal, date]
        df_mentions_clinical (pd.DataFrame]: même colonnes

    Returns:
        list: chaque élément est un dict représentant 1 drug avec la clé 'drug' et 'mentions'.
    """

    df_pubmed = df_mentions_pubmed.copy()
    df_pubmed["source_type"] = "pudmed"

    df_clinical = df_mentions_clinical.copy()
    df_clinical["source_type"] = "clinical_trial"

    df_all = pd.concat([df_pubmed, df_clinical], ignore_index=True)

    results = []
    for drug_name, group_df in df_all.groupby("drug"):
        mentions_list = []
        for _, row in group_df.iterrows():
            mentions_list.append({
                "source_type": row["source_type"],
                "publication_id": row["publication_id"],
                "journal": row["journal"],
                "date": row["date"]
            })
        results.append({
            "drug": drug_name,
            "mentions": mentions_list
        })
    return results
