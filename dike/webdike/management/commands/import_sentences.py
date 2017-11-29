from django.core.management.base import BaseCommand, CommandError
from ...models import Document, Sentence, Step

class Command(BaseCommand):
    help = "Create sentences for a judgement.\
            Usage: python manage.py import_sentences --docid 1 --txtpath sample.txt"

    def add_arguments(self, parser):
        parser.add_argument('--docid', help="Which document to add sentences")
        parser.add_argument('--txtpath', help="Which text file to import sentences")

    def handle(self, *args, **options):
        with open(options['txtpath']) as f:
            lines = f.readlines()
        self.put_sentences(lines, options['docid'])

    def put_sentences(self, lines, doc_id):
        parent_doc = Document.objects.get(id=doc_id)
        for line in lines:
            new_sentence = Sentence.objects.create(
                content=line,
                order=0,
                document=parent_doc,
                )
            new_sentence.save()

            new_step = Step.objects.create(
                stage=Step.IMPORTED,
                sentence=new_sentence,
                result=[line],
            )
            new_step.save()

        parent_doc.last_valid_step_id = new_step.id
        parent_doc.save()

