
from otree.api import *

c = Currency

author = "Daniel Banko (daniel.bankoferran@gmail.com"
doc = """
Code for SYP
"""


class Constants(BaseConstants):
    name_in_url = 'syp_v1'
    # players_per_group = 10 #used for actual trials
    players_per_group = None #testing purposes
    task_timer = 120
    num_rounds = 1 # must be more than the max one person can do in task_timer seconds


class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass


class Player(BasePlayer):
    treatment_group = models.StringField()


    def score_round(self):
        # update player payoffs
        if (self.correct_text == self.user_text):
            self.is_correct = True
            self.payoff_score = 1
        else:
            self.is_correct = False
            self.payoff_score = c(0)

    age = models.PositiveIntegerField

    task_timer = models.PositiveIntegerField( doc = "The length of the real effort task timer.")



    correct_text = models.CharField( doc = "")

    user_text = models.CharField( doc = "")

    user_total = models.PositiveIntegerField(
        min = 1,
        max = 9999,
        doc = "user's score")
        #widget = widgets.TextInput(attrs={'autocomplete':'off'}))

    is_correct = models.BooleanField( doc= "did the user get the task correct?")

    payoff_score = models.FloatField( doc = '''earnings in this task''')

    user_payoff = models.FloatField( doc = '''total earnings for user''')

    def custom_export(players):
        # header row
        yield ['session', 'participant_code', 'round_number', 'id_in_group', 'payoff', 'treatment_group']
        for p in players:
            participant = p.participant
            session = p.session
            yield [session.code, participant.code, p.round_number, p.id_in_group, p.payoff, p.treatment_group]

def creating_session(subsession):
    import itertools
    treatment_groups = itertools.cycle(['NC', 'PC', 'FC'])
    if subsession.round_number == 1:
        for player in subsession.get_players():
            # randomize to treatments
            player.treatment_group = next(treatment_groups)
            print('set treatment_group to', player.treatment_group)
            return player.treatment_group

# def creating_sesssion(self):  # TODO: FIGURE OUT WHY CODE IN CREATING_SESSION IS NOT RUNNING
#
#     print('test')
#     players = self.get_players()
#
#     if 'task_timer' in self.session.config:
#         task_timer = self.session.config['task_timer']
#     else:
#         task_timer = Constants.task_timer
#         print('test')
#
#     for p in self.get_players():
#         p.task_timer = task_timer
#         print('p is', p)
#         # p.correct_text = Constants.reference_texts[self.round_number - 1]


# ------------------------------------------
# PAGES
class start(Page):

    def is_displayed(self):
        return self.round_number == 1

    # def before_next_page(self):
    #     # user has ret_timer seconds to complete as many pages as possible
    #     self.participant.vars['expiry_timestamp'] = 120

    # def vars_for_template(self):
    #
    #     return {
    #         'debug': settings.DEBUG,
    #     }

class task(Page):

    form_model = 'player'
    form_fields = ['user_text']

    timeout_seconds = 120

    # @staticmethod
    # def vars_for_template(player):
    #     a = player.treatment_group
    #     return dict(
    #         a=a,
    #         b=1 + 1,
    #     )

    # def get_timeout_seconds(self):
    #     return self.participant.vars['expiry_timestamp'] - time.time()
    #
    # def is_displayed(self):
    #     return self.participant.vars['expiry_timestamp'] - time.time() > 3
  # current number of correctly done tasks
  #       total_payoff = 0
        # for p in self.player.in_all_rounds():
        #     if p.payoff_score != None:
        #         total_payoff += p.payoff_score

        # set up messages in calculation task
        # if self.round_number == 1:
        #     correct_last_round = "<br>"
        # else:
        #     if self.in_previous_rounds()[-1].is_correct:
        #         correct_last_round = "Your last sum was <font color='green'>correct</font>"
        #     else:
        #         correct_last_round = "Your last sum was <font color='red'>incorrect</font>"
        #
        # return {
        #     'int1': self.int1,
        #     'total_payoff': round(total_payoff),
        #     'round_count':(self.round_number - 1),
        #     # 'debug': settings.DEBUG,
        #     'correct_last_round': correct_last_round
        # }

    # def before_next_page(self):
    #     self.player.score_round()



def vars_for_admin_report(subsession):
    payoffs = sorted([p.payoff for p in subsession.get_players()])
    return dict(payoffs=payoffs)


class ResultsWaitPage(WaitPage):

    wait_for_all_groups = True

    # def is_displayed(self):
    #     return self.round_number == Constants.num_rounds
    # def after_all_players_arrive(subsession):
    #     subsession.


class Results(Page):

    # def is_displayed(self):
    #     return self.round_number == Constants.num_rounds

    def vars_for_template(self):

        total_payoff = 0
        # for p in self.player.in_all_rounds():
        #     if p.payoff_score != None:
        #         total_payoff += p.payoff_score

        # self.participant.vars['task_1_score'] = total_payoff

        # only keep obs if YourEntry player_sum, is not None.
        table_rows = []
        # for prev_player in self.player.in_all_rounds():
        #     if (prev_player.user_total != None):
        #         if (prev_player.user_total > 0):
        #             row = {
        #                 'round_number': prev_player.round_number,
        #                 'int1': prev_player.int1,
        #                 'int2': prev_player.int2,
        #                 'Ints_sum': prev_player.solution,
        #                 'player_sum': round(prev_player.user_total),
        #                 'is_correct': prev_player.is_correct,
        #                 'payoff': round(prev_player.payoff_score),
        #             }
        #             table_rows.append(row)
        #
        # self.participant.vars['t1_results'] = table_rows
        #
        # return {
        #     'table_rows':table_rows,
        #     'total_payoff':round(total_payoff),
        # }

# class survey(Page):
#
#     form_model = 'player'
#     form_fields = ['age']


page_sequence = [
    start,
    task,
    ResultsWaitPage,
    Results
    # survey
]
