#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from django.core.management import setup_environ
from nemeria import settings
setup_environ(settings)
from nemeriatools.models import *

if len(sys.argv) != 2:
    print "Usage: " + sys.argv[0] + " <monde>"
    exit(1)
try:
    Monde.objects.get(nom=sys.argv[1])
except:
    print "Ce monde n'existe pas."
    exit(1)
else:
    print "Suppression des villes..."
    Ville.objects.filter(monde__nom=sys.argv[1]).delete()
    print "Suppression des joueurs..."
    Joueur.objects.filter(monde__nom=sys.argv[1]).delete()
    print "Suppression des alliances..."
    Alliance.objects.filter(monde__nom=sys.argv[1]).delete()
    print "Fait."

