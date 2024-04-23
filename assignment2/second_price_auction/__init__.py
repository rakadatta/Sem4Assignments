from otree.api import *


doc = """
In a common value auction game, players simultaneously bid on the item being
auctioned.<br/>
Prior to bidding, they are given an estimate of the actual value of the item.
This actual value is revealed after the bidding.<br/>
Bids are private. The player with the highest bid wins the auction, but
payoff depends on the bid amount and the actual value.<br/>
"""


class C(BaseConstants):
    NAME_IN_URL = 'common_value_auction'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    BID_MIN = cu(0)
    BID_MAX = cu(25)
    # Error margin for the value estimates shown to the players
    BID_NOISE = cu(1.5)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    item_value = models.CurrencyField(
        doc="""Common value of the item to be auctioned, random for treatment"""
    )
    highest_bid = models.CurrencyField()
    highest_bid_name=models.StringField()


class Player(BasePlayer):
    item_value_estimate = models.CurrencyField(
        doc="""Estimate of the common value, may be different for each player"""
    )
    player_name = models.StringField(label="Name")
    player_age = models.IntegerField(min=18, max=100, label="Age")
    bid_amount = models.CurrencyField(
        min=C.BID_MIN,
        max=C.BID_MAX,
        doc="""Amount bid by the player""",
        label="Bid amount",
    )

    is_winner = models.BooleanField(
        initial=False, doc="""Indicates whether the player is the winner""",
        choices=[
            [False, 'You did not win'],
            [True, 'You won!'],
        ]
    )


# FUNCTIONS
def creating_session(subsession: Subsession):
    for g in subsession.get_groups():
        import random

        item_value = random.uniform(C.BID_MIN, C.BID_MAX)
        g.item_value = round(item_value, 1)


def set_winner(group: Group):
    import random

    players = group.get_players()
    group.highest_bid = max([p.bid_amount for p in players])
    players_with_highest_bid = [p for p in players if p.bid_amount == group.highest_bid]
    winner = random.choice(
        players_with_highest_bid
    )  # if tie, winner is chosen at random
    winner.is_winner = True
    for p in players:
        set_payoff(p)


def generate_value_estimate(group: Group):
    import random

    estimate = group.item_value + random.uniform(-C.BID_NOISE, C.BID_NOISE)
    estimate = round(estimate, 1)
    if estimate < C.BID_MIN:
        estimate = C.BID_MIN
    if estimate > C.BID_MAX:
        estimate = C.BID_MAX
    return estimate


def set_payoff(player: Player):
    group = player.group
    players=group.get_players()

    if player.is_winner:
        # List of bids
        list1 = [p.bid_amount for p in players]
        # Removing duplicates from the list
        list2 = list(set(list1))
        # Sorting the  list
        list2.sort()
        if len(list2)>1:
            second_highest_bid=list2[-2]
        else:
            second_highest_bid=list2[0]

        player.payoff = group.item_value - second_highest_bid

    else:
        player.payoff = 0


# PAGES
class Introduction(Page):
    form_model = 'player'
    form_fields = ["player_name", "player_age"]
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        group = player.group

        player.item_value_estimate = generate_value_estimate(group)


class Bid(Page):
    form_model = 'player'
    form_fields = ['bid_amount']


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_winner


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        group = player.group

        return dict(is_greedy=group.item_value - player.bid_amount < 0)


page_sequence = [Introduction, Bid, ResultsWaitPage, Results]
