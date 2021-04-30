# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 12:52:37 2021

@author: ntrayers
Predicts rating number
"""

import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, precision_score, recall_score

directory = "./train/neg"
x_train = []
y_train = []
for file in os.listdir(directory):
    with open("./train/neg/" + file, 'r', encoding="Latin-1") as f:
        x_train.append(f.read())
        y_train.append(file[len(file) - 5])
        
directory = "./train/pos"
for file in os.listdir(directory):
    with open("./train/pos/" + file, 'r', encoding="Latin-1") as f:
        x_train.append(f.read())
        y_train.append(file[len(file) - 5])


# Test
directory = "./test/neg"
x_test = []
y_test = []
for file in os.listdir(directory):
    with open("./test/neg/" + file, 'r', encoding="Latin-1") as f:
        x_test.append(f.read())
        y_test.append(file[len(file) - 5])

directory = "./test/pos"
for file in os.listdir(directory):
    with open("./test/pos/" + file, 'r', encoding="Latin-1") as f:
        x_test.append(f.read())
        y_test.append(file[len(file) - 5])

# Vectorizer

cv = CountVectorizer(strip_accents='ascii', token_pattern=u'(?ui)\\b\\w*[a-z]+\\w*\\b', lowercase=True, stop_words='english')
X_train_cv = cv.fit_transform(x_train)
X_test_cv = cv.transform(x_test)

# training ratings
naive_bayes = MultinomialNB()
naive_bayes.fit(X_train_cv, y_train)
predictions = naive_bayes.predict(X_test_cv)

# testing ratings
print('Accuracy score: ', accuracy_score(y_test, predictions))
print('Precision score: ', precision_score(y_test, predictions, average='micro'))
print('Recall score: ', recall_score(y_test, predictions, average='micro'))