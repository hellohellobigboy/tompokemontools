import pandas as pd
import matplotlib.pyplot as plt

# dataframe set up and cleaning
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

df = pd.read_csv('battle_log.csv')

df['P1 Start Pokemon'] = df['P1 Start Pokemon'].str.strip()
df['P2 Start Pokemon'] = df['P2 Start Pokemon'].str.strip()
df = df.replace('0 fnt', '0')

cols_to_convert = ['Turn', 'P1 Start Health', 'P1 End Health', 'P2 Start Health', 'P2 End Health']

for col in cols_to_convert:
    df[col] = pd.to_numeric(df[col], errors='coerce').astype('Int64')

df = df[df['Turn'] != 0]

# looking on how ally/opponent types influence move choice
BvB = (df['P1 Start Pokemon'] == 'Blastoise') & (df['P2 Start Pokemon'] == 'Blastoise')
CvC = (df['P1 Start Pokemon'] == 'Charizard') & (df['P2 Start Pokemon'] == 'Charizard')
VvV = (df['P1 Start Pokemon'] == 'Venusaur') & (df['P2 Start Pokemon'] == 'Venusaur')

BvC = (df['P1 Start Pokemon'] == 'Blastoise') & (df['P2 Start Pokemon'] == 'Charizard')
CvV = (df['P1 Start Pokemon'] == 'Charizard') & (df['P2 Start Pokemon'] == 'Venusaur')
VvB = (df['P1 Start Pokemon'] == 'Venusaur') & (df['P2 Start Pokemon'] == 'Blastoise')

BvV = (df['P1 Start Pokemon'] == 'Blastoise') & (df['P2 Start Pokemon'] == 'Venusaur')
CvB = (df['P1 Start Pokemon'] == 'Charizard') & (df['P2 Start Pokemon'] == 'Blastoise')
VvC = (df['P1 Start Pokemon'] == 'Venusaur') & (df['P2 Start Pokemon'] == 'Charizard')

columns = ['P1 Action', 'P2 Action', 'P1 Start Health', 'P2 Start Health']

BlastoiseVsBlastoise = df.loc[BvB][columns]
CharizardVsCharizard = df.loc[CvC][columns]
VenusaurVsVenusaur = df.loc[VvV][columns]

BlastoiseVsCharizard = df.loc[BvC][columns]
CharizardVsVenusaur = df.loc[CvV][columns]
VenusaurVsBlastoise = df.loc[VvB][columns]

BlastoiseVsVenusaur = df.loc[BvV][columns]
CharizardVsBlastoise = df.loc[CvB][columns]
VenusaurVsCharizard = df.loc[VvC][columns]

same1 = pd.concat([BlastoiseVsBlastoise['P1 Action'], BlastoiseVsBlastoise['P2 Action']])
same2 = pd.concat([CharizardVsCharizard['P1 Action'], CharizardVsCharizard['P2 Action']])
same3 = pd.concat([VenusaurVsVenusaur['P1 Action'], VenusaurVsVenusaur['P2 Action']])

same1 = same1.replace({'switch Venusaur': 'switch to advantage', 'Water Attack': 'stab move',
                       'Fire Attack': 'alternate move', 'switch Charizard': 'switch to disadvantage'})
same2 = same2.replace({'switch Blastoise': 'switch to advantage', 'Fire Attack': 'stab move',
                       'Grass Attack': 'alternate move', 'switch Venusaur': 'switch to disadvantage'})
same3 = same3.replace({'switch Charizard': 'switch to advantage', 'Grass Attack': 'stab move',
                       'Water Attack': 'alternate move', 'switch Blastoise': 'switch to disadvantage'})
same = pd.concat([same1, same2, same3])
# print(same.value_counts(normalize=True))

super1 = pd.concat([BlastoiseVsCharizard['P1 Action'], CharizardVsBlastoise['P2 Action']])
super2 = pd.concat([CharizardVsVenusaur['P1 Action'], VenusaurVsCharizard['P2 Action']])
super3 = pd.concat([VenusaurVsBlastoise['P1 Action'], BlastoiseVsVenusaur['P2 Action']])

super1 = super1.replace({'switch Venusaur': 'switch to disadvantage', 'Water Attack': 'stab move',
                       'Fire Attack': 'alternate move', 'switch Charizard': 'switch to same'})
super2 = super2.replace({'switch Blastoise': 'switch to disadvantage', 'Fire Attack': 'stab move',
                       'Grass Attack': 'alternate move', 'switch Venusaur': 'switch to same'})
super3 = super3.replace({'switch Charizard': 'switch to disadvantage', 'Grass Attack': 'stab move',
                       'Water Attack': 'alternate move', 'switch Blastoise': 'switch to same'})
super_combined = pd.concat([super1, super2, super3])
# print(super_combined.value_counts(normalize=True))

resist1 = pd.concat([BlastoiseVsVenusaur['P1 Action'], VenusaurVsBlastoise['P2 Action']])
resist2 = pd.concat([CharizardVsBlastoise['P1 Action'], BlastoiseVsCharizard['P2 Action']])
resist3 = pd.concat([VenusaurVsCharizard['P1 Action'], CharizardVsVenusaur['P2 Action']])

resist1 = resist1.replace({'switch Venusaur': 'switch to same', 'Water Attack': 'stab move',
                       'Fire Attack': 'alternate move', 'switch Charizard': 'switch to advantage'})
resist2 = resist2.replace({'switch Blastoise': 'switch to same', 'Fire Attack': 'stab move',
                       'Grass Attack': 'alternate move', 'switch Venusaur': 'switch to advantage'})
