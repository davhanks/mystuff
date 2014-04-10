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
    ## The commented fields are inherited from Django's user class

    #first_name
    #last_name
    #username
    #email
    #password #This is stored as a hash. Set with the set_password() method
    #is_superuser # boolean field
    #is_staff # boolean field
    street = models.CharField(max_length=30, blank=True, null=True)
    street2 = models.CharField(max_length=30, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=30, blank=True, null=True)
    zipCode = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    active = models.NullBooleanField(blank=True, null=True)
    security_question = models.CharField(max_length=250, blank=True, null=True)
    security_answer = models.CharField(max_length=50, blank=True, null=True)

class PasswordReset(models.Model):
    '''Necessary info to reset the password for a user that has forgotten theirs.'''
    valid_date = models.DateTimeField(auto_now_add=False)
    used = models.NullBooleanField(blank=True, null=True)
    key = models.IntegerField(max_length=100, blank=True, null=True)
    user = models.ForeignKey('User')


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
    times_rented = models.IntegerField(max_length=100, blank=True, null=True)
    rented_out = models.NullBooleanField(blank=True, null=True)
    rental_fee = models.DecimalField(max_length=200,max_digits=10, decimal_places=2, blank=True, null=True)

class JournalEntry(models.Model):
    # transaction = models.OneToOneField('Transaction')
    revenueSource = models.ForeignKey('RevenueSource')
    date = models.DateTimeField(auto_now_add=True)
    note = models.CharField(max_length=200,blank=True,null=True)

class AccountEntry(models.Model):
    GeneralLedgerName = models.ForeignKey('GeneralLedgerName')
    journalEntry = models.ForeignKey('JournalEntry')
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

class GeneralLedgerName(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    # Types of ledgers:
    # 1 Cash
    # 2 Sales
    # 3 COGS
    # 4 Inventory

class Debit(AccountEntry):
    note = models.CharField(max_length=200,blank=True,null=True)

class Credit(AccountEntry):
    note = models.CharField(max_length=200,blank=True,null=True)

class RevenueSource(models.Model):
    # transaction = models.ForeignKey('Transaction')
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    ship_first = models.CharField(max_length=200, blank=True, null=True)
    ship_last = models.CharField(max_length=200, blank=True, null=True)
    ship_street = models.CharField(max_length=30, blank=True, null=True)
    ship_city = models.CharField(max_length=50, blank=True, null=True)
    ship_state = models.CharField(max_length=30, blank=True, null=True)
    ship_zipCode = models.CharField(max_length=20, blank=True, null=True)

    bill_street = models.CharField(max_length=30, blank=True, null=True)
    bill_city = models.CharField(max_length=50, blank=True, null=True)
    bill_state = models.CharField(max_length=30, blank=True, null=True)
    bill_zipCode = models.CharField(max_length=20, blank=True, null=True)

    creditCardNum = models.CharField(max_length=16, blank=True, null=True)
    cvn = models.CharField(max_length=3, blank=True, null=True)
    card_first = models.CharField(max_length=50, blank=True, null=True)
    card_last = models.CharField(max_length=50, blank=True, null=True)
    expDate = models.DateField(blank=True, null=True)

    receipt_number = models.CharField(max_length=200, blank=True, null=True)

class ServiceRepair(RevenueSource):
    employee = models.ForeignKey('Employee')
    customer = models.ForeignKey('User')
    product_name = models.CharField(max_length=50, blank=True, null=True)
    dateStarted = models.DateTimeField(auto_now_add=True)
    dateComplete = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=50, blank=True, null=True)
    labor_hours = models.IntegerField(max_length=10, blank=True, null=True)
    pickup_date = models.DateTimeField(auto_now_add=True)
    work_order = models.IntegerField(max_length=10, blank=True, null=True)
    status = models.CharField(max_length=200,blank=True, null=True)
    picked_up = models.NullBooleanField(blank=True, null=True)

class Rental(RevenueSource):
    user = models.ForeignKey('User')
    dateOut = models.DateTimeField(auto_now_add=False)
    dateIn = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    dateDue = models.DateTimeField(auto_now_add=False)
    returned = models.NullBooleanField(blank=True, null=True)
    work_order = models.IntegerField(max_length=10, blank=True, null=True)

class RentalItem(models.Model):
    rental = models.ForeignKey('Rental')
    product = models.ForeignKey('Product')
    damage_reported = models.NullBooleanField(blank=True, null=True)

class Fee(RevenueSource):
    rental = models.ForeignKey('Rental')
    waived = models.NullBooleanField(blank=True, null=True)

class Late(Fee):
    days_late = models.IntegerField(max_length=10, blank=True, null=True)

class Damage(Fee):
    description = models.CharField(max_length=50, blank=True, null=True)
    product = models.ForeignKey('Product')


class Sale(RevenueSource):
    '''The Sale class'''
    user = models.ForeignKey('User')
    date = models.DateTimeField(auto_now_add=True)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    tax_ammount = models.DecimalField(max_digits=10, decimal_places=2,blank=True, null=True)

class Loan(RevenueSource):
    note = models.CharField(max_length=200,blank=True,null=True)


class SaleItem(models.Model):
    '''An item in a sale'''
    sale = models.ForeignKey('Sale')
    product = models.ForeignKey('Product')

class Commission(models.Model):
    employee = models.ForeignKey('Employee')
    sale = models.OneToOneField('Sale')
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)