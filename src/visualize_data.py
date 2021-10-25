import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from os import path
from create_html import html
from summary import review_summary



def plot_bar(image_path,df):
    plt.figure(figsize=(13, 7))
    sns.set_style("whitegrid",{'axes.grid': True})
    bar = sns.barplot(x=df['movies'], y=df['Overall score'], color='gold',order=df.sort_values('Overall score',ascending = False).movies).set_title('Overall Score:')
    x_axis = bar.axes.get_xaxis()
    y_axis = bar.axes.get_yaxis()
    x_label = x_axis.get_label()
    y_label = y_axis.get_label()
    x_label.set_visible(False)
    y_label.set_visible(False)
    plt.box(False)
    plt.savefig(path.join(image_path,'barplot.png'),transparent=True)
    plt.xticks(plt.xticks()[0], df['movies'], rotation=40)
    plt.tight_layout()
    plt.close()

def scores_summary(summarized_data):
    score_summary = ''
    for index,row in summarized_data.sort_values('Overall score', ascending=False).iterrows():
        score_summary = score_summary + '\n' + (summarized_data.iloc[index]['movies']) +\
                         ': &nbsp;&nbsp; Average Score: ' + str(round(summarized_data.iloc[index]['scores'],2)) + ' &nbsp;&nbsp;  Predicted Review Score: ' + \
                         str(round(summarized_data.iloc[index]['prediction'],2)) + ' <br>'

    return score_summary

def compute_accuracy(result,df):
    global index
    score_classes = result.argmax(axis=1)
    correct = 0
    for index,row in df.iterrows():
        if (row['scores'] > 7 and score_classes[index] == 2) \
                or (8 > row['scores'] > 3 and score_classes[index] == 1) \
                or (4 > row['scores'] and score_classes[index] == 0):
            correct+=1
    accuracy = round((float(correct)/float(index+1)),2)
    print(accuracy)
    return accuracy

def topmovie(data,summarized_data):
    movie = summarized_data.sort_values(by=['Overall score'], ascending=False).iloc[0]['movies']
    df = data.loc[data['movies']==movie].sort_values(by=['prediction'], ascending=False)
    top_review = df.iloc[0]['reviews']
    html_review = ''
    for line in top_review.splitlines():
        html_review =html_review + line +' <br>'


    return df.iloc[0]['movies'],df.iloc[0]['image_url'],html_review

def display_data(data, accuracy, name, output_path, start):
    scores_mean = data.groupby('movies')['scores'].mean().reset_index()
    predicted_scores_mean = data.groupby('movies')['prediction'].mean().reset_index()

    scores_mean = scores_mean.sort_values(by=['scores'], ascending=False)
    predicted_scores_mean = predicted_scores_mean.sort_values(by=['prediction'], ascending=False)
    summarized_data = pd.merge(scores_mean, predicted_scores_mean, on="movies")
    summarized_data['Overall score'] = round(((summarized_data['scores'] + summarized_data['prediction']) / 2),2)

    images_path = 'assets'
    plot_bar(images_path, summarized_data) # barplot image
    score_summary = scores_summary(summarized_data) # p
    movie,image_url,top_review = topmovie(data,summarized_data) # h3 text
    top_movie_data = data.loc[data['movies'] == movie]
    summary_review = review_summary(top_movie_data['reviews'])
    html(score_summary, movie, image_url, top_review, images_path, summary_review, accuracy, name, output_path, start) # exports html

























