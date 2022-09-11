from django.contrib.auth.models import User
from django.db import models
from django.db.models import Model


# Create your models here.
class Room(Model):
    name = models.CharField(max_length=200)
    # s = None -> null
    # s = "" -> blank
    description = models.TextField(null=True, blank=True)
    # vazba M:N pro uzivatele a mistnost
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    # auto_now_add = True -> Pouze pri vytvoreni zaznamu do databaze
    created = models.DateTimeField(auto_now_add=True)
    # auto_now = True -> Pri jakekoliv editaci zaznamu
    updated = models.DateTimeField(auto_now=True)

    # rika jak se ma vytisknout trida model
    def __str__(self):
         return self.name

    class Meta:
        # razeni podle created a pokud jsou stejne bude se radit podle nazvu
        # a kdyz budou dve stejneho jmena a stejneho data vytvoreni seradit podle data a casu update
        # ordering = ['-created', '-name', '-uppdate'] -> razeni DESC
        ordering = ['created', 'name', 'updated']



class Message(Model):
    body = models.TextField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.body[0:50]

    class Meta:
        ordering = ['-created', '-updated']

