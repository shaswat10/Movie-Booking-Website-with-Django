from django.shortcuts import render, redirect
from . import models
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from . import forms
from django.contrib import messages
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
# from mysite.movie import models as movie_models
from movie.models import MovieMaster, SetMovie
from .models import User
import urllib
from django.urls import reverse
from itertools import chain
from operator import attrgetter


#####################################################




####### User register page#####
def registerPage(request):
    form = forms.CreateUserForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username') 
            return redirect('../login/')
            messages.success(request, 'Account was created'+user)
        else:
            context = {'form': form}
            return render(request, 'movie_user/register.html',context)
            
    context = {'form': form}
    return render(request, 'movie_user/register.html', context)



##### User Login page#########
def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username)
        print(password)
        user = authenticate(request, username=username, password=password)
        # user.is_superuser
        if user is not None:
            login(request, user)
            # print("hi")
            print("----------------------------")
            print(user.id)
            print("-----------------------------")
            # request.session['user'] = user
            # print(request.session['user'].id)
            # return render(request, 'movie_user/user_dashboard.html')
            return redirect('../dashboard/')
            # redirect('dashboard')
            # return redirect(reverse('user_side:dashboard'))
        else:
            print("no")
            messages.info(request, '!!Incorrect credientials!!')

  
    return render(request, 'movie_user/login.html')


def userLogout(request):
    logout(request)
    return redirect('../login/')




# Movie seating arrangement page here user will be able to select particular seat number to book it//////////////////////////////////////////////////////
class BookTickets(View):
    form_class = forms.BookedSeatsForm
    initial = {'key': 'value'}
    template_name = "movie_user/bookticket.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        dd = '2021-02-02'

        # Sessions for movie seat data //////////////////////////////////////////////////////////

        time_s = request.session['time']
        date_s = request.session['date']  
        movie_name = request.session['moviename']
        time_fld=0
    # ////////////////////////////////////////////////////////////////////////////////

        if time_s == "Morning":
            time_fld = 1

        elif time_s == "Afternoon":
            time_fld = 2
        
        elif time_s == "Evening":
            time_fld = 3

        else:
            time_fld = 4

        print("here")
        print(request.user.id)
        # print(request.session['user'].id)
        new_dict = {val:0 for val in range(60)} 
        
###########See if previously any seats are booked for this particular show#############
        if models.BookedSeatsModel.objects.filter(date=date_s, time=time_fld, movie_name = movie_name).exists():
        
            bookseats = models.BookedSeatsModel.objects.get(date=date_s, time=time_fld, movie_name = movie_name) 
            temp = bookseats.seats
            print(temp)
            
            for i in temp:

                if i != ',':
                    # new_dict[i]=1
                    temp = int(i)
                    new_dict[temp] = 1

  
        dict = {'seats':new_dict}
        # if models.BookedSeatsModel.objects.get(movie_name='Avenger', date=date_s, time=1).exists():
        #     bookseats = models.BookedSeatsModel.objects.get(date=date_s, time=1, movie_name = movie_name) 




        # context['seats'] = new_dict
        return render(request, self.template_name, dict)
        

    def post(self, request, *args, **kwargs):  
        # form = self.form_class(request.POST)
        if request.method == 'POST':
            booked_seats = request.POST['booked_seats']
            print(booked_seats)
            time_s = request.session['time']
            date_s = request.session['date']    
            movie_name = request.session['moviename']
            number = request.POST['count']

            if time_s == "Morning":
                time_fld = 1

            elif time_s == "Afternoon":
                time_fld = 2
            
            elif time_s == "Evening":
                time_fld = 3

            else:
                time_fld = 4



            print(time_s)
            print(date_s)  
            
           ############Saving booked seats data################
            if models.BookedSeatsModel.objects.filter(movie_name=movie_name, date=date_s, time=time_fld).exists():
                print("same")
                obj1 = models.BookedSeatsModel.objects.get(movie_name=movie_name, date=date_s, time=time_fld)
                obj1.seats = obj1.seats + booked_seats
                obj1.number = int(obj1.number) + number
                obj1.save()

                obj = models.UserBook(user=request.user, movie_name=movie_name, date=date_s, show=time_fld, seats=booked_seats)
                obj.save()

            else:
                print("----------------------------------")
                print(request.user.id)
                print("----------------------------------")
                obj = models.UserBook(user=request.user, movie_name=movie_name, date=date_s, show=time_fld, seats=booked_seats)
                obj.save()

                obj1 = models.BookedSeatsModel(movie_name=movie_name, date=date_s, time=time_fld, seats=booked_seats, number=number)
                obj1.save()




            return redirect('../dashboard/')

        return render(request, self.template_name, dict)


class UserDashboard(generic.ListView):
    model = MovieMaster
    model_add = MovieMaster
    model_set = SetMovie
    template_name = "movie_user/user_dashboard.html"

    def get_context_data(self, **kwargs):
        movies = MovieMaster.objects.filter(setmovie__isnull=False).distinct()
        context = super().get_context_data(**kwargs)
        context['movies'] = movies
        return context

###########Here the user will select a particular show for which he will be redirected to seat booking page############
class BuyTicket(generic.ListView):
    template_name = "movie_user/buyticket.html"
    model = SetMovie
    from_class = forms.CheckDateForm

    def post(self, request, *args, **kwargs):

        if request.method == 'POST':
            time = request.POST['tm']
            date = request.POST['datee']

            print(time)
            print(date)
            # dict = {'time':time, 'date':date} 
            # uri = urllib.urlencode(dict)
            request.session['time'] = time
            request.session['date'] = date

            idd = self.kwargs['pk']
            movie_data = MovieMaster.objects.get(pk=idd)
            request.session['moviename'] = movie_data.m_name

            return redirect(reverse('user_side:booktickets'))



    def get_context_data(self, **kwargs):
        movies = MovieMaster.objects.filter(setmovie__isnull=False)
        context = super().get_context_data(**kwargs)
        idd = self.kwargs['pk']
        movie_data = MovieMaster.objects.get(pk=idd)
        
        context['movies'] = movie_data
        set_movie = SetMovie.objects.filter(active_id=idd)
        # print(set_movie.start_time)
        context['data_set'] = set_movie
        return context



############ User will be able to see all his/her previous bookings done #################
class BookHistory(generic.ListView):

    context_object_name = 'book_history'

    def get_queryset(self):
        return models.UserBook.objects.filter(user_id=self.request.user.id)

    template_name = "movie_user/book_history.html"

################## User can download the ticket booked ##########################
class DownloadTicket(generic.ListView):

    context_object_name = 'ticket_detail'   
    def get_queryset(self):
        return models.UserBook.objects.filter(user_id=self.request.user.id)


    template_name = "movie_user/downloadticket.html"

########### Single ticket download page################
class Ticket(generic.DetailView):

    context_object_name = 'row'
    def get_queryset(self):
        return models.UserBook.objects.filter(user_id=self.request.user.id)

    template_name = "movie_user/ticket.html"
