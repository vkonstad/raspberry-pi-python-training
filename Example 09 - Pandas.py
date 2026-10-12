# Example 09 - Pandas
# The same calculation done in three ways. Compare the timings:
# looping over rows is orders of magnitude slower than vectorized operations.
#
# Concepts: pandas, numpy, row-by-row vs vectorized processing, timing

import pandas as pd, numpy as np, time


def get_data(size=100000):
    df = pd.DataFrame()
    df['age'] = np.random.randint(0, 100, size)
    df['workhours'] = np.random.randint(0, 8, size)
    df['efficiency'] = np.random.rand(size)
    df['bonus'] = np.random.choice(['tech', 'trip', 'check'], size)
    df['penalty'] = np.random.choice(['hours', 'salary'], size)
    return df


def reward_calc(row):
    if row['age'] >= 65:
        return row['bonus']
    if (row['workhours'] >= 4) and (row['efficiency'] >= 0.5):
        return row['bonus']
    return row['penalty']


def with_iterrows(df):
    df = df.copy()
    for index, row in df.iterrows():
        df.loc[index, 'reward'] = reward_calc(row)
    return df


def with_apply(df):
    df = df.copy()
    df['reward'] = df.apply(reward_calc, axis=1)
    return df


def vectorized(df):
    df = df.copy()
    deserves_bonus = ((df['efficiency'] >= 0.5) & (df['workhours'] >= 4)) | (df['age'] >= 65)
    df['reward'] = df['penalty']
    df.loc[deserves_bonus, 'reward'] = df['bonus']
    return df


df = get_data(10000)    # small on purpose: iterrows is very slow, especially on a Pi

for name, method in [('iterrows', with_iterrows), ('apply', with_apply), ('vectorized', vectorized)]:
    t1 = time.perf_counter()
    result = method(df)
    t2 = time.perf_counter()
    print(f"{name:<10} {t2 - t1:.3f} s")

print(result)
