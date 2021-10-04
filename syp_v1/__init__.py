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
    players_per_group = 10 #should be 10 for actual trials
    num_practice_rounds = 1
    num_rounds = 21 #this includes practice rounds
    payment_rate = 0.02 #two cents per keystroke pair? what is it in other studies?
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
<<<<<<< Updated upstream
 #DO NOT CREATE A VARIABLE CALLED PARTICIPANT_ID OR PAYOFF
 #do not create a variable called payoff

    def custom_export(players):
        # header row
        yield ['session', 'participant_code', 'round_number', 'id_in_group', 'payoff', 'treatment_group', 'rank', 'num_key_pairs', 'cum_key_pairs', ]
        for p in players:
            participant = p.participant
            session = p.session
            yield [session.code, participant.code, p.round_number, p.id_in_group, p.payoff, p.treatment_group, p.rank, p.num_key_pairs, p.cum_key_pairs]
=======
    pay_round = models.IntegerField(initial=-1)
    piecerate_payment = models.FloatField(initial=-1.00)
    participant_label_check = models.StringField(initial = 'NA')
    survey_1 = models.IntegerField(initial=-1, widget=widgets.RadioSelect, choices=[
       [1, 'Asian'],  # <- correct answer
       [2, 'Black'],
       [3, 'Caucasion'],
       [4, 'Hispanic'],
       [5, 'Other']
    ])

    survey_2 = models.IntegerField(initial=-1, widget=widgets.RadioSelect, choices=[
       [1, 'Male'],
       [2, 'Female'],
       [3, 'Non-binary / third gender'],
       [4, 'Prefer not to say']
    ])

    survey_3 = models.IntegerField(null=True, min = 16, max = 100)

    survey_4 = models.IntegerField(initial=-1, widget=widgets.RadioSelect, choices=[
       [1, 'Extremely liberal'],
       [2, 'Very liberal'],
       [3, 'Slightly liberal'],
       [4, 'Neutral'],
       [5, 'Slightly conservative'],
       [6, 'Very conservative'],
       [7, 'Extremely conservative'],
    ])

    survey_5= models.IntegerField(initial=-1, widget=widgets.RadioSelect, choices=[
       [1, 'English'],
       [2, 'Other'],
    ])

    survey_6= models.IntegerField(initial=-1, widget=widgets.RadioSelect, choices=[
       [1, 'Freshman'],
       [2, 'Sophomore'],
       [3, 'Junior'],
       [4, 'Senior'],
       [5, 'Graduate Student'],
       [6, 'Other'],
    ])

    survey_7= models.IntegerField(initial=-1, widget=widgets.RadioSelect, choices=[
       [1, 'Arts'],
       [2, 'Business'],
       [3, 'Humanities'],
       [4, 'Natural Sciences'],
       [5, 'Social Sciences'],
       [6, 'Physical Sciences'],
       [7, 'Other'],
    ])

    venmo = models.StringField(initial='NA')

 #DO NOT CREATE A VARIABLE CALLED PARTICIPANT_ID OR PAYOFF breaks things

def custom_export(players):
    # header row
    yield ['session', 'participant_code', 'round_number', 'id_in_group', 'payoff', 'treatment_group', 'rank', 'num_key_pairs', 'cum_key_pairs', ]
    for p in players:
        participant = p.participant
        session = p.session
        yield [session.code, participant.code, p.round_number, p.id_in_group, p.payoff, p.treatment_group, p.rank, p.num_key_pairs, p.cum_key_pairs]
>>>>>>> Stashed changes


#---------------------------------------------------------
#custom methods

def creating_session(subsession):
    # Use this code to figure out how to import practice rounds:
    # # copy values from constant parameter table into player model
    # parameters_for_round = {key: int(value) for key, value in
    #                         Constants.round_parameters[subsession.round_number - 1].items()}
    # for player in subsession.get_players():
    #     player.task = parameters_for_round['task']
    #     player.round_in_task = parameters_for_round['round_in_task']
    #     player.init_in_task = parameters_for_round['init_in_task']
    #     player.last_in_task = parameters_for_round['last_in_task']
    #     player.urns_0 = parameters_for_round['urns_0']
    #     player.urns_1 = parameters_for_round['urns_1']
    #     player.balls0_urn0 = parameters_for_round['balls0_urn0']
    #     player.balls1_urn0 = parameters_for_round['balls1_urn0']
    #     player.balls0_urn1 = parameters_for_round['balls0_urn1']
    #     player.balls1_urn1 = parameters_for_round['balls1_urn1']
    #     player.p_urn1 = Fraction(player.urns_1, player.urns_0 + player.urns_1)
    #     player.p_ball1_urn0 = Fraction(player.balls1_urn0, player.balls0_urn0 + player.balls1_urn0)
    #     player.p_ball1_urn1 = Fraction(player.balls1_urn1, player.balls0_urn1 + player.balls1_urn1)
    #
    #     # get elicitation type from first round
    #     if subsession.round_number != 1:
    #         player_round1 = player.in_round(1)
    #         player.elicit_type = player_round1.elicit_type
    #
    #     # realize new state if first round in task, else use previous state
    #     if subsession.round_number == parameters_for_round['init_in_task']:
    #         state_realization(player)
    #     else:
    #         prev_player = player.in_round(parameters_for_round['init_in_task'])
    #         player.true_state = prev_player.true_state
    #     # print('true state for player', player.id_in_subsession, 'in round', player.round_number, 'is', player.true_state)
    #
    #     signal_realization(player)
    #     # print('signal for player', player.id_in_subsession, 'in round', player.round_number, 'is', player.signal)

    player_list = subsession.get_players()
    if subsession.round_number == 1:
        treatments = itertools.cycle(Constants.treatment_groups)
        groups = [1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2] #id of the group for each participant (one entry per participant)
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
            player.practice_round = 1 #should have just one practice_round


def set_final_payoff(player):
    if player.round_number == Constants.num_rounds: #in final round
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

    form_model = 'player'
    form_fields = ['num_key_pairs']
    timeout_seconds = 30

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

class task(Page):
    form_model = 'player'
    form_fields = ['num_key_pairs']
    timeout_seconds = 120 #number of seconds to complete the task

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.cum_key_pairs = player.cum_key_pairs + player.num_key_pairs
        #need to pass this across rounds. not working.

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
            treatment_group = player.treatment_group
        )
    @staticmethod
    def is_displayed(player):
        return player.practice_round != 1

class survey(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == Constants.num_rounds

<<<<<<< Updated upstream
=======
class survey_5(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == Constants.num_rounds

class payment_information(Page):
    form_model = 'player'
    form_fields = 'participant_label_check'
    @staticmethod
    def is_displayed(player):
        return player.round_number == Constants.num_rounds



>>>>>>> Stashed changes
page_sequence = [
    start,
    instructions,
    treatment_add_instructions,
    start_practice,
    start_practice_2,
    start_practice_3,
    practice_task,
    ResultsWaitPage,
    results_practice,
    FC_choose_group,
    task,
    ResultsWaitPage,
    Results
]
