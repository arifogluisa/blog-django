from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic


class AuthView(generic.View):
    """
    Auth view is just a check
    user is login or not
    if user login send to dashboard
    """

    dashboard_url = reverse_lazy("index")

    def dispatch(self, *args, **kwargs):
        """
        Base Secure class
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        if self.request.user.is_authenticated:
            return redirect(self.dashboard_url)
        else:
            return super(AuthView, self).dispatch(*args, **kwargs)
