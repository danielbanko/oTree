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
        player_list = self.subsession.get_players()

        if self.subsession.round_number in [1]:
                self.player.practice_round = 1  # should have just one practice_round

        case = self.case
        if case == 'success':
            if self.player.treatment_group == 'PC':
                if self.player.round_number == 1:
                    yield start_experiment,
                    yield instructions,
                    yield payment_treatment_instructions,
                # elif self.player.practice_round == 1:
                    yield start_practice,
                    yield start_practice_2,
                    yield start_practice_3,
                    yield practice_task, dict(num_key_pairs=randint(1, 31))
                    yield results_practice,
                    yield start_task
                else:
                    yield task, dict(num_key_pairs=randint(1, 1001))
                    yield Results

            if self.player.treatment_group == 'FC':
                if self.player.round_number == 1:
                    yield start_experiment,
                    yield instructions,
                    yield payment_treatment_instructions,
                # elif self.player.practice_round == 1:
                    yield start_practice,
                    yield start_practice_2,
                    yield start_practice_3,
                    yield practice_task, dict(num_key_pairs=randint(1, 31))
                    yield results_practice,
                    yield start_task
                else:
                    yield FC_choose_group, dict(information_display=random.choice([1,2]))
                    if self.player.information_display == 1:
                        yield task, dict(num_key_pairs=randint(1, 1501))
                        yield Results
                    else:
                        yield task, dict(num_key_pairs=randint(1, 1201))
                        yield Results


            if self.player.treatment_group == 'NC':
                if self.player.round_number == 1:
                    yield start_experiment,
                    yield instructions,
                    yield payment_treatment_instructions,
                # elif self.player.practice_round == 1:
                    yield start_practice,
                    yield start_practice_2,
                    yield start_practice_3,
                    yield practice_task, dict(num_key_pairs=randint(1, 31))
                    yield results_practice,
                    yield start_task
                else:
                    yield task, dict(num_key_pairs=randint(1, 801))
                    yield Results
