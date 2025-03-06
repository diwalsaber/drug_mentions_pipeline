# drug_mentions_pipeline/analysis/journal_analyzer.py

import json
import logging
from collections import defaultdict

logger = logging.getLogger(__name__)

def find_journal_with_most_drugs(json_file_path):
    """
    Analyse le fichier JSON produit par la pipeline pour trouver le journal
    qui mentionne le plus de médicaments différents.

    Args:
        json_file_path (str): Chemin vers le fichier JSON à analyser

    Returns:
        tuple: (nom_du_journal, nombre_de_médicaments_différents, liste_des_médicaments)
    """
    logger.info(f"Analyse du fichier {json_file_path} pour trouver le journal avec le plus de médicaments")

    try:
        # Charger les données du fichier JSON
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Dictionnaire pour stocker les médicaments mentionnés par chaque journal
        journal_drugs = defaultdict(set)

        # Parcourir tous les médicaments et leurs mentions
        for drug_entry in data:
            drug_name = drug_entry['drug']
            for mention in drug_entry['mentions']:
                journal_name = mention['journal']
                # Ajouter ce médicament à l'ensemble des médicaments mentionés par ce journal
                journal_drugs[journal_name].add(drug_name)

        # Trouver le journal avec le plus grand nombre de médicaments différents
        if not journal_drugs:
            logger.warning("Aucun journal trouvé dans les données")
            return None, 0, []

        top_journal = max(journal_drugs.items(), key=lambda x: len(x[1]))
        journal_name = top_journal[0]
        drug_count = len(top_journal[1])
        drug_list = list(top_journal[1])

        logger.info(f"Journal avec le plus de médicaments: {journal_name} ({drug_count} médicaments)")
        return journal_name, drug_count, drug_list

    except Exception as e:
        logger.error(f"Erreur lors de l'analyse du fichier JSON: {e}")
        raise
