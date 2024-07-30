from django.shortcuts import redirect
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from crudapp.models import User1
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from crudapp.models import Contact1
from django.contrib import messages
from django.contrib.auth import logout

# from django.contrib.auth.models import User

from django.contrib.auth import get_user_model  # new added

# from django.contrib.auth import authenticate, login
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from datetime import datetime

User = get_user_model()  # This ensures you are using the custom user model


def homePage(request):
    return render(request, "index.html")


def about(request):
    return render(request, "about.html")


def service(request):
    return render(request, "service.html")


def project(request):
    return render(request, "project.html")


def blog(request):
    return render(request, "blog.html")


def team(request):
    return render(request, "team.html")


def testimonial(request):
    return render(request, "testimonial.html")


def error(request):
    return render(request, "404.html")


def contact(request):
    return render(request, "contact.html")


@login_required
def users(request):
    user = User1.objects.all()
    header_data = request.session.get("header_data", {})

    context = {"users": user, "header": header_data}
    return render(request, "users.html", context)


def add_users(request):
    return render(request, "add_users.html")


def savedata(request):
    if request.method == "POST":
        # Retrieve data from the form
        name = request.POST.get("sname")
        address = request.POST.get("saddress")

        phone = request.POST.get("sphone")

        # Create a new Student instance and save it to the database
        student = User1(uname=name, uaddress=address, uphone=phone)
        student.save()

        # Redirect or render a response as needed
        return redirect("users")


def edit_view(request, id):

    # Retrieve the specific student with the provided id
    user = get_object_or_404(User1, id=id)

    if request.method == "POST":

        # Get the specific student by ID
        user = User1.objects.get(id=id)
        user.uname = request.POST.get("sname")
        user.uaddress = request.POST.get("saddress")

        user.uphone = request.POST.get("sphone")

        # Save the updated student
        user.save()

        # Redirect to a success page or the student detail page
        return redirect("users")

    return render(request, "edit.html", {"users": user})


def delete(request, id):
    user = User1.objects.get(id=id)
    user.delete()
    return redirect("users")


def registration(request):
    if request.user.is_authenticated:
        return redirect("users")
    if request.method == "POST":
        # Retrieve data from the form
        name = request.POST.get("sname")
        email = request.POST.get("semail")
        password = request.POST.get("spassword")

        data = User.objects.create_user(
            username=name, email=email, password=password, date_joined=datetime.now()
        )
        data.save()
        return redirect("login")
    return render(request, "registration.html")


def login(request):
    if request.user.is_authenticated:
        return redirect("users")

    if request.method == "POST":
        # Retrieve data from the form

        name = request.POST["sname"]
        password = request.POST["spassword"]
        user = auth.authenticate(request, username=name, password=password)

        if user is not None:
            auth.login(request, user)
            # last_login = user.last_login
            last_login = user.update_last_login()
            today = datetime.now()
            dayMonth = today.strftime("%B %d %Y")

            # # Convert datetime to string
            # last_login_str = last_login.strftime('%Y-%m-%d %H:%M:%S.%f') if last_login else 'Never'

            # print(f'Last_login : {last_login}, Today : {today}')

            difference = today - last_login

            # Convert the difference to days, hours, and minutes
            total_seconds = difference.total_seconds()
            days = total_seconds // (24 * 3600)
            hours = (total_seconds % (24 * 3600)) // 3600
            minutes = (total_seconds % 3600) // 60

            last_login = (
                f"{int(days)} days"
                if days > 0
                else (
                    f"{int(hours)} hours"
                    if hours > 0
                    else (
                        f"{int(minutes)} minutes"
                        if minutes > 0
                        else f"{int(total_seconds)} seconds"
                    )
                )
            )
            # print(f'Last : {last_login}')
            request.session["header_data"] = {
                "last_login": last_login,
                "dayMonth": dayMonth,
                "name": name,
            }

            # header_data = {'last_login':last_login_str, 'dayMonth':dayMonth, 'name':name}
            # # rendered_response = render(request, 'header_app.html', {'data': data})
            # request.session['rendered_response'] = header_data
            return redirect("users")
        else:
            messages.error(request, "You are not registered.")
            return redirect("registration")
    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("home")  # Redirect to the login page after logout


def contact_users(request):
    user = Contact1.objects.all()
    return render(request, "contactUsers.html", {"contacts": user})


def storedata(request):
    if request.method == "POST":
        # Retrieve data from the form
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        service = request.POST.get("service")

        # Create a new Student instance and save it to the database
        student = Contact1(uname=name, uemail=email, uphone=phone, uservices=service)
        student.save()

        # Redirect or render a response as needed
        return redirect("home")


def delete1(request, id):
    user = Contact1.objects.get(id=id)
    user.delete()
    return redirect("contact_users")
