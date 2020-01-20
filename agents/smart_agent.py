import random
from agents.base_agent import Agent
from combinatoric_tools.tools import choose_from_string, all_hands
from combinatoric_tools.tools import get_secret_options, get_burn_options, get_gift_options, get_comp_options

CARD_DECK_SETUP = 'AABBCCDDDEEEFFFFGGGGG'


class SmartAgent(Agent):
    def __init__(self, name='SmartAgent __'):
        super().__init__(name)
        self.turn_counter = 1
        self.option_mapping = {'secret': get_secret_options,
                               'burn': get_burn_options,
                               'gift': get_gift_options,
                               'comp': get_comp_options}

        self.opponent_actions_done = []
        self.opponent_cards_played = []

    def secret(self, opponent):
        card_chosen, self.hand = choose_from_string(string=self.hand, n=1)
        self.cards_placed += card_chosen

    def burn(self, opponent):
        cards_chosen, self.hand = choose_from_string(string=self.hand, n=2)

    def gift(self, opponent):
        cards_chosen, self.hand = choose_from_string(string=self.hand, n=3)
        self.cards_placed += opponent.receive_gift(cards_chosen)

    def comp(self, opponent):
        cards_chosen, self.hand = choose_from_string(string=self.hand, n=4)
        bundle_1, bundle_2 = choose_from_string(cards_chosen, n=2)
        self.cards_placed += opponent.receive_comp([bundle_1, bundle_2])

    def receive_gift(self, triplet):
        card_chosen, cards_discarded = choose_from_string(triplet, 1)
        self.cards_placed += card_chosen
        return cards_discarded

    def receive_comp(self, bundles):
        ch_idx = random.choice([0, 1])
        if ch_idx == 0:
            self.cards_placed += bundles[0]
            return bundles[1]
        else:
            self.cards_placed += bundles[1]
            return bundles[0]

    def turn(self, deck, opponent):
        # Pull a card:
        self.hand += deck.pull_card()

        # Calculate the options this agent has for this turn:
        # self.own_options()

        # Calculate enemy options:
        # self.enemy_options(opponent)

        # Choose the action randomly for now:
        action_key = random.choice(list(self.actions.keys()))

        # Do the action:
        self.actions[action_key](opponent=opponent)

        # Remove the action from the options:
        self.actions.pop(action_key)

    def enemy_options(self, opponent):
        # Original deck:
        deck_remaining = CARD_DECK_SETUP

        # Remove cards that are in the hand:
        for card in self.hand:
            deck_remaining = deck_remaining.replace(card, '', 1)

        # Remove cards that the AI has placed on the table:
        for card in self.cards_placed:
            deck_remaining = deck_remaining.replace(card, '', 1)

        # Remove cards that the opponent has placed on the table:
        for card in opponent.cards_placed:
            deck_remaining = deck_remaining.replace(card, '', 1)

        # All possible hands that the opponent can have:
        opponent_hands = all_hands(deck=deck_remaining, n=len(opponent.hand)+1)

        print(f'Possible opponent hands: {len(opponent_hands)} \n\n')
        N_op_total = 0
        for op_hand in opponent_hands:
            # print(f'Opponent cards: {op_hand} \n')

            N_choices = 0
            for action_key in opponent.actions.keys():
                options = self.option_mapping[action_key](cards_in_hand=op_hand)
                # print(options)

                if type(options) is list:
                    N_choices += sum([len(i) for i in options])
                else:
                    N_choices += len(options)

            # print(f'\nNumber of choices opponent has for this hand: {N_choices} \n_________________________')
            N_op_total += N_choices

        print(f'\n\nOpponent total options: {N_op_total}\n__________________________')

    def own_options(self):
        print(f'Cards in my hand: {self.hand} \n')

        N_choices = 0
        for action_key in self.actions.keys():
            options = self.option_mapping[action_key](cards_in_hand=self.hand)
            print(options)

            if type(options) is list:
                N_choices += sum([len(i) for i in options])
            else:
                N_choices += len(options)

        print(f'\nNumber of choices I have is: {N_choices} \n_________________________')

    def receive_info(self, action_key, cards_played):
        self.opponent_actions_done.append(action_key)
        self.opponent_cards_played.append(cards_played)