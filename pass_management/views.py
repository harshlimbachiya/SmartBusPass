from django.shortcuts import render, redirect
import random
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User , AnonymousUser
from django.contrib.auth import logout, authenticate, login as user_login
from django.contrib import messages
from .models import *
from django.http import HttpResponse

from django.shortcuts import get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
import razorpay
from django.http import JsonResponse
from datetime import date
from django.views import View
from .forms import *
from django.conf import settings


def index(request):
    return render(request, "index.html")

RAZORPAY_API_KEY = "rzp_test_9KT1VnGZkZcooB"
RAZORPAY_API_SECRET = "X2jkQlU4TiddqahAzkSFdMb5"
razorpay_client = razorpay.Client(auth=(RAZORPAY_API_KEY, RAZORPAY_API_SECRET))


@login_required(login_url='/login/')

def purchase_pass(request):
    # Get source and destination locations for dropdown
    source_locations = Location.objects.all()
    destination_locations = Location.objects.all()

    if request.method == 'POST':
        form = PassForm(request.POST)
        if form.is_valid():
            pass_obj = form.save(commit=False)  
            cost = request.POST.get("Cost", 0)  
            try:
                amount = int(float(cost) * 100)  

                
                razorpay_order = razorpay_client.order.create({
                    "amount": amount,
                    "currency": "INR",
                    "payment_capture": "1"  
                })

              
                pass_obj.razorpay_order_id = razorpay_order['id']
                pass_obj.save() 

                
                context = {
                    'razorpay_order_id': razorpay_order['id'],
                    'razorpay_key': "RAZORPAY_API_KEY", 
                    'amount': amount,
                    'form': form,
                    'source_locations': source_locations,
                    'destination_locations': destination_locations,
                }
                return render(request, 'purchase_pass.html', context)

            except Exception as e:
                messages.error(request, f"Error creating Razorpay order: {str(e)}")
        else:
            messages.error(request, "Form validation failed. Please try again.")
    
    else:
        form = PassForm()

    return render(request, 'purchase_pass.html', {
        'form': form,
        'source_locations': source_locations,
        'destination_locations': destination_locations
    })


# def view_pass(request):
#     sd = None
#     pas = None
#     if request.method == 'POST':
#         sd = request.POST['searchdata']
#     try:
#         pas = Pass.objects.filter(PassNumber=sd)
#     except:
#         pas = ""
#     return render(request, 'pass_enquiry.html', locals())
  # Import Q for OR conditions

def view_pass(request):
    sd = None
    pas = None
    if request.method == 'POST':
        sd = request.POST['searchdata']
        try:
            # Update to use the correct field name 'ContactNumber'
            pas = Pass.objects.filter(Q(PassNumber=sd) | Q(ContactNumber=sd))
        except Exception as e:
            print(f"Error: {e}")  # Debugging log
            pas = None
    return render(request, 'pass_enquiry.html', locals())





