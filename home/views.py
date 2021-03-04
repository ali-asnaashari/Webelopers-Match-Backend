from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, redirect

from home.forms import ContactUsForm


def home(request):
    return render(request, 'home/index.html', {})


def contact_us(request):
    if request.method == 'POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            # form.save()

            title = form.cleaned_data.get('title')
            email = form.cleaned_data.get('email')
            text = form.cleaned_data.get('text')

            subject = title
            message = text
            email_from = settings.EMAIL_HOST_USER
            recipient_list = ['webe21lopers@gmail.com', ]
            send_mail(subject, message, email_from, recipient_list)

            return redirect('contact_us_done')

    else:
        form = ContactUsForm()
    return render(request, 'home/contact-us.html', {'form': form})


def contact_us_done(request):
    return render(request, 'home/contact-us-done.html', {})