import pandas as pd

df = pd.read_csv('battle_log.csv')
df['P1 Start Pokemon'] = df['P1 Start Pokemon'].str.strip()
df['P2 Start Pokemon'] = df['P2 Start Pokemon'].str.strip()

BvB = (df['P1 Start Pokemon'] == 'Blastoise') & (df['P2 Start Pokemon'] == 'Blastoise')
CvC = (df['P1 Start Pokemon'] == 'Charizard') & (df['P2 Start Pokemon'] == 'Charizard')
VvV = (df['P1 Start Pokemon'] == 'Venusaur') & (df['P2 Start Pokemon'] == 'Venusaur')

BvC = (df['P1 Start Pokemon'] == 'Blastoise') & (df['P2 Start Pokemon'] == 'Charizard')
CvV = (df['P1 Start Pokemon'] == 'Charizard') & (df['P2 Start Pokemon'] == 'Venusaur')
VvB = (df['P1 Start Pokemon'] == 'Venusaur') & (df['P2 Start Pokemon'] == 'Blastoise')

BvV = (df['P1 Start Pokemon'] == 'Blastoise') & (df['P2 Start Pokemon'] == 'Venusaur')
CvB = (df['P1 Start Pokemon'] == 'Charizard') & (df['P2 Start Pokemon'] == 'Blastoise')
VvC = (df['P1 Start Pokemon'] == 'Venusaur') & (df['P2 Start Pokemon'] == 'Charizard')

BlastoiseVsBlastoise = df.loc[BvB][['P1 Action', 'P2 Action']]
CharizardVsCharizard = df.loc[CvC][['P1 Action', 'P2 Action']]
VenusaurVsVenusaur = df.loc[VvV][['P1 Action', 'P2 Action']]

BlastoiseVsCharizard = df.loc[BvC][['P1 Action', 'P2 Action']]
CharizardVsVenusaur = df.loc[CvV][['P1 Action', 'P2 Action']]
VenusaurVsBlastoise = df.loc[VvB][['P1 Action', 'P2 Action']]

BlastoiseVsVenusaur = df.loc[BvV][['P1 Action', 'P2 Action']]
CharizardVsBlastoise = df.loc[CvB][['P1 Action', 'P2 Action']]
VenusaurVsCharizard = df.loc[VvC][['P1 Action', 'P2 Action']]

same1 = pd.concat([BlastoiseVsBlastoise['P1 Action'], BlastoiseVsBlastoise['P2 Action']])
same2 = pd.concat([CharizardVsCharizard['P1 Action'], CharizardVsCharizard['P2 Action']])
same3 = pd.concat([VenusaurVsVenusaur['P1 Action'], VenusaurVsVenusaur['P2 Action']])

super1 = pd.concat([BlastoiseVsCharizard['P1 Action'], CharizardVsBlastoise['P2 Action']])
super2 = pd.concat([CharizardVsVenusaur['P1 Action'], VenusaurVsCharizard['P2 Action']])
super3 = pd.concat([VenusaurVsBlastoise['P1 Action'], BlastoiseVsVenusaur['P2 Action']])

resist1 = pd.concat([BlastoiseVsVenusaur['P1 Action'], VenusaurVsBlastoise['P2 Action']])
resist2 = pd.concat([CharizardVsBlastoise['P1 Action'], BlastoiseVsCharizard['P2 Action']])
resist3 = pd.concat([VenusaurVsCharizard['P1 Action'], CharizardVsVenusaur['P2 Action']])


