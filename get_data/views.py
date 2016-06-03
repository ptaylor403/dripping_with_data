from django.shortcuts import render
from django.views.generic.base import TemplateView
from .models import RawClockData



# Create your views here.
class Clone(TemplateView):
    template_name = "clone/clone.html"

    def get(self, request):
        context = {}
        if request.GET.get('clone'):
           RawClockData.csv_reader()
        return render(request, self.template_name, context)