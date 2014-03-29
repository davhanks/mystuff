from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from homepage.models import *
from manager import models as mmod
from . import templater

s = mmod.Store()
s.name = 'Sandy'
s.location = 'Sandy'
s.street = '123 Cottonwood Dr'
s.city = 'Sandy'
s.state = 'UT'
s.zipCode = '84070'
s.phone = '(801) 555-1234'
s.active = True
s.save()

c = mmod.CatalogInventory()
c.product_name = 'Cannon D50'
c.description = 'DSLR'
c.manufacturer = 'Cannon'
c.average_cost = 220.20
c.commission_rate = .1
c.product_category = 'Camera'
c.sku = 349823
c.active = True
c.sale_price = 449.99
c.image = 'cannon_d50.jpg'
c.save()

c = mmod.CatalogInventory()
c.product_name = 'Cannon Tripod'
c.description = 'Collapsable Tripod'
c.manufacturer = 'Cannon'
c.average_cost = 10
c.commission_rate = .05
c.product_category = 'Equipment'
c.sku = 340870
c.active = True
c.sale_price = 29.99
c.image = 'tripod.jpg'
c.save()

c = mmod.CatalogInventory()
c.product_name = 'Sony a350'
c.description = 'DSLR'
c.manufacturer = 'Sony'
c.average_cost = 275.00
c.commission_rate = .1
c.product_category = 'Camera'
c.sku = 492383
c.active = True
c.sale_price = 499.99
c.image = 'sonya350.jpg'
c.save()

c = mmod.CatalogInventory()
c.product_name = 'San Disk 2G SD Card'
c.description = 'SD Card'
c.manufacturer = 'San Disk'
c.average_cost = 5.50
c.commission_rate = .1
c.product_category = 'Accessory'
c.sku = 730847
c.active = True
c.sale_price = 19.99
c.image = 'sandisk2gig.jpg'
c.save()

c = mmod.CatalogInventory()
c.product_name = 'Cannon 50x Zoom Lense'
c.description = '50x Zoom Lense for Cannon Cameras'
c.manufacturer = 'Camera'
c.average_cost = 85.00
c.commission_rate = .1
c.product_category = 'Lense'
c.sku = 373846
c.active = True
c.sale_price = 149.99
c.image = 'cannon_lense.jpg'
c.save()

u = mmod.User()
u.first_name = 'Test'
u.last_name = 'User'
u.username = 'testuser'
u.email = 'testuser@gmail.com'
u.set_password('testpassword')
u.street = 'Test Street'
u.street2 = 'Apt 1'
u.city = 'Provo'
u.state = 'UT'
u.zipCode = '84606'
u.phone = '(801) 555-1111'
u.is_active = True
u.active = True
u.is_staff = False
u.is_superuser = False
