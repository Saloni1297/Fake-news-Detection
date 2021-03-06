# -*- coding: utf-8 -*-
"""
Created on Sat Apr 28 11:22:47 2018

@author: Saloni Gupta
"""

import pandas as pd
import numpy as np
from sklearn.datasets import make_classification
import matplotlib.pyplot as plt;
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.naive_bayes import BernoulliNB, MultinomialNB
from sklearn import metrics
from datetime import datetime as dt
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer,TfidfTransformer
from sklearn.linear_model import SGDClassifier


import seaborn as sns


df = pd.read_csv("fake_or_real_news.csv");


#print data
df = df.set_index("Unnamed: 0")

#print df.head()



# Set `y` 
y = df.label

X = df.text

# Drop the `label` column
df.drop("label", axis=1)

#df = df.dropna()

# Make training and test sets 
X_train, X_test, y_train, y_test = train_test_split(df['text'], y, test_size=0.33, random_state=53)


#print df.head()

# Initialize the `count_vectorizer` 
count_vectorizer = CountVectorizer(stop_words='english')

# Fit and transform the training data 
count_train = count_vectorizer.fit_transform(X_train) 

# Transform the test set 
count_test = count_vectorizer.transform(X_test)


# Initialize the `tfidf_vectorizer` 
tfidf_vectorizer = TfidfVectorizer(stop_words='english', max_df=0.7) 

# Fit and transform the training data 
tfidf_train = tfidf_vectorizer.fit_transform(X_train) 

# Transform the test set 
tfidf_test = tfidf_vectorizer.transform(X_test)

#print tfidf_vectorizer.get_feature_names()[-10:]

# Get the feature names of `count_vectorizer` 
#print count_vectorizer.get_feature_names()[:10]




def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    See full source and example: 
    http://scikit-learn.org/stable/auto_examples/model_selection/plot_confusion_matrix.html
    
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, cm[i, j],
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    
'''
The multinomial Naive Bayes classifier is suitable for classification
with discrete features (e.g., word counts for text classification).
The multinomial distribution normally requires integer feature counts.
However, in practice, fractional counts such as tf-idf may also work.
'''

clf = MultinomialNB() 

clf.fit(tfidf_train, y_train)
pred = clf.predict(tfidf_test)
score = metrics.accuracy_score(y_test, pred)
print "Accuracy using tfidf_vectorizer:   %0.3f" % score
cm = metrics.confusion_matrix(y_test, pred, labels=['FAKE','REAL'])
#plot_confusion_matrix(cm, classes=['FAKE','REAL'])

clf = MultinomialNB()  

clf.fit(count_train, y_train)
pred = clf.predict(count_test)
score = metrics.accuracy_score(y_test, pred)
print("Accuracy using count_vectorizer:   %0.3f" % score)
cm1 = metrics.confusion_matrix(y_test, pred, labels=['FAKE','REAL'])
#plot_confusion_matrix(cm1, classes=['FAKE','REAL'])


clf = svm.SVC()
clf.fit(count_train, y_train)  
pred = clf.predict(count_test)
score = metrics.accuracy_score(y_test, pred)
print("Accuracy using svm:   %0.3f" % score)


text_clf = text_clf.fit(X, y)
predicted = text_clf.predict(X_test)
print ("Accuracy using pipeline: ", np.mean(predicted == y_test))




    