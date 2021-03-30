from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User, Permission
from django.contrib.auth.models import Group


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(name='contributor')
        superuser = User.objects.create_superuser('admin', 'admin@gmail.com', '1UT2BM9O')
