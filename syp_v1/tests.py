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
                    yield start_practice_2,
                    yield practice_task, dict(num_key_pairs=randint(1, 31))
                    yield results_practice,
                else:
                    yield FC_choose_group, dict(information_display=random.choice([1,2]))
                    if self.player.information_display == 1:
                        yield task, dict(num_key_pairs=randint(1, 1501))
                        yield Results
                    else:
                        yield task, dict(num_key_pairs=randint(1, 1201))
                        yield Results
                if self.player.round_number == Constants.num_rounds:
                    yield survey_1, dict(survey_1=randint(1,5), survey_2=randint(1,4), survey_3=randint(18,100),)
                    yield survey_2, dict(survey_4=randint(1,7), survey_5=randint(1,2), survey_6=randint(1,6), survey_7=randint(1,7))
                    yield survey_3, dict(survey_8="testing the short paragraph response")


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

 # start_experiment,
 #    ResultsWaitPage,
 #    # instructions,
 #    # payment_treatment_instructions,
 #    # information_display_instructions,
 #    # start_practice,
 #    wait_instructions,
 #    start_practice_2,
 #    start_practice_3,
 #    ResultsWaitPage,
 #    practice_task,
 #    ResultsWaitPage,
 #    results_practice,
 #    start_task,
 #    FC_choose_group,
 #    task,
 #    ResultsWaitPage,
 #    Results,
 #    # start_survey,
 #    survey_1,
 #    survey_2,
 #    survey_3,
 #    payment_information