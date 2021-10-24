import tensorflow as tf
from sklearn.model_selection import train_test_split
from tensorflow.keras.layers import Dense,Embedding, Bidirectional, LSTM,Dropout
from keras.callbacks import EarlyStopping
from  matplotlib import pyplot as plt
import pandas as pd
from os import path
import nltk
import numpy as np
from nltk.stem.porter import PorterStemmer


english_words = set(nltk.corpus.words.words())

dataset_path = 'C:/Users/ADMIN/Documents/Ds/nlp'


df = pd.read_csv(path.join(dataset_path,'datasett.csv'))
df = df[:50000]
reviews = df['review'].tolist()
stopwords = nltk.corpus.stopwords.words('english')


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


reviews = clean_reviews(reviews)
review = np.array(reviews)


def scores(df): # divide comments to 3 categories
    labels = []
    for label in df['score']:
        if int(label) > 7:  # 10 9 8 good
            labels.append(float(2))
        elif int(label) > 3:  # 7 6 5 4 mediocare
            labels.append(float(1))
        else:                # 3 2 1
            labels.append(float(0))
    df['label'] = labels
    return df

dataset = scores(df)

labels = dataset['label']
training_sentences, testing_sentences, training_labels, testing_labels = train_test_split(review,labels, test_size = 0.15 , shuffle=True)
print(training_sentences.shape,training_labels.shape)
print(testing_sentences.shape,testing_labels.shape)


# model parameters

batch_size = 64
vocab_size = 50000

encoder = tf.keras.layers.TextVectorization(
    max_tokens=vocab_size)
encoder.adapt(reviews)

early_stopping = EarlyStopping(patience=3)
# model

model = tf.keras.Sequential([
    encoder,
    Embedding(
        input_dim=len(encoder.get_vocabulary()),
        output_dim=125,
        mask_zero=False), #  padding layers for a fixed length
    Bidirectional(LSTM(125)),
    Dropout(0.2),
    Dense(125, activation='relu'),
    Dense(3, activation='softmax')
])


model.compile(loss='sparse_categorical_crossentropy',
              optimizer=tf.keras.optimizers.Adam(1e-4),
              metrics=['accuracy'])

history = model.fit(training_sentences,training_labels, epochs=10,
                    validation_data=(testing_sentences, testing_labels),
                    validation_steps=100,callbacks=[early_stopping])
model.save(path.join(dataset_path,"weights"))



def plot_graphs(history):

    #plots accuracy
    accuracy = history.history['accuracy']
    validation_accuracy = history.history['val_accuracy']
    epoch = history.epoch
    a =plt.figure(figsize=(16, 8))
    plt.plot(epoch, accuracy, label='Training Accuracy')
    plt.plot(epoch, validation_accuracy, label='Validation Accuracy')
    plt.legend(loc='lower right')
    plt.title('Training and Validation Accuracy')
    a.show()
    plt.savefig(path.join(dataset_path,'accuracy.png'))

    #plots loss
    b = plt.figure(figsize=(16, 8))
    loss = history.history['loss']
    validation_loss = history.history['val_loss']
    plt.plot(epoch, loss, label='Training Loss')
    plt.plot(epoch, validation_loss, label='Validation Loss')
    plt.legend(loc='upper right')
    plt.title('Training and Validation Loss')
    b.show()
    plt.savefig(path.join(dataset_path,'loss.png'))

plot_graphs(history)
