def test_full_pipeline_simple():
    import tempfile
    import os
    import pandas as pd
    import json
    from pathlib import Path

    temp_dir = tempfile.TemporaryDirectory()
    test_dir = Path(temp_dir.name)

    # 2. Créer les répertoires input/output
    input_dir = test_dir / "input"
    output_dir = test_dir / "output"
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    # 3. Préparer les données de test
    drugs_df = pd.DataFrame({
        "atccode": ["A01", "A02", "A03"],
        "drug": ["Aspirin", "Betamethasone", "Atropine"]
    })

    publications_df = pd.DataFrame({
        "id": [1, 2, 3],
        "title": [
            "Study of Aspirin effects",
            "Betamethasone in treatment of inflammation",
            "Effects of various drugs"
        ],
        "date": ["01/01/2020", "01/02/2020", "01/03/2020"],
        "journal": ["Journal A", "Journal B", "Journal C"]
    })

    # 4. Créer les fichiers de test
    drugs_path = input_dir / "drugs.csv"
    pubmed_csv_path = input_dir / "pubmed.csv"
    pubmed_json_path = input_dir / "pubmed.json"
    clinical_trials_path = input_dir / "clinical_trials.csv"
    output_path = output_dir / "drug_graph.json"

    drugs_df.to_csv(drugs_path, index=False)
    publications_df.to_csv(pubmed_csv_path, index=False)

    with open(pubmed_json_path, "w") as f:
        json.dump(publications_df.to_dict(orient="records"), f)

    publications_df.rename(columns={"title": "scientific_title"}).to_csv(
        clinical_trials_path, index=False
    )

    # 5. Exécuter le pipeline
    from drug_mentions_pipeline.main import run_pipeline
    result = run_pipeline(
        drugs_path=str(drugs_path),
        pubmed_csv_path=str(pubmed_csv_path),
        pubmed_json_path=str(pubmed_json_path),
        clinical_path=str(clinical_trials_path),
        output_file=str(output_path)
    )

    # 6. Vérifications
    assert isinstance(result, list)
    assert len(result) > 0

    # Vérifier que le fichier a été créé
    assert output_path.exists()

    # Charger et vérifier le contenu du fichier
    with open(output_path, "r") as f:
        file_content = json.load(f)

    assert file_content == result

    # Nettoyage
    temp_dir.cleanup()
