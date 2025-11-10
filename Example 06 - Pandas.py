import pandas as pd, numpy as np, time
import numba

def get_data(size = 100000):
    df = pd.DataFrame()
    df['age'] = np.random.randint(0, 100, size)
    df['workhours'] = np.random.randint(0,8,size)
    df['efficiency'] = np.random.rand(size)
    df['bonus'] = np.random.choice(['tech', 'trip', 'check'], size)
    df['penalty'] = np.random.choice(['hours', 'salary', 'hours'], size)
    return df

def reward_calc(row):
    if row['age'] >= 65:
        return row ['bonus']
    if (row['workhours'] >= 4) & (row['efficiency'] >= 0.5):
        return row ['bonus']
    return row['penalty']

df = get_data()

t1 = time.time()

#for index, row in df.iterrows():
#    df.loc[index, 'reward'] = reward_calc(row)

#df['reward'] = df.apply(reward_calc, axis=1)

df['reward'] = df['penalty']
df.loc[((df['efficiency'] >= 0.5) & (df['workhours'] >= 4)) | (df['age'] >= 65), 'reward'] = df['bonus']

t2 = time.time()
print(round(t2-t1,3))
print(df)
