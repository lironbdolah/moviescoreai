from extract_from_html import *
import tensorflow
from tensorflow import keras
import nltk
from visualize_data import display_data,compute_accuracy
from os import path
from nltk.stem.porter import PorterStemmer
import pandas as pd
import argparse
stopwords = nltk.corpus.stopwords.words('english')
english_words = set(nltk.corpus.words.words())

def clean_reviews(reviews):
    clean_reviews = []
    for text in reviews:
        tokens = nltk.word_tokenize(text)

        no_digits = [w for w in tokens if
                     not any(n.isdigit() for n in w)]  # remove numbers and words containing numbers

        wnl = nltk.WordNetLemmatizer()
        lemmatize = [wnl.lemmatize(t) for t in no_digits if t in english_words]

        punctuation = [word for word in lemmatize if word.isalpha()] # remove punctuation

        stopwords = nltk.corpus.stopwords.words('english')
        processed = [w for w in punctuation if w.lower() not in stopwords]  # remove stop words

        porter = PorterStemmer()
        stemmed = [porter.stem(word) for word in processed]


        clean_reviews.append(' '.join([s for s in stemmed if len(s) > 2]))  # removes words shorter then 2
    return clean_reviews

def compute_scores(result):

    result[:,0] *= 2
    result[:,1] *= 5.5
    result[:,2] *= 9

    return result.sum(axis=1)

def run(name='moviescoreai',output='run',
                    start=False):
    dataset_path = 'src'
    model = tensorflow.saved_model.load(path.join(dataset_path, "weights"))
    print(model.summary())

    reviews_df = pd.DataFrame()
    url = 'https://www.imdb.com/movies-in-theaters/?ref_=nv_mv_inth'
    reviews_url_list, movies_names, images = extract_movies_url(url)
    reviews_df['reviews'], reviews_df['movies'], reviews_df['scores'] = extract_reviews(reviews_url_list, movies_names)
    reviews_df = add_images(reviews_df, images, movies_names)
    reviews = reviews_df['reviews'].tolist()

    reviews = clean_reviews(reviews)
    result = model.predict(reviews)
    reviews_df['prediction'] = compute_scores(result)
    accuracy = compute_accuracy(result, reviews_df)


    display_data(reviews_df, accuracy, name,output,start)


def parse_opt():
        parser = argparse.ArgumentParser()
        parser.add_argument('--name', type=str, default='moviescoreai',
                            help='Choose a name for the html file')
        parser.add_argument('--output', type=str, default='run',
                            help='Choose a path for the output file')
        parser.add_argument('--start', type=bool, default=False, action=argparse.BooleanOptionalAction,
                            help='open the html file')
        opt = parser.parse_args()
        return opt

def main(opt):
        print(' '.join(f'{k}={v}' for k, v in vars(opt).items()))
        run(**vars(opt))

if __name__ == "__main__":
    opt = parse_opt()
    main(opt)




