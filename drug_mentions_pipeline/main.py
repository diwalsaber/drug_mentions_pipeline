"""
Main entry point for the drug mentions pipeline.
"""
import json
import pandas as pd
from pathlib import Path
from drug_mentions_pipeline.config import (
    DRUGS_PATH, 
    PUBMED_CSV_PATH, 
    PUBMED_JSON_PATH, 
    CLINICAL_TRIALS_PATH, 
    OUTPUT_FILE
)
from drug_mentions_pipeline.extract.extract import extract_csv, extract_json
from drug_mentions_pipeline.transform import detect_drug_mentions, build_drug_graph
from drug_mentions_pipeline.utils.logging_utils import setup_logging


def run_pipeline(
    drugs_path=None,
    pubmed_csv_path=None,
    pubmed_json_path=None,
    clinical_path=None,
    output_file=None
):
    """
    Run the complete drug mentions pipeline.

    Args:
        drugs_path (str, optional): Path to drugs CSV file. Defaults to None.
        pubmed_csv_path (str, optional): Path to PubMed CSV file. Defaults to None.
        pubmed_json_path (str, optional): Path to PubMed JSON file. Defaults to None.
        clinical_path (str, optional): Path to clinical trials CSV file. Defaults to None.
        output_file (str, optional): Path to output JSON file. Defaults to None.
    """
    logger = setup_logging()
    logger.info("Starting drug mentions pipeline")

    # Use default paths from config if not specified
    drugs_path = drugs_path or DRUGS_PATH
    pubmed_csv_path = pubmed_csv_path or PUBMED_CSV_PATH
    pubmed_json_path = pubmed_json_path or PUBMED_JSON_PATH
    clinical_path = clinical_path or CLINICAL_TRIALS_PATH
    output_file = output_file or OUTPUT_FILE

    # Ensure output directory exists
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)

    # I. Extraction
    logger.info("Extracting data from source files")
    drugs_df = extract_csv(drugs_path)
    pubmed_csv_df = extract_csv(pubmed_csv_path)
    pubmed_json_df = extract_json(pubmed_json_path)
    clinical_df = extract_csv(clinical_path)

    logger.info(f"Extracted data shapes:")
    logger.info(f"- drugs_df: {drugs_df.shape}")
    logger.info(f"- pubmed_csv_df: {pubmed_csv_df.shape}")
    logger.info(f"- pubmed_json_df: {pubmed_json_df.shape}")
    logger.info(f"- clinical_df: {clinical_df.shape}")

    # II. Transform
    logger.info("Transforming data")
   
    # II.1 Transform - PubMed CSV
    mentions_pubmed_csv = detect_drug_mentions(
        df_publications=pubmed_csv_df,
        df_drugs=drugs_df,
        title_col="title"
    )

    # II.2 Transform - PubMed JSON
    mentions_pubmed_json = detect_drug_mentions(
        df_publications=pubmed_json_df,
        df_drugs=drugs_df,
        title_col="title"
    )

    # Combine PubMed mentions
    mentions_pubmed = pd.concat([mentions_pubmed_csv, mentions_pubmed_json], ignore_index=True)

    # II.3 Transform - Clinical Trials
    mentions_clinical = detect_drug_mentions(
        df_publications=clinical_df,
        df_drugs=drugs_df,
        title_col="scientific_title"
    )

    # II.4 Transform - Graph build
    drug_graph_data = build_drug_graph(mentions_pubmed, mentions_clinical)

    # III. Load
    logger.info(f"Writing output to {output_file}")
    with open(output_file, "w", encoding="utf-8") as out_file:
        json.dump(drug_graph_data, out_file, indent=2, ensure_ascii=False)

    logger.info("Pipeline completed. Drug graph JSON generated.")
    return drug_graph_data


def main():
    """Entry point for the command-line interface."""
    run_pipeline()


if __name__ == "__main__":
    main()
