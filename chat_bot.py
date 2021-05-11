import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

import numpy
import tflearn
import tensorflow
from tensorflow.python.framework import ops
import random
import json
import pickle
from mysql_python_interface import read_from_db
from dotenv import dotenv_values

env = dotenv_values(".env")
PATTERNS_TABLE = env["patterns_table"]
RESPONSES_TABLE = env["responses_table"]

try:
    with open("data.pickle", "rb") as f:
        words, labels, training, output = pickle.load(f)
except:
    words = []
    labels = []
    docs_x = []
    docs_y = []

    patterns_from_db = read_from_db(PATTERNS_TABLE,"*")

    for pattern_tag in patterns_from_db:
        wrds = nltk.word_tokenize(pattern_tag[1])
        words.extend(wrds)
        docs_x.append(wrds)
        docs_y.append(pattern_tag[0])

        if pattern_tag[0] not in labels:
            labels.append(pattern_tag[0])

    words = [stemmer.stem(w.lower()) for w in words if w != "?"]
    words = sorted(set(words))

    labels = sorted(labels)

    training = []
    output = []

    out_empty = [0 for _ in range(len(labels))]

    for x,doc in enumerate(docs_x):
        bag = []

        wrds = [stemmer.stem(w) for w in doc]

        for w in words:
            if w in wrds:
                bag.append(1)
            else:
                bag.append(0)

        output_row = out_empty[:]
        output_row[labels.index(docs_y[x])] = 1

        training.append(bag)
        output.append(output_row)

    training = numpy.array(training)
    output = numpy.array(output)

    try:
        with open("data.pickle","wb") as f:
            pickle.dump((words,labels, training, output), f)
    except:
        ops.reset_default_graph()

        net = tflearn.input_data(shape=[None, len(training[0])])
        net = tflearn.fully_connected(net, 32)
        net = tflearn.fully_connected(net, 32)
        net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
        net = tflearn.regression(net)

        model = tflearn.DNN(net)

        model.fit(training, output, n_epoch=50, batch_size=8, show_metric=True)
        model.save("model.tflearn")

def bag_of_words(s,words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1

    return numpy.array(bag)

def create_response(inp):
    results = model.predict([bag_of_words(inp,words)]) # render probabilities
    results_index = numpy.argmax(results) # choose the highest probability in the array

    # print(results)

    #if results[results_index] > 0.6:
    tag = labels[results_index]

    try:
        with open("data_response.pickle","rb") as f:
            responses_from_db = pickle.load(f)
    except:
        responses_from_db = read_from_db(RESPONSES_TABLE,"*")

        with open("data_response.pickle","wb") as f:
            pickle.dump((responses_from_db),f)

    responses = []
    if len(responses_from_db) == 0:
        return "Buna verecek bir cevabım yok, hayretler içerisindeyim"
    for tag_response in responses_from_db:
        if tag_response[0] == tag:
            responses.append(tag_response[1])

    return random.choice(responses)
