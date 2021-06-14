from otree.api import *
import time

c = Currency

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'syp_v1'
    players_per_group = None
    num_rounds = 1
    task_timer = 120
    num_rounds = 100 # must be more than the max one person can do in task_timer seconds

    INTS_T1 = [
        [90, 95],
        [14, 19],
        [35, 50],
        [30, 29],
        [34, 31],
        [78, 82],
        [60, 27],
        [38, 70],
        [85, 19],
        [89, 26],
        [19, 18],
        [64, 83],
        [32, 99],
        [14, 17],
        [51, 60]]


class Subsession(BaseSubsession):
    # def before_session_starts(subsession):

    def creating_sesssion(subsession): #TODO: FIGURE OUT WHY CODE IN CREATING_SESSION IS NOT RUNNING
        print('test')

        if 'task_timer' in subsession.session.config:
            task_timer = subsession.session.config['task_timer']
        else:
            task_timer = Constants.task_timer
            print('test')

        for p in subsession.get_players():
            p.task_timer = task_timer
            p.int1 = Constants.INTS_T1[subsession.round_number - 1][0]
            print('p is', p)
            print('p.int1 is', p.int1)
            p.int2 = Constants.INTS_T1[subsession.round_number - 1][1]
            p.solution = p.int1+p.int2



class Group(BaseGroup):
    pass


class Player(BasePlayer):

    def score_round(self):
        # update player payoffs
        if (self.solution == self.user_total):
            self.is_correct = True
            self.payoff_score = 1
        else:
            self.is_correct = False
            self.payoff_score = 0


    task_timer = models.PositiveIntegerField( doc = "The length of the real effort task timer.", initial = 0)

    int1 = models.PositiveIntegerField( doc ="This round's first int", initial = 0)

    int2 = models.PositiveIntegerField( doc = "This round's second int", initial = 0)

    solution = models.PositiveIntegerField( doc = "This round's correct summation", initial = 0)

    user_total = models.PositiveIntegerField(
        min = 1,
        max = 9999,
        doc = "user's summation")
        #widget = widgets.TextInput(attrs={'autocomplete':'off'}))

    is_correct = models.BooleanField( doc= "did the user get the task correct?" , initial = 0)

    payoff_score = models.FloatField( doc = '''score in this task''', initial = 0)


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
    form_fields = ['user_total']

    # def get_timeout_seconds(self):
    #     return self.participant.vars['expiry_timestamp'] - time.time()
    #
    # def is_displayed(self):
    #     return self.participant.vars['expiry_timestamp'] - time.time() > 3

    def vars_for_template(self):

        # current number of correctly done tasks
        total_payoff = 0
        for p in self.in_all_rounds():
            if p.payoff_score != None:
                total_payoff += p.payoff_score

        # set up messages in calculation task
        if self.round_number == 1:
            correct_last_round = "<br>"
        else:
            if self.player.in_previous_rounds()[-1].is_correct:
                correct_last_round = "Your last sum was <font color='green'>correct</font>"
            else:
                correct_last_round = "Your last sum was <font color='red'>incorrect</font>"

        return {
            'int1': self.int1,
            'total_payoff': round(total_payoff),
            'round_count':(self.round_number - 1),
            # 'debug': settings.DEBUG,
            'correct_last_round': correct_last_round,
        }

    def before_next_page(self):
        self.player.score_round()


class ResultsWaitPage(WaitPage):

    def is_displayed(self):
        return self.round_number == Constants.num_rounds
    def after_all_players_arrive(self):
        pass


class Results(Page):

    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):

        total_payoff = 0
        for p in self.player.in_all_rounds():
            if p.payoff_score != None:
                total_payoff += p.payoff_score

        self.participant.vars['task_1_score'] = total_payoff

        # only keep obs if YourEntry player_sum, is not None.
        table_rows = []
        for prev_player in self.player.in_all_rounds():
            if (prev_player.user_total != None):
                if (prev_player.user_total > 0):
                    row = {
                        'round_number': prev_player.round_number,
                        'int1': prev_player.int1,
                        'int2': prev_player.int2,
                        'Ints_sum': prev_player.solution,
                        'player_sum': round(prev_player.user_total),
                        'is_correct': prev_player.is_correct,
                        'payoff': round(prev_player.payoff_score),
                    }
                    table_rows.append(row)

        self.participant.vars['t1_results'] = table_rows

        return {
            'table_rows':table_rows,
            'total_payoff':round(total_payoff),
        }



page_sequence = [start, task, ResultsWaitPage, Results]
