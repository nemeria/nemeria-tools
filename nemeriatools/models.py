from django.db import models

class Alliance(models.Model):
    id = models.IntegerField(primary_key=True)
    nom = models.CharField(max_length=30)
    pop = models.IntegerField()
    classement = models.IntegerField()
    def __unicode(self):
        return self.nom

class Joueur(models.Model):
    id = models.IntegerField(primary_key=True)
    nom = models.CharField(max_length=30)
    pop = models.IntegerField()
    classement = models.IntegerField()
    alliance = models.ForeignKey(Alliance)
    def __unicode__(self):
        return self.nom

class Ville(models.Model):
    id = models.IntegerField(primary_key=True)
    nom = models.CharField(max_length=30)
    terrain = models.IntegerField()
    pop = models.IntegerField()
    joueur = models.ForeignKey(Joueur)
    def __unicode__(self):
        return self.nom
