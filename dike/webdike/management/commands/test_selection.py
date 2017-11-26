from django.core.management.base import BaseCommand, CommandError
import random
from ...models import Document, Sentence, Step
from ...natural_selection import get_work_routing_info, change_populations

class Command(BaseCommand):
    help = ""
    test_steps_start = 253
    sample_step_id = 238

    def add_arguments(self, parser):
        parser.add_argument('--nostop', action='store_true')
        pass

    def handle(self, *args, **options):
        print("deleted steps id larger than {}".format(self.test_steps_start))
        Step.objects.filter(id__gte=self.test_steps_start).delete()
        current_step = Step.objects.get(id=self.sample_step_id)
        for i in range(100):
            print('{}th round'.format(i))
            next_action = get_work_routing_info(current_step.id)
            print(next_action)
            # if next_action['creatable'] and current_step.stage is not 4:
            if current_step.stage is not 4:
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
            if next_action['votable']:
                print('\tvoting')
                step_list = next_action["step_list"]
                rest_list = step_list[2:]
                winner = random.choice(step_list[:2])
                winner.do_vote()
                while len(rest_list) is not 0:
                    winner = random.choice([winner, rest_list[0]])
                    rest_list = rest_list[1:]
            if current_step.stage is 4:
                current_step = Step.objects.get(id=self.sample_step_id)
            change_populations(current_step.stage)
            if not options['nostop']:
                input('\tenter any key to proceed')
