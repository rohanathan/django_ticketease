from django.urls import path
from .views import movies_list, movies_detail  

urlpatterns = [
    path('', movies_list, name='movies_list'),
    path('<int:movie_id>/', movies_detail, name='movies_detail'),
]
