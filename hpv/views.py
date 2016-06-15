from django.shortcuts import render
from django.views.generic.base import TemplateView
import datetime as dt
from api.models import HPVATM
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from collections import OrderedDict


class HPV(LoginRequiredMixin, TemplateView):
    template_name = "hpv/hpv2.html"
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        """



        """

        # Recursive call for context
        context = super().get_context_data(**kwargs)

        # If no data in API
        if HPVATM.objects.count() == 0:
            return context

        # Checking for objects
        current = HPVATM.objects.latest('timestamp')
        shift1 = HPVATM.objects.filter(shift=1)
        shift2 = HPVATM.objects.filter(shift=2)
        shift3 = HPVATM.objects.filter(shift=3)

        # Seperate into depatrments
        depts = {
            'CIW': {},
            'FCB': {},
            'PNT': {},
            'PCH': {},
            'FCH': {},
            'DAC': {},
            'MAINT': {},
            'QA': {},
            'MAT': {},
            'PLANT': {}
        }

        # For printing out the time of the most recent object
        current_time = current.timestamp
        context.update({'current_time': current_time})

        # Function call for the each portion context data
        self.set_day_data(current, context, depts)
        self.set_shift1_data(current, shift1, context, depts)
        self.set_shift2_data(current, shift2, context, depts)
        self.set_shift3_data(current, shift3, context, depts)

        # Set order of the departments dictionary so the table in the HTML is
        # in order
        keyorder = ['CIW', 'FCB', 'PNT', 'PCH', 'FCH', 'DAC', 'MAINT', 'QA',
                    'MAT', 'PLANT']

        context['depts'] = OrderedDict(sorted(depts.items(), key=lambda
                                              i: keyorder.index(i[0])))

        return context

    def set_day_data(self, current, context, depts):
        """


        """

        # Catching the data from the API object and putting it in the depts
        # dictionary
        depts['CIW']['d_hpv'] = current.CIW_d_hpv
        depts['FCB']['d_hpv'] = current.FCB_d_hpv
        depts['PNT']['d_hpv'] = current.PNT_d_hpv
        depts['PCH']['d_hpv'] = current.PCH_d_hpv
        depts['FCH']['d_hpv'] = current.FCH_d_hpv
        depts['DAC']['d_hpv'] = current.DAC_d_hpv
        depts['MAINT']['d_hpv'] = current.MAINT_d_hpv
        depts['QA']['d_hpv'] = current.QA_d_hpv
        depts['MAT']['d_hpv'] = current.MAT_d_hpv
        depts['PLANT']['d_hpv'] = current.PLANT_d_hpv

        # Catching the days claims data and adding it to the context
        claims_d = current.claims_d
        context.update({'claims_d': claims_d})

    def set_shift1_data(self, current, shift1, context, depts):
        """


        """

        # If the most recent API object is not shift 1 it moves onto the next
        # if statement
        if not shift1:
            return

        # Finds most recent API object that is shift 1 between now and 17 hours
        # ago (near end of last shift)
        # If there is no shift 1 within the last 17 hours it returns out of the
        # funtion
        shift1 = shift1.latest('timestamp')
        if not (shift1.timestamp >=
                current.timestamp - dt.timedelta(hours=17)):
            return

        # Catching the data from the API object and putting it in the depts
        # dictionary
        depts['CIW']['s1_hpv'] = shift1.CIW_s_hpv
        depts['FCB']['s1_hpv'] = shift1.FCB_s_hpv
        depts['PNT']['s1_hpv'] = shift1.PNT_s_hpv
        depts['PCH']['s1_hpv'] = shift1.PCH_s_hpv
        depts['FCH']['s1_hpv'] = shift1.FCH_s_hpv
        depts['DAC']['s1_hpv'] = shift1.DAC_s_hpv
        depts['MAINT']['s1_hpv'] = shift1.MAINT_s_hpv
        depts['QA']['s1_hpv'] = shift1.QA_s_hpv
        depts['MAT']['s1_hpv'] = shift1.MAT_s_hpv
        depts['PLANT']['s1_hpv'] = shift1.PLANT_s_hpv

        # Catching the shifts claims data and adding it to the context
        s1_claims = shift1.claims_s
        context.update({'s1_claims': s1_claims})

    def set_shift2_data(self, current, shift2, context, depts):
        """


        """

        # If the most recent API object is shift 2 function skips to the next
        # step
        if not shift2:
            return

        # Finds most recent API object that is shift 2 between now and 17 hours
        # ago (near end of last shift)
        # If there is no shift 2 within the last 17 hours it returns out of the
        # funtion
        shift2 = shift2.latest('timestamp')
        if not (shift2.timestamp >=
                current.timestamp - dt.timedelta(hours=17)):
            return

        # Catching the data from the API object and putting it in the depts
        # dictionary
        depts['CIW']['s2_hpv'] = shift2.CIW_s_hpv
        depts['FCB']['s2_hpv'] = shift2.FCB_s_hpv
        depts['PNT']['s2_hpv'] = shift2.PNT_s_hpv
        depts['PCH']['s2_hpv'] = shift2.PCH_s_hpv
        depts['FCH']['s2_hpv'] = shift2.FCH_s_hpv
        depts['DAC']['s2_hpv'] = shift2.DAC_s_hpv
        depts['MAINT']['s2_hpv'] = shift2.MAINT_s_hpv
        depts['QA']['s2_hpv'] = shift2.QA_s_hpv
        depts['MAT']['s2_hpv'] = shift2.MAT_s_hpv
        depts['PLANT']['s2_hpv'] = shift2.PLANT_s_hpv

        # Catching the shifts claims data and adding it to the context
        s2_claims = shift2.claims_s
        context.update({'s2_claims': s2_claims})

    def set_shift3_data(self, current, shift3, context, depts):
        """


        """

        # If the most recent API object is not shift 3, shift 3 is False and is
        # added to the context, passes to the next if statment
        if not shift3:
            shift_3 = False
            context.update({'shift_3': shift_3})
            return

        # Finds most recent API object that is shift 3 between now and 17 hours
        # ago (near end of last shift)
        # If there is no shift 2 within the last 17 hours it returns out of the
        # funtion
        shift3 = shift3.latest('timestamp')
        if not (shift3.timestamp >=
                current.timestamp - dt.timedelta(hours=17)):
            return

        # Catching the data from the API object and putting it in the depts
        # dictionary
        depts['CIW']['s3_hpv'] = shift3.CIW_s_hpv
        depts['FCB']['s3_hpv'] = shift3.FCB_s_hpv
        depts['PNT']['s3_hpv'] = shift3.PNT_s_hpv
        depts['PCH']['s3_hpv'] = shift3.PCH_s_hpv
        depts['FCH']['s3_hpv'] = shift3.FCH_s_hpv
        depts['DAC']['s3_hpv'] = shift3.DAC_s_hpv
        depts['MAINT']['s3_hpv'] = shift3.MAINT_s_hpv
        depts['QA']['s3_hpv'] = shift3.QA_s_hpv
        depts['MAT']['s3_hpv'] = shift3.MAT_s_hpv
        depts['PLANT']['s3_hpv'] = shift3.PLANT_s_hpv

        # Catching the shifts claims data, shift 3 is now True, adding both to
        # the context
        s3_claims = shift3.claims_s
        shift_3 = True
        context.update({'s3_claims': s3_claims, 'shift_3': shift_3})


def logout_view(request):
    logout(request)
    return render(request, 'registration/logout.html')


class Detail(LoginRequiredMixin, TemplateView):
    template_name = "hpv/detail.html"
    login_url = '/login/'

    def detail(request):
        return render(request, self.template_name)
