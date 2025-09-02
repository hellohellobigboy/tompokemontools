import random

advantage = {'Charizard': 'Venusaur', 'Venusaur': 'Blastoise', 'Blastoise': 'Charizard'}
disadvantage = {'Charizard': 'Blastoise', 'Venusaur': 'Charizard', 'Blastoise': 'Venusaur'}

moves = {'Charizard': ['move normalattack', 'move fireattack', 'move grassattack', 'switch Venusaur', 'switch Blastoise'],
         'Venusaur': ['normalattack', 'move grassattack', 'move waterattack', 'switch Blastoise', 'switch Charizard'],
         'Blastoise': ['move normalattack', 'move waterattack', 'move fireattack','switch Charizard', 'switch Venusaur']}

p1_health = {'Charizard': 100, 'Venusaur': 100, 'Blastoise': 100}
p2_health = {'Charizard': 100, 'Venusaur': 100, 'Blastoise': 100}

startinggamestate = {'p1_action': 'move normalattack', 'p1_start_health': 0, 'p1_end_health': 0, 'p1_start_pokemon': 'Venusaur',
                    'p2_action': 'move normalattack', 'p2_start_health': 0, 'p2_end_health': 0, 'p2_start_pokemon': 'Venusaur'}


# dom(-1) random move
class domrandom:
    def __init__(self, player):
        self.player = player
        self.health = {'Charizard': 100, 'Venusaur': 100, 'Blastoise': 100}
    def choose_move(self, game_state):
        ally = f'p{self.player}_pokemon'
        return random.choice(moves[game_state[ally]])

# dom(0) reactive based on what they see
class dom0:
    def __init__(self, player):
        self.player = player
        self.health = {'Charizard': 100, 'Venusaur': 100, 'Blastoise': 100}
    def get_health(self):
        return self.health
    def choose_move(self, game_state):
        ally = game_state['p1_start_pokemon'] if self.player == 1 else game_state['p2_start_pokemon']
        opponent = game_state['p2_start_pokemon'] if self.player == 1 else game_state['p1_start_pokemon']
        # health = p1_health if self.player == 1 else p2_health
        health = self.health
        current = ally

        # faint handling
        if health[current] <= 0:
            if health[advantage[opponent]] > 0:
                return f'switch {advantage[opponent]}' # advantage switch
            elif health[opponent] > 0:
                return f'switch {opponent}' # same pokemon switch
            elif health[disadvantage[opponent]] > 0:
                return f'switch {disadvantage[opponent]}' # you got no one left
            else:
                return 'lose'

        if advantage[ally] == opponent:
            return moves[ally][1] # stab super effective move
        elif disadvantage[ally] == opponent:
            return moves[ally][2] # alternate super effective move
        else: # both players have same type on the field
            return 'move normalattack'


# dom(1) predict super effective move so we switch (tentative)
class dom1:
    def __init__(self, player):
        self.player = player
        # self.minus = minus
        self.health = {'Charizard': 100, 'Venusaur': 100, 'Blastoise': 100}
    def get_health(self):
        return self.health
    def choose_move(self, game_state):
        ally = game_state['p1_start_pokemon'] if self.player == 1 else game_state['p2_start_pokemon']
        opponent = game_state['p2_start_pokemon'] if self.player == 1 else game_state['p1_start_pokemon']
        # health = p1_health if self.player == 1 else p2_health
        health = self.health
        # predicted = self.minus.choose_move(game_state)

        current = ally

        # faint handling
        if health[current] <= 0:
            if health[advantage[opponent]] > 0:
                return f'switch {advantage[opponent]}'  # advantage switch
            elif health[opponent] > 0:
                return f'switch {opponent}'  # same pokemon switch
            elif health[disadvantage[opponent]] > 0:
                return f'switch {disadvantage[opponent]}'  # you got no one left
            else:
                return 'lose' # everyone is dead

        if advantage[ally] == opponent:
            return moves[ally][1] # super effective move
        else:
            intended_switch = disadvantage[opponent]
            if health[intended_switch] > 0:
                return f'switch {intended_switch}' # switch to advantage
            elif health[opponent] > 0:
                return f'switch {opponent}' # if we don't have advantage to switch to then switch to same
            elif ally == opponent:
                return moves[ally][0] # same pokemon on the field normal attack
            else:
                return moves[ally][2] # desperate


# dom(2) predict a switch so we use our alternative super effective move
class dom2:
    def __init__(self, player, minus):
        self.player = player
        self.minus = minus
        self.dangerous = False
        self.health = {'Charizard': 100, 'Venusaur': 100, 'Blastoise': 100}
    def get_health(self):
        return self.health
    def choose_move(self, game_state):
        ally = game_state['p1_start_pokemon'] if self.player == 1 else game_state['p2_start_pokemon']
        opponent = game_state['p2_start_pokemon'] if self.player == 1 else game_state['p1_start_pokemon']
        ally_health = self.health
        opponent_health = self.minus.get_health()
        # predicted = self.minus.choose_move(game_state)

        current = ally

        # faint handling
        if ally_health[current] <= 0:
            if ally_health[advantage[opponent]] > 0:
                return f'switch {advantage[opponent]}'  # advantage switch
            elif ally_health[opponent] > 0:
                return f'switch {opponent}'  # same pokemon switch
            elif ally_health[disadvantage[opponent]] > 0:
                return f'switch {disadvantage[opponent]}'  # you got no one left
            else:
                return 'lose'

        # if opponent doesn't have advantage, they will switch
        if advantage[opponent] != ally and not self.dangerous:
            self.dangerous = True
            return moves[ally][2]
        elif len([hp for hp in opponent_health.values() if hp > 0]) == 1: # opponent on their last pokemon
            if current == disadvantage[opponent]: # if we're already at advantage just blast them
                return moves[ally][1]
            else: # otherwise switch for advantage
                return f'switch {disadvantage[opponent]}'
        else: # otherwise bait their switch
            self.dangerous = False
            return moves[ally][3]

