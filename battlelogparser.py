import pandas as pd
from bs4 import BeautifulSoup
import openpyxl

log_file = input("name of log file: ")
with open(log_file, "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')
script_tag = soup.find('script', {'class':'battle-log-data'})
log_text = script_tag.string.strip() if script_tag else ""

turn_data = []
current_turn = 0
TOTAL_HEALTH = 341

def eval_health(line):
    nums = line.split('|')[-1].strip().split(r'\/')
    if nums[-1] == '100':
        return round(int(nums[0]) * 0.01 * TOTAL_HEALTH)
    else:
        return nums[0]

current = {
        'p1startmon': '',
        'p1starthealth': 0,
        'p2startmon': '',
        'p2starthealth': 0
}

single_turn = {
            'Turn': current_turn,
            'P1 Start Pokemon': current['p1startmon'],
            'P1 Start Health': current['p1starthealth'],
            'P1 End Pokemon': "",
            'P1 End Health': "",
            'P1 Action': '',
            'P2 Start Pokemon': current['p2startmon'],
            'P2 Start Health': current['p2starthealth'],
            'P2 End Pokemon': "",
            'P2 End Health': "",
            'P2 Action': ''
}

for line in log_text.splitlines():

    if '|turn|' in line:
        turn_data.append(single_turn)
        current_turn = int(line.split('|turn|')[1])
        single_turn = {
            'Turn': current_turn,
            'P1 Start Pokemon': current['p1startmon'],
            'P1 Start Health': current['p1starthealth'],
            'P1 End Pokemon': current['p1startmon'],
            'P1 End Health': current['p1starthealth'],
            'P1 Action': '',
            'P2 Start Pokemon': current['p2startmon'],
            'P2 Start Health': current['p2starthealth'],
            'P2 End Pokemon': current['p2startmon'],
            'P2 End Health': current['p2starthealth'],
            'P2 Action': ''
        }

    if '|switch|' in line:
        pokemon = line.split('|')[2].split(':')[1]

        if 'p2a' in line:
           single_turn['P2 Action'] = f'switch {pokemon}'
           single_turn['P2 End Pokemon'] = pokemon
           current['p2startmon'] = single_turn['P2 End Pokemon']
           single_turn['P2 End Health'] = eval_health(line)
           current['p2starthealth'] = single_turn['P2 End Health']

        else:
            single_turn['P1 Action'] = f'switch {pokemon}'
            single_turn['P1 End Pokemon'] = pokemon
            current['p1startmon'] = single_turn['P1 End Pokemon']
            single_turn['P1 End Health'] = eval_health(line)
            current['p1starthealth'] = single_turn['P1 End Health']


    elif '|-damage|' in line:
        if 'p2a' in line:
            single_turn['P2 End Health'] = eval_health(line)
            current['p2starthealth'] = single_turn['P2 End Health']
        else:
            single_turn['P1 End Health'] = eval_health(line)
            current['p1starthealth'] = single_turn['P1 End Health']

    elif '|move|' in line:
        split_line = line.split('|')
        mover = split_line[2].split(':')[0]
        move = split_line[3]
        if mover == 'p2a':
            single_turn['P2 Action'] = move
        else:
            single_turn['P1 Action'] = move

if single_turn:
    turn_data.append(single_turn)

df = pd.DataFrame(turn_data)
df.to_excel('battle_log.xlsx', index=False)
print('Finished!')



    # previous turn's end becomes next turn's start - handled
    # move: changes ACTION - handled
    # switch: changes END POKEMON and ACTION - handled
    # -damage: changes END HEALTH - handled
    # when do we want to write to spreadsheet? - handled
        # probably when we see the next turn

