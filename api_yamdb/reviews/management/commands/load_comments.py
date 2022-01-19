import csv

import requests
from django.core.management.base import BaseCommand
from reviews.models import Comment


class Command(BaseCommand):
    help = 'Loading data from csv via url'

    def add_arguments(self, parser):
        parser.add_argument('link', type=str)

    def handle(self, link: str, *args, **options):
        response = requests.get(link)
        reader = csv.DictReader(response.text.splitlines())

        Comment.objects.bulk_create(
            [Comment(
                **{k.lower(): v for k, v in data.items()}
            ) for data in reader]
        )

        self.stdout.write(self.style.SUCCESS('Successfully loaded'))
