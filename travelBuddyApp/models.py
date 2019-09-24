from django.db import models
import re
import bcrypt
import datetime

# Create your models here.

class UserManager(models.Manager):
    def registration_validator(self, postData):
        print('!!! running REGISTRATION VALIDATOR method !!!')
        registered_users = User.objects.filter(user_name = postData['user_name'])

        errors = {}
        # add keys and values to errors dictionary for each invalid field
        if len(postData['name']) < 3:
            errors["name"] = "Name should be at least 3 characters"
        if len(postData['user_name']) < 3:
            errors["user_name_short"] = "User Name should be at least 3 characters"
        if len(registered_users)>0:
            errors['user_name_taken'] = 'User Name is taken, choose another'
        if len(postData['password']) < 8:
            # This will be changed to ....postData['password']) <8:, but is left for now until i delete test users and upload real users
            errors['passwordlength'] = 'Password must be at least 8 characters'
        if postData['confirmPassword'] != postData['password']:
            errors['pwMatch'] = 'Password and confirm password must match'
        print(errors)
        return errors

    def login_validator(self,postData):
        print('!!! running LOGIN VALIDATOR method !!!')
        registered_users = User.objects.filter(user_name = postData['user_name'])
        print('!!!   printing REGISTERED USERS below:   !!!')
        print(registered_users)
        print('!!!   printing a USER below:   !!!')

        errors={}
        
        if len(postData['user_name'])<1:
            errors['user_name']= 'You must enter a User Name'
        if len(postData['password'])<1:
            errors['passwordrequired']= 'You must enter a password'
        if len(registered_users)<1:
            errors['user_not_found']= 'This User is not registered'
        else:
            user = registered_users[0]
            if bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
                print("!!!   PASSWORD MATCH   !!!")
            else:
                print("!!!   FAILED PASSWORD   !!!")
                errors['passwordInvalid']='The password is incorrect'
        
        print(errors)
        return errors

class TripManager(models.Manager):
    def trip_validator(self, postData):
        print('!!! running TRIP VALIDATOR method !!!')
        # date = postData['']
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        if len(postData['dest']) < 1:
            errors["dest"] = "Enter Destination"
        if len(postData['desc']) < 3:
            errors["desc"] = "Enter Trip Description"
        if postData['travel_start'] == "":
            errors["no_start_date"] = "Enter Start Date"
        if postData['travel_start']<= str(datetime.date.today()):
            errors['early_start_date']= 'Start date must be after today!'
        if postData['travel_end'] =="":
            errors["no_end_date"] = "Enter End Date"
        if postData['travel_end'] <= str(postData['travel_start']):
            errors['early_start_date']= 'End date must be after Start date!'


        # if len(postData['password']) < 2:
        #     errors['passwordlength'] = 'Password must be at least 8 characters'
        # if postData['confirmPassword'] != postData['password']:
        #     errors['pwMatch'] = 'Password and confirm password must match'
        print(errors)
        return errors

class User(models.Model):
    name = models.CharField(max_length=255)
    user_name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Trip(models.Model):
    dest = models.CharField(max_length=255)
    desc = models.CharField(max_length=255)
    travel_start = models.DateField()
    travel_end = models.DateField()
    users = models.ManyToManyField(User, related_name='trips')
    #  on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TripManager()
    
    
