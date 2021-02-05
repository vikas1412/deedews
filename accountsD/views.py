from django.core.mail import send_mail
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as login_auth, logout as logout_auth
from django.contrib import messages
from accountsD.models import Profile


def login(request):
    if request.user.is_authenticated:
        # do something if the user is authenticated
        messages.success(request, "You are already logged in to your account. If however, you want to log in from another account, you must log out of this account first.")
        return redirect('homepage')
    else:

        if request.method == 'POST':
            email = request.POST['username']
            password = request.POST['password']

            curr_user = authenticate(username=email, password=password)
            if curr_user is not None:
                login_auth(request, curr_user)

                # to admin to let them know
                username = email
                subject = username + ' logged in'
                to = 'deedews@gmail.com'
                body_html = f"""
                            
                               """
                # send_mail(subject, to, body_html)


                messages.success(
                    request, "Welcome back to Deedews. Now you can comment on articles, save articles, manage your profile, and do a lot more right under the hood.")
                return redirect('homepage')
            else:
                messages.error(request, 'Invalid username or password. Make sure that you enter a correct username or password. Incase you forget it, please reset your password')
                return redirect('login')

        users = User.objects.all()

        params = {
            'users': users,
        }
        # return render(request, 'account/login.html', params)
    return render(request, 'accounts/login.html', params)



def signup(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            try:
                user = User.objects.get(username=email)
                messages.warning(request, "Email already exists, try resetting password for this email.")
                redirect('signup')
            except User.DoesNotExist:
                new_user = User.objects.create_user(email, email, password1)

                # updating to Profile as well
                new_profile = Profile(fullname=name, username=email)

                new_user.save()
                new_profile.save()
                curr_user = authenticate(username=email, password=password1)
                if curr_user is not None:
                    login_auth(request, curr_user)

                    messages.warning(
                        request, f"Welcome to 'Deedews blog', {name} your account has been created sucessfully. Now you may go ahead and create your profile or surf article feeds.")
                    return redirect('homepage')

    return render(request, 'accounts/signup.html')


def profile(request):
    return render(request, 'accounts/profile.html')


def logout(request):
    if request.method == "GET":
        logout_auth(request)
        request.session.flush()
        messages.warning(
            request, "You have sucessfully been logged out of your account.")
        return redirect('homepage')
    return render(request, 'blog/homepage-e.html')


