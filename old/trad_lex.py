


import nltk
import numpy as np
import pandas as pd

from igraph import *
from nltk.corpus import movie_reviews
from scipy import sparse
from time import time

from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn import cross_validation
from sklearn.cross_validation import StratifiedKFold, KFold
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, f1_score

from nltk.corpus import sentiwordnet as swn
from statistics import mean, stdev
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import adjusted_rand_score,normalized_mutual_info_score


#def eval_func()

def main():
    tokenize = nltk.tokenize.RegexpTokenizer(r'\w+')
    stopwords = nltk.corpus.stopwords.words('english')

    lex_file = open('opinion-lexicon/negative-words.txt', 'r')
    neg_lexicon = lex_file.read().splitlines()
    lex_file.close()

    lex_file = open('opinion-lexicon/positive-words.txt', 'r')
    pos_lexicon = lex_file.read().splitlines()
    lex_file.close()


    df_train = pd.read_csv('tweets/downloaded/gold/train/CLEAN_100_topics_100_tweets.sentence-three-point.subtask-A.train.gold.txt', delimiter='\t', header=None)
    df_dev = pd.read_csv('tweets/downloaded/gold/dev/CLEAN_100_topics_100_tweets.sentence-three-point.subtask-A.dev.gold.txt', delimiter='\t', header=None)
    df_test = pd.read_csv('tweets/downloaded/gold/devtest/CLEAN_100_topics_100_tweets.sentence-three-point.subtask-A.devtest.gold.txt', delimiter='\t', header=None)


    X_train = df_train.values[:,0]
    y_train = df_train.values[:,1]

    X_dev = df_dev.values[:, 0]
    y_dev = df_dev.values[:, 1]

    X_dev = df_test.values[:, 0]
    y_dev = df_test.values[:, 1]

    vectorizer = TfidfVectorizer(vocabulary=set(neg_lexicon+pos_lexicon))  # sublinear_tf=True, max_df=0.5)
    X_train = vectorizer.fit_transform(X_train).toarray()
    X_dev = vectorizer.transform(X_dev).toarray()

    clf = GaussianNB()
    clf.fit(X_train, y_train)
    print('CLF ==== NB')
    print('Accuracy: %.2f' % accuracy_score(y_dev, clf.predict(X_dev)))

    X_train = sparse.csr_matrix(X_train)
    X_dev =  sparse.csr_matrix(X_dev)

    clf = SVC(kernel='poly', C=1, random_state=42)
    clf.fit(X_train, y_train)
    print('CLF ==== SVM poly')
    print('Accuracy: %.2f' % accuracy_score(y_dev, clf.predict(X_dev)))

    clf = SVC(kernel='linear', C=1, random_state=42)
    clf.fit(X_train, y_train)
    print('CLF ==== SVM linear')
    print('Accuracy: %.2f' % accuracy_score(y_dev, clf.predict(X_dev)))

    clf = SVC(kernel='rbf', C=1, random_state=42)
    clf.fit(X_train, y_train)
    print('CLF ==== SVM rbf')
    print('Accuracy: %.2f' % accuracy_score(y_dev, clf.predict(X_dev)))

    clf = DecisionTreeClassifier(random_state=42)
    clf.fit(X_train, y_train)
    print('CLF ==== DecisionTree')
    print('Accuracy: %.2f' % accuracy_score(y_dev, clf.predict(X_dev)))

    clf = KNeighborsClassifier(n_neighbors=1)
    clf.fit(X_train, y_train)
    print('CLF ==== KNN1')
    print('Accuracy: %.2f' % accuracy_score(y_dev, clf.predict(X_dev)))

    clf = KNeighborsClassifier(n_neighbors=3)
    clf.fit(X_train, y_train)
    print('CLF ==== KNN3')
    print('Accuracy: %.2f' % accuracy_score(y_dev, clf.predict(X_dev)))

    clf = KNeighborsClassifier(n_neighbors=5)
    clf.fit(X_train, y_train)
    print('CLF ==== KNN5')
    print('Accuracy: %.2f' % accuracy_score(y_dev, clf.predict(X_dev)))

    clf = AdaBoostClassifier(random_state=42)
    clf.fit(X_train, y_train)
    print('CLF ==== AdaBoost')
    print('Accuracy: %.2f' % accuracy_score(y_dev, clf.predict(X_dev)))


if __name__ == '__main__':
    main()



