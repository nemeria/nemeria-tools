from django.db import models

class Monde(models.Model):
    nom=models.CharField(max_length=10)
    carte_x=models.IntegerField()
    carte_y=models.IntegerField()
    def __unicode__(self):
		return self.nom

class Alliance(models.Model):
    autoinc = models.AutoField(primary_key=True)
    id = models.IntegerField()
    nom = models.CharField(max_length=30)
    pop = models.IntegerField()
    classement = models.IntegerField()
    monde = models.ForeignKey(Monde)
    def __unicode__(self):
        return self.nom

class Joueur(models.Model):
    autoinc = models.AutoField(primary_key=True)
    id = models.IntegerField()
    nom = models.CharField(max_length=30)
    pop = models.IntegerField()
    classement = models.IntegerField()
    alliance = models.ForeignKey(Alliance, null=True)
    monde = models.ForeignKey(Monde)    
    def __unicode__(self):
        return self.nom

class Ville(models.Model):
    autoinc = models.AutoField(primary_key=True)
    id = models.IntegerField()
    nom = models.CharField(max_length=30)
    terrain = models.IntegerField()
    pop = models.IntegerField()
    joueur = models.ForeignKey(Joueur)
    def __unicode__(self):
        return self.nom
