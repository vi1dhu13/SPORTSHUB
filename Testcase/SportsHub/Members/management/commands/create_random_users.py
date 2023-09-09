# import random
# # from faker import Faker
# from django.contrib.auth.hashers import make_password
# from django.core.management.base import BaseCommand
# from users.models import CustomUser
# from Members.models import FitnessUser, FitnessTrainer, SportsTrainer

# fake = Faker()

# class Command(BaseCommand):
#     help = 'Create random users with different roles'

#     def handle(self, *args, **kwargs):
#         roles = ['FitnessUser', 'FitnessTrainer', 'SportsTrainer']

#         for _ in range(10):
#             username = fake.user_name()
#             email = fake.email()
#             first_name = fake.first_name()
#             last_name = fake.last_name()
#             role = random.choice(roles)
#             description = fake.text()
#             password = make_password('password123')

#             custom_user = CustomUser.objects.create(
#                 username=username,
#                 email=email,
#                 first_name=first_name,
#                 last_name=last_name,
#                 role=role,
#                 description=description,
#                 password=password,
#             )

#             if role == 'FitnessUser':
#                 FitnessUser.objects.create(
#                     user=custom_user,
#                     fitness_goal=fake.random_element(elements=('Weight Loss', 'Muscle Gain')),
#                     height=fake.random_int(min=150, max=200),
#                     weight=fake.random_int(min=40, max=100),
#                 )
#             elif role == 'FitnessTrainer':
#                 FitnessTrainer.objects.create(
#                     user=custom_user,
#                     experience=fake.random_int(min=1, max=10),
#                     certification=fake.company_suffix(),
#                     training_goal=fake.random_element(elements=('Weight Loss', 'Muscle Gain')),
#                 )
#             elif role == 'SportsTrainer':
#                 SportsTrainer.objects.create(
#                     user=custom_user,
#                     specialization=fake.word(),
#                 )

#         self.stdout.write(self.style.SUCCESS('Random users created successfully.'))
