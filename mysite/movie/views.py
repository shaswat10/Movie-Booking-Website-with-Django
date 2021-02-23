from django.shortcuts import render, redirect
from django.views import generic
from . import models
from .models import SetMovie, MovieMaster
from . import forms
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from movie_user.models import BookedSeatsModel
from django.http import JsonResponse
# Create your views here.

############ADmin login page######################
class LoiginAdmin(View):
    template_name = "movie/admin_login.html"

    def get(self, request, *args, **kwargs):
        
        return render(request, self.template_name)

    def post(self,request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            superusers = User.objects.get(username = username)
            print("-------------------------------------")
            print(superusers.username)
            print(superusers.is_superuser)
            print("--------------------------------------")
            if superusers.is_superuser == True:
                login(request, user)
                return redirect('../dashboard/')

        else:
            return render(request, self.template_name)


def adminLogout(request):
    logout(request)
    return redirect('../login/')


##########ADmin dashboard page##########
class Dashboard(generic.ListView):
    model_add = models.MovieMaster
    model_set = models.SetMovie
    movies = MovieMaster.objects.filter(setmovie__isnull=False).distinct()
    # context_object_name = 'moviesss'
    model = MovieMaster

    template_name = "movie/dashboard.html"

    def get_context_data(self, **kwargs):
        movies = MovieMaster.objects.filter(setmovie__isnull=False).distinct()
        context = super().get_context_data(**kwargs)
        context['movies'] = movies
        return context


########This page will be used by admin for adding movies to system when then will be used for setting shows####################
class AddMovies(generic.CreateView):  
    form_class = forms.AddMovieForm
    model = models.MovieMaster
    template_name = "movie/addmovies.html"
    # fields = '__all__'

    
    ###############From the list of movies added admin can set show for particular movie############################
class SetMovies(generic.CreateView):
    form_class = forms.SetMovieForm
    model = models.SetMovie
    # context_object_name = 'movies'
    # def post(self, request, *args, **kwargs): 
    #     if request.method == 'POST':
    #         request.POST['']
    #         models.MovieGraphCount(m_name=)
    
    template_name = "movie/setmovies.html"
    




