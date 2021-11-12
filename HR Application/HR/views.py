from django.shortcuts import render
from .models import User, Employee, RequestedLeaves
from django.http import HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from datetime import datetime
import dateutil.parser
import pickle
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt

sid = SentimentIntensityAnalyzer()


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/HR/home/')
            else:
                return HttpResponseRedirect("Account Disabled")
        else:
            print("Invalid credentials: {0}, {1}".format(username, password))
            return HttpResponseRedirect("Invalid login credentials")
    else:
        return render(request, 'HR/login.html', {})


@login_required(redirect_field_name='/HR/login/')
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/HR/home/')


def home(request):
    context = {}
    return render(request, 'HR/home.html', context)


def employee_profile(request):
    context = {}
    try:
        user = User.objects.get(username=request.user.username)
        emp = Employee.objects.get(emp=user)
        context["emp"] = emp
    except:
        pass
    return render(request, 'HR/employee_profile.html', context)



def employee_leaves(request):
    context = {}
    if request.method == 'POST':

        try:
            user = User.objects.get(username=request.user.username)
            emp = Employee.objects.get(emp=user)
            dt = dateutil.parser.parse(datetime.now().strftime("%m/%d/%y %H:%M:%S"))
            leave = RequestedLeaves(id=None, subject=request.POST.get('subject'), requestedLeaves_text=request.POST.get('text'), date_time=dt,  whyLeaves=emp.name, requestedLeaves=user)
            leave.save()
        except:
            pass

    return render(request, 'HR/employee_leaves.html', context)


def dashboard(request):
    context = {}
    profiles = []
    user = User.objects.get(username=request.user.username)
    if user.is_superuser:
        employees = Employee.objects.all()
        for emp in employees:
            profiles.append(emp)
    context["profiles"] = profiles
    return render(request, 'HR/dashboard.html', context)


def requested_leaves(request):
    context = {}
    comp = []
    user = User.objects.get(username=request.user.username)
    if user.is_superuser:
        requestedLeaves = RequestedLeaves.objects.all()
        for i in requestedLeaves:
            comp.append(i)
    else:
        requestedLeaves = RequestedLeaves.objects.filter(requestedLeaves=user)
        for i in requestedLeaves:
            comp.append(i)
    context['leaves'] = comp

    return render(request, 'HR/leaves.html', context)

def display_leaves(request):
    context = {}
    comp = []
    user = User.objects.get(username=request.user.username)
    if user.is_superuser:
        requestedLeaves = RequestedLeaves.objects.all()
        for i in requestedLeaves:
            comp.append(i)
    else:
        requestedLeaves = RequestedLeaves.objects.filter(requestedLeaves=user)
        for i in requestedLeaves:
            comp.append(i)
    context['leaves'] = comp

    return render(request, 'HR/display_myleaves.html', context)

def pie_chart(reviews, label):

    fig = plt.figure()
    plt.pie(reviews, labels=label, explode=(0.05, 0.05, 0.05, 0.05, 0.05), autopct='%1.1f%%', shadow=True, startangle=140)
    plt.axis('equal')
    fig.savefig("/home/mayank/ERP/HR/static/HR/graph.png")
    plt.close(fig)


def about(request):
    context = {}
    try:
        user = User.objects.get(username=request.user.username)
        emp = Employee.objects.get(emp=user)
        context["emp"] = emp
    except:
        pass
    return render(request, 'HR/about.html', context)
