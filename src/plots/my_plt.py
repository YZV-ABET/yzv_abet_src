import numpy as np
import pandas as pd
import ipywidgets as widgets
from ipywidgets import interact, interactive, fixed, interact_manual
from IPython.display import clear_output, display, HTML
from src.parsers.parser import *
from src.widgets.my_widgets import *
import matplotlib.pyplot as plt
import seaborn as sns
from copy import deepcopy


df1, df2, df3, mand_df, elec_df = parse_courses()

colors = sns.color_palette('pastel')[0:50]


def pi_dist_pie(course, filter_choice):
    clear_output(wait=True)
    df = df2.loc[course]["1":"7"]
    if filter_choice:
        df_filter = df.copy()
        df_filter[df < 3] = 0
        df = df_filter.copy()
    df_print = pd.DataFrame(data=df.sum(level=0).values / df.sum(level=0).values.sum() * 100, index=df.sum(level=0).index, columns=['PI Percentage'])
    display(HTML(df_print.T.to_html()))
    plt.figure(figsize=(8, 6), dpi=80)
    plt.pie(df.sum(level=0).values, labels = df.sum(level=0).index, colors = colors[:7], autopct='%.0f%%')
    plt.legend(labels=df.sum(level=0).index)
    plt.title("PI Distribution Chart of Course")
    plt.show()


def pi_levels_percourse(course):
    clear_output(wait=True)
    df = df2.loc[course]["1":"7"]
    fig, axs = plt.subplots(1, 7, figsize=(28,4))
    for i in range(1, 8):
        sns.barplot(x=df[str(i)].index, y=df[str(i)].values, palette = colors[:len(df[str(i)].index)], ax=axs[i-1])
        axs[i-1].set_xlabel("PI: {}".format(i))
        axs[i-1].set_ylabel("Contribution Level")


def total_course_pi(choice, filter_choice):
    clear_output(wait=True)
    idx = handle_choice(choice)
    df = df2.loc[idx].T.loc["1":"7"].T
    if filter_choice:
        df_filter = df.copy()
        df_filter[df < 3] = 0
        df = df_filter.copy()
    df_print = pd.DataFrame(data=df.sum(axis=1), index=df.index, columns=['Sum of Contributions'])
    display(HTML(df_print.T.to_html()))
    plt.figure(figsize=(len(idx), 5), dpi=80)
    ax = sns.pointplot(x=df.index, y=df.sum(axis=1), palette=colors[:len(df)])
    plt.show()
    return


def pi_contr_level_dist(choice):
    clear_output(wait=True)
    idx = handle_choice(choice)
    df = df2.loc[idx].T.loc["1":"7"]
    df_save = deepcopy(df)
    df['pis'] = df.index.levels[1][2:]
    deneme = pd.melt(df, id_vars=['pis'], value_vars=list(df.columns).remove('pis'))
    plt.figure(figsize=(12, 8), dpi=80)
    ax1 = sns.boxplot(x='pis', y='value', data=deneme, palette=colors[:len(deneme['pis'])])
    ax1.set_xlabel("Sub-PI")
    ax1.set_ylabel("Contribution Level")
    plt.title("Sub-PI Contribution Level Distribution of Courses")
    plt.show()
    
    df_save = df_save.groupby(level=0).sum() / df_save.groupby(level=0).count()
    df = deepcopy(df_save)
    df['pis'] = df.index
    deneme = pd.melt(df, id_vars=['pis'], value_vars=list(df.columns).remove('pis'))
    plt.figure(figsize=(12, 8), dpi=80)
    ax2 = sns.boxplot(x='pis', y='value', data=deneme, palette=colors[:len(deneme['pis'])])
    ax2.set_xlabel("PI")
    ax2.set_ylabel("Contribution Level")
    plt.title("PI Contribution Level Distribution of Courses")
    plt.show()
    
    return
    
    
