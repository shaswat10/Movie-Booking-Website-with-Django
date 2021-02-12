from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name='user_side'

urlpatterns = [
    path('dashboard/', views.UserDashboard.as_view(), name='dashboard'),
    path('booktickets/', views.BookTickets.as_view(), name='booktickets'),
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.userLogout, name='logout'),
    path('selectseats/<int:pk>', views.BuyTicket.as_view(), name='selectseats'),
    path('history/', views.BookHistory.as_view(), name='bookhistory'),
    path('download/', views.DownloadTicket.as_view(), name='download'),
    path('ticket/<int:pk>', views.Ticket.as_view(), name ='ticket')
]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)