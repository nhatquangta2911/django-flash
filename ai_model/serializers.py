from rest_framework import serializers
from .models import Result


class ResultSerializers(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = '__all__'
