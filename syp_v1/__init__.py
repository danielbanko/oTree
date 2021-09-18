import itertools
import random, csv
import math
from otree.api import *

c = Currency

author = "Daniel Banko (daniel.bankoferran@gmail.com)"
doc = """
Code for SYP project
"""


class Constants(BaseConstants):
    name_in_url = 'syp_v1'
    players_per_group = 10 #this has to be 10, otherwise breaks
    num_practice_rounds = 1
    num_rounds = 6 #this includes practice rounds
    payment_rate = 0.05 #ten or two cents per keystroke pair? what is it in other studies?
    # treatment_groups = ['NC'] #for testing purposes
    treatment_groups = ['NC', 'PC', 'FC'] #for actual implementation
    showupfee = 6.00

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass


class Player(BasePlayer):
    rank = models.IntegerField(initial=-1)
    treatment_group = models.StringField(initial='NA')
    group_number = models.IntegerField(initial=-1)
    num_key_pairs = models.IntegerField(initial=-1)
    cum_key_pairs = models.IntegerField(initial=0) #not working yet
    practice_round = models.IntegerField(initial=-1)
    percentile = models.FloatField(initial=-1.00)
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
    survey_id = models.StringField(initial = 'NA')
    pay_round = models.IntegerField(initial=-1)


 #DO NOT CREATE A VARIABLE CALLED PARTICIPANT_ID OR PAYOFF breaks things

def custom_export(players):
    # header row
    yield ['session', 'participant_code', 'round_number', 'id_in_group', 'payoff', 'treatment_group', 'rank', 'num_key_pairs', 'cum_key_pairs', ]
    for p in players:
        participant = p.participant
        session = p.session
        yield [session.code, participant.code, p.round_number, p.id_in_group, p.payoff, p.treatment_group, p.rank, p.num_key_pairs, p.cum_key_pairs]


#---------------------------------------------------------
#custom methods

def creating_session(subsession):
    player_list = subsession.get_players()
    if subsession.round_number == 1:
        treatments = itertools.cycle(Constants.treatment_groups)
        groups = [1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2] #id of the group for each participant (one entry per participant) -- requires players_per_group == 10
        index = 1
        for player in player_list:
            player.group_number = groups.pop(0)

            # randomize to treatments
            player.treatment_group = next(treatments)
            print('setting treatment_group to', player.treatment_group, 'for player', player.id_in_group)

    for player in player_list:
        if subsession.round_number != 1:
            player_round1 = player.in_round(1)
            player.treatment_group = player_round1.treatment_group
            player.group_number = player_round1.group_number

    if subsession.round_number in [1]:
        for player in player_list:
            player.practice_round = 1 #this must always be 1


def set_final_payoff(player):
    if player.round_number == Constants.num_rounds: #in final round
        # determine random round for payment
        random_round = random.randint(2, Constants.num_rounds)
        player.pay_round = random_round
        player_in_pay_round = player.in_round(random_round)
        player.num_key_pairs = player_in_pay_round.num_key_pairs
        player.payoff = player.num_key_pairs*Constants.payment_rate + Constants.showupfee
        return player.payoff


# ------------------------------------------
# PAGES
class start_experiment(Page):

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
        return player.round_number == 1 and player.treatment_group != 'NC'

    @staticmethod
    def vars_for_template(player):
        return dict(
            treatment_group = player.treatment_group,
            round_number = Constants.num_rounds,
        )

class start_practice(Page):
    @staticmethod
    def is_displayed(player):
        return player.practice_round == 1

class start_practice_2(Page):
    @staticmethod
    def is_displayed(player):
        return player.practice_round == 1


class start_practice_3(Page):
    @staticmethod
    def is_displayed(player):
        return player.practice_round == 1

class practice_task(Page):
    @staticmethod
    def is_displayed(player):
        return player.practice_round == 1
    timeout_seconds = 30 #TODO TURN THIS BACK ON
    timer_text = 'Time left:'
    form_model = 'player'
    form_fields = ['num_key_pairs']


class results_practice(Page):
    @staticmethod
    def is_displayed(player):
        return player.practice_round == 1

    @staticmethod
    def vars_for_template(player):
        return dict(
            rank=player.rank,
            practice_round = player.practice_round
        )

class start_task(Page):

    def is_displayed(self):
        return self.round_number == 1

class task(Page):
    form_model = 'player'
    form_fields = ['num_key_pairs']
    timeout_seconds = 120 #number of seconds to complete the task. In ariely, it is 300 (but i think he only had one round)
    timer_text = 'Time left:'

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # player.cum_key_pairs = player.cum_key_pairs + player.num_key_pairs #TODO need to pass this across rounds. not working.
        if player.round_number == Constants.num_rounds:
            set_final_payoff(player)

    @staticmethod
    def is_displayed(player):
        return player.practice_round != 1


class FC_choose_group(Page):
    @staticmethod
    def is_displayed(player):
        return player.treatment_group == "FC" and player.practice_round != 1
    form_model = 'player'
    form_fields = ['information_display']


class ResultsWaitPage(WaitPage):
    wait_for_all_groups = True
    performance_ranking = []
    @staticmethod
    def after_all_players_arrive(subsession):
        performances = []
        for p in subsession.get_players():
            performance = [p.id_in_group,p.num_key_pairs]
            performances.append(performance)
            print('performances is', performances)

        #split performances by group
        num_groups = math.ceil(len(subsession.get_players()) / Constants.players_per_group)

        performances_grouped = []
        index = 0
        for group in range(num_groups):
            performance_group = performances[index:index+Constants.players_per_group]
            performance_group_sorted = sorted(performance_group, key=lambda tup: tup[1], reverse=True)
            performances_grouped.append(performance_group_sorted)
            index = index + Constants.players_per_group

        #determining ranking
        for p in subsession.get_players():
            players_group = performances_grouped[p.group_number-1]
            p.rank = players_group.index([p.id_in_group, p.num_key_pairs]) + 1
            p.percentile = (p.rank / Constants.players_per_group) * 100
            p.is_top20 = 1 if p.percentile <= 20 else 0
            p.is_top50 = 1 if (20 < p.percentile <= 50) else 0
            p.is_bottom50 = 1 if p.percentile > 50 else 0

        print('performances_grouped is:', performances_grouped)


    @staticmethod
    def vars_for_template(player):
        return dict(
            num_key_pairs = player.num_key_pairs,
            rank=player.rank,
            treatment_group = player.treatment_group
        )



class Results(Page):
    @staticmethod
    def vars_for_template(player):
        return dict(
            num_key_pairs = player.num_key_pairs,
            rank=player.rank,
            treatment_group = player.treatment_group,
            payoff = player.payoff
        )
    @staticmethod
    def is_displayed(player):
        return player.practice_round != 1

class survey(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == Constants.num_rounds

class payment_information(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == Constants.num_rounds

page_sequence = [
    start_experiment,
    instructions,
    treatment_add_instructions,
    start_practice,
    start_practice_2,
    start_practice_3,
    practice_task,
    ResultsWaitPage,
    results_practice,
    start_task,
    FC_choose_group,
    task,
    ResultsWaitPage,
    Results,
    payment_information
]

# page_sequence = [
#     practice_task,
#     ResultsWaitPage,
#     Results
# ]
