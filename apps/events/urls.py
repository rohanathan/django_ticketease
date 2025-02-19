from django.urls import path
from django.http import HttpResponse

# Placeholder view to prevent errors
def placeholder_view(request):
    return HttpResponse("<h2>Events feature is under development.</h2>")

urlpatterns = [
    path('', placeholder_view, name='events_list'),  # ✅ Placeholder page
]
