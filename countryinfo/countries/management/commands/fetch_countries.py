import requests
import json
from django.core.management.base import BaseCommand
from countries.models import Country

class Command(BaseCommand):
    help = 'Fetch country data from restcountries API and store in DB'

    def handle(self, *args, **kwargs):
        url = 'https://restcountries.com/v3.1/all'
        response = requests.get(url)
        data = response.json()

        for c in data:
            name = c.get('name', {}).get('common')
            cca2 = c.get('cca2')
            capitals = c.get('capital', [])
            capital = capitals[0] if capitals else ''
            population = c.get('population', 0)
            timezones = c.get('timezones', [])
            region = c.get('region', '')
            languages_dict = c.get('languages', {})
            languages = json.dumps(languages_dict)  # Store JSON string
            flag_url = c.get('flags', {}).get('png', '')

            country, created = Country.objects.update_or_create(
                cca2=cca2,
                defaults={
                    'name': name,
                    'capital': capital,
                    'population': population,
                    'timezones': json.dumps(timezones),
                    'region': region,
                    'languages': languages,
                    'flag_url': flag_url,
                }
            )
            if created:
                self.stdout.write(f"Added {name}")
            else:
                self.stdout.write(f"Updated {name}")
