from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    enonce = models.TextField()  # L'énoncé de la question
    choix_1 = models.CharField(max_length=200)  # Option 1
    choix_2 = models.CharField(max_length=200)  # Option 2
    choix_3 = models.CharField(max_length=200)  # Option 3
    choix_4 = models.CharField(max_length=200)  # Option 4
    bonne_reponse = models.CharField(max_length=200)  # La réponse correcte
    explication = models.TextField()  # Explication si la réponse est incorrecte

    def __str__(self):
        return self.enonce


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class UserScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.score} points"
