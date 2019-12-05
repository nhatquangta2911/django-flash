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
# import json
import numpy as np
import pandas as pd

@api_view(["POST"])
def predict(request):
    try:
        # mdl = joblib.load("./question_model.pkl")
        mydata = request.data
        # unit = np.array(list(mydata.values()))
        # unit = unit.reshape(1, -1)
        # X = mdl.transform(unit)
        # y_pred = mdl.predict(X)
        # y_pred = (y_pred > 0.5)
        # newdf = pd.DataFrame(y_pred, columns=['Result'])
        # newdf = newdf.replace({True: 'Positive', False: 'Negative'})
        # newdf = serializers.serialize('json', newdf)
        return JsonResponse(mydata, safe=False)
    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def train(request):
    try:
        
        return JsonResponse('Training sucks',safe=False)
    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)