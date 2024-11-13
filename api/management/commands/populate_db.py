import random
from django.core.management.base import BaseCommand
from faker import Faker
from api.models import User, Contact, Spam

fake = Faker()

class Command(BaseCommand):
    help = 'Populate the database with random sample data'

    def add_arguments(self, parser):
        parser.add_argument('--users', type=int, default=10, help='Number of users to create')
        parser.add_argument('--contacts', type=int, default=50, help='Number of contacts to create per user')
        parser.add_argument('--spams', type=int, default=20, help='Number of spam numbers to generate')

    def handle(self, *args, **kwargs):
        num_users = kwargs['users']
        num_contacts = kwargs['contacts']
        num_spams = kwargs['spams']

        self.stdout.write(self.style.SUCCESS(f'Creating {num_users} users...'))
        users = self._create_users(num_users)

        self.stdout.write(self.style.SUCCESS(f'Creating {num_contacts} contacts per user...'))
        self._create_contacts(users, num_contacts)

        self.stdout.write(self.style.SUCCESS(f'Creating {num_spams} spam entries...'))
        self._create_spam_numbers(num_spams)

        self.stdout.write(self.style.SUCCESS('Database populated successfully!'))

    def _create_users(self, num_users):
        users = []
        for _ in range(num_users):
            username = fake.unique.user_name()
            phone_number = self._generate_phone_number()  
            email = fake.unique.email()

            user = User.objects.create_user(
                username=username,
                password='password123', 
                phone_number=phone_number,
                email=email
            )
            users.append(user)
        return users

    def _create_contacts(self, users, num_contacts):
        for user in users:
            contacts_set = set()
            for _ in range(num_contacts):
                name = fake.name()
                phone_number = self._generate_phone_number()

                if phone_number not in contacts_set:
                    contacts_set.add(phone_number)
                    Contact.objects.create(
                        owner=user,
                        name=name,
                        phone_number=phone_number
                    )

    def _create_spam_numbers(self, num_spams):
        spam_set = set()
        for _ in range(num_spams):
            phone_number = self._generate_phone_number()
            spam_reports = random.randint(1, 10)

           
            if phone_number not in spam_set:
                spam_set.add(phone_number)
                Spam.objects.create(
                    phone_number=phone_number,
                    spam_reports=spam_reports
                )

    def _generate_phone_number(self):
        return fake.unique.numerify(text="##########")  