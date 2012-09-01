from django.template import Context, loader
from django.http import HttpResponse
from nemeriatools.models import Joueur
from django.shortcuts import render_to_response
def home(request):
    return render_to_response('home.html')

def pseudo_detail(request,joueur_id):
    return HttpResponse(Joueur.objects.get(pk=joueur_id))

def pseudo_index(request):
    t=loader.get_template('pseudo/list.html')
    c=Context({
        'joueurs': [j for j in Joueur.objects.all()]
    })
    return HttpResponse(t.render(c))
