import seaborn as sns 
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from wordcloud import STOPWORDS, WordCloud
def Barchart(df, col):
    plt.switch_backend('agg')
    n = len(df[col].value_counts())
    if(n<10):
        img = sns.countplot(x = df[col])
        plot_file = f"./static/Images/Categorical/{col}_BarChart.png"
        plt.savefig(plot_file)
        plt.close()
        return plot_file
    else:
        plt.figure(figsize=(n, 10))
        plot_file = f"./static/Images/Categorical/{col}_BarChart.png"
        plt.close()
        return plot_file

def PieChart(df, col):
    plt.switch_backend('agg')
    labels = df[col].value_counts().index
    n = len(labels)
    explode = np.array(df[col].value_counts())
    explode = np.floor(explode/max(explode))/10
    if(n<10):
        plt.pie(df[col].value_counts(), labels = labels, explode = explode)
        plt.legend()
        plot_file = f"./static/Images/Categorical/{col}_PieChart.png"
        plt.savefig(plot_file)
        plt.close()
        return plot_file
    else:
        plt.figure(figsize=(n, 10))
        plt.pie(df[col].value_counts(), labels = labels, explode = explode)
        plt.legend()
        plot_file = f"./static/Images/Categorical/{col}_PieChart.png"
        plt.savefig(plot_file)
        plt.close()
        return plot_file
    

def BoxPlot(df, col):
    plt.switch_backend('agg')
    sns.boxplot(data=df, y=f"{col}")
    plot_file = f"./static/Images/Numerical/{col}_BoxPlot.png"
    plt.savefig(plot_file)
    plt.close()
    return plot_file

def HistPlot(df, col):
    plt.switch_backend('agg')
    sns.histplot(data=df, x=f"{col}", kde=True)
    plot_file = f"./static/Images/Numerical/{col}_HistPlot.png"
    plt.savefig(plot_file)
    plt.close()
    return plot_file

def DistPlot(df, col):
    plt.switch_backend('agg')
    sns.distplot(df[col], kde = True, color ='red')
    plot_file = f"./static/Images/Numerical/{col}_DistPlot.png"
    plt.savefig(plot_file)
    plt.close()
    return plot_file

def ScatterPlot(df, col):
    plt.switch_backend('agg')
    sns.scatterplot(data=df, x=f'{col}', y=df.index)
    plot_file = f"./static/Images/Numerical/{col}_ScatterPlot.png"
    plt.savefig(plot_file)
    plt.close()
    return plot_file

def Word_Cloud(df, col):
    plt.switch_backend('agg')
    comment_words = ''
    stopwords = set(STOPWORDS)
    for val in df["Questions"].values:
        val = str(val).lower()[:-2]  
        comment_words += val   
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(comment_words)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    plot_file = f"./static/Images/Text/{col}_WordCloud.png"
    plt.savefig(plot_file)
    plt.close()
    return plot_file