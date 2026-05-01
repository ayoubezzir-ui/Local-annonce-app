from django.db import models
from django.conf import settings

class Message(models.Model):
    expediteur = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='messages_envoyes', on_delete=models.CASCADE)
    destinataire = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='messages_recus', on_delete=models.CASCADE)
    sujet = models.CharField(max_length=200)
    contenu = models.TextField()
    date_envoi = models.DateTimeField(auto_now_add=True)
    est_lu = models.BooleanField(default=False)

    def __str__(self):
        return f"De {self.expediteur} à {self.destinataire} - {self.sujet}"
