# models.py

from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password

class Authentic(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100, default="first_name")
    last_name = models.CharField(max_length=100, default="last_name")
    email = models.EmailField(max_length=254, unique=True)  
    password = models.CharField(max_length=200) 
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # def set_password(self, raw_password):
    #     self.password = make_password(raw_password)
    
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
    
    def save(self, *args, **kwargs):
        if not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)
    

    
    def __str__(self):
        return self.first_name

class LoginUser(models.Model):
    authentic = models.ForeignKey(Authentic, on_delete=models.CASCADE)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=200)

    def validate_login(self):
        try:
            authentic_user = Authentic.objects.get(email=self.email)
        except Authentic.DoesNotExist:
            return False

        return authentic_user.check_password(self.password)

















