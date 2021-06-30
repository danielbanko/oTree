
from otree.api import *

c = Currency

author = "Daniel Banko (daniel.bankoferran@gmail.com)"
doc = """
Code for SYP
"""


class Constants(BaseConstants):
    name_in_url = 'syp_v1'
    # players_per_group = 10 #used for actual trials
    players_per_group = None #testing purposes
    num_rounds = 1


class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass


class Player(BasePlayer):
    rank = models.IntegerField()
    treatment_group = models.StringField()
    num_key_pairs = models.IntegerField()

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
    import itertools
    treatment_groups = itertools.cycle(['NC', 'PC', 'FC'])
    if subsession.round_number == 1:
        for player in subsession.get_players():
            # randomize to treatments
            player.treatment_group = next(treatment_groups)
            print('set treatment_group to', player.treatment_group)



# ------------------------------------------
# PAGES
class start(Page):

    # def is_displayed(self):
    #     return self.round_number == 1

    @staticmethod
    def vars_for_template(player):
        return dict(
            treatment_group = player.treatment_group,
        )


class task(Page):

    form_model = 'player'
    form_fields = ['num_key_pairs']
    timeout_seconds = 120


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
        print(*performance_ranking)
        print(*performance_sorted_by_ranking)
        for p in subsession.get_players():
            p.rank = performance_sorted_by_ranking.index([p.id_in_group,p.num_key_pairs]) + 1


class Results(Page):
    pass
    @staticmethod
    def vars_for_template(player):
        return dict(
            rank=player.rank
        )





page_sequence = [
    start,
    task,
    ResultsWaitPage,
    Results
]
