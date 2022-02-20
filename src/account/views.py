from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView, LogoutView
from django.core.signing import BadSignature
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView
from django.views.generic import TemplateView

from .forms import AccountRegistrationForm, AccountUpdateForm
from .utils import signer


class AccountRegistrationView(CreateView):
    model = get_user_model()
    template_name = 'account/registration.html'
    success_url = reverse_lazy('account:registration_done')
    form_class = AccountRegistrationForm


class AccountRegistrationDoneView(TemplateView):
    template_name = 'account/registration_done.html'


def user_activate(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'account/bad_signature.html')

    user = get_object_or_404(get_user_model(), username=username)
    if user.is_activated:
        template = 'account/user_is_activated.html'
    else:
        template = 'account/activation_done.html'
        user.is_active = True
        user.is_activated = True
        user.save()

    return render(request, template)


class AccountLoginView(LoginView):
    template_name = 'account/login.html'

    def get_redirect_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url

        return reverse('index')


class AccountLogoutView(LogoutView):
    template_name = 'account/logout.html'


def account_profile_view(request):
    return render(request, 'account/profile.html')


class AccountUpdateProfileView(UpdateView):
    template_name = 'account/profile_update.html'
    model = get_user_model()
    success_url = reverse_lazy('account:profile')
    form_class = AccountUpdateForm

    def get_object(self, queryset=None):
        return self.request.user
