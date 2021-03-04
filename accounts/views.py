from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from accounts.forms import SignUpForm, CreateItemForm


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            raw_password2 = form.cleaned_data.get('password2')

            if raw_password != raw_password2:
                pass

            return redirect('home')

            # return HttpResponse("ok ")
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect(reverse('home'))


def panel(request):
    if request.method == 'POST':
        seller_status = False
        if request.user.groups.count() == 1:
            pass
        else:
            seller_status = True
            request.user.groups.create(name="seller")

        return render(request, 'accounts/panel.html', {'has_msg': True, 'become_seller': seller_status})

    return render(request, 'accounts/panel.html', {})


def create_item(request):
    if request.method == 'POST':
        form = CreateItemForm(request.POST)
        if form.is_valid():
            # form.save()

            name = form.cleaned_data.get('name')
            quantity = form.cleaned_data.get('quantity')
            price = form.cleaned_data.get('price')
            # should fix
            return redirect('contact_us_done')

    else:
        form = CreateItemForm()
    return render(request, 'accounts/create-item.html', {'form': form})
