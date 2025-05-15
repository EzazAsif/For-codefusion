from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Country
from .serializers import CountrySerializer
from django.db.models import Q
import json
from django.shortcuts import render, get_object_or_404
import json
from django.contrib.auth.decorators import login_required

class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

    # List same regional countries
    @action(detail=True, methods=['get'])
    def same_region(self, request, pk=None):
        country = self.get_object()
        region_countries = Country.objects.filter(region=country.region).exclude(pk=pk)
        serializer = self.get_serializer(region_countries, many=True)
        return Response(serializer.data)

    # List countries that speak the same language (given language code or name)
    @action(detail=False, methods=['get'])
    def by_language(self, request):
        lang = request.query_params.get('language', None)
        if not lang:
            return Response({"error": "language query param required"}, status=status.HTTP_400_BAD_REQUEST)

        countries = []
        for country in Country.objects.all():
            languages = json.loads(country.languages)
            if lang in languages.keys() or lang in languages.values():
                countries.append(country)

        serializer = self.get_serializer(countries, many=True)
        return Response(serializer.data)

    # Search countries by name (partial)
    def list(self, request, *args, **kwargs):
        search = request.query_params.get('search', None)
        queryset = self.queryset
        if search:
            queryset = queryset.filter(name__icontains=search)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

@login_required
def country_list_view(request):
    search = request.GET.get('search', '')
    if search:
        countries = Country.objects.filter(name__icontains=search)
    else:
        countries = Country.objects.all()

    # Convert JSON fields to Python lists/dicts for template usage
    for c in countries:
        c.timezones = json.loads(c.timezones)
        c.languages = json.loads(c.languages)

    return render(request, 'countries/country_list.html', {'countries': countries})

@login_required
def country_detail_view(request, pk):
    country = get_object_or_404(Country, pk=pk)
    country.timezones = json.loads(country.timezones)
    country.languages = json.loads(country.languages)

    same_region_countries = Country.objects.filter(region=country.region).exclude(pk=pk)
    for c in same_region_countries:
        c.timezones = json.loads(c.timezones)

    # Find countries speaking any of the languages of this country
    lang_values = set(country.languages.values())
    same_language_countries = []
    for c in Country.objects.exclude(pk=pk):
        langs = json.loads(c.languages).values()
        if lang_values.intersection(langs):
            same_language_countries.append(c)

    return render(request, 'countries/country_detail.html', {
        'country': country,
        'same_region_countries': same_region_countries,
        'same_language_countries': same_language_countries,
    })