resist3 = resist3.replace({'switch Charizard': 'switch to same', 'Grass Attack': 'stab move',
                       'Water Attack': 'alternate move', 'switch Blastoise': 'switch to advantage'})
resist_combined = pd.concat([resist1, resist2, resist3])
# print(resist_combined.value_counts(normalize=True))

# looking at how health in addition to ally/opponent types influences move choice
player1 = ['P1 Start Health', 'P1 Action']
player2 = ['P2 Start Health', 'P2 Action']
player1_rename = {'P1 Start Health': 'Start Health', 'P1 Action': 'Action'}
player2_rename = {'P2 Start Health': 'Start Health', 'P2 Action': 'Action'}

bins = [0, 0.25, 0.5, 0.75, 1.0]
labels = ['0-25%', '25-50%', '50-75%', '75-100%']

same1_tom0 = pd.concat([BlastoiseVsBlastoise[player1].rename(columns=player1_rename),
                        BlastoiseVsBlastoise[player2].rename(columns=player2_rename)])
same2_tom0 = pd.concat([CharizardVsCharizard[player1].rename(columns=player1_rename),
                        CharizardVsCharizard[player2].rename(columns=player2_rename)])
same3_tom0 = pd.concat([VenusaurVsVenusaur[player1].rename(columns=player1_rename),
                        VenusaurVsVenusaur[player2].rename(columns=player2_rename)])

same1_tom0 = same1_tom0.replace({'switch Venusaur': 'switch to advantage', 'Water Attack': 'stab move',
                       'Fire Attack': 'alternate move', 'switch Charizard': 'switch to disadvantage'})
same2_tom0 = same2_tom0.replace({'switch Blastoise': 'switch to advantage', 'Fire Attack': 'stab move',
                       'Grass Attack': 'alternate move', 'switch Venusaur': 'switch to disadvantage'})
same3_tom0 = same3_tom0.replace({'switch Charizard': 'switch to advantage', 'Grass Attack': 'stab move',
                       'Water Attack': 'alternate move', 'switch Blastoise': 'switch to disadvantage'})

same_tom0 = pd.concat([same1_tom0, same2_tom0, same3_tom0])

super1_tom0 = pd.concat([BlastoiseVsCharizard[player1].rename(columns=player1_rename),
                        CharizardVsBlastoise[player2].rename(columns=player2_rename)])
super2_tom0 = pd.concat([VenusaurVsBlastoise[player1].rename(columns=player1_rename),
                        BlastoiseVsVenusaur[player2].rename(columns=player2_rename)])
super3_tom0 = pd.concat([CharizardVsVenusaur[player1].rename(columns=player1_rename),
                        VenusaurVsCharizard[player2].rename(columns=player2_rename)])

super1_tom0 = super1_tom0.replace({'switch Venusaur': 'switch to disadvantage', 'Water Attack': 'stab move',
                       'Fire Attack': 'alternate move', 'switch Charizard': 'switch to same'})
super3_tom0 = super3_tom0.replace({'switch Blastoise': 'switch to disadvantage', 'Fire Attack': 'stab move',
                       'Grass Attack': 'alternate move', 'switch Venusaur': 'switch to same'})
super2_tom0 = super2_tom0.replace({'switch Charizard': 'switch to disadvantage', 'Grass Attack': 'stab move',
                       'Water Attack': 'alternate move', 'switch Blastoise': 'switch to same'})
super_tom0 = pd.concat([super1_tom0, super3_tom0, super2_tom0])

resist1_tom0 = pd.concat([VenusaurVsCharizard[player1].rename(columns=player1_rename),
                        CharizardVsVenusaur[player2].rename(columns=player2_rename)])
resist2_tom0 = pd.concat([BlastoiseVsVenusaur[player1].rename(columns=player1_rename),
                        VenusaurVsBlastoise[player2].rename(columns=player2_rename)])
resist3_tom0 = pd.concat([CharizardVsBlastoise[player1].rename(columns=player1_rename),
                        BlastoiseVsCharizard[player2].rename(columns=player2_rename)])

resist2_tom0 = resist2_tom0.replace({'switch Venusaur': 'switch to same', 'Water Attack': 'stab move',
                       'Fire Attack': 'alternate move', 'switch Charizard': 'switch to advantage'})
resist3_tom0 = resist3_tom0.replace({'switch Blastoise': 'switch to same', 'Fire Attack': 'stab move',
                       'Grass Attack': 'alternate move', 'switch Venusaur': 'switch to advantage'})
resist1_tom0 = resist1_tom0.replace({'switch Charizard': 'switch to same', 'Grass Attack': 'stab move',
                       'Water Attack': 'alternate move', 'switch Blastoise': 'switch to advantage'})
resist_tom0 = pd.concat([resist1_tom0, resist2_tom0, resist3_tom0])

def result(table):
    table['Start Health'] = table['Start Health'] / 341
    table['Health Bin'] = pd.cut(table['Start Health'], bins=bins, labels=labels)
    table['Health Bin'] = pd.Categorical(table['Health Bin'], categories=labels, ordered=True)

    proportions = (
        table.groupby('Health Bin')['Action']
        .value_counts(normalize=True)
        .rename('proportion')
        .reset_index()
    )

    pivot_df = proportions.pivot(index='Health Bin', columns='Action', values='proportion').fillna(0)
    return pivot_df


# making visualization
graph = result(resist_tom0)
print(graph)
ax = graph.plot(kind='bar', stacked=True, figsize=(12,8))
ax.set_ylabel('Proportion')
ax.set_xlabel('Health Bin')
ax.set_title('Action by Health Bin')
plt.tight_layout()
plt.show()

