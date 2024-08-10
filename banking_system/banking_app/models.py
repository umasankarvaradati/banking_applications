# Create your models here.

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError("Users must have a username")
        user = self.model(username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None):
        user = self.create_user(username, password)
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    username = models.CharField(max_length=30, unique=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'

    objects = UserManager()

    class Meta:
        app_label = 'banking_app' 

class Customer(models.Model):
    full_name = models.CharField(max_length=100)
    address = models.TextField()
    mobile_no = models.CharField(max_length=15)
    email_id = models.EmailField()
    ACCOUNT_TYPES = [
        ('S', 'Saving'),
        ('C', 'Current'),
    ]
    account_type = models.CharField(max_length=1, choices=ACCOUNT_TYPES)
    initial_balance = models.FloatField(max_length=10)
    dob = models.DateField()
    id_proof = models.CharField(max_length=50)
    account_no = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)

class Transaction(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    transaction_date = models.DateTimeField(auto_now_add=True)
    transaction_type = models.CharField(max_length=10) 
    amount = models.FloatField(max_length=10)
   