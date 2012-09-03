from django.template import Context, loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from nemeriatools.models import *
from django.shortcuts import render_to_response
def home(request):
    return render_to_response('home.html')
#### JOUEURS
def joueur_detail(request,joueur_autoinc):
    return render_to_response('joueur/detail.html',{"joueur": Joueur.objects.get(pk=joueur_autoinc)})

def joueur_index(request):
    nom = request.GET.get('nom','')
    monde = request.GET.get('monde','')
    alliance = request.GET.get('alliance','')
    joueur_list=Joueur.objects.filter(
        nom__icontains=nom,
        monde__nom__icontains=monde,
        alliance__nom__icontains=alliance,
    )
    return render_to_response('joueur/list.html',{"joueurs": joueur_list, })
#### ALLIANCES
def alliance_detail(request,alliance_autoinc):
    return render_to_response('alliance/detail.html',{"alliance": Alliance.objects.get(pk=alliance_autoinc)})

def alliance_index(request):
    nom = request.GET.get('nom','')
    monde = request.GET.get('monde','')
    alliance_list=Alliance.objects.filter(
        nom__icontains=nom,
        monde__nom__icontains=monde,
    )
    return render_to_response('alliance/list.html',{"alliances": alliance_list})
#### VILLES
def ville_detail(request,ville_autoinc):
    return render_to_response('ville/detail.html',{"ville": Ville.objects.get(pk=ville_autoinc)})

def ville_index(request):
    nom = request.GET.get('nom','')
    monde = request.GET.get('monde','')
    joueur = request.GET.get('joueur','')
    alliance = request.GET.get('alliance','')
    ville_list=Ville.objects.filter(
        nom__icontains=nom,
        joueur__monde__nom__icontains=monde,
        joueur__nom__icontains=joueur,
        joueur__alliance__nom__icontains=alliance
    )
    return render_to_response('ville/list.html',{"villes": ville_list})
