import environ
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from ...models import UserProfile
env = environ.Env()
environ.Env.read_env()

class Command(BaseCommand):
    help = 'Create a superuser with ADMIN role if none exists'

    def handle(self, *args, **options):
        User = get_user_model()
        if not User.objects.filter(is_superuser=True).exists():
            email = env('SUPERUSER_EMAIL', default='admin@example.com')
            password = env('SUPERUSER_PASSWORD', default='securepassword')
            username = env('SUPERUSER_NAME', default='admin')
            
            user = User.objects.create_superuser(email=email, password=password, username=username)
            UserProfile.objects.create(user=user, role=UserProfile.Role.ADMIN)
            
            self.stdout.write(self.style.SUCCESS(f'Superuser with email "{email}" created successfully with ADMIN role.'))
        else:
            self.stdout.write(self.style.SUCCESS('Superuser already exists.'))
