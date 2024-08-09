
from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.utils.crypto import get_random_string
import uuid

class Authentic(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100, default="first_name")
    last_name = models.CharField(max_length=100, default="last_name")
    email = models.EmailField(max_length=254, unique=True)  
    password = models.CharField(max_length=200) 
    is_verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=32, blank=True, null=True)
    reset_token = models.CharField(max_length=32, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # def set_password(self, raw_password):
    #     self.password = make_password(raw_password)
    
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
    
    def generate_reset_token(self):
        self.reset_token = get_random_string(length=32)
        self.save()
        
        
    def generate_verification_token(self):
        self.verification_token = get_random_string(length=32)
        self.save()

    def clear_verification_token(self):
        self.verification_token = None
        self.save()    

    def clear_reset_token(self):
        self.reset_token = None
        self.save()
    
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




class CustomUser(models.Model):
    authentic_token = models.ForeignKey(Authentic, on_delete=models.CASCADE)
    reset_token = models.CharField(max_length=32, blank=True, null=True)
    reset_token_expiry = models.DateTimeField(blank=True, null=True)

# class PasswordResetToken(models.Model):
#     user = models.ForeignKey(Authentic, on_delete=models.CASCADE)
#     token = models.UUIDField(default=uuid.uuid4, editable=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     expires_at = models.DateTimeField()










