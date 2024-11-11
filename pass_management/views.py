from django.shortcuts import render, redirect
import random
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User , AnonymousUser
from django.contrib.auth import logout, authenticate, login as user_login
from django.contrib import messages
from .models import *
from datetime import date
from django.views import View
from .forms import RegistrationForm, AddPassForm

def index(request):
    return render(request, "index.html")

def purchase_pass(request):
    return render(request, "purchase_pass.html")

class Signup(View):
    def get(self,request):
        form = RegistrationForm()
        context = {"form":form}
        return render(request, "signup.html", context)
    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User created successfully.")
            return redirect('login')
        else:
            messages.error(request, "Error in creating user.")
        return render(request, "signup.html")
    

def login(request):
    if request.method == "POST":
        Username = request.POST.get('Username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=Username, password=password)
        
        if user is not None:
            user_login(request, user) 
            
            if user.is_staff:
                return redirect('/dashborad/') 
            else:
                return redirect('/user_dashboard/')  
        else:
            return render(request, "login.html", {"error": "Invalid Username or password"})

    return render(request, "login.html")

@login_required(login_url='/login/')
def logoutUser(request):
    logout(request)
    return redirect("/login")

@login_required(login_url='/login/')
def dashborad(request):
    return render(request,'dashboard.html')

@login_required(login_url='/login/')
def user_dashborad(request):
    return render(request,'user_dashborad.html')

@login_required(login_url='/login/')
def add_category(request):
    error = ""
    if request.method == "POST":
        catname = request.POST['categoryname']
        try:
            Category.objects.create(categoryname=catname)
            error = "no"
        except:
            error = "yes"
    return render(request, 'add_Category.html', locals())

@login_required(login_url='/login/')
def manage_category(request):
    cat = Category.objects.all()
    return render(request,'mange_category.html', locals())

@login_required(login_url='/login/')
def edit_Category(request, pid):
    cat = Category.objects.get(id=pid)
    error = ""
    if request.method == "POST":
        catname = request.POST['categoryname']

        cat.categoryname = catname

        try:
            cat.save()
            error = "no"
        except:
            error = "yes"
    return render(request, 'edit_catergory.html', locals())

class AddPass(View):
    def get(self, request):
        form = AddPassForm()
        category = Category.objects.all()
        return render(request,'add_pass.html', {"form": form, 'category':category})
    
    def post(self, request):
        form  = AddPassForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Data saved sccessfully.")
        else:
            messages.error(request, "error in saving data")
        return redirect('add_pass')

@login_required(login_url='/login/')
def delete_Category(request, pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    cat = Category.objects.get(id=pid)
    cat.delete()
    return redirect('manage_category')

@login_required(login_url='/login/')
def manage_pass(request):
    pas = Pass.objects.all()
    return render(request,'manage_pass.html',locals())

def edit_pass(request, pid):
    pas = Pass.objects.get(id=pid)
    category1 = Category.objects.all()
    error = ""
    if request.method == "POST":
        fn = request.POST['FullName']
        cno = request.POST['ContactNumber']
        email = request.POST['Email']
        itype = request.POST['IdentityType']
        icardno = request.POST['IdentityCardno']
        ct = request.POST['category']
        source = request.POST['Source']
        dest = request.POST['Destination']
        fdate = request.POST['FromDate']
        todate = request.POST['ToDate']
        cost = request.POST['Cost']

        category = Category.objects.get(id=ct)

        pas.FullName = fn
        pas.ContactNumber = cno
        pas.Email = email
        pas.IdentityType = itype
        pas.IdentityCardno = icardno
        pas.category = category
        pas.Source = source
        pas.Destination = dest
        pas.Cost = cost

        if fdate:
            pas.FromDate = fdate
        if todate:
            pas.ToDate = todate

        try:
            pas.save()
            error = "no"
        except:
            error = "yes"

        try:
            pimg = request.FILES['ProfileImage']
            pas.ProfileImage = pimg
            pas.save()
        except:
            pass
    return render(request, 'edit_pass.html', locals())

def delete_pass(request, pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    pas = Pass.objects.get(id=pid)
    pas.delete()
    return redirect('manage_pass')

@login_required(login_url='/login/')
def read_queries(request):
    return render(request,'read_queries.html')

@login_required(login_url='/login/')
def mange_queries(request):
    return render(request,'manage_queries.html')

def contact(request):
    return render(request,"contact.html")
def about(request):
    return render(request,"about.html")
