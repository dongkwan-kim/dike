from django.core.management.base import BaseCommand, CommandError
import random
import math
import pprint
from ...models import Document, Sentence, Step
from ...natural_selection import get_work_routing_info, change_populations

class Command(BaseCommand):
    help = ""

    def add_arguments(self, parser):
        parser.add_argument('--docid', action='store_true')
        parser.add_argument('--users', action='store_true')
        parser.add_argument('--nostop', action='store_true')
        pass

    def get_docid(self, options):
        if not options['docid']:
            docid = max([d.id for d in Document.objects.all()])
        else:
            docid = options['docid']
        return docid

    def get_users(self, options):
        if not options['users']:
            users = 20
        else:
            users = options['users']
        return users

    def handle(self, *args, **options):

        docid = self.get_docid(options)
        users = self.get_users(options)

        test_steps_start = Document.objects.get(id=docid).last_valid_step_id
        sample_step_id = test_steps_start

        print("deleted steps id larger than {}".format(test_steps_start))
        Step.objects.filter(id__gt=test_steps_start).delete()
        initial_step = Step.objects.get(id=sample_step_id)

        ordinal = lambda n: "%d%s" % (n, "tsnrhtdd"[(math.floor(n / 10) % 10 != 1) * (n % 10 < 4) * n % 10::4])

        for i in range(users):

            current_step = initial_step
            trials = random.randint(1, 5)
            print('--------------------------------')
            print('{} user will make {} Steps at maximum'.format(ordinal(i), trials))

            for _ in range(trials):

                next_action = get_work_routing_info(current_step.id)
                creatable = next_action['creatable']
                votable = next_action['votable']
                pprint.pprint(next_action)

                if creatable:
                    next_stage = current_step.stage + 1
                    print('\tcreating step at {} stage'.format(next_stage))

                    new_step = Step.objects.create(
                        stage=next_stage,
                        result=[str(i), str(i)],
                        sentence_id=current_step.sentence_id,
                        parent_step=current_step
                    )
                    new_step.save()
                    current_step = new_step

                if votable:
                    print('\tvoting')
                    step_list = next_action["step_list"]
                    rest_list = step_list[2:]

                    # privilege
                    winner = random.choice([step_list[0]] + step_list[:2])
                    winner.do_vote()

                    while len(rest_list) > 0:
                        winner = random.choice([winner, rest_list[0]])
                        rest_list = rest_list[1:]

                # current step is 4
                if not creatable and not votable:
                    # current_step = Step.objects.get(id=sample_step_id)
                    break

                # Change populations of next generation
                change_populations(current_step.stage + 1)

            if not options['nostop']:
                input('\tenter any key to proceed\n')

