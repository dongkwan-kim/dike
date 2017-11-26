## How to load judgements
1. Create `Document` at admin panel
2. Put each sentences in judgement in one line, in a text file.
3. Load
```commandline
python manage.py import_sentences --docid 1 --txtpath ../data/sample.txt
```
