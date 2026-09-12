# Raw benchmark data

Raw TruthfulQA and SQuAD downloads are not committed because they are reproducible external datasets. Run:

`python -m app.knowledge_base.ingest --mode benchmarks --squad-limit 200 --truthfulqa-limit 200`
