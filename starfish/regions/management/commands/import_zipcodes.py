from django.core.management.base import BaseCommand
from uszipcode import SearchEngine

from regions.models import State, Zip

STATE_NAMES = {
    "AL": "Alabama",
    "AK": "Alaska",
    "AZ": "Arizona",
    "AR": "Arkansas",
    "CA": "California",
    "CO": "Colorado",
    "CT": "Connecticut",
    "DE": "Delaware",
    "FL": "Florida",
    "GA": "Georgia",
    "HI": "Hawaii",
    "ID": "Idaho",
    "IL": "Illinois",
    "IN": "Indiana",
    "IA": "Iowa",
    "KS": "Kansas",
    "KY": "Kentucky",
    "LA": "Louisiana",
    "ME": "Maine",
    "MD": "Maryland",
    "MA": "Massachusetts",
    "MI": "Michigan",
    "MN": "Minnesota",
    "MS": "Mississippi",
    "MO": "Missouri",
    "MT": "Montana",
    "NE": "Nebraska",
    "NV": "Nevada",
    "NH": "New Hampshire",
    "NJ": "New Jersey",
    "NM": "New Mexico",
    "NY": "New York",
    "NC": "North Carolina",
    "ND": "North Dakota",
    "OH": "Ohio",
    "OK": "Oklahoma",
    "OR": "Oregon",
    "PA": "Pennsylvania",
    "RI": "Rhode Island",
    "SC": "South Carolina",
    "SD": "South Dakota",
    "TN": "Tennessee",
    "TX": "Texas",
    "UT": "Utah",
    "VT": "Vermont",
    "VA": "Virginia",
    "WA": "Washington",
    "WV": "West Virginia",
    "WI": "Wisconsin",
    "WY": "Wyoming",
    "DC": "District of Columbia",
}


class Command(BaseCommand):
    help = (
        "Import U.S. zip codes and their corresponding states using uszipcode (v1.0+)"
    )

    def handle(self, *args, **kwargs):
        search = SearchEngine()
        created = 0
        skipped = 0

        for code, name in STATE_NAMES.items():
            State.objects.get_or_create(code=code, defaults={"name": name})

        # The new uszipcode requires searching by state one at a time
        for state_code in STATE_NAMES.keys():
            results = search.by_state(state_code, returns=1000)
            for record in results:
                zip_code = record.zipcode
                if not zip_code:
                    skipped += 1
                    continue

                state = State.objects.get(code=state_code)
                _, was_created = Zip.objects.get_or_create(
                    code=zip_code, defaults={"state": state}
                )
                if was_created:
                    created += 1

        self.stdout.write(
            self.style.SUCCESS(f"Imported {created} zip codes, skipped {skipped}")
        )
