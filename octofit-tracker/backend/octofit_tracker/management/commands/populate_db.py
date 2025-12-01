from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Workout, Leaderboard
from django.db import connection

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        self.stdout.write('Deleting old data...')
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Workout.objects.all().delete()
        Leaderboard.objects.all().delete()

        self.stdout.write('Creating teams...')
        marvel = Team.objects.create(name='Marvel')
        dc = Team.objects.create(name='DC')

        self.stdout.write('Creating users...')
        tony = User.objects.create(name='Tony Stark', email='tony@marvel.com', team=marvel)
        steve = User.objects.create(name='Steve Rogers', email='steve@marvel.com', team=marvel)
        bruce = User.objects.create(name='Bruce Banner', email='bruce@marvel.com', team=marvel)
        clark = User.objects.create(name='Clark Kent', email='clark@dc.com', team=dc)
        diana = User.objects.create(name='Diana Prince', email='diana@dc.com', team=dc)
        barry = User.objects.create(name='Barry Allen', email='barry@dc.com', team=dc)

        self.stdout.write('Creating activities...')
        Activity.objects.create(user=tony, type='run', duration=30, date='2025-12-01')
        Activity.objects.create(user=steve, type='swim', duration=45, date='2025-12-01')
        Activity.objects.create(user=clark, type='fly', duration=60, date='2025-12-01')
        Activity.objects.create(user=diana, type='fight', duration=50, date='2025-12-01')

        self.stdout.write('Creating workouts...')
        w1 = Workout.objects.create(name='Pushups', description='Do 50 pushups')
        w2 = Workout.objects.create(name='Sprints', description='Run 5x100m sprints')
        w1.suggested_for.add(marvel)
        w2.suggested_for.add(dc)

        self.stdout.write('Creating leaderboard...')
        Leaderboard.objects.create(team=marvel, points=150)
        Leaderboard.objects.create(team=dc, points=120)

        self.stdout.write(self.style.SUCCESS('Database populated with test data!'))

        # Ensure unique index on email
        with connection.cursor() as cursor:
            cursor.execute('db.users.createIndex({ "email": 1 }, { unique: true })')
        self.stdout.write(self.style.SUCCESS('Unique index on email ensured.'))
