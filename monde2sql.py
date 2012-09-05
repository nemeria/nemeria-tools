#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import urllib
from django.core.management import setup_environ
from nemeria import settings

setup_environ(settings)
from nemeriatools.models import Monde,Alliance,Joueur,Ville

Ville.objects.all().delete()
Joueur.objects.all().delete()
Alliance.objects.all().delete()

for monde in Monde.objects.all():
    urllib.urlretrieve("http://"+monde.nom+".nemeria.com/img/carte.png","nemeriatools/static/img/"+monde.nom+".png")
    mondeJson=json.loads(urllib.urlopen("http://"+monde.nom+".nemeria.com/ext/json").read())
    for allianceJson in mondeJson['alliances']:
        Alliance(id=allianceJson['id'],
            nom=allianceJson['nom'],
            pop=allianceJson['population'],
            classement=allianceJson['classement'],
            monde=monde
        ).save()
    for joueurJson in mondeJson['joueurs']:
        alliance=None
        try: alliance=Alliance.objects.get(id=joueurJson['alliance'],monde=monde.id)
        except: pass # = pas d'alliance, on laisse à None
        joueur=Joueur(id=joueurJson['id'],
            nom=joueurJson['nom'],
            pop=joueurJson['population'],
            classement=joueurJson['classement'],
            alliance=alliance,
            monde=monde
        )
        joueur.save()
        for villeJson in joueurJson['villes']:
            Ville(id=villeJson['id'],
                nom=villeJson['nom'],
                terrain=villeJson['terrain'],
                pop=villeJson['population'],
                joueur=joueur,
            ).save()
