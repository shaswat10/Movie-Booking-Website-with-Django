from django.db import models
from django.contrib.auth.models import User
# Create your models here.


# class UserBook(models.Model):
#     user = models.ForeignKey(User)
#     # movie_name = 
class UserBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie_name = models.CharField(max_length=50)
    date = models.DateField()
    show = models.IntegerField()
    seats = models.CharField(max_length=50)
    
class BookedSeatsModel(models.Model):
    movie_name = models.CharField(max_length=50)
    date = models.DateField()
    time = models.IntegerField()
    seats = models.CharField(max_length=50)
    number = models.IntegerField(default=0)