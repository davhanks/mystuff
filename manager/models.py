from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth.models import AbstractUser

  
class Store(models.Model):
    '''This is the store class with all fields'''
    name = models.CharField(max_length=200, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    street = models.CharField(max_length=30, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=30, blank=True, null=True)
    zipCode = models.CharField(max_length=20, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    active = models.NullBooleanField(blank=True, null=True)

    def __str__(self):
        return 'Location: %s, street address: %s' %(self.location, self.street)

class User(AbstractUser):
    '''This is the extention of the AbstractUser class defined by django'''
    street = models.CharField(max_length=30, blank=True, null=True)
    street2 = models.CharField(max_length=30, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=30, blank=True, null=True)
    zipCode = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    active = models.NullBooleanField(blank=True, null=True)

class Employee(models.Model):
    '''This class has a one-to-one relationship with User'''
    user = models.OneToOneField('User')
    hire_date = models.DateField(blank=True, null=True)
    termination_date = models.DateField(blank=True, null=True)
    salary = models.DecimalField(max_digits=20,decimal_places=2,blank=True, null=True)
    active = models.NullBooleanField(blank=True, null=True)

class CatalogInventory(models.Model):
    '''The conceptual inventory class'''
    product_name = models.CharField(max_length=200,blank=True, null=True)
    description = models.CharField(max_length=200,blank=True, null=True)
    manufacturer = models.CharField(max_length=200,blank=True, null=True)
    average_cost = models.DecimalField(max_length=200,max_digits=10, decimal_places=2, blank=True, null=True)
    commission_rate = models.DecimalField(max_digits=20,decimal_places=2,blank=True, null=True)
    product_category = models.CharField(max_length=200,blank=True, null=True)
    sku = models.IntegerField(max_length=10,blank=True, null=True)
    active = models.NullBooleanField(blank=True, null=True)
    sale_price = models.DecimalField(max_length=200,max_digits=10, decimal_places=2, blank=True, null=True)
    image = models.CharField(max_length=200, blank=True, null=True)

class Product(models.Model):
    '''This is the physical product class'''
    catalog_inventory = models.ForeignKey('CatalogInventory')
    store = models.ForeignKey('Store')
    serial_number = models.CharField(max_length=200,blank=True,null=True)
    shelf_location = models.CharField(max_length=200,blank=True,null=True)
    purchase_date = models.DateField(blank=True,null=True)
    is_rental = models.NullBooleanField(blank=True, null=True)
    active = models.NullBooleanField(blank=True, null=True)

class Sale(models.Model):
    '''The Sale (Transaction) class'''
    employee = models.ForeignKey('Employee')
    date = models.DateTimeField(auto_now_add=True)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    tax_ammount = models.DecimalField(max_digits=10, decimal_places=2,blank=True, null=True)

class SaleItem(models.Model):
    '''An item in a sale'''
    sale = models.ForeignKey('Sale')
    product = models.ForeignKey('Product')

class Commission(models.Model):
    employee = models.ForeignKey('Employee')
    sale = models.OneToOneField('Sale')
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)