from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from reviews.models import Review
from faker import Faker
from faker.providers import lorem, company, phone_number, date_time
import random
from datetime import timedelta
from django.utils import timezone
from django.conf import settings

User = get_user_model()

SAMPLE_REVIEWS = [
    "Great service! Will definitely use again.",
    "Average experience, nothing special.",
    "Terrible customer support. Avoid at all costs.",
    "Product was exactly as described.",
    "Shipping took longer than expected.",
    "Excellent quality for the price.",
    "Not worth the money in my opinion.",
    "Highly recommend this service!",
    "Had some issues but they were resolved quickly.",
    "Would give zero stars if I could."
]

class Command(BaseCommand):
    help = 'Generates fake review data for testing purposes'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=50,
            help='Number of reviews to create (default: 50)'
        )
        parser.add_argument(
            '--users',
            type=int,
            default=5,
            help='Number of users to associate with reviews (default: 5)'
        )
        parser.add_argument(
            '--delete',
            action='store_true',
            help='Delete all existing reviews before creating new ones'
        )

    def handle(self, *args, **options):
        if not settings.DEBUG:
            self.stdout.write(self.style.ERROR(
                'This command can only be run in DEBUG mode'
            ))
            return

        fake = Faker()
        fake.add_provider(lorem)
        fake.add_provider(company)
        fake.add_provider(phone_number)
        fake.add_provider(date_time)
        
        count = options['count']
        user_count = options['users']
        delete_existing = options['delete']

        confirm = input(
            f'This will create {count} fake reviews for {user_count} users. Continue? [y/N] '
        )
        if confirm.lower() != 'y':
            self.stdout.write(self.style.WARNING('Operation cancelled'))
            return

        if delete_existing:
            deleted_count, _ = Review.objects.all().delete()
            self.stdout.write(
                self.style.WARNING(f'Deleted {deleted_count} existing reviews')
            )

        # Create or get test users
        users = []
        for i in range(user_count):
            username = f'testuser{i+1}'
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': f'{username}@example.com',
                    'company_name': fake.company(),
                    'phone': fake.phone_number(),
                    'password': 'testpass123'
                }
            )
            users.append(user)
            self.stdout.write(self.style.SUCCESS(f'Created/retrieved user: {username}'))

        # Location data for realistic distribution
        locations = [
            {'name': 'New York', 'lat': 40.7128, 'lng': -74.0060},
            {'name': 'London', 'lat': 51.5074, 'lng': -0.1278},
            {'name': 'Tokyo', 'lat': 35.6762, 'lng': 139.6503},
            {'name': 'Sydney', 'lat': -33.8688, 'lng': 151.2093},
            {'name': 'Berlin', 'lat': 52.5200, 'lng': 13.4050},
        ]

        # Generate reviews
        for i in range(count):
            user = random.choice(users)
            location = random.choice(locations)
            rating = random.randint(1, 5)
            days_ago = random.randint(0, 365)
            
            review_text = random.choice(SAMPLE_REVIEWS)
            if random.random() > 0.3:  # 70% chance to add more text
                review_text += " " + fake.paragraph(nb_sentences=random.randint(1, 3))
            
            review = Review.objects.create(
                user=user,
                text=review_text,
                rating=rating,
                sentiment=self._get_sentiment(rating),
                location_name=location['name'],
                latitude=location['lat'] + random.uniform(-0.5, 0.5),
                longitude=location['lng'] + random.uniform(-0.5, 0.5),
                is_public=random.choice([True, False]),
                created_at=timezone.now() - timedelta(days=days_ago)
            )
            
            if i % 10 == 0:
                self.stdout.write(f'Created review {i+1}/{count}')

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {count} reviews for {user_count} users')
        )

    def _get_sentiment(self, rating):
        if rating >= 4:
            return 'positive'
        elif rating <= 2:
            return 'negative'
        return 'neutral'
