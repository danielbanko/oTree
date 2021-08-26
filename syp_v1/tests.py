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
                    yield start,
                    yield instructions,
                    yield treatment_add_instructions,
                # elif self.player.practice_round == 1:
                    yield start_practice,
                    yield start_practice_2,
                    yield start_practice_3,
                    yield practice_task, dict(num_key_pairs=randint(1, 31))
                    yield results_practice
                else:
                    yield task, dict(num_key_pairs=randint(1, 101))
                    yield Results

            if self.player.treatment_group == 'FC':
                if self.player.round_number == 1:
                    yield start,
                    yield instructions,
                    yield treatment_add_instructions,
                # elif self.player.practice_round == 1:
                    yield start_practice,
                    yield start_practice_2,
                    yield start_practice_3,
                    yield practice_task, dict(num_key_pairs=randint(1, 31))
                    yield results_practice
                else:
                    yield FC_choose_group, dict(information_display=random.choice([0,1]))
                    yield task, dict(num_key_pairs=randint(1, 101))
                    yield Results

            if self.player.treatment_group == 'NC':
                if self.player.round_number == 1:
                    yield start,
                    yield instructions,
                # elif self.player.practice_round == 1:
                    yield start_practice,
                    yield start_practice_2,
                    yield start_practice_3,
                    yield practice_task, dict(num_key_pairs=randint(1, 31))
                    yield results_practice
                else:
                    yield task, dict(num_key_pairs=randint(1, 101))
                    yield Results
