# -*- coding: utf-8 -*-
"""
Created on Fri Apr  9 15:42:00 2021

@author: ntrayers
Predicts positive/negative
"""

import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import metrics

directory = "./train/neg"
x_train = []
for file in os.listdir(directory):
    with open("./train/neg/" + file, 'r', encoding="Latin-1") as f:
        x_train.append(f.read())
        
y_train = [0] * len(x_train)
pos_len = 0
        
directory = "./train/pos"
for file in os.listdir(directory):
    with open("./train/pos/" + file, 'r', encoding="Latin-1") as f:
        pos_len += 1
        x_train.append(f.read())
        
y_pos = [1] * pos_len        
y_train += y_pos


# Test
directory = "./test/neg"
x_neg_test = []
for file in os.listdir(directory):
    with open("./test/neg/" + file, 'r', encoding="Latin-1") as f:
        x_neg_test.append(f.read())
        
y_neg_test = [0] * len(x_neg_test)

directory = "./test/pos"
x_pos_test = []
for file in os.listdir(directory):
    with open("./test/pos/" + file, 'r', encoding="Latin-1") as f:
        x_pos_test.append(f.read())
        
y_pos_test = [1] * len(x_pos_test)        

x_test = x_neg_test + x_pos_test
y_test = y_neg_test + y_pos_test

# Vectorizer
cv = CountVectorizer(strip_accents='ascii', token_pattern=u'(?ui)\\b\\w*[a-z]+\\w*\\b', lowercase=True, stop_words='english')
X_train_cv = cv.fit_transform(x_train)
X_test_cv = cv.transform(x_test)
tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_cv)
X_train_tfidf.shape
X_test_tfidf = tfidf_transformer.transform(X_test_cv)
X_test_tfidf.shape

# training ratings
naive_bayes = MultinomialNB()
naive_bayes.fit(X_train_cv, y_train)
predictions_nb = naive_bayes.predict(X_test_cv)

svm = SGDClassifier().fit(X_train_tfidf, y_train)
predicted_svm = svm.predict(X_test_tfidf)

# testing ratings
print('Naive Bayes Pos/Neg Accuracy score: ', accuracy_score(y_test, predictions_nb))
print('Naive Bayes Pos/Neg Precision score: ', precision_score(y_test, predictions_nb))
print('Naive Bayes Pos/Neg Recall score: ', recall_score(y_test, predictions_nb))
print('SVM Pos/Neg Accuracy score: ', accuracy_score(y_test, predicted_svm))
print('SVM Pos/Neg Precision score: ', precision_score(y_test, predicted_svm))
print('SVM Pos/Neg Recall score: ', recall_score(y_test, predicted_svm))

plt.figure()
cm1 = confusion_matrix(y_test, predictions_nb)
sns.heatmap(cm1, square=True, annot=True, cmap='RdBu', cbar=False, xticklabels=['Negative', 'Positive'], yticklabels=['Negative', 'Positive'])
plt.title('Naive Bayes')
plt.xlabel('predicted label')
plt.ylabel('true label')

plt.figure()
cm2 = confusion_matrix(y_test, predicted_svm)
sns.heatmap(cm2, square=True, annot=True, cmap='RdBu', cbar=False, xticklabels=['Negative', 'Positive'], yticklabels=['Negative', 'Positive'])
plt.title('SVM')
plt.xlabel('predicted label')
plt.ylabel('true label')

print("Naive Bayes")
print(metrics.confusion_matrix(y_test, predictions_nb))
print(metrics.classification_report(y_test, predictions_nb, digits=3))
print("SVM")
print(metrics.confusion_matrix(y_test, predicted_svm))
print(metrics.classification_report(y_test, predicted_svm, digits=3))