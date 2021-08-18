from otree.api import Currency as c, currency_range, expect, Bot
from . import *
from random import randint
random.seed(10)


class PlayerBot(Bot):

    cases = [
        'success',  # players enter valid inputs
        # 'fail',  # players enter invalid inputs
    ]
    def play_round(self):
        # start, each yield will be run "self.round_number" of times.
        case = self.case
        if case == 'success':
            if self.player.treatment_group == 'PC':
                if self.player.round_number == 1:
                    yield start,
                    yield instructions,
                    yield treatment_add_instructions,
                    yield start_practice,
                    yield demonstration,
                    yield start_practice_2,
                    yield practice_task, dict(num_key_pairs=randint(1,31))
                    yield results_practice
                    yield task, dict(num_key_pairs=randint(1,101))
                    yield Results
                else:
                    yield task, dict(num_key_pairs=randint(1, 101))
                    yield Results

            if self.player.treatment_group == 'FC':
                if self.player.round_number == 1:
                    yield start,
                    yield instructions,
                    yield treatment_add_instructions,
                    yield start_practice,
                    yield demonstration,
                    yield start_practice_2,
                    yield practice_task, dict(num_key_pairs=randint(1,31))
                    yield results_practice,
                    yield task, dict(num_key_pairs=randint(1,101))
                    yield Results
                else:
                    yield FC_choose_group, dict(information_display=random.choice([0,1]))
                    yield task, dict(num_key_pairs=randint(1, 101))
                    yield Results

            if self.player.treatment_group == 'NC':
                if self.player.round_number == 1:
                    yield start,
                    yield instructions,
                    yield start_practice,
                    yield demonstration,
                    yield start_practice_2,
                    yield practice_task, dict(num_key_pairs=randint(1,31))
                    yield results_practice,
                    yield task, dict(num_key_pairs=randint(1,101))
                    yield Results
                else:
                    yield task, dict(num_key_pairs=randint(1, 101))
                    yield Results
