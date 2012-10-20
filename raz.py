#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.core.management import setup_environ
from nemeria import settings
setup_environ(settings)
from nemeriatools.models import *

Ville.objects.all().delete()
Joueur.objects.all().delete()
Alliance.objects.all().delete()
