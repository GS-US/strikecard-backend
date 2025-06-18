# CSV of ZIP codes available for free at
# https://www.unitedstateszipcodes.org/zip-code-database/

from django.core.management.base import BaseCommand
from regions.models import State, Zip

STATE_NAMES = {
    'AL': 'Alabama',
    'AK': 'Alaska',
    'AZ': 'Arizona',
    'AR': 'Arkansas',
    'CA': 'California',
    'CO': 'Colorado',
    'CT': 'Connecticut',
    'DE': 'Delaware',
    'FL': 'Florida',
    'GA': 'Georgia',
    'HI': 'Hawaii',
    'ID': 'Idaho',
    'IL': 'Illinois',
    'IN': 'Indiana',
    'IA': 'Iowa',
    'KS': 'Kansas',
    'KY': 'Kentucky',
    'LA': 'Louisiana',
    'ME': 'Maine',
    'MD': 'Maryland',
    'MA': 'Massachusetts',
    'MI': 'Michigan',
    'MN': 'Minnesota',
    'MS': 'Mississippi',
    'MO': 'Missouri',
    'MT': 'Montana',
    'NE': 'Nebraska',
    'NV': 'Nevada',
    'NH': 'New Hampshire',
    'NJ': 'New Jersey',
    'NM': 'New Mexico',
    'NY': 'New York',
    'NC': 'North Carolina',
    'ND': 'North Dakota',
    'OH': 'Ohio',
    'OK': 'Oklahoma',
    'OR': 'Oregon',
    'PA': 'Pennsylvania',
    'RI': 'Rhode Island',
    'SC': 'South Carolina',
    'SD': 'South Dakota',
    'TN': 'Tennessee',
    'TX': 'Texas',
    'UT': 'Utah',
    'VT': 'Vermont',
    'VA': 'Virginia',
    'WA': 'Washington',
    'WV': 'West Virginia',
    'WI': 'Wisconsin',
    'WY': 'Wyoming',
    'DC': 'District of Columbia',
    'PR': 'Puerto Rico',
}

import csv

from django.core.management.base import BaseCommand
from regions.models import Zip


class Command(BaseCommand):
    help = 'Import ZIP codes from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str)

    def handle(self, *args, **options):
        for code, name in STATE_NAMES.items():
            State.objects.update_or_create(code=code, defaults={'name': name})

        with open(options['csv_file'], newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    Zip.objects.update_or_create(
                        code=row['zip'],
                        defaults={
                            'type': row['type'] or None,
                            'primary_city': row['primary_city'] or None,
                            'acceptable_cities': row['acceptable_cities'] or None,
                            'state_id': row['state'],
                            'county': row['county'] or None,
                            'timezone': row['timezone'] or None,
                            'area_codes': row['area_codes'] or None,
                            'latitude': (
                                float(row['latitude']) if row['latitude'] else None
                            ),
                            'longitude': (
                                float(row['longitude']) if row['longitude'] else None
                            ),
                            'population': (
                                int(row['irs_estimated_population'])
                                if row['irs_estimated_population']
                                else None
                            ),
                        },
                    )
                except:
                    pass
