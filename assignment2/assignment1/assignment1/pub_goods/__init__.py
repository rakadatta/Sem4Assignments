from otree.api import BaseConstants, BaseGroup, BasePlayer, BaseSubsession
from otree.api import Currency as c
from otree.api import Page, WaitPage, currency_range, models, widgets

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = "my_pub_goods"
    players_per_group = 3
    num_rounds = 3
    MPCR1 = 3
    MPCR2 = 5
    MPCR3 = 10
    endowment = 100
    instructions_template = "my_pub_goods/instructions.html"


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    MPCR = models.FloatField()


class Player(BasePlayer):
    contribution = models.IntegerField(
        min=0, max=Constants.endowment, label="How much are you willing to contribute?"
    )


# FUNCTIONS


def creating_session(subsession: Subsession):
    # Establish a total earnings variable for each participant and
    # initialize to 0 at beginning of session.
    for p in subsession.get_players():
        if subsession.round_number == 1:
            p.participant.vars["totalEarnings"] = 0

    # Assign varying MPCR (first half of periods one value
    # and second half of periods another).

    for g in subsession.get_groups():
        if subsession.round_number == 1:  # in first half
            g.MPCR = Constants.MPCR1
        elif subsession.round_number == 2:  # in first half
            g.MPCR = Constants.MPCR2
        else:  # second half
            g.MPCR = Constants.MPCR3


def setPayoffs(g: Group):
    # First we need to calculate the total contributed by all group members
    total_contribution = 0
    for p in g.get_players():
        total_contribution += p.contribution
    # Second we need to calculate the earnings for each group member
    for p in g.get_players():
        #  print("payoff ", p.participant.payoff)
        #  print("endowment ", Constants.endowment)
        #  print("contribution ", p.contribution)
        #  print("total contribution ", total_contribution)
        #  print("MPCR ", g.MPCR)
        p.participant.payoff = float(
            Constants.endowment - p.contribution + total_contribution * g.MPCR
        )
        p.participant.vars["totalEarnings"] += p.participant.payoff


# PAGES
class Introduction(Page):
    pass


class Action(Page):
    form_model = "player"
    form_fields = ["contribution"]


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = "setPayoffs"
    body_text = "Please wait for everyone to make decisions."


class Results(Page):
    pass


page_sequence = [Introduction, Action, ResultsWaitPage, Results]
