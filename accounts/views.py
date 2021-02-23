from django.contrib.messages.api import success
from django.db.models import fields
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .token import account_activation_token
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView
from django.views import generic
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse

# custom imports here.
from .forms import CreateUserForm, Editprofileform
from accounts.models import UserProfile


def home(request):
    return render(request, "home.html")


# Fuction to get user information from registration form....
def register(request):
    user = User
    if request.user.is_authenticated:
        return redirect("profile")
    else:

        form = CreateUserForm()

        if request.method == "POST":
            form = CreateUserForm(request.POST)

            if form.is_valid():

                user = form.save(commit=False)
                user.is_active = False
                user = form.save()
                current_site = get_current_site(request)
                subject = "'Activate Your SizExpress Account"
                email_body = {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": account_activation_token.make_token(user),
                }

                link = reverse(
                    "activate",
                    kwargs={"uidb64": email_body["uid"], "token": email_body["token"]},
                )

                activate_url = "http://" + current_site.domain + link
                email_from = settings.EMAIL_HOST_USER

                email = EmailMessage(
                    subject,
                    "Hi "
                    + user.first_name
                    + ", Clik the link below to activate your SizExpress account \n"
                    + activate_url,
                    email_from,
                    [user.email],
                )
                email.send(fail_silently=False)
                messages.success(
                    request,
                    (
                        "Please activate your account to login, Activation link was sent to your email.(Check Spam)"
                    ),
                )

                firstname = form.cleaned_data.get("first_name")

                UserProfile.objects.create(
                    user=user,
                )

                messages.success(request, "Account was created for" + " " + firstname)
                return redirect("login")

        context = {"form": form}
        return render(request, "register.html", context)


from django.contrib.auth.forms import AuthenticationForm

# Fuction to log in User into the website
def loginPage(request):

    if request.user.is_authenticated:

        if request.user.userprofile.user_confirm == False:
            return redirect("profileinfo")
        else:
            return redirect("profile")
    else:

        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")

            user = authenticate(
                request,
                username=username,
                password=password,
            )
            if user is not None:

                # user.confirm_email.email_confirmed = True
                # print(user.confirm_email.email_confirmed)
                user.save()
                print("Person was logged in ")
                if user.is_active == True:

                    # if user.confirm_email.email_confirmed == True:
                    print("User is valid, active and authenticated")
                    login(request, user)
                    if request.user.userprofile.user_confirm == False:
                        return redirect("profileinfo")
                    else:
                        return redirect("profile")
                else:
                    print("The password is valid, but the account has been disabled!")
                    messages.info(
                        request,
                        "Please activate your account to login, Activation link was sent to your email.",
                    )
            else:
                messages.info(request, "Incorrect Email or Password")

        context = {}
        return render(request, "login.html", context)


# Function to logout user from the website
def logoutPage(request):
    logout(request)
    return redirect("/")


# This is the function to display the users account page
@login_required(login_url="login")
def profile(request):
    return render(request, "profile.html")


def rates(request):
    return render(request, "rates.html")


@login_required(login_url="login")
def profileInfo(request):

    if request.user.is_authenticated:
        if request.user.userprofile.user_confirm == True:
            return redirect("profile")

        e_P_F = Editprofileform()
        if request.method == "POST":
            e_P_F = Editprofileform(request.POST, instance=request.user.userprofile)

            if e_P_F.is_valid():
                request.user.userprofile.user_confirm = True
                request.user.save
                e_P_F.save()
                messages.success(request, "Account has been updated")
                return redirect("login")

        e_P_F = Editprofileform(instance=request.user.userprofile)
        context = {"e_P_F": e_P_F}
        return render(request, "profileinfo.html", context)


@login_required(login_url="login")
def customer(request):
    return render(request, "cust.html")


from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.views.generic import View, UpdateView


class ActivateAccount(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            # user.confirm_email.email_confirmed = True
            user.save()
            login(request, user)
            messages.success(request, ("Your account have been confirmed."))
            return redirect("profile")
        else:
            messages.warning(
                request,
                (
                    "The confirmation link was invalid, possibly because it has already been used."
                ),
            )
            return redirect("home")
