# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 12:52:37 2021

@author: ntrayers
Predicts rating number
"""

import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.feature_extraction.text import TfidfTransformer
import numpy as np
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict

def read_data():
    
    directory = "./train/neg"
    x_train = []
    y_train = []
    for file in os.listdir(directory):
        with open("./train/neg/" + file, 'r', encoding="Latin-1") as f:
            x_train.append(f.read())
            rating = file[len(file) - 5]
            y_train.append(rating)
            
    directory = "./train/pos"
    for file in os.listdir(directory):
        with open("./train/pos/" + file, 'r', encoding="Latin-1") as f:
            x_train.append(f.read())
            rating = file[len(file) - 5]
            if int(rating) == 0:
                y_train.append(str(10))
            else:
                y_train.append(rating)
    
    
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
            rating = file[len(file) - 5]
            if int(rating) == 0:
                y_test.append(str(10))
            else:
                y_test.append(rating)
    
    return x_train, y_train, x_test, y_test

def vectorize_cv(x_train, x_test):
    cv = CountVectorizer(strip_accents='ascii', token_pattern=u'(?ui)\\b\\w*[a-z]+\\w*\\b', lowercase=True, stop_words='english')
    X_train_cv = cv.fit_transform(x_train)
    X_test_cv = cv.transform(x_test)
    return X_train_cv, X_test_cv

def transform_tfidf(X_train_cv, X_test_cv): 
    tfidf_transformer = TfidfTransformer()
    X_train_tfidf = tfidf_transformer.fit_transform(X_train_cv)
    X_train_tfidf.shape
    X_test_tfidf = tfidf_transformer.transform(X_test_cv)
    X_test_tfidf.shape
    
    return X_train_tfidf, X_test_tfidf

def naive_bayes(X_train_tfidf, X_test_tfidf):
    # training ratings
    naive_bayes = MultinomialNB()
    naive_bayes.fit(X_train_tfidf, y_train)
    predictions = naive_bayes.predict(X_test_tfidf)
    return predictions

def svm(X_train_tfidf, X_test_tfidf):
    svm = SGDClassifier().fit(X_train_tfidf, y_train)
    predicted_svm = svm.predict(X_test_tfidf)
    return predicted_svm

def test_ratings(y_test, predictions, rating, model):
    print(model + ' Accuracy score for rating ' + rating + ': ', accuracy_score(y_test, predictions))
    # print('Precision score: ', precision_score(y_test, predictions, average='micro'))
    # print('Recall score: ', recall_score(y_test, predictions, average='micro'))

def conf_matrix(y_test, predictions):
    cm = confusion_matrix(y_test, predictions)
    sns.heatmap(cm, square=True, annot=True, cmap='RdBu', cbar=False, xticklabels=['0', '1', '2', '3', '4', '7', '8', '9'], yticklabels=['0', '1', '2', '3', '4', '7', '8', '9'])
    plt.xlabel('true label')
    plt.ylabel('predicted label')
    
def test_range(y_test, predicted_nb, predicted_svm):
    for t in range(1, 6):
        print("Naive Bayes Accuracy with tolerance " + str(t))
        r = [int(m) - int(n) for m,n in zip(y_test,predicted_nb)]
        correct = sum(abs(int(i)) <= t for i in r)
        print(correct/len(y_test))
        
    for t in range(1, 6):
        print("SVM Accuracy with tolerance " + str(t))
        r = [int(m) - int(n) for m,n in zip(y_test,predicted_svm)]
        correct = sum(abs(int(i)) <= t for i in r)
        print(correct/len(y_test))
    
def ind_accuracies(y_test, predicted_nb, predicted_svm):
    values = np.unique(y_test)
    dictionary = defaultdict(list)

    for index, xVal in enumerate(y_test):
        for v in values:
            if (xVal == v):
                dictionary[v].append(index)
    
    for v in values:
        y_test_partition = [y_test[i] for i in dictionary[v]]
        predicted_nb_partition = [predicted_nb[i] for i in dictionary[v]]
        test_ratings(y_test_partition, predicted_nb_partition, v, "Naive Bayes")
        
    for v in values:
        y_test_partition = [y_test[i] for i in dictionary[v]]
        predicted_svm_partition = [predicted_svm[i] for i in dictionary[v]]
        test_ratings(y_test_partition, predicted_svm_partition, v, "SVM")
        

if __name__ == '__main__':
    # read data
    x_train, y_train, x_test, y_test = read_data()
    # # transform data
    X_train_cv, X_test_cv = vectorize_cv(x_train, x_test)
    X_train_tfidf, X_test_tfidf = transform_tfidf(X_train_cv, X_test_cv)
    # # train model with naive bayes and predict test data
    predicted_nb = naive_bayes(X_train_cv, X_test_cv)
    # # result
    print("Naive Bayes Average Accuracy with 0 tolerance: ")
    print(np.mean(predicted_nb == y_test))
    predicted_svm = svm(X_train_tfidf, X_test_tfidf)
    print("SVM Average Accuracy with 0 tolerance: ")
    print(np.mean(predicted_svm == y_test))
    ind_accuracies(y_test, predicted_nb, predicted_svm)
    test_range(y_test, predicted_nb, predicted_svm)