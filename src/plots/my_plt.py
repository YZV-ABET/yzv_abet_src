import numpy as np
import pandas as pd
import ipywidgets as widgets
from ipywidgets import interact, interactive, fixed, interact_manual
from parser import parse_courses
from my_widgets import course_widget, pi_widget, dist_widget, handle_choice
import matplotlib.pyplot as plt
import seaborn as sns
from copy import deepcopy


df1, df2, df3, mand_df, elec_df = parse_courses()

colors = sns.color_palette('pastel')[0:50]


def plot1(course):
    df = df2.loc[course]["1":"7"]
    plt.figure(figsize=(8, 6), dpi=80)
    plt.pie(df.sum(level=0).values, labels = df.sum(level=0).index, colors = colors[:7], autopct='%.0f%%')
    plt.legend(labels=df.sum(level=0).index)
    plt.show()


def plot2(course, pi):
    df = df2.loc[course]["1":"7"]
    plt.figure(figsize=(6, 6), dpi=80)
    ax = sns.barplot(x=df[pi].index, y=df[pi].values, palette = colors[:len(df[pi].index)])
    ax.set_box_aspect(2.5/len(ax.patches))
    plt.show()


def plot3(choice):
    idx = handle_choice(choice)
    df = df2.loc[idx].T.loc["1":"7"].T
    plt.figure(figsize=(40, 10), dpi=80)
    ax = sns.pointplot(x=df.index, y=df.sum(axis=1), palette=colors[:len(df)])
    plt.legend(labels=df.index)
    plt.show()
    return


def plot4(choice):
    idx = handle_choice(choice)
    df = df2.loc[idx].T.loc["1":"7"]
    df_save = deepcopy(df)
    df['pis'] = df.index.levels[1][2:]
    deneme = pd.melt(df, id_vars=['pis'], value_vars=list(df.columns).remove('pis'))
    plt.figure(figsize=(12, 8), dpi=80)
    sns.boxplot(x='pis', y='value', data=deneme, palette=colors[:len(deneme['pis'])])
#    plt.legend(labels=deneme['pis'], loc='center left')
    plt.show()
    df_save = df_save.groupby(level=0).sum() / df_save.groupby(level=0).count()
    df = deepcopy(df_save)
    df['pis'] = df.index
    deneme = pd.melt(df, id_vars=['pis'], value_vars=list(df.columns).remove('pis'))
    plt.figure(figsize=(12, 8), dpi=80)
    sns.boxplot(x='pis', y='value', data=deneme, palette=colors[:len(deneme['pis'])])
#    plt.legend(labels=deneme['pis'], loc='center left')
    plt.show()
    
    return
    
    
def plot5(course):
    df = df2.loc[course]["1":"7"]
    plt.figure(figsize=(8, 6), dpi=80)
    ax = sns.histplot(data=df, x=df.values, binwidth=0.1)
#    mids = [rect.get_x() - rect.get_width() / 2 for rect in ax.patches]
#    ax.set_xticks(mids)
    plt.show()
    

def plot6(choice):
    idx = handle_choice(choice)
    print(len(idx))
    df = df2.loc[idx, "1":"7"]
    print(df.mean(axis=1))
    plt.figure(figsize=(len(idx), 8), dpi=80)
    ax = sns.barplot(x=df.index, y=df.mean(axis=1),palette = colors[:len(df.index)])
#    mids = [rect.get_x() - rect.get_width() / 2 for rect in ax.patches]
#    ax.set_xticks(mids)
    plt.legend(labels=df.index)
    plt.show()
    

def plot7():
    df = df2.loc[:, "1":"7"]
    df_save = deepcopy(df.T)
    df_save['pis'] = df_save.index.levels[1][2:]
    deneme = pd.melt(df_save, id_vars=['pis'], value_vars=list(df_save.columns).remove('pis'))
    df_gb = deneme[deneme['value']>0].groupby('pis').count()
    df_gb.plot(kind='bar', y='value')


def plot8(pi):
    df = df2.iloc[:, df2.columns.get_level_values(1)==pi]
    df.plot(kind='hist')

def plot9():
    df = df2.loc[:, "1":"7"]
    df_save = deepcopy(df.T)
    df_save['pis'] = df_save.index.levels[1][2:]
    df = pd.melt(df_save, id_vars=['pis'], value_vars=list(df_save.columns).remove('pis'))
    df = df.drop(df.columns[1], axis=1)
    df['value'] = df['value'].astype(float)
    df = df.groupby('pis').mean().reset_index()
    plt.figure(figsize=(10, 8), dpi=80)
    ax = sns.barplot(x='value', y = 'pis', data = df)
    plt.show()


