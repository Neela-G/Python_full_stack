
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Student_table
from .forms import Student_form_data
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def home(request):
    data = {
        'name': 'Neela',
        'age': 20,
        'department': 'BCA'
    }

    marks = [100, 80, 90]

    return render(request, 'home.html', {
        'data': data,
        'marks': marks
    })


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


# Normal HTML Form
def form(request):
    if request.method == "POST":
        Student_table.objects.create(
            reg_no=request.POST.get('reg_no'),
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            marks=request.POST.get('marks'),
            dob=request.POST.get('dob')
        )

        return HttpResponse("Saved Successfully!")

    return render(request, 'Student_form.html')


# Django Form
def Student_form_dj(request):
    if request.method == "POST":
        form = Student_form_data(request.POST)

        if form.is_valid():
            Student_table.objects.create(
                reg_no=form.cleaned_data['reg_no1'],
                name=form.cleaned_data['name1'],
                email=form.cleaned_data['email1'],
                marks=form.cleaned_data['marks1'],
                dob=form.cleaned_data['dob1']
            )

            return HttpResponse("Saved Successfully!")

    else:
        form = Student_form_data()

    return render(request, 'Student_form_data.html', {'form': form})


# User Login
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return HttpResponse("Invalid username or password!")

    return render(request, 'login.html')


# Dashboard
@login_required(login_url='login')
def dashboard(request):
    return render(request, 'dashboard.html')


# User Logout
def user_logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')

    return HttpResponse("Invalid request!")
