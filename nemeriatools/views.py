from django.template import Context, loader
from django.http import HttpResponse
from nemeriatools.models import Joueur

def pseudo_detail(request,joueur_id):
    return HttpResponse(Joueur.objects.get(pk=joueur_id))

def pseudo_index(request):
    t=loader.get_template('index.html')
    c=Context({
        'joueurs': [j for j in Joueur.objects.all()]
    })
    return HttpResponse(t.render(c))
