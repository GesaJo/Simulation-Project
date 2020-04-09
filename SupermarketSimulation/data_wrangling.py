""" Preprocessing the data for the simulation and excerpt initial-state-vector
and probability matrix """

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
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

# aisles visited first and following
df['firsts'] = df.duplicated('customer')
firsts = df[df['firsts'] == False]
following = df[df['firsts'] == True]
first_grouped = firsts.groupby('location').count()
following_grouped = following.groupby('location').count()

f_grouped = firsts.groupby('location').count()
initial_state_abs = f_grouped['customer']
denominator = initial_state_abs.sum()

# initial_state_vector
initial_state_vector = initial_state_abs/denominator

# probability matrix
next_aisle = df.groupby(['customer'])['location'].shift(-1)
df['next'] = next_aisle
trans_prob_matrix = pd.crosstab(df['location'], df['next'], normalize='index')
