from django.core.management.base import BaseCommand, CommandError

from tasks.models import User, Team

import pytz
from faker import Faker
from random import randint, random, sample

user_fixtures = [
    {
        "username": "@johndoe",
        "email": "john.doe@example.org",
        "first_name": "John",
        "last_name": "Doe",
        "super_user": True,
    },
    {
        "username": "@janedoe",
        "email": "jane.doe@example.org",
        "first_name": "Jane",
        "last_name": "Doe",
        "super_user": False,
    },
    {
        "username": "@charlie",
        "email": "charlie.johnson@example.org",
        "first_name": "Charlie",
        "last_name": "Johnson",
        "super_user": False,
    },
]

team_fixtures = [
    {
        "name": "Alpha",
        "description": "Alpha description",
        "members": ["@johndoe", "@charlie", "@janedoe"],
    },
    {"name": "Beta", "description": "Beta description", "members": []},
    {"name": "Charlie", "description": "Charlie description", "members": []},
    {"name": "Delta", "description": "Delta description", "members": []},
    {"name": "Echo", "description": "Echo description", "members": []},
    {"name": "Foxtrot", "description": "Foxtrot description", "members": []},
    {"name": "Gold", "description": "Gold description", "members": []},
    {"name": "Halo", "description": "Halo description", "members": []},
]


# TODO team leader stuff
class Command(BaseCommand):
    """Build automation command to seed the database."""

    USER_COUNT = 100
    TEAM_COUNT = 100
    DEFAULT_PASSWORD = "Password123"
    help = "Seeds the database with sample data for user and teams"

    def __init__(self):
        self.faker = Faker("en_GB")

    def handle(self, *args, **options):
        self.create_users()
        self.users = User.objects.all()
        self.create_teams()
        self.teams = Team.objects.all()

    def create_users(self):
        self.generate_user_fixtures()
        self.generate_random_users()

    def generate_user_fixtures(self):
        for data in user_fixtures:
            self.try_create_user(data)

    def generate_random_users(self):
        user_count = User.objects.count()
        while user_count < self.USER_COUNT:
            print(f"Seeding user {user_count}/{self.USER_COUNT}", end="\r")
            self.generate_user()
            user_count = User.objects.count()
        print("User seeding complete.      ")

    def generate_user(self):
        first_name = self.faker.first_name()
        last_name = self.faker.last_name()
        email = self.create_email(first_name, last_name)
        username = self.create_username(first_name, last_name)

        self.try_create_user(
            {
                "username": username,
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
                "super_user": False,
            }
        )

    def create_username(self, first_name, last_name):
        return "@" + first_name.lower() + last_name.lower()

    def create_email(self, first_name, last_name):
        return first_name + "." + last_name + "@example.org"

    def try_create_user(self, data):
        try:
            self.create_user(data)
        except:
            pass

    def create_user(self, data):
        if not data["super_user"] == True:
            User.objects.create_user(
                username=data["username"],
                email=data["email"],
                password=Command.DEFAULT_PASSWORD,
                first_name=data["first_name"],
                last_name=data["last_name"],
            )
        else:
            User.objects.create_superuser(
                username=data["username"],
                email=data["email"],
                password=Command.DEFAULT_PASSWORD,
                first_name=data["first_name"],
                last_name=data["last_name"],
            )

    def create_teamname(self):
        return self.faker.company()

    def create_teams(self):
        self.generate_team_fixtures()
        self.generate_random_teams()

    def generate_team_fixtures(self):
        for data in team_fixtures:
            data["members"] = self.convert_usernames_to_objects(data["members"])
            self.try_create_team(data)

    def generate_random_teams(self):
        team_count = Team.objects.count()
        while team_count < self.TEAM_COUNT:
            print(f"Seeding team {team_count}/{self.TEAM_COUNT}", end="\r")
            self.generate_team()
            team_count = Team.objects.count()

    def get_random_users(self, count):
        return sample(list(self.users), count)

    def generate_team(self):
        team = {
            "name": self.create_teamname(),
            "description": self.create_description(),
            "members": self.get_random_users(randint(3, 6)),
        }
        self.try_create_team(team)

    def convert_usernames_to_objects(self, usernames):
        return User.objects.filter(username__in=usernames)

    def try_create_team(self, data):
        try:
            self.create_team(data)
        except Exception as e:
            print(e)
            pass

    def create_team(self, data):
        team = Team.objects.create(name=data["name"], description=data["description"])
        team.members.add(data["members"])
        return team

    def create_description(self):
        return self.faker.sentence()
