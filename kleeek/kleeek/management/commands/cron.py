# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from kleeek.kleeek.views import close_rooms, kill_rooms

class Command(BaseCommand):
  
    # def handle(self, *args, **options):
    #     print args

    def handle(self, *args, **options):#_noargs(self, *args, **options):
        close_rooms('')
        kill_rooms('')