def contrib_dist_percourse(course):
    clear_output(wait=True)
    df = df2.loc[course]["1":"7"]
    display(HTML(df.value_counts().to_frame().T.to_html()))
    plt.figure(figsize=(8, 6), dpi=80)
    ax = sns.histplot(data=df, x=df.values, binwidth=0.1)
    ax.set_xticks([0, 1, 2, 3])
    ax.set_xlabel("Contribution Level")
    ax.set_ylabel("Number of PI\'s")
    plt.title("Number of Contributions of Level 1-2-3 per Course")
    plt.show()
    

def average_course_contribution(choice, filter_choice):
    clear_output(wait=True)
    idx = handle_choice(choice)
    df = df2.loc[idx, "1":"7"]
    if filter_choice:
        df_filter = df.copy()
        df_filter[df < 3] = 0
        df = df_filter.copy()
    df_print = pd.DataFrame(data=df.mean(axis=1), index=df.index, columns=['Average Contribution'])
    display(HTML(df_print.T.to_html()))
    plt.figure(figsize=(len(idx) + 5, 8), dpi=80)
    ax = sns.barplot(x=df.index, y=df.mean(axis=1),palette = colors[:len(df.index)])
    ax.set_xlabel("Course Code")
    ax.set_ylabel("Average Contribution")
    plt.title("Average of Contributions of Courses per Course")
    plt.show()
    

def course_pi_usage(filter_choice):
    clear_output(wait=True)
    df = df2.loc[:, "1":"7"]
    if filter_choice:
        df_filter = df.copy()
        df_filter[df < 3] = 0
        df = df_filter.copy()
    df_save = deepcopy(df.T)
    df_save['pis'] = df_save.index.levels[1][2:]
    deneme = pd.melt(df_save, id_vars=['pis'], value_vars=list(df_save.columns).remove('pis'))
    df_gb = deneme[deneme['value']>0].groupby('pis').count()
    df_print = df_gb['value'].to_frame().rename(columns={'value': 'Number of Courses with Contribution Level'})
    display(HTML(df_print.T.to_html()))
    ax = df_gb.plot(kind='bar', y='value', color = colors[:len(df_gb.index)], title='Number of Courses that Uses a Specific PI', legend=False)
    ax.set_xlabel("PI")
    ax.set_ylabel("Number of Courses")


def contrib_dist_perpi(pi):
    clear_output(wait=True)
    df = df2.iloc[:, df2.columns.get_level_values(1)==pi]
    display(HTML(df.value_counts().to_frame().T.to_html()))
    ax = df.plot(kind='hist', title='Number of Contributions of Level 1-2-3 per PI', legend=False)
    ax.set_xticks([0, 1, 2, 3])
    ax.set_xlabel("Contribution Level")
    ax.set_ylabel("Number of Courses")

def average_pi_contribution(filter_choice):
    clear_output(wait=True)
    df = df2.loc[:, "1":"7"]
    if filter_choice:
        df_filter = df.copy()
        df_filter[df < 3] = 0
        df = df_filter.copy()
    df_save = deepcopy(df.T)
    df_save['pis'] = df_save.index.levels[1][2:]
    df = pd.melt(df_save, id_vars=['pis'], value_vars=list(df_save.columns).remove('pis'))
    df = df.drop(df.columns[1], axis=1)
    df['value'] = df['value'].astype(float)
    df = df.groupby('pis').mean().reset_index()
    df_print = pd.DataFrame(data=df['value'].values, index=df['pis'], columns=['Average Contribution'])
    display(HTML(df_print.T.to_html()))
    plt.figure(figsize=(10, 8), dpi=80)
    ax = sns.barplot(x='value', y = 'pis', data = df, palette = colors[:len(df.index)])
    ax.set_xlabel("Contribution Average")
    ax.set_ylabel("PI")
    plt.title("Average of Contributions of Courses per PI")
    plt.show()


