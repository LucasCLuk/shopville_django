from background_task.models import Task
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
from django.views.generic import TemplateView

from shopville.models import Buyer, BuyerSchedule


class Dashboard(LoginRequiredMixin, TemplateView):
    template_name = "shopville/dashboard.html"


class Accounting(LoginRequiredMixin, TemplateView):
    template_name = "shopville/accounting.html"

    def get_context_data(self, **kwargs):
        context = super(Accounting, self).get_context_data(**kwargs)
        if self.request.user.is_staff:
            context['buyers'] = [buyer for buyer in Buyer.objects.all()]
        try:
            self_buyer = Buyer.objects.get(user=self.request.user)
        except Buyer.DoesNotExist:
            self_buyer = None
        context['buyer'] = self_buyer
        return context


class TaskManager(LoginRequiredMixin, TemplateView):
    template_name = "shopville/tasks.html"

    def get_context_data(self, **kwargs):
        context = super(TaskManager, self).get_context_data(**kwargs)
        context['buyers'] = [buyer for buyer in BuyerSchedule.objects.all()]
        return context
