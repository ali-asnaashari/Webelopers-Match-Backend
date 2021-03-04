from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView

from accounts.forms import SignUpForm, CreateItemForm
from accounts.models import Product


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
        become_seller = False
        try:
            my_group = Group.objects.get(name='seller')
        except:
            my_group = Group.objects.create(name='seller')
            my_group.save()

        if request.user.groups.count() == 0:
            my_group.user_set.add(request.user)
            become_seller = True
        return render(request, 'accounts/panel.html',
                      {'has_msg': True, 'become_seller': become_seller, 'is_seller': True})

    is_seller = request.user.groups.count() > 0
    return render(request, 'accounts/panel.html', {'has_msg': False, 'is_seller': is_seller})


def create_item(request):
    if request.method == 'POST':
        form = CreateItemForm(request.POST)
        if form.is_valid():
            # form.save()

            name = form.cleaned_data.get('name')
            quantity = int(form.cleaned_data.get('quantity'))
            price = int(form.cleaned_data.get('price'))
            # should fix
            Product.objects.create(user=request.user, name=name, quantity=quantity, price=price)
            return redirect('contact_us_done')

    else:
        form = CreateItemForm()
    return render(request, 'accounts/create-item.html', {'form': form})


class AllProducts(ListView):
    template_name = 'accounts/all_products.html'
    context_object_name = 'products'
    model = Product

    def get_queryset(self):
        def space_to_underline(string):
            return string.replace(' ', '_')

        products = Product.objects.filter(user=self.request.user)
        result = [(product.name, product.price, product.quantity,
                   space_to_underline(product.name) + "_" + product.user.username,
                   product.id) for product in products]
        # 0 : name
        # 1 : price
        # 2: quentity
        # 3: class name
        # 4: id
        return result


def edit(request, id):
    form = CreateItemForm()
    form.fields['name'].text = 'name'
    return render(request, 'accounts/edit_product.html', {'form': form})
