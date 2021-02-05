from collections import Counter

from django.contrib import messages
from django.shortcuts import render, redirect

from blog.models import Article
from homepage.models import Contact_User


def about(request):
    return render(request, 'homepage/about.html')

def teams(request):
    return render(request, 'homepage/teams.html')

def contact(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        matter = request.POST['message']
        contact = Contact_User(name=name, email=email, subject=subject, matter=matter)
        contact.save()
        messages.success(request, f"Thankyou for contacting us {name}. Our team will reach out to you ar {email}")
        return redirect('homepage')

    else:
        # messages.warning(request, "Only POST requests are accepted for this type of forms.")
        return render(request, 'homepage/contact.html')
        # return redirect('homepage')
