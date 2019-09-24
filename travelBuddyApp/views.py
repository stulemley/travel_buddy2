from django.shortcuts import render, redirect
from .models import User, Trip
from django.contrib import messages
from django.contrib.auth import logout
import bcrypt

# Create your views here.

def index(request):
    print('!!! running INDEX method !!!')
    return render(request, 'index.html')

def main(request):
    print('!!! running MAIN method !!!')
    return render(request, 'main.html')

def register(request):
    print('!!! running REGISTER method !!!')
    print(request.POST)
    errorsFromModelsValidator = User.objects.registration_validator(request.POST)
    print(errorsFromModelsValidator)
    print(len(errorsFromModelsValidator))
    
    if len(errorsFromModelsValidator) > 0:
        # entry is incorrect
        print('!!!   entry is INCORRECT   !!!')
        for key, value in errorsFromModelsValidator.items():
            messages.error(request, value)
        return redirect('/main')
    else:
        # entry is correct
        print('!!!   entry is CORRECT   !!!')
        print(request.POST['password'])
        hash1 = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        print(hash1)
        user = User.objects.create(name= request.POST['name'], user_name = request.POST['user_name'], password = hash1.decode() )
        print(user)
        request.session['loggedinuser']=user.id

    return redirect('/travels') 
# THERE IS A PROBLEM WITH THE ABOVE METHOD IN THAT LOGGEDINUSER DOES NOT CARRY THRU LOGIN. I CAN FIX THIS PRETTY EASILY I THINK
def login(request):
    print('!!! running LOGIN method !!!')
    print(request.POST)
    errorsFromLoginValidator = User.objects.login_validator(request.POST)
    if len(errorsFromLoginValidator)>0:
        for key, value in errorsFromLoginValidator.items():
            messages.error(request, value)
        return redirect('/')
    
    user = User.objects.filter(user_name = request.POST['user_name'])[0]
    print(user.id)
    request.session['loggedinuser']= user.id
    return redirect('/travels')

def logout(request):
    print('!!! running LOGOUT method !!!')
    if 'loggedinuser' not in request.session:
        return redirect('/main')
    else:  
        del request.session['loggedinuser']
    return redirect('/main')



def add_plan(request):
    print('!!!   running ADD_PLAN method   !!!')
    if 'loggedinuser' not in request.session:
        return redirect('/main')
    else:        
        context = {
            'loggedinuser': User.objects.get(id = request.session['loggedinuser']),
            # 'users_trips': Trip.objects.filter(user=request.POST['user']).all()
            # 'all_trips': Trip.objects.all()

        }
    return render(request, 'add_trip_form.html', context)

def create_trip(request):
    print('!!!   running CREATE_TRIP method   !!!')
    print(request.POST)
    errorsFromTripsValidator = Trip.objects.trip_validator(request.POST)
    if len(errorsFromTripsValidator)>0:
        print('!!!   entry is INCORRECT   !!!')
        for key, value in errorsFromTripsValidator.items():
            messages.error(request, value)
        return redirect('/travels/add')
    else:
        print('!!!   entry is CORRECT   !!!')
        loggedinuser = User.objects.get(id = request.session['loggedinuser'])
        trip = Trip.objects.create(dest=request.POST['dest'], desc=request.POST['desc'], travel_start=request.POST['travel_start'], travel_end = request.POST['travel_end'])
        print(trip)
        trip.users.add(loggedinuser)
    return redirect('/travels')

def read_all_trips(request):
    print('!!!   running READ_ALL_TRIPS method   !!!')
    if 'loggedinuser' not in request.session:
        return redirect('/main')
    else: 
        loggedinuser =  User.objects.get(id = request.session['loggedinuser'])
        trips_by_user = loggedinuser.trips.all()
        other_users_trips = Trip.objects.exclude(users = loggedinuser)
        # trip_creator = Trip.objects.filter      
        context = {
            'loggedinuser': loggedinuser,
            'trips_by_user': trips_by_user,
            'other_users_trips': other_users_trips,
            # 'trip_creator': trip_creator,
            # 'all_trips': Trip.objects.all()
        }
    return render(request, 'all_trips.html', context)

def trip_info(request, num):
    print('!!!   running TRIP_INFO method   !!!')
    if 'loggedinuser' not in request.session:
        return redirect('/main')
    else: 
        this_trip = Trip.objects.get(id=num)
        this_trip_creator = this_trip.users.first()
        this_trips_users = this_trip.users.all()
        this_trips_other_users = this_trip.users.exclude(id = request.session['loggedinuser'])
        context = {
            'this_trip': this_trip,
            'this_trip_creator' : this_trip_creator,
            'this_trips_users' : this_trips_users,
            'this_trips_other_users' : this_trips_other_users,
        }
    return render(request, 'one_trip.html', context)

def join(request, num):
    print('!!!   running JOIN method   !!!')
    if 'loggedinuser' not in request.session:
        return redirect('/main')
    else: 
        loggedinuser = User.objects.get(id = request.session['loggedinuser'])
        this_trip = Trip.objects.get(id=num)
        this_trip.users.add(loggedinuser)
    return redirect('/travels')





  