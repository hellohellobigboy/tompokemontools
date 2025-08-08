import pandas as pd
from bs4 import BeautifulSoup
import os

lengths = []
turn_data = []
TOTAL_HEALTH = 341

def eval_health(line):
    nums = line.split('|')[-1].strip().split(r'\/')
    if nums[-1] == '100':
        return round(int(nums[0]) * 0.01 * TOTAL_HEALTH)
    else:
        return nums[0]

def parse_battle(html):

    soup = BeautifulSoup(html, 'html.parser')
    script_tag = soup.find('script', {'class': 'battle-log-data'})
    log_text = script_tag.string.strip() if script_tag else ""
    timestamps = []

    current_turn = 0

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
                'P1 Action': 'no action',
                'P2 Start Pokemon': current['p2startmon'],
                'P2 Start Health': current['p2starthealth'],
                'P2 End Pokemon': current['p2startmon'],
                'P2 End Health': current['p2starthealth'],
                'P2 Action': 'no action'
            }

        elif '|switch|' in line:
            pokemon = line.split('|')[2].split(':')[1]
            new_health = eval_health(line)
            if 'p2a' in line:
               current['p2startmon'] = pokemon
               current['p2starthealth'] = new_health

               single_turn['P2 Action'] = f'switch {pokemon}'
               single_turn['P2 End Pokemon'] = pokemon
               single_turn['P2 End Health'] = new_health

            else:
                current['p1startmon'] = pokemon
                current['p1starthealth'] = new_health

                single_turn['P1 Action'] = f'switch {pokemon}'
                single_turn['P1 End Pokemon'] = pokemon
                single_turn['P1 End Health'] = eval_health(line)


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

        elif '|t:|' in line:
            split_line = line.split('|')
            timestamps.append(int(split_line[2]))


    if single_turn:
        turn_data.append(single_turn)

    df = pd.DataFrame(turn_data)
    length = timestamps[-1] - timestamps[0] if timestamps else 0
    return df, length

# folder_path = input('folder path please: ')
folder_path = '/Users/clintonnguyen/Downloads/battles'

for filename in os.listdir(folder_path):
    filepath = os.path.join(folder_path, filename)

    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        html = f.read()

    df, battle_length = parse_battle(html)
    df.to_excel('battle_log.xlsx', index=False)
    print(f'Finished! {filename} took: {battle_length} seconds')
    lengths.append(abs(battle_length))









