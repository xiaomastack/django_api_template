# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from account.models import User


class Command(BaseCommand):
    help = 'generate api_secret for specified username'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='username')
        parser.add_argument(
            '--create',
            action='store_true',
            dest='create',
            default=False,
            help='Whether create user if username not exist')

    def handle(self, *args, **options):
        try:
            user = User.objects.get(username=options['username'])
        except User.DoesNotExist:
            self.stdout.write('User %s does not exist.' % options['username'])
            if not options['create']:
                return
            self.stdout.write('Create user %s.' % options['username'])
            user = User.objects.create(username=options['username'])
        if not user.api_secret:
            user.generate_api_secret()
        else:
            self.stdout.write('api_secret aleady exist.')
        self.stdout.write('api_key: %s' % user.username)
        self.stdout.write('api_secret: %s' % user.api_secret)
