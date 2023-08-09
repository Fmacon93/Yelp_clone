from django.db import models
import re

# Create your models here.
class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First Name should be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last Name should be at least 2 characters"
        if len(postData['city']) < 2:
            errors["city"] = "City should be at least 2 characters"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] =  "Invalid email address"
        if len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters"
        if postData['password'] != postData['confirm']:
            errors['confirm'] = "Passwords don't match!"
        return errors
    def login_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['login_email']):
            errors['login'] =  "Invalid Email/Password"
        if len(postData['login_pw']) < 8:
            errors["login"] = "Invalid Email/Password"
        return errors

    def edit_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First name should be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last name should be at least 2 characters"
        if len(postData['city']) < 2:
            errors["city"] = "City should be at least 2 characters"
        if len(postData['state']) != 2:
            errors["state"] = "State should be two characters"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    city = models.CharField(max_length=45)
    state = models.CharField(max_length=2)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    profile_image = models.ImageField(upload_to='profile_image', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    def __repr__(self): 
        return f"<ID: {self.id} First Name: {self.first_name} Last Name: {self.last_name} City: {self.city} State: {self.city} Email: {self.email}>"

class RestaurantManager(models.Manager):
    def restaurant_validator(self, postData):
        errors = {}
        if len(postData['name']) < 2:
            errors['name'] = "Restaurant name should be atleast 2 characters."
        if len(postData['owner']) < 2:
            errors['owner'] = "Owner name should be atleast 2 characters."
        if len(postData['address']) < 2:
            errors['address'] = "Adress name should be atleast 2 characters."
        if len(postData['city']) < 1:
            errors['city'] = "City is required."
        if len(postData['desc']) < 10:
            errors['desc'] = "Description should be atleast 10 characters."
        if len(postData['category']) < 1:
            errors['desc'] = "Category is required."
        return errors

class Restaurant(models.Model):
    name = models.CharField(max_length=45)
    owner = models.CharField(max_length=255)
    address = models.CharField(max_length=45)
    city = models.CharField(max_length=45)
    state = models.CharField(max_length=2)
    desc = models.TextField()
    category = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = RestaurantManager()

    def __repr__(self): 
        return f"<ID: {self.id} First Name: {self.name} Last Name: {self.address}"

class ReviewManager(models.Manager):
    def review_validator(self, postData):
        errors = {}
        if len(postData['user']) < 1:
            errors['user'] = "User required."
        if len(postData['review']) == 0:
            errors['review'] = "Review required."
        return errors
    
class Review(models.Model):
    user = models.ForeignKey(User, related_name="user", on_delete = models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, related_name="restaurant", on_delete = models.CASCADE)
    rating = models.PositiveIntegerField()
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = ReviewManager()
    def __repr__(self): 
        return f"<ID: {self.user} First Name: {self.name} Last Name: {self.rating}>"

class UploadedImage(models.Model):
    image = models.ImageField(upload_to='uploads')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)