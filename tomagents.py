import random

advantage = {'Charizard': 'Venusaur', 'Venusaur': 'Blastoise', 'Blastoise': 'Charizard'}
disadvantage = {'Charizard': 'Blastoise', 'Venusaur': 'Charizard', 'Blastoise': 'Venusaur'}

moves = {'Charizard': ['normalattack', 'fireattack', 'grassattack', 'switch Venusaur', 'switch Blastoise'],
         'Venusaur': ['normalattack', 'grassattack', 'waterattack','switch Blastoise', 'switch Charizard'],
         'Blastoise': ['normalattack', 'grassattack', 'fireattack','switch Charizard', 'switch Venusaur']}

p1_health = {'Charizard': 100, 'Venusaur': 100, 'Blastoise': 100}
p2_health = {'Charizard': 100, 'Venusaur': 100, 'Blastoise': 100}

startinggamestate = {'p1_action': 'move normalattack', 'p1_start_health': 0, 'p1_end_health': 0, 'p1_pokemon': 'Venusaur',
                    'p2_action': 'move normalattack', 'p2_start_health': 0, 'p2_end_health': 0, 'p2_pokemon': 'Venusaur'}


# dom(-1) random move
class domrandom:
    def __init__(self, player):
        self.player = player
    def choose_move(self, game_state):
        ally = f'p{self.player}_pokemon'
        return random.choice(moves[game_state[ally]])

# dom(0) reactive based on what they see
class dom0:
    def __init__(self, player):
        self.player = player
    def choose_move(self, game_state):
        ally = 'p1_pokemon' if self.player == 1 else 'p2_pokemon'
        opponent = 'p2_pokemon' if self.player == 1 else 'p1_pokemon'
        health = p1_health if self.player == 1 else p2_health

        current = game_state[ally]

        # faint handling
        if health[current] <= 0:
            if health[advantage[game_state[opponent]]] > 0:
                return f'switch {advantage[game_state[opponent]]}' # advantage switch
            elif health[game_state[opponent]] > 0:
                return f'switch {game_state[opponent]}' # same pokemon switch
            else:
                return f'switch {disadvantage[game_state[opponent]]}' # you got no one left

        if advantage[game_state[ally]] == game_state[opponent]:
            return moves[ally][1] # stab super effective move
        elif disadvantage[game_state[ally]] == game_state[opponent]:
            return moves[ally][2] # alternate super effective move
        else: # both players have same type on the field
            intended_switch = moves[ally][4].split()[1]
            if health[intended_switch] > 0:
                return moves[ally][4] # advantageous switch
            else:
                return 'normalattack'


# dom(1) predict super effective move so we switch (tentative)
class dom1:
    def __init__(self, player, minus):
        self.player = player
        self.minus = minus
    def choose_move(self, game_state):
        ally = 'p1_pokemon' if self.player == 1 else 'p2_pokemon'
        opponent = 'p2_pokemon' if self.player == 1 else 'p1_pokemon'
        health = p1_health if self.player == 1 else p2_health
        predicted = self.minus.choose_move(game_state)

        current = game_state[ally]

        # faint handling
        if health[current] <= 0:
            if health[advantage[game_state[opponent]]] > 0:
                return f'switch {advantage[game_state[opponent]]}'  # advantage switch
            elif health[game_state[opponent]] > 0:
                return f'switch {game_state[opponent]}'  # same pokemon switch
            else:
                return f'switch {disadvantage[game_state[opponent]]}'  # you got no one left

        if advantage[game_state[ally]] == game_state[opponent]:
            return moves[ally][1] # super effective move
        else:
            intended_switch = advantage[game_state[opponent]]
            if health[intended_switch] > 0:
                return f'switch {intended_switch}' # switch to advantage
            elif health[game_state[opponent]] > 0:
                return f'switch {game_state[opponent]}' # if we don't have advantage to switch to then switch to same
            elif game_state[ally] == game_state[opponent]:
                return moves[ally][0] # same pokemon on the field
            else:
                return moves[ally][2] # desperate


# dom(2) predict a switch so we use our alternative super effective move
class dom2:
    def __init__(self, player, minus):
        self.player = player
        self.minus = minus
        self.dangerous = False
    def choose_move(self, game_state):
        ally = 'p1_pokemon' if self.player == 1 else 'p2_pokemon'
        opponent = 'p2_pokemon' if self.player == 1 else 'p1_pokemon'
        ally_health = p1_health if self.player == 1 else p2_health
        opponent_health = p2_health if self.player == 1 else p1_health
        predicted = self.minus.choose_move(game_state)

        current = game_state[ally]

        # faint handling
        if ally_health[current] <= 0:
            if ally_health[advantage[game_state[opponent]]] > 0:
                return f'switch {advantage[game_state[opponent]]}'  # advantage switch
            elif ally_health[game_state[opponent]] > 0:
                return f'switch {game_state[opponent]}'  # same pokemon switch
            else:
                return f'switch {disadvantage[game_state[opponent]]}'  # you got no one left

        # if opponent doesn't have advantage, they will switch
        if advantage[game_state[opponent]] != game_state[ally] and not self.dangerous:
            self.dangerous = True
            return moves[ally][2]
        elif len([hp for hp in opponent_health.values() if hp > 0]) == 1: # opponent on their last pokemon
            if current == disadvantage[game_state[opponent]]: # if we're already at advantage just blast them
                return moves[ally][1]
            else: # otherwise switch for advantage
                return f'switch {disadvantage[game_state[opponent]]}'
        else: # otherwise bait their switch
            self.dangerous = False
            return moves[ally][3]

