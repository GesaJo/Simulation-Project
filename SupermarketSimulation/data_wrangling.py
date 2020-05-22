""" Preprocessing the data for the simulation and excerpt initial-state-vector
and probability matrix """

import pandas as pd
import numpy as np

Monday = pd.read_csv('data/monday.csv', sep=';')
Tuesday = pd.read_csv('data/tuesday.csv', sep=';')
Wednesday = pd.read_csv('data/wednesday.csv', sep=';')
Thursday = pd.read_csv('data/thursday.csv', sep=';')
Friday = pd.read_csv('data/friday.csv', sep=';')

# Preparing data
def customer_separation(customer_col, day):
    customer = []
    for c in customer_col:
        customer.append(str(c) + day)
    return customer

Monday['customer'] = customer_separation(Monday['customer_no'], 'mon')
Tuesday['customer'] = customer_separation(Tuesday['customer_no'], 'tue')
Wednesday['customer'] = customer_separation(Wednesday['customer_no'], 'wed')
Thursday['customer'] = customer_separation(Thursday['customer_no'], 'thu')
Friday['customer'] = customer_separation(Friday['customer_no'], 'fri')

Monday['weekday'] = 'mon'
Tuesday['weekday'] = 'tue'
Wednesday['weekday'] = 'wed'
Thursday['weekday'] = 'thu'
Friday['weekday'] = 'fri'

# merging dataframes
df = Monday.append([Tuesday, Wednesday, Thursday, Friday], sort=True)
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['day'] = df['timestamp'].dt.weekday

# aisles visited first
df['firsts'] = df.duplicated('customer')
firsts = df[df['firsts'] == False]

# initial_state_vector
initial_state_abs = firsts.groupby('location').count()['customer']
initial_state_vector = initial_state_abs/initial_state_abs.sum()

# probability matrix
df['next'] = df.groupby(['customer'])['location'].shift(-1)
trans_prob_matrix = pd.crosstab(df['location'], df['next'], normalize='index')
