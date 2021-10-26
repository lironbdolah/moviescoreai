import numpy as np
import nltk
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
from scipy import spatial
import networkx as nx
english_words = set(nltk.corpus.words.words())


def summary_score(sentence_tokens,sentences_padded,clean_sentences):
    similarity_matrix = np.zeros([len(sentence_tokens), len(sentence_tokens)])
    for i,row_embedding in enumerate(sentences_padded):
        for j,column_embedding in enumerate(sentences_padded):
            similarity_matrix[i][j]=1-spatial.distance.cosine(row_embedding,column_embedding)

    nx_graph = nx.from_numpy_array(similarity_matrix)
    scores = nx.pagerank(nx_graph,max_iter=600)

    top_sentence = {sentence: scores[index] for index, sentence in enumerate(clean_sentences)}
    top = dict(sorted(top_sentence.items(), key=lambda x: x[1], reverse=True)[:4])

    summary = ''
    for sent in clean_sentences:
        if sent in top.keys():
            summary = summary + '"' + sent + ' "' + ' <br>'
    return summary

def review_summary(reviews):
    clean_sentences = []
    max_length = 100  # length of sentence
    vocab_size = 5000
    for text in reviews:

        tokens = nltk.word_tokenize(text)

        stopwords = nltk.corpus.stopwords.words('english')
        processed = [w for w in tokens if w.lower() not in stopwords]  # remove stop words

        no_digits = [w for w in processed if
                     not any(n.isdigit() for n in w)]  # remove numbers and words containing numbers

        clean_sentences.append(' '.join([s for s in no_digits if len(s) > 2]))  # removes words shorter then 2
        clean_sentences = clean_sentences + [i for i in text.split('.') if len(i) > 0]

    tokenizer = Tokenizer(num_words=vocab_size,filters='!"#$%&()*+,-./:;<=>?@[\]^_`{|}~')
    tokenizer.fit_on_texts(clean_sentences)  # removes punctuation, lower case, breaking sentences into words and indexing them
    sequences = tokenizer.texts_to_sequences(clean_sentences) # transforms sentences to vectors
    trunc_type='post'
    padding_type='post'
    sentences_padded = pad_sequences(sequences, maxlen=max_length,
                                     padding=padding_type, truncating=trunc_type) # fit each sentence to same length

    sentence_tokens = [nltk.sent_tokenize(i) for i in clean_sentences]


    summary = summary_score(sentence_tokens,sentences_padded, clean_sentences)
    return summary










