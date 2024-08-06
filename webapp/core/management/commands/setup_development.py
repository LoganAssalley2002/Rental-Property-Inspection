from django.core.management import call_command
from django.core.management.base import BaseCommand

from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission

from core.models import Profile


class Command(BaseCommand):
    help = 'Prepares development environment'

    def handle(self, *args, **options):
        '''Prepares development environment:

            1. Create "Inspector" group
            2. Create a superuser and add to "Inspector" group
            3. Create a test user
        '''
        # Create "Inspector" group
        inspector_group, _ = Group.objects.get_or_create(name='Inspector')
        inspector_group.permissions.add(*Permission.objects.all())

        # Create super user
        call_command('createsuperuser', no_input=False, username='hand', email='')

        for user in User.objects.filter(is_superuser=True):
            # Create Profile instances for superusers
            if not Profile.objects.filter(user=user).exists():
                Profile.objects.create(user=user)

            # Add superusers to "Inspector" group
            user.groups.add(inspector_group)

        # Create regular user
        regular_user = User.objects.create(username='regular_user', password='somePassword')
        regular_user.set_password('somePassword')
        regular_user.save()
        Profile.objects.create(user=regular_user)
