from django.db import models
from django.urls import reverse

# Create your models here.
class AdminSide(models.Model):
    username = models.CharField(max_length=25)
    password = models.CharField(max_length=16)



class MovieMaster(models.Model):
    m_name = models.CharField('Movie Name',max_length=50)
    m_desc = models.CharField('Movie Description', max_length=50)
    m_image = models.ImageField('Movie Image',upload_to="pics/")

    class Meta:
        unique_together = ["m_name", "m_desc", "m_image",]

    def get_absolute_url(self):
        return reverse("setadmin:addmovie")

    def __str__(self):
        return self.m_name


class SetMovie(models.Model):
    active = models.ForeignKey(MovieMaster, on_delete=models.CASCADE)
    show = models.CharField('Show Time', max_length=50)
    start_time = models.DateField()
    end_time = models.DateField()
    price = models.IntegerField()
    seats = models.CharField(max_length=100, default="")

    class Meta:
        unique_together = ["active", "show", "start_time", "end_time"]

    def get_absolute_url(self):
        return reverse("setadmin:setmovie")


