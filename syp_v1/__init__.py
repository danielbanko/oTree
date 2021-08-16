import itertools
import random, csv
from otree.api import *

c = Currency

author = "Daniel Banko (daniel.bankoferran@gmail.com)"
doc = """
Code for SYP project
"""


class Constants(BaseConstants):
    name_in_url = 'syp_v1'
    players_per_group = None
    num_rounds = 2
    payment_rate = 0.02 #two cents per keystroke pair?
    treatment_groups = ['NC', 'PC', 'FC']
    showupfee = 6.00

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass


class Player(BasePlayer):
    rank = models.IntegerField()
    treatment_group = models.StringField(initial='NA')
    num_key_pairs = models.IntegerField(initial=-1)
    cum_key_pairs = models.IntegerField(initial=-1)
    practice_round = models.IntegerField(initial=-1)
    is_top20 = models.IntegerField(initial=-1)
    is_top50 = models.IntegerField(initial=-1)
    is_bottom50 = models.IntegerField(initial=-1)
    information_display = models.IntegerField(initial = -1,
                                              label="Do you want to receive peer information?",
                                              widget=widgets.RadioSelectHorizontal,
                                              choices = [
                                                  [0, 'No'],
                                                  [1, 'Yes'],
                                                ]
                                              )
    participant_id = models.StringField(initial = 'NA')
    survey_id = models.StringField(initial = 'NA')

    payoff = models.FloatField(initial = -1.00)

    def custom_export(players):
        # header row
        yield ['session', 'participant_code', 'round_number', 'id_in_group', 'payoff', 'treatment_group']
        for p in players:
            participant = p.participant
            session = p.session
            yield [session.code, participant.code, p.round_number, p.id_in_group, p.payoff, p.treatment_group]


#---------------------------------------------------------
#custom methods

def creating_session(subsession):
    player_list = subsession.get_players()
    if subsession.round_number == 1:
        random.shuffle(player_list)
        treatments = itertools.cycle(Constants.treatment_groups)
        for player in player_list:
            # randomize to treatments
            player.treatment_group = next(treatments)
            print('setting treatment_group to', player.treatment_group, 'for player', player.id_in_group)

    for player in player_list:
        if subsession.round_number != 1:
            player_round1 = player.in_round(1)
            player.treatment_group = player_round1.treatment

def set_final_payoff(player):
    if player.round_number == Constants.num_rounds:
        player.payoff = player.cum_key_pairs*Constants.payment_rate + Constants.showupfee
        return player.payoff


# ------------------------------------------
# PAGES
class start(Page):

    def is_displayed(self):
        return self.round_number == 1

    @staticmethod
    def vars_for_template(player):
        return dict(
            treatment_group = player.treatment_group,
            round_number = Constants.num_rounds,
        )

class instructions(Page):

    def is_displayed(self):
        return self.round_number == 1

class treatment_add_instructions(Page):
    @staticmethod
    def is_displayed(player):
        return player.treatment_group != "NC", player.round_number == 1

class start_practice(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1

class demonstration(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1


class start_practice_2(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1

class practice_task(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1

    form_model = 'player'
    form_fields = ['num_key_pairs']
    timeout_seconds = 30

class results_practice(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1

    @staticmethod
    def vars_for_template(player):
        player.practice_round = 1
        return dict(
            rank=player.rank,
            practice_round = player.practice_round
        )

class task(Page):
    form_model = 'player'
    form_fields = ['num_key_pairs']
    timeout_seconds = 120


class FC_choose_group(Page):
    @staticmethod
    def is_displayed(player):
        return player.treatment_group == "FC", player.round_number != 1
    form_model = 'player'
    form_fields = ['information_display']


class ResultsWaitPage(WaitPage):
    wait_for_all_groups = True
    performance_ranking = []
    @staticmethod
    def after_all_players_arrive(subsession):
        performance_ranking = []
        for p in subsession.get_players():
            performance = [p.id_in_group,p.num_key_pairs]
            performance_ranking.append(performance)
        performance_sorted_by_ranking = sorted(performance_ranking, key = lambda tup:tup[1], reverse=True)
        for p in subsession.get_players():
            p.rank = performance_sorted_by_ranking.index([p.id_in_group,p.num_key_pairs]) + 1
            percentile = (p.rank / Constants.players_per_group)*100
            p.is_top20 = 1 if percentile <= 20 else 0
            p.is_top50 = 1 if (20 <= percentile < 50) else 0
            p.is_bottom50 = 1 if percentile >= 50 else 0
        print(*performance_ranking)
        print(*performance_sorted_by_ranking)



class Results(Page):
    @staticmethod
    def vars_for_template(player):
        return dict(
            num_key_pairs = player.num_key_pairs,
            rank=player.rank,
            treatment_group = player.treatment_group
        )

class survey(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == Constants.num_rounds

page_sequence = [
    start,
    instructions,
    treatment_add_instructions,
    start_practice,
    demonstration,
    start_practice_2,
    practice_task,
    ResultsWaitPage,
    results_practice,
    FC_choose_group,
    task,
    ResultsWaitPage,
    Results
]
