#IMPORT LIBRARY
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix
from imblearn.over_sampling import SMOTE
from sklearn.preprocessing import MinMaxScaler
import warnings
from collections import Counter
warnings.filterwarnings('ignore')
from keras import Sequential
from keras.layers import Dense
from keras import backend as K
from rest_framework.decorators import api_view
# from django.core import serializers
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
# from rest_framework.parsers import JSONParser
from .models import Result
from .serializers import ResultSerializers
import pickle
from sklearn.externals import joblib
import json
import datetime

@api_view(["POST"])
def predict(request):
    try:
        model = joblib.load("./question_model.pkl")
        mydata = request.data
        sc = MinMaxScaler()
        w = np.array([[3, 4, 1, 1, 3, 3, 2, 2], [3, 4, 1, 1, 2, 2, 2, 1], [mydata['Question_Period'], mydata['Question_Type'], mydata['Question_Content_Type'], mydata['Gender'], mydata['Goal'], mydata['Activity_Level'], mydata['Body_Fat'], mydata['Job']]])
        w = w.reshape(-3, 8)
        X_test = sc.fit_transform(w)
        y_pred = model.predict(X_test) 
        return Response({ "result" : y_pred })
    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def train(request):
    try:
        beginning = datetime.datetime.now()
        df = pd.read_csv('new_dataset.csv')
        df = df.dropna()
        df.isna().any()
        Counter(df['Answer_Result'])
        pre_y = df['Answer_Result']
        pre_X = df.drop('Answer_Result', axis=1)
        dm_X = pd.get_dummies(pre_X)
        dm_y = pre_y.map(dict(Positive=1, Negative=0))
        smote = SMOTE(ratio='minority')
        X1, y = smote.fit_sample(dm_X, dm_y)
        sc = MinMaxScaler()
        X = sc.fit_transform(X1)
        Counter(y)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, shuffle=True)
        classifier = Sequential()
        classifier.add(Dense(request.data['node1'], activation=request.data['af1'], kernel_initializer='random_normal', input_dim=X_test.shape[1]))
        classifier.add(Dense(request.data['node2'], activation=request.data['af2'], kernel_initializer='random_normal'))
        classifier.add(Dense(request.data['node3'], activation=request.data['af3'], kernel_initializer='random_normal'))
        classifier.add(Dense(1, activation='sigmoid', kernel_initializer='random_normal'))
        classifier.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        classifier.fit(X_train, y_train, batch_size=20, epochs=request.data['epochs'])
        eval_model = classifier.evaluate(X_train, y_train)
        joblib.dump(classifier, 'question_model.pkl')
        ending = datetime.datetime.now()
        K.clear_session()
        return Response({ "process_status": "done", "duration": (ending - beginning) * 1000 })
    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)