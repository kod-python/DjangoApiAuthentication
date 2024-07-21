# your_app/management/commands/hash_passwords.py

from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from trial.models import Authentic

class Command(BaseCommand):
    help = 'Hashes all plain-text passwords in the Authentic model'

    def handle(self, *args, **kwargs):
        users = Authentic.objects.all()
        for user in users:
            if not user.password.startswith('pbkdf2_'):  # Assuming 'pbkdf2_' is the prefix for hashed passwords
                user.password = make_password(user.password)
                user.save()
                self.stdout.write(self.style.SUCCESS(f'Password for {user.email} hashed successfully'))
            else:
                self.stdout.write(self.style.WARNING(f'Password for {user.email} is already hashed'))
