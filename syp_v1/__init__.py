
from otree.api import *

c = Currency

author = "Daniel Banko (daniel.bankoferran@gmail.com)"
doc = """
Code for SYP
"""


class Constants(BaseConstants):
    name_in_url = 'syp_v1'
    players_per_group = 2
    num_rounds = 2

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass


class Player(BasePlayer):
    rank = models.IntegerField()
    treatment_group = models.StringField()
    num_key_pairs = models.IntegerField()
    practice_round = models.BooleanField(default = 0)
    is_top20 = models.BooleanField()
    is_top50 = models.BooleanField()
    is_bottom50 = models.BooleanField()
    information_display = models.BooleanField(default = 0)

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
            # player.treatment_group = next(treatment_groups)
            player.treatment_group = 'FC' #for testing purposes TODO GET RID OF THIS WHEN DONE
            print('set treatment_group to', player.treatment_group)



# ------------------------------------------
# PAGES
class start(Page):

    def is_displayed(self):
        return self.round_number == 1

    @staticmethod
    def vars_for_template(player):
        return dict(
            treatment_group = player.treatment_group,
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

class start_practice_2(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1

class task(Page):
    form_model = 'player'
    form_fields = ['num_key_pairs']
    timeout_seconds = 120

class practice_task(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1

    form_model = 'player'
    form_fields = ['num_key_pairs']
    timeout_seconds = 30

class demonstration(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1

class FC_choose_group(Page):
    @staticmethod
    def is_displayed(player):
        return player.treatment_group == "FC"
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
        print(*performance_ranking)
        print(*performance_sorted_by_ranking)
        for p in subsession.get_players():
            p.rank = performance_sorted_by_ranking.index([p.id_in_group,p.num_key_pairs]) + 1
            percentile = (p.rank / Constants.players_per_group)*100
            p.is_top20 = 1 if percentile <= 20 else 0
            p.is_top50 = 1 if (20 <= percentile < 50) else 0
            p.is_bottom50 = 1 if percentile >= 50 else 0



class Results(Page):
    pass
    @staticmethod
    def vars_for_template(player):
        return dict(
            rank=player.rank,
            treatment_group = player.treatment_group
        )

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
