from rest_framework import serializers
from .models import Country
import json

class CountrySerializer(serializers.ModelSerializer):
    timezones = serializers.SerializerMethodField()
    languages = serializers.SerializerMethodField()

    def get_timezones(self, obj):
        return json.loads(obj.timezones)

    def get_languages(self, obj):
        return json.loads(obj.languages)

    class Meta:
        model = Country
        fields = ['id', 'name', 'cca2', 'capital', 'population', 'timezones', 'region', 'languages', 'flag_url']
