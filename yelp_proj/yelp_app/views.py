from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from .models import *
from .forms import *
from django.contrib import messages
import bcrypt


def index(request):
    if 'user_id' in request.session:
        print(request.session['user_id'])
        context = {
            'all_the_restaurants' : Restaurant.objects.all(),
            'user' : request.session['user_id']
        }
        return render(request, 'index.html', context)
    else:
        print("I'm in the else")
        context = {
            'all_the_restaurants' : Restaurant.objects.all(),
            'user': 0
        }
        return render(request, 'index.html', context)

def login(request):
    return render(request, 'login.html')


def addUser(request):
    if request.method == "POST":
        errors = User.objects.register_validator(request.POST)
        # check if the errors dictionary has anything in it
        if len(errors) > 0:
            for key, value in errors.items():
            
                messages.error(request, value, extra_tags=key)
            return redirect('/')
    
        user = User.objects.filter(email=request.POST['email'])
        if len(user) > 0:
            messages.error(request, "Email is already in use.", extra_tags="email")
            return redirect('/')

        pw = bcrypt.hashpw(request.POST['password'].encode(),bcrypt.gensalt()).decode()

        User.objects.create(
            first_name=request.POST['first_name'], 
            last_name=request.POST['last_name'],
            city = request.POST['city'],
            state = request.POST['state'],
            email=request.POST['email'],
            password=pw
            )

        request.session['user_id'] = User.objects.last().id
        return redirect('/')
    else:
        return redirect('/')

def userlogin(request):
    if request.method == "POST":
        errors = User.objects.login_validator(request.POST)
        if len(errors) > 0:
            for key,value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect('/login')

        user = User.objects.filter(email=request.POST['login_email'])
        if len(user) == 0:
            messages.error(request, "Invalid Email/Password.", extra_tags="login")
            return redirect('/login')

        if not bcrypt.checkpw(request.POST['login_pw'].encode(),user[0].password.encode()):
            messages.error(request, "Invalid Email/Password.", extra_tags="login")
            return redirect('/login')

        request.session['user_id'] = user[0].id
        request.session['first_name'] = user[0].first_name
        request.session['last_name'] = user[0].last_name
        request.session['city'] = user[0].city
        request.session['state'] = user[0].state
        request.session['email'] = user[0].email

        return redirect('/')
    else:
        return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')



#Users

def user(request, user_id):#User Page
    form = User_Form()
    context ={
        'user' : User.objects.get(id=user_id),
        'form' : form,
        'first': request.session['first_name'],
        'last': request.session['last_name'],
        'city': request.session['city'],
        'state': request.session['state'],
        'email': request.session['email']
    }
    return render(request, 'user.html', context)




def edit(request):
    if request.method == "POST":
        errors = User.objects.edit_validator(request.POST)
        user_id = request.session['user_id']
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags = key)
            return redirect('/user/' + str(user_id))
    

        user_id = request.session['user_id']
        user_to_update = User.objects.get(id = user_id)
        user_to_update.first_name = request.POST['first_name']
        user_to_update.last_name = request.POST['last_name']
        user_to_update.city = request.POST['city']
        user_to_update.state = request.POST['state']
        user_to_update.save()

        request.session['message'] = "Edit successful, please re-login!"

        return redirect('/user/' + str(user_id))
    else:
        return redirect('/user/' + str(user_id))
        


# def update_profile_image(request):
#     form = User_Form()
#     if request.method == 'POST':
#         form = Profile_Form(request.POST, request.FILES)
#         if form.is_valid():
#             user_pr = form.save(commit=False)
#             user_pr.display_picture = request.FILES['profile_picture']
#             file_type = user_pr.display_picture.url.split('.')[-1]
#             file_type = file_type.lower()
#             if file_type not in IMAGE_FILE_TYPES:
#     return render(request, 'profile_maker/error.html')
#             user_pr.save()
#             return render(request, 'profile_maker/details.html', {'user_pr': user_pr})
#     context = {"form": form,}
#     return render(request, 'profile_maker/create.html', context)




#Restaurants


def add_restaurant(request):

    return render(request, 'addrestaurant.html')






def makerestaurant(request):
    if request.method == "POST":
        errors = Restaurant.objects.restaurant_validator(request.POST)

        if len(errors) > 0:
            for key,value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect('/')
    
    restaurant = Restaurant.objects.create(name = request.POST['name'], owner = request.POST['owner'], address= request.POST['address'], city =request.POST['city'], state=request.POST['state'], desc=request.POST['desc'], category=request.POST['category'])

    rest_id = restaurant.id
    request.session['rest_id'] = rest_id 

    return redirect('/restaurant/' + str(rest_id))

def restaurant(request, rest_id):
    onerest = Restaurant.objects.get(id=rest_id)

    context = {
        'onerest': onerest,
        'all_restaurant': Restaurant.objects.all(),
        # 'user': user,
        'review': Review.objects.all()
    }

    return render(request, 'restaurant.html', context)

def all_restaurants(request):
    context = {
        'all_restaurant': Restaurant.objects.all(),
    }
    return render(request, 'all_restaurants.html', context)








#Reviews



def addreview(request, rest_id, user_id):

    onerest = Restaurant.objects.get(id=rest_id)
    user = User.objects.get(id = request.session['user_id'])

    context = {
        'onerest': onerest,
        'all_restaurant': Restaurant.objects.all(),
        'user': user,
    }

    return render(request, 'addreview.html', context)

def add_review(request, rest_id, user_id):
    onerest = Restaurant.objects.get(id=rest_id)
    user = User.objects.get(id = request.session['user_id'])

    Review.objects.create(user = user, restaurant = onerest, rating = request.POST['rating'], review = request.POST['review'])

    return redirect('/restaurant/' + str(rest_id))

def delete(request, rest_id, rev_id):

    destroy = Review.objects.get(id=rev_id)
    destroy.delete()
    return redirect('/restaurant/' + str(rest_id))

