from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomLoginForm, CustomUserUpdateForm
from django.views.generic import View
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.models import User
from .models import UserProfile

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# for sanding email

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


# Create your views here.

class UserLoginView(LoginView):
    template_name = 'login_form.html'
    form_class = CustomLoginForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def get_success_url(self):
        messages.success(self.request, 'User login successfully !!')
        return reverse_lazy('homepage')


@login_required(login_url='login')
def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect(reverse_lazy('homepage'))


def RegistrationView(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.user_profile.is_admin = form.cleaned_data['is_admin']
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            confirm_link = (
                f"https://phi-sdp-final-exam.onrender.com/account/signup/"
                f"{uid}/{token}"
            )
            user.user_profile.save()
            email_subject = 'Confirm Your Email'
            email_body = render_to_string(
                'confirm_email.html', {'confirmation_link': confirm_link})
            email = EmailMultiAlternatives(email_subject, '', to=[user.email])
            email.attach_alternative(email_body, 'text/html')
            email.send()
            messages.success(request, 'Check your mail form confirmation !!')

            form = CustomUserCreationForm(initial={'is_admin': False})

            return render(request, 'register_form.html', {'form': form})
    else:

        form = CustomUserCreationForm(initial={'is_admin': False})

    return render(request, 'register_form.html', {'form': form})


class UserProfileUpdateView(View):
    template_name = 'update_profile.html'
    form_class = CustomUserUpdateForm
    success_url = reverse_lazy('homepage')

    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, instance=request.user)
        if form.is_valid():

            user_profile = request.user.user_profile
            user_profile.is_admin = form.cleaned_data['is_admin']
            user_profile.save()

            form.save()

            messages.success(request, 'User Update Successfully')
            return redirect(self.success_url)
        return render(request, self.template_name, {'form': form})


def activate(request, uid64, token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk=uid)

    except User.DoesNotExist:
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('user_login')
    else:

        messages.success(request, 'Invalid User !!!')
        return redirect('user_login')
