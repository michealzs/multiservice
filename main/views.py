# from .models import
from django.views.generic import ListView #, DetailView, CreateView, UpdateView, TemplateView, DeleteView



###################################################
#                    Home                         #
###################################################

class HomeView(ListView):
    paginate_by = 10
    template_name = 'main/home.html'

