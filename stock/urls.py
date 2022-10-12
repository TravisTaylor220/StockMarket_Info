from django.urls import path
from . import views

urlpatterns = [
    path('', views.TickerSearch.as_view(template_name='stock/home.html'), name='stock-home'),
    path('learn/', views.learn, name='stock-learn'),
    path('portfolio/', views.portfolio, name='stock-portfolio'),
]