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
    joueur_list=Joueur.objects.filter(
        nom__icontains=nom,
        monde__nom__icontains=monde,
        alliance__nom__icontains=alliance,
    ).order_by(order)
    paginator = Paginator(joueur_list, 50)
    try: joueurs = paginator.page(page)
    except PageNotAnInteger: joueurs = paginator.page(1)
    except EmptyPage: joueurs = paginator.page(paginator.num_pages)
    return render_to_response('joueur/list.html',{"joueurs": joueurs, "nom": nom, "monde": monde, "alliance": alliance, "order": order})
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
    return render_to_response('alliance/list.html',{"alliances": alliances, "nom": nom, "monde": monde, "order": order})
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
    return render_to_response('ville/list.html',{"villes": villes, "nom": nom, "monde": monde, "joueur": joueur, "alliance": alliance, "order": order})
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
    colors=[(255,0,0),(0,255,0),(0,0,255),(255,200,0),(255,0,255),(0,255,255),(0,0,0)]


    todraw=request.GET.getlist('alliance')
    todraw=[x.lower() for x in todraw]
    drawall=request.GET.get('drawall')
    height=int(request.GET.get('h', 1000))
    zoom=int(request.GET.get('z', 0))
    ypos=int(request.GET.get('y', 0))
    xpos=int(request.GET.get('x', 0))
    
    print xpos,ypos,zoom
    if height > 3000: height=3000
    blocksize=int(height/CARTE_X)
    height=blocksize*CARTE_X 

    im=Image.new('RGB',(height+200,height))
    #~ minimap=Image.open("nemeriatools/static/img/"+monde+".png")
    #~ minimap=minimap.resize((height,height), Image.NEAREST)
    #~ im.paste(minimap,(0,0))
    draw=ImageDraw.Draw(im)
    draw.rectangle([height,0,height+200,height],fill=(250,250,250))
    draw.rectangle([0,0,height,height],fill=(255,255,255))
    
    blocksize=blocksize*(zoom+1)
    xpos=xpos-CARTE_X+CARTE_X*(zoom+1)
    ypos=ypos-CARTE_Y+CARTE_Y*(zoom+1)
    print xpos,ypos,zoom
    i=0 # compteur de l'alliance, utilise pour les couleurs et le texte
    for alliance in Alliance.objects.filter(monde__nom__iexact=monde).order_by("classement"):
        if not drawall and not alliance.nom.lower() in todraw: continue # si l'alliance n'est pas demandee, ne pas la dessiner
        try: colors[c] # si y'a pas assez de couleurs, on en rajoute une
        except: colors.append((randrange(0,230),randrange(0,230),randrange(0,230)))
        for ville in Ville.objects.filter(joueur__alliance__nom=alliance.nom,joueur__monde__nom=monde):
            x=(ville.id%CARTE_Y)*blocksize-xpos
            y=int(CARTE_Y-floor(ville.id/CARTE_Y))*blocksize-ypos

            draw.rectangle([x+1,y+1,x+blocksize-1,y+blocksize-1],fill=colors[i]) 
        draw.rectangle([height+10,i*30+5,height+35,i*30+25],fill=colors[i]) 
        draw.text((height+50,i*30+10), alliance.nom, fill=colors[i])
        i+=1
    
    response=HttpResponse(mimetype="image/png")
    im.save(response,'PNG')
    return response
    
