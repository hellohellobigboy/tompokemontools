from tomagents import domrandom, dom0, dom1, dom2
import random

state = {'p1_action': 'move normalattack', 'p1_start_health': 0, 'p1_end_health': 100, 'p1_start_pokemon': 'Blastoise', 'p1_end_pokemon': 'Charizard',
         'p2_action': 'move normalattack', 'p2_start_health': 0, 'p2_end_health': 100, 'p2_start_pokemon': 'Venusaur', 'p2_end_pokemon': 'Venusaur'}

p1_team = {'Venusaur': 100, 'Charizard': 100, 'Blastoise': 100}
p2_team = {'Venusaur': 100, 'Charizard': 100, 'Blastoise': 100}

p1_prev_health = 100
p2_prev_health = 100

# player1 = dom0(1)
# player2 = dom1(2)

player1 = dom1(1)
player2 = dom2(2, player1)

def compute_damage(move, user, target):
    stab = (user == 'Charizard' and move == 'fireattack') or (user == 'Venusaur' and move == 'grassattack') or (user == 'Blastoise' and move == 'waterattack')
    super_effective = (target == 'Charizard' and move == 'waterattack') or (target == 'Venusaur' and move == 'fireattack') or (target == 'Blastoise' and move == 'grassattack')
    damage = 16

    if stab:
        damage *= 1.5
    if super_effective:
        damage *= 2

    return damage

def perform_move(player, key, action):
    if action == 'move':
        p = 'p1' if player == 1 else 'p2'
        opp = 'p2' if player == 1 else 'p1'
        team = p2_team if player == 1 else p1_team

        move = key
        user = state[f'{p}_start_pokemon']
        target = state[f'{opp}_end_pokemon']
        opponent_new_health = team[target] - compute_damage(move, user, target)
        state[f'{opp}_end_health'] = opponent_new_health
        team[target] = opponent_new_health

def perform_switch(player, key):
    p = 'p1' if player == 1 else 'p2'
    team = p2_team if player == 1 else p1_team

    state[f'{p}_end_pokemon'] = key
    state[f'{p}_end_health'] = team[key]



while True:
    player1_choice = player1.choose_move(state)
    player2_choice = player2.choose_move(state)

    state['p1_action'] = player1_choice
    state['p2_action'] = player2_choice

    # update game state
    # {'p1_action': 'move normalattack', 'p1_start_health': 0, 'p1_end_health': 0, 'p1_start_pokemon': 'Venusaur', 'p1_end_pokemon': 'Venusaur',
    #  'p2_action': 'move normalattack', 'p2_start_health': 0, 'p2_end_health': 0, 'p2_start_pokemon': 'Venusaur', 'p2_end_pokemon': 'Venusaur'}

    # 2 moves: coin flip for turn order
    # switching will always go through
    # move: update end health
    # switch: update end health and end pokemon
    # keep updating until we get lose

    p1_team = player1.get_health()
    p2_team = player2.get_health()
    print(p1_team)
    print(p2_team)

    player1_choice_split = player1_choice.split(' ')
    player2_choice_split = player2_choice.split(' ')

    p1_action_type = player1_choice_split[0] # move/switch/lose
    p2_action_type = player2_choice_split[0]

    p1_key = player1_choice_split[1] if len(player1_choice_split) > 1 else ''
    p2_key = player2_choice_split[1] if len(player2_choice_split) > 1 else ''

    state['p1_start_health'] = p1_prev_health
    state['p2_start_health'] = p2_prev_health

    if p1_action_type == 'lose' or p2_action_type == 'lose':
        break

    if p1_action_type == 'switch':
        # essentially change p2 end pokemon
        # state['p1_end_pokemon'] = p1_key
        # state['p1_end_health'] = p1_team[p1_key]
        perform_switch(1, p1_key)
    if p2_action_type == 'switch':
        # state['p2_end_pokemon'] = p2_key
        # state['p2_end_health'] = p2_team[p2_key]
        perform_switch(2, p2_key)


    first = random.randint(1,2)
    if first == 1 and p1_action_type == 'move':
        perform_move(1, p1_key, p1_action_type)
        target = state['p2_end_pokemon']
        if p2_team[target] > 0:
            perform_move(2, p2_key, p2_action_type)
        else:
            new_pokemon = player2.choose_move(state).split(' ')
            if len(new_pokemon) > 1:
                perform_switch(1, new_pokemon[1])
            else:
                break

    elif p2_action_type == 'move':
        perform_move(2, p2_key, p2_action_type)
        target = state['p1_end_pokemon']
        if p1_team[target] > 0:
            perform_move(1, p1_key, p1_action_type)
        else:
            new_pokemon = player1.choose_move(state).split(' ')
            if len(new_pokemon) > 1:
                perform_switch(2, new_pokemon[1])
            else:
                break



    # update the game states and health values
    print(state)
    state['p1_start_pokemon'] = state['p1_end_pokemon']
    state['p2_start_pokemon'] = state['p2_end_pokemon']
    p1_prev_health = state['p1_end_health']
    p2_prev_health = state['p2_end_health']


print(p1_team)
print(p2_team)







