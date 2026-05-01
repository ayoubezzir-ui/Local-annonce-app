from django.db import models
from django.conf import settings
from categories.models import Department

class Annonce(models.Model):
    PRIORITY_CHOICES = [
        ('normal', 'Normal 🟢'),
        ('important', 'Important 🟠'),
        ('urgent', 'Urgent 🔴'),
    ]

    titre = models.CharField(max_length=200)
    contenu = models.TextField()
    departement = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    auteur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    priorite = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='normal')
    image = models.ImageField(upload_to='annonces/images/', null=True, blank=True)
    fichier = models.FileField(upload_to='annonces/fichiers/', null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titre

class Commentaire(models.Model):
    annonce = models.ForeignKey(Annonce, on_delete=models.CASCADE, related_name='commentaires')
    auteur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    contenu = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Commentaire de {self.auteur} sur {self.annonce}"

class LectureAnnonce(models.Model):
    annonce = models.ForeignKey(Annonce, on_delete=models.CASCADE, related_name='lectures')
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_lecture = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('annonce', 'utilisateur')