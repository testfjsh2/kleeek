# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from kleeek.kleeek.views import set_day_bonus

class Command(BaseCommand):
  
    # def handle(self, *args, **options):
    #     print args

    def handle(self, *args, **options):#_noargs(self, *args, **options):
        set_day_bonus('')