def PassEnquiryDtls(request,pid):
    pas = Pass.objects.get(id=pid)
    return render(request, 'view_PassEnquiryDtls.html', locals())


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
    return render(request, 'add_category.html', locals())

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
@login_required(login_url='/login/')
def delete_Category(request, pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    cat = Category.objects.get(id=pid)
    cat.delete()
    return redirect('manage_category')

@login_required(login_url='/login/')
def add_pass(request):
    # Get source and destination locations for dropdown
    source_locations = Location.objects.all()  # Or any other logic you use to fetch locations
    destination_locations = Location.objects.all()

    if request.method == 'POST':
        form = PassForm(request.POST)
        if form.is_valid():
            pass_obj = form.save()
            # Assuming 'pn' is the pass number or some identifier for success message
            return render(request, 'add_pass.html', {'form': form, 'source_locations': source_locations, 'destination_locations': destination_locations, 'error': 'no', 'pn': pass_obj.PassNumber})
        else:
            # If the form is invalid, return the same form with errors
            return render(request, 'add_pass.html', {'form': form, 'source_locations': source_locations, 'destination_locations': destination_locations, 'error': 'yes'})
    else:
        form = PassForm()

    # Render the form on the page with empty data on GET request
    return render(request, 'add_pass.html', {'form': form, 'source_locations': source_locations, 'destination_locations': destination_locations})

@staff_member_required
def manage_pass(request):
    # Fetch all the pass entries
    pas = Pass.objects.all()
    return render(request, 'manage_pass.html', {'pas': pas})

@login_required(login_url='/login/')
def edit_pass(request, pass_id):
    # Get the pass instance you want to edit
    pass_instance = get_object_or_404(Pass, id=pass_id)

    # Check if the form is being submitted via POST
    if request.method == 'POST':
        form = PassForm(request.POST, instance=pass_instance)
        if form.is_valid():
            # Save the form data to the database
            form.save()
            # Redirect to the manage pass page after saving
            return redirect('manage_pass')
    else:
        # If it's a GET request, load the form with the existing pass data
        form = PassForm(instance=pass_instance)

    # Render the edit_pass template with the form
    return render(request, 'edit_pass.html', {'form': form})





def get_cost(request):
    source_id = request.GET.get('source')
    destination_id = request.GET.get('destination')
    category_id = request.GET.get('category')

    try:
        # Get the source, destination, and category objects
        source = Location.objects.get(id=source_id)
        destination = Location.objects.get(id=destination_id)
        category = Category.objects.get(id=category_id)

        # Get the route cost
        route_cost = RouteCost.objects.get(source=source, destination=destination)
        base_cost = route_cost.base_cost

        # Calculate cost based on category
        if category.categoryname == 'Daily':
            cost = base_cost * 1
        elif category.categoryname == 'Monthly':
            cost = base_cost * 30
        elif category.categoryname == 'Quarterly':
            cost = base_cost * 90
        else:
            cost = base_cost

        return JsonResponse({'success': True, 'cost': cost})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required(login_url='/login/')
def delete_pass(request, pid):
    try:
        pas = Pass.objects.get(id=pid)
        pas.delete()  # Delete the pass
        messages.success(request, "Pass deleted successfully.")
    except Pass.DoesNotExist:
        messages.error(request, "Pass not found.")
    
    return redirect('manage_pass')



class RouteCostListView(View):
    def get(self, request):
        route_costs = RouteCost.objects.all()
        return render(request, 'routecost_list.html', {'route_costs': route_costs})

class RouteCostCreateView(View):
    def get(self, request):
        # Get the list of source and destination locations
        source_locations = Location.objects.all()
        destination_locations = Location.objects.all()

        # Create the form instance
        form = RouteCostForm()

        # Pass the form and locations to the template
        return render(request, 'routecost_form.html', {
            'form': form,
            'source_locations': source_locations,
            'destination_locations': destination_locations,
        })

    def post(self, request):
        form = RouteCostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('routecost_list')
        # Pass the form and locations again on POST to handle validation errors
        source_locations = Location.objects.all()
        destination_locations = Location.objects.all()
        return render(request, 'routecost_form.html', {
            'form': form,
            'source_locations': source_locations,
            'destination_locations': destination_locations,
        })

class RouteCostUpdateView(View):
    def get(self, request, pk):
        route_cost = get_object_or_404(RouteCost, pk=pk)
        form = RouteCostForm(instance=route_cost)
        return render(request, 'routecost_form.html', {'form': form})

    def post(self, request, pk):
        route_cost = get_object_or_404(RouteCost, pk=pk)
        form = RouteCostForm(request.POST, instance=route_cost)
        if form.is_valid():
            form.save()
            return redirect('routecost_list')
        return render(request, 'routecost_form.html', {'form': form})

class RouteCostDeleteView(View):
    def get(self, request, pk):
        route_cost = get_object_or_404(RouteCost, pk=pk)
        route_cost.delete()
        return redirect('routecost_list')



class LocationListView(View):
    def get(self, request):
        locations = Location.objects.all()
        return render(request, 'location_list.html', {'locations': locations})

class LocationCreateView(View):
    def get(self, request):
        form = LocationForm()
        return render(request, 'location_form.html', {'form': form})

    def post(self, request):
        form = LocationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('location_list')  # Redirect to the location list view after saving
        return render(request, 'location_form.html', {'form': form})

class LocationUpdateView(View):
    def get(self, request, pk):
        location = get_object_or_404(Location, pk=pk)
        form = LocationForm(instance=location)
        return render(request, 'location_form.html', {'form': form})

    def post(self, request, pk):
        location = get_object_or_404(Location, pk=pk)
        form = LocationForm(request.POST, instance=location)
        if form.is_valid():
            form.save()
            return redirect('location_list')  # Redirect to the location list view after updating
        return render(request, 'location_form.html', {'form': form})

class LocationDeleteView(View):
    def get(self, request, pk):
        location = get_object_or_404(Location, pk=pk)
        location.delete()  # Correct deletion logic
        return redirect('location_list')  # Correct redirect name
    
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


# List all queries (Read)
def read_queries(request):
    # Only allow admins to access the contact queries
    if not request.user.is_staff:
        return redirect('home')  # or a different page if necessary
    
    contacts = Contact.objects.all()
    return render(request, "admin/read_queries.html", {"contacts": contacts})

# Create or update a contact query
def manage_queries(request):
    if not request.user.is_staff:
        return redirect('home')  # or a different page if necessary
    
    contacts = Contact.objects.all()
    return render(request, "admin/manage_queries.html", {"contacts": contacts})

# Update an existing contact query
def update_query(request, pk):
    if not request.user.is_staff:
        return redirect('home')  # or a different page if necessary

    contact = get_object_or_404(Contact, pk=pk)
    if request.method == "POST":
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            return redirect('read_queries')
    else:
        form = ContactForm(instance=contact)
    
    return render(request, 'admin/update_query.html', {'form': form, 'contact': contact})

# Delete a contact query
def delete_query(request, pk):
    if not request.user.is_staff:
        return redirect('home')  # or a different page if necessary

    contact = get_object_or_404(Contact, pk=pk)
    contact.delete()
    return redirect('read_queries')



@login_required(login_url='/login/')
def payment_success(request):
    payment_id = request.GET.get('payment_id')
    order_id = request.GET.get('order_id')
    signature = request.GET.get('signature')

    # Optional: Verify payment signature using Razorpay API
    try:
        razorpay_client.utility.verify_payment_signature({
            "razorpay_order_id": order_id,
            "razorpay_payment_id": payment_id,
            "razorpay_signature": signature
        })
        return HttpResponse("Payment successful! Your Pass has been generated.")
    except razorpay.errors.SignatureVerificationError:
        return HttpResponse("Payment verification failed. Please contact support.")