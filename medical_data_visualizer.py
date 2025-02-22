import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv("medical_examination.csv")

# Add 'overweight' column
#df['overweight'] = df['weight']/((df['height']/100)**2) 
#df['overweight'] = [0 if x<=25 else 1 for x in df['overweight']]
df['overweight'] = [0 if x/((y/100)**2)<=25 else 1 for x,y in zip(df['weight'], df['height'])]

# Normalize data by making 0 always good and 1 always bad. If the value of 'cholestorol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.
df['cholesterol'] = [0 if x==1 else 1 for x in df['cholesterol']]
df['gluc'] = [0 if x==1 else 1 for x in df['gluc']]

# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    df_cat = pd.melt(df, id_vars=['cardio'], value_vars=['active', 'alco', 'cholesterol', 'gluc', 'overweight', 'smoke'])

    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the collumns for the catplot to work correctly.
    df_cat_grouped = df_cat.groupby(['cardio','variable', 'value'], as_index = False).size().rename(columns={'size':'total'})

    # Draw the catplot with 'sns.catplot()'
    # Option 1: using the original df_cat
    #g = sns.catplot(x='variable', y=None, hue='value', col='cardio', data=df_cat, kind='count', ci=None)
    #g.set(ylabel='total')

    # Option 2: using the grouped df_cat
    g = sns.catplot(x='variable', y='total', hue='value', col='cardio', data=df_cat_grouped, kind='bar', ci=None)
    
    # Get figure from FacetGrid object
    fig = g.fig

    # Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig


# Draw Heat Map
def draw_heat_map():
    # Clean the data
    df_heat = df[(df['ap_lo'] <= df['ap_hi']) & 
                 (df['height'] >= df['height'].quantile(0.025)) & 
                 (df['height'] <= df['height'].quantile(0.975)) & 
                 (df['weight'] >= df['weight'].quantile(0.025)) &
                 (df['weight'] <= df['weight'].quantile(0.975))]

    # Calculate the correlation matrix
    corr = df_heat.corr()

    # Generate a mask for the upper triangle
    mask = np.zeros_like(corr)
    mask[np.triu_indices_from(mask)] = True

    # Set up the matplotlib figure
    fig, ax = plt.subplots()

    # Draw the heatmap with 'sns.heatmap()'
    ax = sns.heatmap(corr, annot=True, fmt=".1f", square=True, mask=mask, center=0)

    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig
