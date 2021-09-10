from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View, generic
from django.views.generic import TemplateView
from django.utils.translation import gettext_lazy as _

from customer.forms import RegistrationForm, AddressFrom, UpdateInfoForm, MyPasswordChangeForm, UserLoginForm



# Login View
class MyLoginView(LoginView):
    template_name = "customer_temp/login.html"
    authentication_form = UserLoginForm


# Register View
def register(request):
    context = {}
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            login(request, account)

            return redirect('customer:profile_detail')
        else:
            context['registration_form'] = form
    elif request.method == 'GET':
        form = RegistrationForm()
        context['registration_form'] = form

    return render(request, 'customer_temp/register_form.html', context)




# Profile View
class ProfileView(LoginRequiredMixin, generic.ListView):
    model = User
    template_name = 'customer_temp/profile-datail.html'


# Update Information of User
class UpdateInfo(LoginRequiredMixin, generic.UpdateView):
    model = User
    # fields = ['phone', 'first_name', 'last_name', 'email']
    form_class = UpdateInfoForm
    template_name = 'customer_temp/update_info_form.html'
    success_url = reverse_lazy('customer:profile_detail')

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, pk=self.request.user.pk)


# Change Password View
class MyPasswordChangeView(PasswordChangeView):
    form_class = MyPasswordChangeForm
    template_name = "customer_temp/change_password.html"
    success_url = reverse_lazy('customer:profile_detail')


# Address Create View
class AddressCreateView(LoginRequiredMixin, generic.FormView):
    form_class = AddressFrom
    template_name = 'customer_temp/address_create.html'
    success_url = reverse_lazy('customer:address_create')

    def form_valid(self, form):
        address = form.save(commit=False)
        address.owner = self.request.user
        address.save()
        form.save()
        return super().form_valid(form)


