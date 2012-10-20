#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import urllib
from django.core.management import setup_environ
from nemeria import settings

setup_environ(settings)
from nemeriatools.models import *

#~ Ville.objects.all().delete()
#~ Joueur.objects.all().delete()
#~ Alliance.objects.all().delete()
# A utiliser si besoin de RAZ

for monde in Monde.objects.all():
    urllib.urlretrieve("http://"+monde.nom+".nemeria.com/img/carte.png","nemeriatools/static/img/"+monde.nom+".png")
    mondeJson=json.loads(urllib.urlopen("http://"+monde.nom+".nemeria.com/ext/json").read())
    for allianceJson in mondeJson['alliances']:
        try: alliance=Alliance.objects.get(id=allianceJson['id'],monde=monde)
        except:
            print "Nouvelle alliance sur",monde.nom,":",allianceJson['nom']
            alliance=Alliance()
        alliance.id=allianceJson['id']
        alliance.nom=allianceJson['nom']
        alliance.pop=allianceJson['population']
        alliance.classement=allianceJson['classement']
        alliance.monde=monde
        alliance.save()
    for joueurJson in mondeJson['joueurs']:
        alliance=None
        try: alliance=Alliance.objects.get(id=joueurJson['alliance'],monde=monde)
        except: pass # = pas d'alliance, on laisse à None
        try: joueur=Joueur.objects.get(id=joueurJson['id'],monde=monde)
        except:
            print "Un joueur s'est inscrit sur", monde.nom,":", joueurJson['nom']
            joueur=Joueur()
        joueur.id=joueurJson['id']
        joueur.nom=joueurJson['nom']
        joueur.pop=joueurJson['population']
        joueur.classement=joueurJson['classement']
        joueur.alliance=alliance
        joueur.monde=monde
        joueur.save()
        for villeJson in joueurJson['villes']:
            try: ville=Ville.objects.get(id=villeJson['id'],joueur=joueur)
            except:
                print "Nouvelle ville sur", monde.nom,"de",joueurJson['nom'],":", villeJson['nom']
                ville=Ville()
            ville.id=villeJson['id']
            ville.nom=villeJson['nom']
            ville.terrain=villeJson['terrain']
            ville.pop=villeJson['population']
            ville.joueur=joueur
            ville.save()
