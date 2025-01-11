import uuid
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
import environ
from ...models import UserProfile, 
from Bankist.models import Bankist
from django.contrib.auth.hashers import make_password, check_password


env = environ.Env()
environ.Env.read_env()

def account_num_generator():
    return str(uuid.uuid4().int)[:10]

class Command(BaseCommand):
    help = 'Create a superuser with ADMIN role and a bank account if none exists'

    def handle(self, *args, **options):
        User = get_user_model()
        if not User.objects.filter(is_superuser=True).exists():
            email = env('SUPERUSER_EMAIL', default='admin@example.com')
            password = env('SUPERUSER_PASSWORD', default='securepassword')
            username = env('SUPERUSER_NAME', default='admin')
            
            
            user = User.objects.create_superuser(email=email, password=password, username=username)
            
            
            user_profile = UserProfile.objects.create(user=user, role=UserProfile.Role.ADMIN)
            
           
            bank_account = Bankist.objects.create(
                user_profile=user_profile,
                pin='1234' 
            )
            
            self.stdout.write(self.style.SUCCESS(f'Superuser with email "{email}" created successfully with ADMIN role and bank account.'))
        else:
            self.stdout.write(self.style.SUCCESS('Superuser already exists.'))
