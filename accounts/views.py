import sys

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.db.models import F, Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView

from accounts.forms import SignUpForm, CreateItemForm
from accounts.models import Product, Tag


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
        data = request.POST.copy()
        data.update({'user': request.user, })
        form = CreateItemForm(data, request.FILES)
        if form.is_valid():
            # form.save()

            name = form.cleaned_data.get('name')
            quantity = int(form.cleaned_data.get('quantity'))
            price = int(form.cleaned_data.get('price'))
            tags = form.cleaned_data.get('tag')

            tag_names = tags.split(',')
            # Product.objects.create(user=request.user, name=name, quantity=quantity, price=price)
            product = Product(user=request.user, name=name, quantity=quantity, price=price)
            product.save()
            for tag in tag_names:
                # tag_count = Tag.objects.filter(name__exact=name).count()

                Tag.objects.get_or_create(name=tag)
                my_tag = Tag.objects.get(name=tag)
                print("TAAAG")
                print(my_tag)
                my_tag.save()
                product.tag.add(my_tag)

            product.save()

            # should fix

            return redirect('contact_us_done')

    else:
        form = CreateItemForm()
    return render(request, 'accounts/create-item.html', {'form': form})


def space_to_underline(string):
    return string.replace(' ', '_')


def get_link(obj):
    if obj:
        return obj.url

    return 'https://google.com'

class AllProducts(ListView):
    template_name = 'accounts/all_products.html'
    context_object_name = 'products'
    model = Product

    def get_queryset(self):
        products = Product.objects.filter(user=self.request.user)
        result = [(product.name, product.price, product.quantity,
                   space_to_underline(product.name) + "_" + product.user.username,
                   product.id,
                   product.tag.all(),
                   get_link(product.product_image)) for product in products]
        print(result[0][5])
        # 0 : name
        # 1 : price
        # 2: quentity
        # 3: class name
        # 4: id
        # 5: tags
        # 6: image url
        return result


def edit(request, id):
    product = Product.objects.get(id=id)
    name = product.name
    price = product.price
    quantity = product.quantity

    if request.method == 'POST':

        data = request.POST.copy()
        data.update({'user': request.user, })
        # data.update({'user': request.user, 'comments': product.comments.all(), 'tag': product.tag.all()})
        form = CreateItemForm(data, request.FILES)
        if form.is_valid():
            form.save()

            # product.name = form.cleaned_data.get('name')
            # product.quantity = int(form.cleaned_data.get('quantity'))
            # product.price = int(form.cleaned_data.get('price'))
            # should fix
            # Product.objects.create(user=request.user, name=name, quantity=quantity, price=price)
            # product.save()
            return redirect('accounts:all_products')

    form = CreateItemForm()
    form.set_initial(name_text=name, price_text=price, quantity_text=quantity)
    # form.fields['name'].initil = 'name'
    return render(request, 'accounts/edit_product.html', {'form': form})


def delete_product(request, id):
    product = Product.objects.get(id=id)
    product.delete()
    return HttpResponse('ok')


class EntireProducts(ListView):
    template_name = 'accounts/enitre_products.html'
    context_object_name = 'products'
    model = Product

    def post(self, request):
        title = request.POST.get('title')
        min_price = request.POST.get('min_price')
        max_price = request.POST.get('max_price')
        tags = request.POST.get('tag').split(',')

        products = Product.objects.filter(name__contains=title)
        if max_price != '' or min_price != '':
            print("min price= ", min_price)
            print("max price= ", max_price)
            if min_price != '' and max_price != '':

                products = Product.objects.filter(
                    Q(price__gte=int(min_price)) & Q(price__lte=int(max_price)))

            elif min_price == '':
                products = Product.objects.filter(
                    Q(price__lte=int(max_price)))
            elif max_price == '':
                products = Product.objects.filter(
                    Q(price__gte=int(min_price)))



        if len(tags):
            res = Product.objects.filter(tag__name__in=tags)
            for item in res:
                if not products.get(name__exact=item.name):
                    products += item


        result = [(product.name, product.price, product.quantity,
                   space_to_underline(product.name) + "_" + product.user.username,
                   product.id,
                   product.user.first_name,
                   product.user.last_name,
                   product.tag.all(),
                   get_link(product.product_image)) for product in products]
        # 0 : name
        # 1 : price
        # 2: quentity
        # 3: class name
        # 4: id
        # 5: first name
        # 6: last name
        # 7: tag
        # 8: product image url
        return render(request, 'accounts/enitre_products.html', {'products': result})

    def get_queryset(self, ):


        products = Product.objects.all()
        result = [(product.name, product.price, product.quantity,
                   space_to_underline(product.name) + "_" + product.user.username,
                   product.id,
                   product.user.first_name,
                   product.user.last_name,
                   product.tag.all(),
                   get_link(product.product_image)) for product in products]
        # 0 : name
        # 1 : price
        # 2: quentity
        # 3: class name
        # 4: id
        # 5: first name
        # 6: last name
        # 7: tag
        # 8: product image
        return result


def product_page(request, id):
    product = Product.objects.get(id=id)
    comments = product.comments.all()

    if request.method == 'POST':
        text = request.POST.get('text')
        product.comments.create(text=text, user=request.user)

    return render(request, 'accounts/product_page.html', {'product': product, 'comments': comments})
