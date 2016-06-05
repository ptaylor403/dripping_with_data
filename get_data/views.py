from django.shortcuts import render
from django.views.generic.base import TemplateView
from .models import RawClockData, RawDirectRunData, RawCrysData, RawPlantActivity


# Create your views here.
class Clone(TemplateView):
    template_name = "clone/clone.html"

    def get(self, request):
        context = {}
        done = False
        if request.GET.get('clone'):
            RawClockData.load_raw_data()
            RawDirectRunData.load_raw_data()
            RawCrysData.load_raw_data()
            RawPlantActivity.load_raw_data()
            done=True

        context = {'done': done}
        return render(request, self.template_name, context)
