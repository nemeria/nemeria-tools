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
    order = request.GET.get('order_by','autoinc')
    page = request.GET.get('page',1)
    joueur_list=None
    if alliance == '':
	joueur_list=Joueur.objects.filter(
	    nom__icontains=nom,
	    monde__nom__icontains=monde,
	).order_by(order)
    else:
	joueur_list=Joueur.objects.filter(
	    nom__icontains=nom,
	    monde__nom__icontains=monde,
	    alliance__nom__icontains=alliance,
	).order_by(order)
    paginator = Paginator(joueur_list, 50)
    try: joueurs = paginator.page(page)
    except PageNotAnInteger: joueurs = paginator.page(1)
    except EmptyPage: joueurs = paginator.page(paginator.num_pages)
    return render_to_response('joueur/list.html',{
	"joueurs": joueurs,
	"nom": nom,
	"monde": monde,
	"alliance": alliance,
	"order": order,
	"monde_list": Monde.objects.all()
    })
#### ALLIANCES
def alliance_detail(request,alliance_autoinc):
    return render_to_response('alliance/detail.html',{"alliance": Alliance.objects.get(pk=alliance_autoinc)})

def alliance_index(request):
    nom = request.GET.get('nom','')
    monde = request.GET.get('monde','')
    order = request.GET.get('order_by','autoinc')
    page = request.GET.get('page',1)
    alliance_list=Alliance.objects.filter(
        nom__icontains=nom,
        monde__nom__icontains=monde,
    ).order_by(order)
    paginator = Paginator(alliance_list, 50)
    try: alliances = paginator.page(page)
    except PageNotAnInteger: alliances = paginator.page(1)
    except EmptyPage: alliances = paginator.page(paginator.num_pages)
    return render_to_response('alliance/list.html',{
	"alliances": alliances,
	"nom": nom,
	"monde": monde,
	"order": order,
	"monde_list": Monde.objects.all()
    })
#### VILLES
def ville_detail(request,ville_autoinc):
    return render_to_response('ville/detail.html',{"ville": Ville.objects.get(pk=ville_autoinc)})

def ville_index(request):
    nom = request.GET.get('nom','')
    monde = request.GET.get('monde','')
    joueur = request.GET.get('joueur','')
    alliance = request.GET.get('alliance','')
    order = request.GET.get('order_by','autoinc')
    page = request.GET.get('page',1)
    ville_list=None
    if alliance == '':
	ville_list=Ville.objects.filter(
	    nom__icontains=nom,
	    joueur__monde__nom__icontains=monde,
	    joueur__nom__icontains=joueur,
	).order_by(order)
    else:
	ville_list=Ville.objects.filter(
	nom__icontains=nom,
	    joueur__monde__nom__icontains=monde,
	    joueur__nom__icontains=joueur,
	    joueur__alliance__nom__icontains=alliance
	).order_by(order)
    paginator = Paginator(ville_list, 50)
    try: villes = paginator.page(page)
    except PageNotAnInteger: villes = paginator.page(1)
    except EmptyPage: villes = paginator.page(paginator.num_pages)
    return render_to_response('ville/list.html',{"villes": villes,
	"nom": nom,
	"monde": monde,
	"joueur": joueur,
	"alliance": alliance,
	"order": order,
	"monde_list": Monde.objects.all()
    })
##############################
#### CARTE
def carte(request):
    return render_to_response('carte.html', {"alliances": Alliance.objects.all(), "mondes": Monde.objects.all()})
def carte_image(request):
    import Image, ImageDraw
    from math import ceil,floor
    from random import randrange
    
    monde = request.GET.get('monde')
    CARTE_X=Monde.objects.get(nom=monde).carte_x
    CARTE_Y=Monde.objects.get(nom=monde).carte_y
    colors=[(255,0,0),(0,255,0),(0,0,255),(255,200,0),(255,0,255),(0,255,255),(255,127,0),(255,127,127),(127,0,255),(0,0,0)]
    
    height=int(request.GET.get('h', 1))
    todraw=request.GET.getlist('alliance')
    todraw=[x.lower() for x in todraw]
    drawall=request.GET.get('drawall')
    zoom=int(request.GET.get('z', 1))
    xpos=int(request.GET.get('x', 0))
    ypos=int(request.GET.get('y', 0))
    
    legende=Image.new('RGB',(200,height))
    lighten=Image.new('RGB',(CARTE_X,CARTE_Y),(255,255,255))
    minimap=Image.open("static/img/"+monde+".png")
    minimap=minimap.convert('RGB')
    minimap=Image.blend(minimap,lighten,0.6)
    minidraw=ImageDraw.Draw(minimap)
    legedraw=ImageDraw.Draw(legende)
    legedraw.rectangle([0,0,200,height],(255,255,255))
    i=0 # compteur de l'alliance, utilise pour les couleurs et le texte
    for alliance in Alliance.objects.filter(monde__nom__iexact=monde).order_by("classement")[:10]:
        if not drawall and not alliance.nom.lower() in todraw: continue # si l'alliance n'est pas demandee, ne pas la dessiner
        try: colors[c] # si y'a pas assez de couleurs, on en rajoute une
        except: colors.append((randrange(0,230),randrange(0,230),randrange(0,230)))
        for ville in Ville.objects.filter(joueur__alliance__nom=alliance.nom,joueur__monde__nom=monde):
            x=(ville.id%CARTE_Y)
            y=int(CARTE_Y-floor(ville.id/CARTE_Y))
            print x,y
            minidraw.rectangle([x,y,x,y],fill=colors[i]) 
        legedraw.rectangle([10,i*30+5,35,i*30+25],fill=colors[i]) 
        legedraw.text((50,i*30+10), alliance.nom, fill=colors[i])
        i+=1
    
    minimap=minimap.resize((301*zoom,301*zoom), Image.NEAREST)
    minimap_x=(height-CARTE_X*zoom)/2-(xpos*zoom)
    minimap_y=(height-CARTE_X*zoom)/2+(ypos*zoom)

    im=Image.new('RGB',(height+200,height))
    im.paste(minimap,(minimap_x,minimap_y))
    im.paste(legende,(height,0))

    response=HttpResponse(mimetype="image/png")
    im.save(response,'PNG')
    return response

def cuisse(request):
    return render_to_response('cuisse.html')
