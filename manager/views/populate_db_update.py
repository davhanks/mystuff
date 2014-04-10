from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from homepage.models import *
from manager import models as mmod
from . import templater
from datetime import datetime
import random

def process_request(request):
	'''populate_db'''
	# Assets

	# id 1
	gln = mmod.GeneralLedgerName()
	gln.name = 'Cash'
	gln.save()

	# id 2
	gln = mmod.GeneralLedgerName()
	gln.name = 'Sales'
	gln.save()

	# id 3
	gln = mmod.GeneralLedgerName()
	gln.name = 'COGS'
	gln.save()

	# id 4
	gln = mmod.GeneralLedgerName()
	gln.name = 'Inventory'
	gln.save()

	#id 5
	gln = mmod.GeneralLedgerName()
	gln.name = 'Accounts Receivable'
	gln.save()

	#id 6
	gln = mmod.GeneralLedgerName()
	gln.name = 'Other Current Assets'
	gln.save()

	#id 7
	gln = mmod.GeneralLedgerName()
	gln.name = 'Long-Term Assets'
	gln.save()

	# Liabilities

	# id 8
	gln = mmod.GeneralLedgerName()
	gln.name = 'Accounts Payable'
	gln.save()

	# id 9
	gln = mmod.GeneralLedgerName()
	gln.name = 'Salaries Payable'
	gln.save()

	# id 10
	gln = mmod.GeneralLedgerName()
	gln.name = 'Long-Term Debt'
	gln.save()

	# Equity

	#id 11
	gln = mmod.GeneralLedgerName()
	gln.name = 'Captial Stock'
	gln.save()

	#id 12
	gln = mmod.GeneralLedgerName()
	gln.name = 'Retained Earnings'
	gln.save()


	# Initial Accounting Entries
	revSrc = mmod.Loan()
	revSrc.amount = 300000.00
	revSrc.save()

	journ = mmod.JournalEntry()
	journ.revenueSource_id = revSrc.id
	journ.save()

	# debit cash for amount of loan
	ent = mmod.Debit()
	ent.GeneralLedgerName_id = 1
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()

	# credit long-term debt for amount of loan
	ent = mmod.Credit()
	ent.GeneralLedgerName_id = 10
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()

	################################################

	revSrc = mmod.Loan()
	revSrc.amount = 100000.00
	revSrc.save()

	journ = mmod.JournalEntry()
	journ.revenueSource_id = revSrc.id
	journ.save()

	# debit cash for amount of investment
	ent = mmod.Debit()
	ent.GeneralLedgerName_id = 1
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()

	# credit CS for amount of investment
	ent = mmod.Credit()
	ent.GeneralLedgerName_id = 11
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()


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


	revSrc = mmod.Loan()
	revSrc.amount = 200000.00
	revSrc.note = 'Purchase of Sandy location Building'
	revSrc.save()

	journ = mmod.JournalEntry()
	journ.revenueSource_id = revSrc.id
	journ.save()

	# debit lta for amount of store
	ent = mmod.Debit()
	ent.GeneralLedgerName_id = 7
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()

	# credit cash for amount of store
	ent = mmod.Credit()
	ent.GeneralLedgerName_id = 1
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()


	# Start Product
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

	# Start instance of adc bot

	u = mmod.Product()
	u.catalog_inventory_id = c.id
	u.store_id = s.id
	u.shelf_location = 'Storage Room'
	u.purchase_date = datetime.now().date()
	u.serial_number = random.randrange(1000,99999)
	u.active = True
	u.is_rental = False
	u.save()

	###############################################################
	revSrc = mmod.Loan()
	revSrc.amount = c.average_cost
	revSrc.note = 'Prodcut Purchase'
	revSrc.save()

	journ = mmod.JournalEntry()
	journ.revenueSource_id = revSrc.id
	journ.save()

	# debit lta for amount of store
	ent = mmod.Debit()
	ent.GeneralLedgerName_id = 4
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()

	# credit cash for amount of store
	ent = mmod.Credit()
	ent.GeneralLedgerName_id = 1
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()
	# END

	c = mmod.CatalogInventory()
	c.product_name = 'Cannon Tripod'
	c.description = 'Collapsable Tripod'
	c.manufacturer = 'Cannon'
	c.average_cost = 10
	c.commission_rate = .05
	c.product_category = 'Equipment'
	c.sku = random.randrange(1000,99999)
	c.active = True
	c.sale_price = 29.99
	c.image = 'tripod.jpg'
	c.save()

	u = mmod.Product()
	u.catalog_inventory_id = c.id
	u.store_id = s.id
	u.shelf_location = 'Storage Room'
	u.purchase_date = datetime.now().date()
	u.serial_number = random.randrange(1000,99999)
	u.active = True
	u.is_rental = False
	u.save()

	###############################################################
	revSrc = mmod.Loan()
	revSrc.amount = c.average_cost
	revSrc.note = 'Prodcut Purchase'
	revSrc.save()

	journ = mmod.JournalEntry()
	journ.revenueSource_id = revSrc.id
	journ.save()

	# debit lta for amount of store
	ent = mmod.Debit()
	ent.GeneralLedgerName_id = 4
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()

	# credit cash for amount of store
	ent = mmod.Credit()
	ent.GeneralLedgerName_id = 1
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()
	# END

	c = mmod.CatalogInventory()
	c.product_name = 'Sony a350'
	c.description = 'DSLR'
	c.manufacturer = 'Sony'
	c.average_cost = 275.00
	c.commission_rate = .1
	c.product_category = 'Camera'
	c.sku = random.randrange(1000,99999)
	c.active = True
	c.sale_price = 499.99
	c.image = 'sonya350.jpg'
	c.save()

	u = mmod.Product()
	u.catalog_inventory_id = c.id
	u.store_id = s.id
	u.shelf_location = 'Storage Room'
	u.purchase_date = datetime.now().date()
	u.serial_number = random.randrange(1000,99999)
	u.active = True
	u.is_rental = False
	u.save()

	###############################################################
	revSrc = mmod.Loan()
	revSrc.amount = c.average_cost
	revSrc.note = 'Prodcut Purchase'
	revSrc.save()

	journ = mmod.JournalEntry()
	journ.revenueSource_id = revSrc.id
	journ.save()

	# debit lta for amount of store
	ent = mmod.Debit()
	ent.GeneralLedgerName_id = 4
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()

	# credit cash for amount of store
	ent = mmod.Credit()
	ent.GeneralLedgerName_id = 1
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()
	# END

	c = mmod.CatalogInventory()
	c.product_name = 'San Disk 2G SD Card'
	c.description = 'SD Card'
	c.manufacturer = 'San Disk'
	c.average_cost = 5.50
	c.commission_rate = .1
	c.product_category = 'Accessory'
	c.sku = random.randrange(1000,99999)
	c.active = True
	c.sale_price = 19.99
	c.image = 'sandisk2gig.jpg'
	c.save()

	u = mmod.Product()
	u.catalog_inventory_id = c.id
	u.store_id = s.id
	u.shelf_location = 'Storage Room'
	u.purchase_date = datetime.now().date()
	u.serial_number = random.randrange(1000,99999)
	u.active = True
	u.is_rental = False
	u.save()

	###############################################################
	revSrc = mmod.Loan()
	revSrc.amount = c.average_cost
	revSrc.note = 'Prodcut Purchase'
	revSrc.save()

	journ = mmod.JournalEntry()
	journ.revenueSource_id = revSrc.id
	journ.save()

	# debit lta for amount of store
	ent = mmod.Debit()
	ent.GeneralLedgerName_id = 4
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()

	# credit cash for amount of store
	ent = mmod.Credit()
	ent.GeneralLedgerName_id = 1
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()
	# END

	c = mmod.CatalogInventory()
	c.product_name = 'Cannon 50x Zoom Lense'
	c.description = '50x Zoom Lense for Cannon Cameras'
	c.manufacturer = 'Camera'
	c.average_cost = 85.00
	c.commission_rate = .1
	c.product_category = 'Lens'
	c.sku = random.randrange(1000,99999)
	c.active = True
	c.sale_price = 149.99
	c.image = 'cannon_lense.jpg'
	c.save()

	u = mmod.Product()
	u.catalog_inventory_id = c.id
	u.store_id = s.id
	u.shelf_location = 'Storage Room'
	u.purchase_date = datetime.now().date()
	u.serial_number = random.randrange(1000,99999)
	u.active = True
	u.is_rental = False
	u.save()

	###############################################################
	revSrc = mmod.Loan()
	revSrc.amount = c.average_cost
	revSrc.note = 'Prodcut Purchase'
	revSrc.save()

	journ = mmod.JournalEntry()
	journ.revenueSource_id = revSrc.id
	journ.save()

	# debit lta for amount of store
	ent = mmod.Debit()
	ent.GeneralLedgerName_id = 4
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()

	# credit cash for amount of store
	ent = mmod.Credit()
	ent.GeneralLedgerName_id = 1
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()
	# END

	# Start EQUIPMENT #################################################################
	c = mmod.CatalogInventory()
	c.product_name = 'Pearstone Camera Bag'
	c.description = 'Digit video camcorder bag'
	c.manufacturer = 'Pearstone'
	c.average_cost = 34.00
	c.commission_rate = .1
	c.product_category = 'Equipment'
	c.sku = random.randrange(1000,99999)
	c.active = True
	c.sale_price = 74.95
	c.image = 'case1.jpg'
	c.save()

	# Start instance of 
	u = mmod.Product()
	u.catalog_inventory_id = c.id
	u.store_id = s.id
	u.shelf_location = 'Storage Room'
	u.purchase_date = datetime.now().date()
	u.serial_number = random.randrange(1000,99999)
	u.active = True
	u.is_rental = False
	u.save()
	# END

	###############################################################
	revSrc = mmod.Loan()
	revSrc.amount = c.average_cost
	revSrc.note = 'Prodcut Purchase'
	revSrc.save()

	journ = mmod.JournalEntry()
	journ.revenueSource_id = revSrc.id
	journ.save()

	# debit lta for amount of store
	ent = mmod.Debit()
	ent.GeneralLedgerName_id = 4
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()

	# credit cash for amount of store
	ent = mmod.Credit()
	ent.GeneralLedgerName_id = 1
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()
	# END

	# Start Product
	c = mmod.CatalogInventory()
	c.product_name = 'Pearstone Pro Camera Bag w/ Wheels'
	c.description = 'Wheeled camera bag for cameras up to 24" long'
	c.manufacturer = 'Pearstone'
	c.average_cost = 50.65
	c.commission_rate = .1
	c.product_category = 'Equipment'
	c.sku = random.randrange(1000,99999)
	c.active = True
	c.sale_price = 139.95
	c.image = 'case2.jpg'
	c.save()

	# Start instance of 
	u = mmod.Product()
	u.catalog_inventory_id = c.id
	u.store_id = s.id
	u.shelf_location = 'Storage Room'
	u.purchase_date = datetime.now().date()
	u.serial_number = random.randrange(1000,99999)
	u.active = True
	u.is_rental = False
	u.save()
	# END

	###############################################################
	revSrc = mmod.Loan()
	revSrc.amount = c.average_cost
	revSrc.note = 'Prodcut Purchase'
	revSrc.save()

	journ = mmod.JournalEntry()
	journ.revenueSource_id = revSrc.id
	journ.save()

	# debit lta for amount of store
	ent = mmod.Debit()
	ent.GeneralLedgerName_id = 4
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()

	# credit cash for amount of store
	ent = mmod.Credit()
	ent.GeneralLedgerName_id = 1
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()
	# END

	# Start Product
	c = mmod.CatalogInventory()
	c.product_name = 'Kata cc 192 Compact Case'
	c.description = 'DSLR'
	c.manufacturer = 'Cannon'
	c.average_cost = 220.20
	c.commission_rate = .1
	c.product_category = 'Equipment'
	c.sku = random.randrange(1000,99999)
	c.active = True
	c.sale_price = 89.95
	c.image = 'case3.jpg'
	c.save()

	# Start instance of 
	u = mmod.Product()
	u.catalog_inventory_id = c.id
	u.store_id = s.id
	u.shelf_location = 'Storage Room'
	u.purchase_date = datetime.now().date()
	u.serial_number = random.randrange(1000,99999)
	u.active = True
	u.is_rental = False
	u.save()
	# END

	###############################################################
	revSrc = mmod.Loan()
	revSrc.amount = c.average_cost
	revSrc.note = 'Prodcut Purchase'
	revSrc.save()

	journ = mmod.JournalEntry()
	journ.revenueSource_id = revSrc.id
	journ.save()

	# debit lta for amount of store
	ent = mmod.Debit()
	ent.GeneralLedgerName_id = 4
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()

	# credit cash for amount of store
	ent = mmod.Credit()
	ent.GeneralLedgerName_id = 1
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()
	# END

	
	# Start Product
	c = mmod.CatalogInventory()
	c.product_name = 'Magnus vt 4000 Tripod System'
	c.description = 'Supports 8.8 lb (4 kg) camera'
	c.manufacturer = 'Magnus'
	c.average_cost = 102.15
	c.commission_rate = .1
	c.product_category = 'Equipment'
	c.sku = random.randrange(1000,99999)
	c.active = True
	c.sale_price = 134.95
	c.image = 'tripod1.jpg'
	c.save()

	# Start instance of 
	u = mmod.Product()
	u.catalog_inventory_id = c.id
	u.store_id = s.id
	u.shelf_location = 'Storage Room'
	u.purchase_date = datetime.now().date()
	u.serial_number = random.randrange(1000,99999)
	u.active = True
	u.is_rental = False
	u.save()
	# END

	###############################################################
	revSrc = mmod.Loan()
	revSrc.amount = c.average_cost
	revSrc.note = 'Prodcut Purchase'
	revSrc.save()

	journ = mmod.JournalEntry()
	journ.revenueSource_id = revSrc.id
	journ.save()

	# debit lta for amount of store
	ent = mmod.Debit()
	ent.GeneralLedgerName_id = 4
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()

	# credit cash for amount of store
	ent = mmod.Credit()
	ent.GeneralLedgerName_id = 1
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()
	# END

		# Start Product
	c = mmod.CatalogInventory()
	c.product_name = 'Manfrotto MVH500A Tripod and Bag'
	c.description = 'Supports 10 lb camera and has wide platform for camcorders & HDSLRs'
	c.manufacturer = 'Manfrotto'
	c.average_cost = 185.15
	c.commission_rate = .1
	c.product_category = 'Equipment'
	c.sku = random.randrange(1000,99999)
	c.active = True
	c.sale_price = 349.99
	c.image = 'tripod2.jpg'
	c.save()

	# Start instance of 
	u = mmod.Product()
	u.catalog_inventory_id = c.id
	u.store_id = s.id
	u.shelf_location = 'Storage Room'
	u.purchase_date = datetime.now().date()
	u.serial_number = random.randrange(1000,99999)
	u.active = True
	u.is_rental = False
	u.save()
	# END

	###############################################################
	revSrc = mmod.Loan()
	revSrc.amount = c.average_cost
	revSrc.note = 'Prodcut Purchase'
	revSrc.save()

	journ = mmod.JournalEntry()
	journ.revenueSource_id = revSrc.id
	journ.save()

	# debit lta for amount of store
	ent = mmod.Debit()
	ent.GeneralLedgerName_id = 4
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()

	# credit cash for amount of store
	ent = mmod.Credit()
	ent.GeneralLedgerName_id = 1
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()
	# END

	# Start Product
	c = mmod.CatalogInventory()
	c.product_name = 'Sony VCTR640 Tripod (Light Weight)'
	c.description = 'Light weight, easy adjustment mechanism'
	c.manufacturer = 'Sony'
	c.average_cost = 18.00
	c.commission_rate = .1
	c.product_category = 'Equipment'
	c.sku = random.randrange(1000,99999)
	c.active = True
	c.sale_price = 34.95
	c.image = 'tripod3.jpg'
	c.save()

	# Start instance of 
	u = mmod.Product()
	u.catalog_inventory_id = c.id
	u.store_id = s.id
	u.shelf_location = 'Storage Room'
	u.purchase_date = datetime.now().date()
	u.serial_number = random.randrange(1000,99999)
	u.active = True
	u.is_rental = False
	u.save()
	# END

	###############################################################
	revSrc = mmod.Loan()
	revSrc.amount = c.average_cost
	revSrc.note = 'Prodcut Purchase'
	revSrc.save()

	journ = mmod.JournalEntry()
	journ.revenueSource_id = revSrc.id
	journ.save()

	# debit lta for amount of store
	ent = mmod.Debit()
	ent.GeneralLedgerName_id = 4
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()

	# credit cash for amount of store
	ent = mmod.Credit()
	ent.GeneralLedgerName_id = 1
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()
	# END

	# Start Product
	c = mmod.CatalogInventory()
	c.product_name = 'Revo Quad Skate Tabletop Dolly with Scale Marks'
	c.description = '4-Wheel dolly for fluid tabletop shots'
	c.manufacturer = 'Revo'
	c.average_cost = 12.05
	c.commission_rate = .1
	c.product_category = 'Equipment'
	c.sku = random.randrange(1000,99999)
	c.active = True
	c.sale_price = 30.55
	c.image = 'dolly1.jpg'
	c.save()

	# Start instance of 
	u = mmod.Product()
	u.catalog_inventory_id = c.id
	u.store_id = s.id
	u.shelf_location = 'Storage Room'
	u.purchase_date = datetime.now().date()
	u.serial_number = random.randrange(1000,99999)
	u.active = True
	u.is_rental = False
	u.save()
	# END

	###############################################################
	revSrc = mmod.Loan()
	revSrc.amount = c.average_cost
	revSrc.note = 'Prodcut Purchase'
	revSrc.save()

	journ = mmod.JournalEntry()
	journ.revenueSource_id = revSrc.id
	journ.save()

	# debit lta for amount of store
	ent = mmod.Debit()
	ent.GeneralLedgerName_id = 4
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()

	# credit cash for amount of store
	ent = mmod.Credit()
	ent.GeneralLedgerName_id = 1
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()
	# END

	# Start Product
	c = mmod.CatalogInventory()
	c.product_name = 'Cinetics CineSkates Camera Tripod Dolly Wheel kit'
	c.description = '(3) Skateboard wheels for mini tripod'
	c.manufacturer = 'Cinetics'
	c.average_cost = 12.05
	c.commission_rate = .1
	c.product_category = 'Equipment'
	c.sku = random.randrange(1000,99999)
	c.active = True
	c.sale_price = 192.75
	c.image = 'dolly2.jpg'
	c.save()

	# Start instance of 
	u = mmod.Product()
	u.catalog_inventory_id = c.id
	u.store_id = s.id
	u.shelf_location = 'Storage Room'
	u.purchase_date = datetime.now().date()
	u.serial_number = random.randrange(1000,99999)
	u.active = True
	u.is_rental = False
	u.save()
	# END

	###############################################################
	revSrc = mmod.Loan()
	revSrc.amount = c.average_cost
	revSrc.note = 'Prodcut Purchase'
	revSrc.save()

	journ = mmod.JournalEntry()
	journ.revenueSource_id = revSrc.id
	journ.save()

	# debit lta for amount of store
	ent = mmod.Debit()
	ent.GeneralLedgerName_id = 4
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()

	# credit cash for amount of store
	ent = mmod.Credit()
	ent.GeneralLedgerName_id = 1
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()
	# END


# Start Product
	c = mmod.CatalogInventory()
	c.product_name = 'Dot Line Komodo Tabletop Dolly'
	c.description = 'Made for full-Size DSLRs & camcorders, fluid roller bearings'
	c.manufacturer = 'Dot Line'
	c.average_cost = 122.14
	c.commission_rate = .1
	c.product_category = 'Equipment'
	c.sku = random.randrange(1000,99999)
	c.active = True
	c.sale_price = 189.95
	c.image = 'dolly3.jpg'
	c.save()

	# Start instance of 
	u = mmod.Product()
	u.catalog_inventory_id = c.id
	u.store_id = s.id
	u.shelf_location = 'Storage Room'
	u.purchase_date = datetime.now().date()
	u.serial_number = random.randrange(1000,99999)
	u.active = True
	u.is_rental = False
	u.save()
	# END

	###############################################################
	revSrc = mmod.Loan()
	revSrc.amount = c.average_cost
	revSrc.note = 'Prodcut Purchase'
	revSrc.save()

	journ = mmod.JournalEntry()
	journ.revenueSource_id = revSrc.id
	journ.save()

	# debit lta for amount of store
	ent = mmod.Debit()
	ent.GeneralLedgerName_id = 4
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()

	# credit cash for amount of store
	ent = mmod.Credit()
	ent.GeneralLedgerName_id = 1
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()
	# END

	# Start Product
	c = mmod.CatalogInventory()
	c.product_name = 'Revo ST-1000 Pro Video Stabilizer'
	c.description = 'Enables shake-Free handheld shots'
	c.manufacturer = 'Dot Line'
	c.average_cost = 78.90
	c.commission_rate = .1
	c.product_category = 'Equipment'
	c.sku = random.randrange(1000,99999)
	c.active = True
	c.sale_price = 125.95
	c.image = 'steady1.jpg'
	c.save()

	# Start instance of 
	u = mmod.Product()
	u.catalog_inventory_id = c.id
	u.store_id = s.id
	u.shelf_location = 'Storage Room'
	u.purchase_date = datetime.now().date()
	u.serial_number = random.randrange(1000,99999)
	u.active = True
	u.is_rental = False
	u.save()
	# END

	###############################################################
	revSrc = mmod.Loan()
	revSrc.amount = c.average_cost
	revSrc.note = 'Prodcut Purchase'
	revSrc.save()

	journ = mmod.JournalEntry()
	journ.revenueSource_id = revSrc.id
	journ.save()

	# debit lta for amount of store
	ent = mmod.Debit()
	ent.GeneralLedgerName_id = 4
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()

	# credit cash for amount of store
	ent = mmod.Credit()
	ent.GeneralLedgerName_id = 1
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()
	# END

		# Start Product
	c = mmod.CatalogInventory()
	c.product_name = 'GlideCam HD2000 Stabilizer System'
	c.description = 'For small cameras (2-6 lbs)'
	c.manufacturer = 'GlideCam'
	c.average_cost = 300.00
	c.commission_rate = .1
	c.product_category = 'Equipment'
	c.sku = random.randrange(1000,99999)
	c.active = True
	c.sale_price = 449.00
	c.image = 'steady2.jpg'
	c.save()

	# Start instance of 
	u = mmod.Product()
	u.catalog_inventory_id = c.id
	u.store_id = s.id
	u.shelf_location = 'Storage Room'
	u.purchase_date = datetime.now().date()
	u.serial_number = random.randrange(1000,99999)
	u.active = True
	u.is_rental = False
	u.save()
	# END

	###############################################################
	revSrc = mmod.Loan()
	revSrc.amount = c.average_cost
	revSrc.note = 'Prodcut Purchase'
	revSrc.save()

	journ = mmod.JournalEntry()
	journ.revenueSource_id = revSrc.id
	journ.save()

	# debit lta for amount of store
	ent = mmod.Debit()
	ent.GeneralLedgerName_id = 4
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()

	# credit cash for amount of store
	ent = mmod.Credit()
	ent.GeneralLedgerName_id = 1
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()
	# END


		# Start Product
	c = mmod.CatalogInventory()
	c.product_name = 'Steadicam Merlin 2 Camera Stabilizing System'
	c.description = 'Create smooth, elegant shots on the fly. Swing arm and vest included'
	c.manufacturer = 'Steadicam'
	c.average_cost = 450.00
	c.commission_rate = .1
	c.product_category = 'Equipment'
	c.sku = random.randrange(1000,99999)
	c.active = True
	c.sale_price = 958.95
	c.image = 'steady3.jpg'
	c.save()

	# Start instance of 
	u = mmod.Product()
	u.catalog_inventory_id = c.id
	u.store_id = s.id
	u.shelf_location = 'Storage Room'
	u.purchase_date = datetime.now().date()
	u.serial_number = random.randrange(1000,99999)
	u.active = True
	u.is_rental = False
	u.save()
	# END

	###############################################################
	revSrc = mmod.Loan()
	revSrc.amount = c.average_cost
	revSrc.note = 'Prodcut Purchase'
	revSrc.save()

	journ = mmod.JournalEntry()
	journ.revenueSource_id = revSrc.id
	journ.save()

	# debit lta for amount of store
	ent = mmod.Debit()
	ent.GeneralLedgerName_id = 4
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()

	# credit cash for amount of store
	ent = mmod.Credit()
	ent.GeneralLedgerName_id = 1
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()
	# END


		# Start Product
	c = mmod.CatalogInventory()
	c.product_name = 'Genaray LED 7100 312 LED Variable Color Cam Light'
	c.description = 'Professional series on-camera LED light'
	c.manufacturer = 'Genaray'
	c.average_cost = 89.50
	c.commission_rate = .1
	c.product_category = 'Equipment'
	c.sku = random.randrange(1000,99999)
	c.active = True
	c.sale_price = 170.10
	c.image = 'light1.jpg'
	c.save()

	# Start instance of 
	u = mmod.Product()
	u.catalog_inventory_id = c.id
	u.store_id = s.id
	u.shelf_location = 'Storage Room'
	u.purchase_date = datetime.now().date()
	u.serial_number = random.randrange(1000,99999)
	u.active = True
	u.is_rental = False
	u.save()
	# END

	###############################################################
	revSrc = mmod.Loan()
	revSrc.amount = c.average_cost
	revSrc.note = 'Prodcut Purchase'
	revSrc.save()

	journ = mmod.JournalEntry()
	journ.revenueSource_id = revSrc.id
	journ.save()

	# debit lta for amount of store
	ent = mmod.Debit()
	ent.GeneralLedgerName_id = 4
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()

	# credit cash for amount of store
	ent = mmod.Credit()
	ent.GeneralLedgerName_id = 1
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()
	# END

		# Start Product
	c = mmod.CatalogInventory()
	c.product_name = 'Genaray LED-2100 36 LED Compact Light'
	c.description = '40W equivalent light intensity'
	c.manufacturer = 'Genaray'
	c.average_cost = 14.99
	c.commission_rate = .1
	c.product_category = 'Equipment'
	c.sku = random.randrange(1000,99999)
	c.active = True
	c.sale_price = 26.95
	c.image = 'light2.jpg'
	c.save()

	# Start instance of 
	u = mmod.Product()
	u.catalog_inventory_id = c.id
	u.store_id = s.id
	u.shelf_location = 'Storage Room'
	u.purchase_date = datetime.now().date()
	u.serial_number = random.randrange(1000,99999)
	u.active = True
	u.is_rental = False
	u.save()
	# END

	###############################################################
	revSrc = mmod.Loan()
	revSrc.amount = c.average_cost
	revSrc.note = 'Prodcut Purchase'
	revSrc.save()

	journ = mmod.JournalEntry()
	journ.revenueSource_id = revSrc.id
	journ.save()

	# debit lta for amount of store
	ent = mmod.Debit()
	ent.GeneralLedgerName_id = 4
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()

	# credit cash for amount of store
	ent = mmod.Credit()
	ent.GeneralLedgerName_id = 1
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()
	# END

		# Start Product
	c = mmod.CatalogInventory()
	c.product_name = 'Bescor LED-70 70W Camera Light'
	c.description = 'Ultra bright 70W beam'
	c.manufacturer = 'Bescor'
	c.average_cost = 18.72
	c.commission_rate = .1
	c.product_category = 'Equipment'
	c.sku = random.randrange(1000,99999)
	c.active = True
	c.sale_price = 39.95
	c.image = 'steady3.jpg'
	c.save()

	# Start instance of 
	u = mmod.Product()
	u.catalog_inventory_id = c.id
	u.store_id = s.id
	u.shelf_location = 'Storage Room'
	u.purchase_date = datetime.now().date()
	u.serial_number = random.randrange(1000,99999)
	u.active = True
	u.is_rental = False
	u.save()
	# END



	###############################################################
	revSrc = mmod.Loan()
	revSrc.amount = c.average_cost
	revSrc.note = 'Prodcut Purchase'
	revSrc.save()

	journ = mmod.JournalEntry()
	journ.revenueSource_id = revSrc.id
	journ.save()

	# debit lta for amount of store
	ent = mmod.Debit()
	ent.GeneralLedgerName_id = 4
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()

	# credit cash for amount of store
	ent = mmod.Credit()
	ent.GeneralLedgerName_id = 1
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()
	# END








	# END EQUIPMENT#################################################################################


	# Start ACCESSORIES #################################################################


		# Start Product
	c = mmod.CatalogInventory()
	c.product_name = 'SanDisk 16 GB SDHC Extreme Class 10'
	c.description = '16 gb capacity, 45 mbps read/write speed'
	c.manufacturer = 'SanDisk'
	c.average_cost = 9.99
	c.commission_rate = .1
	c.product_category = 'Accessory'
	c.sku = random.randrange(1000,99999)
	c.active = True
	c.sale_price = 17.95
	c.image = 'card1.jpg'
	c.save()

	# Start instance of 
	u = mmod.Product()
	u.catalog_inventory_id = c.id
	u.store_id = s.id
	u.shelf_location = 'Storage Room'
	u.purchase_date = datetime.now().date()
	u.serial_number = random.randrange(1000,99999)
	u.active = True
	u.is_rental = False
	u.save()
	# END

	###############################################################
	revSrc = mmod.Loan()
	revSrc.amount = c.average_cost
	revSrc.note = 'Prodcut Purchase'
	revSrc.save()

	journ = mmod.JournalEntry()
	journ.revenueSource_id = revSrc.id
	journ.save()

	# debit lta for amount of store
	ent = mmod.Debit()
	ent.GeneralLedgerName_id = 4
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()

	# credit cash for amount of store
	ent = mmod.Credit()
	ent.GeneralLedgerName_id = 1
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()
	# END

			# Start Product
	c = mmod.CatalogInventory()
	c.product_name = 'SanDisk 32 GB SDHC Extreme Class 10'
	c.description = '32 gb capacity, 45 mbps read/write speed'
	c.manufacturer = 'SanDisk'
	c.average_cost = 14.99
	c.commission_rate = .1
	c.product_category = 'Accessory'
	c.sku = random.randrange(1000,99999)
	c.active = True
	c.sale_price = 27.95
	c.image = 'card2.jpg'
	c.save()

	# Start instance of 
	u = mmod.Product()
	u.catalog_inventory_id = c.id
	u.store_id = s.id
	u.shelf_location = 'Storage Room'
	u.purchase_date = datetime.now().date()
	u.serial_number = random.randrange(1000,99999)
	u.active = True
	u.is_rental = False
	u.save()
	# END


	###############################################################
	revSrc = mmod.Loan()
	revSrc.amount = c.average_cost
	revSrc.note = 'Prodcut Purchase'
	revSrc.save()

	journ = mmod.JournalEntry()
	journ.revenueSource_id = revSrc.id
	journ.save()

	# debit lta for amount of store
	ent = mmod.Debit()
	ent.GeneralLedgerName_id = 4
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()

	# credit cash for amount of store
	ent = mmod.Credit()
	ent.GeneralLedgerName_id = 1
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()
	# END

		# Start Product
	c = mmod.CatalogInventory()
	c.product_name = 'SanDisk 64 GB SDXC Memory Card Extreme Pro Class 10 UHS-I'
	c.description = '64 gb capacity, 95 mbps read/write speed'
	c.manufacturer = 'SanDisk'
	c.average_cost = 49.99
	c.commission_rate = .1
	c.product_category = 'Accessory'
	c.sku = random.randrange(1000,99999)
	c.active = True
	c.sale_price = 98.95
	c.image = 'card3.jpg'
	c.save()

	# Start instance of 
	u = mmod.Product()
	u.catalog_inventory_id = c.id
	u.store_id = s.id
	u.shelf_location = 'Storage Room'
	u.purchase_date = datetime.now().date()
	u.serial_number = random.randrange(1000,99999)
	u.active = True
	u.is_rental = False
	u.save()
	# END

	###############################################################
	revSrc = mmod.Loan()
	revSrc.amount = c.average_cost
	revSrc.note = 'Prodcut Purchase'
	revSrc.save()

	journ = mmod.JournalEntry()
	journ.revenueSource_id = revSrc.id
	journ.save()

	# debit lta for amount of store
	ent = mmod.Debit()
	ent.GeneralLedgerName_id = 4
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()

	# credit cash for amount of store
	ent = mmod.Credit()
	ent.GeneralLedgerName_id = 1
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()
	# END

			# Start Product
	c = mmod.CatalogInventory()
	c.product_name = 'SanDisk 32GB CompactFlash Memory Card Extreme Pro 600x UDMA'
	c.description = '32 gb capacity, 90 MB/s read/write speed'
	c.manufacturer = 'SanDisk'
	c.average_cost = 49.99
	c.commission_rate = .1
	c.product_category = 'Accessory'
	c.sku = random.randrange(1000,99999)
	c.active = True
	c.sale_price = 89.95
	c.image = 'card4.jpg'
	c.save()

	# Start instance of 
	u = mmod.Product()
	u.catalog_inventory_id = c.id
	u.store_id = s.id
	u.shelf_location = 'Storage Room'
	u.purchase_date = datetime.now().date()
	u.serial_number = random.randrange(1000,99999)
	u.active = True
	u.is_rental = False
	u.save()
	# END

	###############################################################
	revSrc = mmod.Loan()
	revSrc.amount = c.average_cost
	revSrc.note = 'Prodcut Purchase'
	revSrc.save()

	journ = mmod.JournalEntry()
	journ.revenueSource_id = revSrc.id
	journ.save()

	# debit lta for amount of store
	ent = mmod.Debit()
	ent.GeneralLedgerName_id = 4
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()

	# credit cash for amount of store
	ent = mmod.Credit()
	ent.GeneralLedgerName_id = 1
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()
	# END

			# Start Product
	c = mmod.CatalogInventory()
	c.product_name = 'SanDisk 32GB microSDHC Memory Card Ultra Class 10 UHS-I with microSD Adapter'
	c.description = '32 gb capacity, 30 mbps read/write speed, water proof'
	c.manufacturer = 'SanDisk'
	c.average_cost = 12.99
	c.commission_rate = .1
	c.product_category = 'Accessory'
	c.sku = random.randrange(1000,99999)
	c.active = True
	c.sale_price = 21.95
	c.image = 'card5.jpg'
	c.save()

	# Start instance of 
	u = mmod.Product()
	u.catalog_inventory_id = c.id
	u.store_id = s.id
	u.shelf_location = 'Storage Room'
	u.purchase_date = datetime.now().date()
	u.serial_number = random.randrange(1000,99999)
	u.active = True
	u.is_rental = False
	u.save()
	# END

	###############################################################
	revSrc = mmod.Loan()
	revSrc.amount = c.average_cost
	revSrc.note = 'Prodcut Purchase'
	revSrc.save()

	journ = mmod.JournalEntry()
	journ.revenueSource_id = revSrc.id
	journ.save()

	# debit lta for amount of store
	ent = mmod.Debit()
	ent.GeneralLedgerName_id = 4
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()

	# credit cash for amount of store
	ent = mmod.Credit()
	ent.GeneralLedgerName_id = 1
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()
	# END

			# Start Product
	c = mmod.CatalogInventory()
	c.product_name = 'Fujifilm 32GB SDHC Memory Card Class 10'
	c.description = '32 gb capacity, 10 mbps read/write speed'
	c.manufacturer = 'SanDisk'
	c.average_cost = 6.99
	c.commission_rate = .1
	c.product_category = 'Accessory'
	c.sku = random.randrange(1000,99999)
	c.active = True
	c.sale_price = 14.95
	c.image = 'card6.jpg'
	c.save()

	# Start instance of 
	u = mmod.Product()
	u.catalog_inventory_id = c.id
	u.store_id = s.id
	u.shelf_location = 'Storage Room'
	u.purchase_date = datetime.now().date()
	u.serial_number = random.randrange(1000,99999)
	u.active = True
	u.is_rental = False
	u.save()
	# END

	###############################################################
	revSrc = mmod.Loan()
	revSrc.amount = c.average_cost
	revSrc.note = 'Prodcut Purchase'
	revSrc.save()

	journ = mmod.JournalEntry()
	journ.revenueSource_id = revSrc.id
	journ.save()

	# debit lta for amount of store
	ent = mmod.Debit()
	ent.GeneralLedgerName_id = 4
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()

	# credit cash for amount of store
	ent = mmod.Credit()
	ent.GeneralLedgerName_id = 1
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()
	# END

				# Start Product
	c = mmod.CatalogInventory()
	c.product_name = 'Watson NP-F975 Lithium-Ion Battery Pack (7.4V, 7800mAh)'
	c.description = '400 photo battery life'
	c.manufacturer = 'Watson'
	c.average_cost = 39.99
	c.commission_rate = .1
	c.product_category = 'Accessory'
	c.sku = random.randrange(1000,99999)
	c.active = True
	c.sale_price = 59.99
	c.image = 'bat1.jpg'
	c.save()

	# Start instance of 
	u = mmod.Product()
	u.catalog_inventory_id = c.id
	u.store_id = s.id
	u.shelf_location = 'Storage Room'
	u.purchase_date = datetime.now().date()
	u.serial_number = random.randrange(1000,99999)
	u.active = True
	u.is_rental = False
	u.save()
	# END

	###############################################################
	revSrc = mmod.Loan()
	revSrc.amount = c.average_cost
	revSrc.note = 'Prodcut Purchase'
	revSrc.save()

	journ = mmod.JournalEntry()
	journ.revenueSource_id = revSrc.id
	journ.save()

	# debit lta for amount of store
	ent = mmod.Debit()
	ent.GeneralLedgerName_id = 4
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()

	# credit cash for amount of store
	ent = mmod.Credit()
	ent.GeneralLedgerName_id = 1
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()
	# END


							# Start Product
	c = mmod.CatalogInventory()
	c.product_name = 'Watson VW-VBG6 Lithium-Ion Battery Pack (7.4V, 4800mAh)'
	c.description = '200 photo battery life'
	c.manufacturer = 'Watson'
	c.average_cost = 39.99
	c.commission_rate = .1
	c.product_category = 'Accessory'
	c.sku = random.randrange(1000,99999)
	c.active = True
	c.sale_price = 69.99
	c.image = 'bat2.jpg'
	c.save()

	# Start instance of 
	u = mmod.Product()
	u.catalog_inventory_id = c.id
	u.store_id = s.id
	u.shelf_location = 'Storage Room'
	u.purchase_date = datetime.now().date()
	u.serial_number = random.randrange(1000,99999)
	u.active = True
	u.is_rental = False
	u.save()
	# END


	###############################################################
	revSrc = mmod.Loan()
	revSrc.amount = c.average_cost
	revSrc.note = 'Prodcut Purchase'
	revSrc.save()

	journ = mmod.JournalEntry()
	journ.revenueSource_id = revSrc.id
	journ.save()

	# debit lta for amount of store
	ent = mmod.Debit()
	ent.GeneralLedgerName_id = 4
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()

	# credit cash for amount of store
	ent = mmod.Credit()
	ent.GeneralLedgerName_id = 1
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()
	# END

							# Start Product
	c = mmod.CatalogInventory()
	c.product_name = 'Blackmagic Design Pocket Cinema Camera Battery'
	c.description = '7.4 V lithium-ion battery, 50 minutes of continuous recording'
	c.manufacturer = 'Blackmagic'
	c.average_cost = 4.99
	c.commission_rate = .1
	c.product_category = 'Accessory'
	c.sku = random.randrange(1000,99999)
	c.active = True
	c.sale_price = 14.95
	c.image = 'bat3.jpg'
	c.save()

	# Start instance of 
	u = mmod.Product()
	u.catalog_inventory_id = c.id
	u.store_id = s.id
	u.shelf_location = 'Storage Room'
	u.purchase_date = datetime.now().date()
	u.serial_number = random.randrange(1000,99999)
	u.active = True
	u.is_rental = False
	u.save()
	# END


	###############################################################
	revSrc = mmod.Loan()
	revSrc.amount = c.average_cost
	revSrc.note = 'Prodcut Purchase'
	revSrc.save()

	journ = mmod.JournalEntry()
	journ.revenueSource_id = revSrc.id
	journ.save()

	# debit lta for amount of store
	ent = mmod.Debit()
	ent.GeneralLedgerName_id = 4
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()

	# credit cash for amount of store
	ent = mmod.Credit()
	ent.GeneralLedgerName_id = 1
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()
	# END

								# Start Product
	c = mmod.CatalogInventory()
	c.product_name = 'Pearstone High-Speed HDMI to HDMI Cable with Ethernet - Black, 6 ft' 
	c.description = 'Supports 3D, 4K, deep color'
	c.manufacturer = 'Pearstone'
	c.average_cost = 2.73
	c.commission_rate = .1
	c.product_category = 'Accessory'
	c.sku = random.randrange(1000,99999)
	c.active = True
	c.sale_price = 7.95
	c.image = 'cable1.jpg'
	c.save()

	# Start instance of 
	u = mmod.Product()
	u.catalog_inventory_id = c.id
	u.store_id = s.id
	u.shelf_location = 'Storage Room'
	u.purchase_date = datetime.now().date()
	u.serial_number = random.randrange(1000,99999)
	u.active = True
	u.is_rental = False
	u.save()
	# END

	###############################################################
	revSrc = mmod.Loan()
	revSrc.amount = c.average_cost
	revSrc.note = 'Prodcut Purchase'
	revSrc.save()

	journ = mmod.JournalEntry()
	journ.revenueSource_id = revSrc.id
	journ.save()

	# debit lta for amount of store
	ent = mmod.Debit()
	ent.GeneralLedgerName_id = 4
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()

	# credit cash for amount of store
	ent = mmod.Credit()
	ent.GeneralLedgerName_id = 1
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()
	# END

									# Start Product
	c = mmod.CatalogInventory()
	c.product_name = 'Pearstone 1.5 ft Swiveling HDMI to Mini HDMI Cable' 
	c.description = 'HDMI Type A to HDMI type C connectors'
	c.manufacturer = 'Pearstone'
	c.average_cost = 2.73
	c.commission_rate = .1
	c.product_category = 'Accessory'
	c.sku = random.randrange(1000,99999)
	c.active = True
	c.sale_price = 6.95
	c.image = 'cable2.jpg'
	c.save()

	# Start instance of 
	u = mmod.Product()
	u.catalog_inventory_id = c.id
	u.store_id = s.id
	u.shelf_location = 'Storage Room'
	u.purchase_date = datetime.now().date()
	u.serial_number = random.randrange(1000,99999)
	u.active = True
	u.is_rental = False
	u.save()
	# END

	###############################################################
	revSrc = mmod.Loan()
	revSrc.amount = c.average_cost
	revSrc.note = 'Prodcut Purchase'
	revSrc.save()

	journ = mmod.JournalEntry()
	journ.revenueSource_id = revSrc.id
	journ.save()

	# debit lta for amount of store
	ent = mmod.Debit()
	ent.GeneralLedgerName_id = 4
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()

	# credit cash for amount of store
	ent = mmod.Credit()
	ent.GeneralLedgerName_id = 1
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()
	# END


								# Start Product
	c = mmod.CatalogInventory()
	c.product_name = 'Pearstone 3 ft SDI Video Cable - BNC to BNC' 
	c.description = '18 AWG RG-6 coaxial cable'
	c.manufacturer = 'Pearstone'
	c.average_cost = 2.73
	c.commission_rate = .1
	c.product_category = 'Accessory'
	c.sku = random.randrange(1000,99999)
	c.active = True
	c.sale_price = 5.91
	c.image = 'cable3.jpg'
	c.save()

	# Start instance of 
	u = mmod.Product()
	u.catalog_inventory_id = c.id
	u.store_id = s.id
	u.shelf_location = 'Storage Room'
	u.purchase_date = datetime.now().date()
	u.serial_number = random.randrange(1000,99999)
	u.active = True
	u.is_rental = False
	u.save()
	# END

	###############################################################
	revSrc = mmod.Loan()
	revSrc.amount = c.average_cost
	revSrc.note = 'Prodcut Purchase'
	revSrc.save()

	journ = mmod.JournalEntry()
	journ.revenueSource_id = revSrc.id
	journ.save()

	# debit lta for amount of store
	ent = mmod.Debit()
	ent.GeneralLedgerName_id = 4
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()

	# credit cash for amount of store
	ent = mmod.Credit()
	ent.GeneralLedgerName_id = 1
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()
	# END

								# Start Product
	c = mmod.CatalogInventory()
	c.product_name = 'Teradek VidiU On-Camera Wireless Streaming Video Encoder' 
	c.description = 'Streams 1080p from a camera to the web'
	c.manufacturer = 'Teradek'
	c.average_cost = 350.80
	c.commission_rate = .1
	c.product_category = 'Accessory'
	c.sku = random.randrange(1000,99999)
	c.active = True
	c.sale_price = 699.99
	c.image = 'trans1.jpg'
	c.save()

	# Start instance of 
	u = mmod.Product()
	u.catalog_inventory_id = c.id
	u.store_id = s.id
	u.shelf_location = 'Storage Room'
	u.purchase_date = datetime.now().date()
	u.serial_number = random.randrange(1000,99999)
	u.active = True
	u.is_rental = False
	u.save()
	# END

	###############################################################
	revSrc = mmod.Loan()
	revSrc.amount = c.average_cost
	revSrc.note = 'Prodcut Purchase'
	revSrc.save()

	journ = mmod.JournalEntry()
	journ.revenueSource_id = revSrc.id
	journ.save()

	# debit lta for amount of store
	ent = mmod.Debit()
	ent.GeneralLedgerName_id = 4
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()

	# credit cash for amount of store
	ent = mmod.Credit()
	ent.GeneralLedgerName_id = 1
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()
	# END


								# Start Product
	c = mmod.CatalogInventory()
	c.product_name = 'IDX CW-1 Wireless HDMI Video Transmission System' 
	c.description = 'Wireless HDMI transmitter & receiver set'
	c.manufacturer = 'IDX'
	c.average_cost = 480.80
	c.commission_rate = .1
	c.product_category = 'Accessory'
	c.sku = random.randrange(1000,99999)
	c.active = True
	c.sale_price = 734.99
	c.image = 'trans2.jpg'
	c.save()

	# Start instance of 
	u = mmod.Product()
	u.catalog_inventory_id = c.id
	u.store_id = s.id
	u.shelf_location = 'Storage Room'
	u.purchase_date = datetime.now().date()
	u.serial_number = random.randrange(1000,99999)
	u.active = True
	u.is_rental = False
	u.save()
	# END

	###############################################################
	revSrc = mmod.Loan()
	revSrc.amount = c.average_cost
	revSrc.note = 'Prodcut Purchase'
	revSrc.save()

	journ = mmod.JournalEntry()
	journ.revenueSource_id = revSrc.id
	journ.save()

	# debit lta for amount of store
	ent = mmod.Debit()
	ent.GeneralLedgerName_id = 4
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()

	# credit cash for amount of store
	ent = mmod.Credit()
	ent.GeneralLedgerName_id = 1
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()
	# END

								# Start Product
	c = mmod.CatalogInventory()
	c.product_name = 'Teradek Cube 255 HDMI Encoder with WiFi' 
	c.description = 'Streams H.264 files by WiFi / ethernet'
	c.manufacturer = 'Teradek'
	c.average_cost = 980.80
	c.commission_rate = .1
	c.product_category = 'Accessory'
	c.sku = random.randrange(1000,99999)
	c.active = True
	c.sale_price = 1045.00
	c.image = 'trans3.jpg'
	c.save()

	# Start instance of 
	u = mmod.Product()
	u.catalog_inventory_id = c.id
	u.store_id = s.id
	u.shelf_location = 'Storage Room'
	u.purchase_date = datetime.now().date()
	u.serial_number = random.randrange(1000,99999)
	u.active = True
	u.is_rental = False
	u.save()
	# END

	###############################################################
	revSrc = mmod.Loan()
	revSrc.amount = c.average_cost
	revSrc.note = 'Prodcut Purchase'
	revSrc.save()

	journ = mmod.JournalEntry()
	journ.revenueSource_id = revSrc.id
	journ.save()

	# debit lta for amount of store
	ent = mmod.Debit()
	ent.GeneralLedgerName_id = 4
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()

	# credit cash for amount of store
	ent = mmod.Credit()
	ent.GeneralLedgerName_id = 1
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()
	# END



	# END ACCESSORIES #################################################################

	# START CAMERA #################################################################

	c = mmod.CatalogInventory()
	c.product_name = 'Canon EOS 6d DSLR' 
	c.description = '20.2 MP Full frame CMOS sensor'
	c.manufacturer = 'Canon'
	c.average_cost = 1550.00
	c.commission_rate = .1
	c.product_category = 'Camera'
	c.sku = random.randrange(1000,99999)
	c.active = True
	c.sale_price = 1995.99
	c.image = 'canon_camera_1.jpg'
	c.save()

	# Start instance of 
	u = mmod.Product()
	u.catalog_inventory_id = c.id
	u.store_id = s.id
	u.shelf_location = 'Storage Room'
	u.purchase_date = datetime.now().date()
	u.serial_number = random.randrange(1000,99999)
	u.active = True
	u.is_rental = False
	u.save()
	# END

	###############################################################
	revSrc = mmod.Loan()
	revSrc.amount = c.average_cost
	revSrc.note = 'Prodcut Purchase'
	revSrc.save()

	journ = mmod.JournalEntry()
	journ.revenueSource_id = revSrc.id
	journ.save()

	# debit lta for amount of store
	ent = mmod.Debit()
	ent.GeneralLedgerName_id = 4
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()

	# credit cash for amount of store
	ent = mmod.Credit()
	ent.GeneralLedgerName_id = 1
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()
	# END

	c = mmod.CatalogInventory()
	c.product_name = 'Canon EOS Rebel T3i DSLR Camera with EF-S 18-55mm IS II Lens Kit' 
	c.description = '18MP APS-C CMOS sensor'
	c.manufacturer = 'Canon'
	c.average_cost = 410.15
	c.commission_rate = .1
	c.product_category = 'Camera'
	c.sku = random.randrange(1000,99999)
	c.active = True
	c.sale_price = 599.00
	c.image = 'canon_camera_2.jpg'
	c.save()

	# Start instance of 
	u = mmod.Product()
	u.catalog_inventory_id = c.id
	u.store_id = s.id
	u.shelf_location = 'Storage Room'
	u.purchase_date = datetime.now().date()
	u.serial_number = random.randrange(1000,99999)
	u.active = True
	u.is_rental = False
	u.save()
	# END

	###############################################################
	revSrc = mmod.Loan()
	revSrc.amount = c.average_cost
	revSrc.note = 'Prodcut Purchase'
	revSrc.save()

	journ = mmod.JournalEntry()
	journ.revenueSource_id = revSrc.id
	journ.save()

	# debit lta for amount of store
	ent = mmod.Debit()
	ent.GeneralLedgerName_id = 4
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()

	# credit cash for amount of store
	ent = mmod.Credit()
	ent.GeneralLedgerName_id = 1
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()
	# END


	c = mmod.CatalogInventory()
	c.product_name = 'Canon EOS 70D DSLR Camera with 18-135mm STM f/3.5-5.6 Lens' 
	c.description = '20.2MP APS-C CMOS sensor, DIGIC 5+ image processor'
	c.manufacturer = 'Canon'
	c.average_cost = 1000.00
	c.commission_rate = .1
	c.product_category = 'Camera'
	c.sku = random.randrange(1000,99999)
	c.active = True
	c.sale_price = 1494.99
	c.image = 'canon_camera_3.jpg'
	c.save()

	# Start instance of 
	u = mmod.Product()
	u.catalog_inventory_id = c.id
	u.store_id = s.id
	u.shelf_location = 'Storage Room'
	u.purchase_date = datetime.now().date()
	u.serial_number = random.randrange(1000,99999)
	u.active = True
	u.is_rental = False
	u.save()
	# END

	###############################################################
	revSrc = mmod.Loan()
	revSrc.amount = c.average_cost
	revSrc.note = 'Prodcut Purchase'
	revSrc.save()

	journ = mmod.JournalEntry()
	journ.revenueSource_id = revSrc.id
	journ.save()

	# debit lta for amount of store
	ent = mmod.Debit()
	ent.GeneralLedgerName_id = 4
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()

	# credit cash for amount of store
	ent = mmod.Credit()
	ent.GeneralLedgerName_id = 1
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()
	# END


	c = mmod.CatalogInventory()
	c.product_name = 'Canon EOS 70D DSLR Camera' 
	c.description = 'Body only - no lens'
	c.manufacturer = 'Canon'
	c.average_cost = 770.00
	c.commission_rate = .1
	c.product_category = 'Camera'
	c.sku = random.randrange(1000,99999)
	c.active = True
	c.sale_price = 1099.99
	c.image = 'canon_camera_4.jpg'
	c.save()

	# Start instance of 
	u = mmod.Product()
	u.catalog_inventory_id = c.id
	u.store_id = s.id
	u.shelf_location = 'Storage Room'
	u.purchase_date = datetime.now().date()
	u.serial_number = random.randrange(1000,99999)
	u.active = True
	u.is_rental = False
	u.save()
	# END

	###############################################################
	revSrc = mmod.Loan()
	revSrc.amount = c.average_cost
	revSrc.note = 'Prodcut Purchase'
	revSrc.save()

	journ = mmod.JournalEntry()
	journ.revenueSource_id = revSrc.id
	journ.save()

	# debit lta for amount of store
	ent = mmod.Debit()
	ent.GeneralLedgerName_id = 4
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()

	# credit cash for amount of store
	ent = mmod.Credit()
	ent.GeneralLedgerName_id = 1
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()
	# END


	c = mmod.CatalogInventory()
	c.product_name = 'Canon Powershot G15 Digital Camera' 
	c.description = '12.1 MP CMOS Sensor, 5x optical zoom'
	c.manufacturer = 'Canon'
	c.average_cost = 195.15
	c.commission_rate = .1
	c.product_category = 'Camera'
	c.sku = random.randrange(1000,99999)
	c.active = True
	c.sale_price = 369.99
	c.image = 'canon_camera_5.jpg'
	c.save()

	# Start instance of 
	u = mmod.Product()
	u.catalog_inventory_id = c.id
	u.store_id = s.id
	u.shelf_location = 'Storage Room'
	u.purchase_date = datetime.now().date()
	u.serial_number = random.randrange(1000,99999)
	u.active = True
	u.is_rental = False
	u.save()
	# END

	###############################################################
	revSrc = mmod.Loan()
	revSrc.amount = c.average_cost
	revSrc.note = 'Prodcut Purchase'
	revSrc.save()

	journ = mmod.JournalEntry()
	journ.revenueSource_id = revSrc.id
	journ.save()

	# debit lta for amount of store
	ent = mmod.Debit()
	ent.GeneralLedgerName_id = 4
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()

	# credit cash for amount of store
	ent = mmod.Credit()
	ent.GeneralLedgerName_id = 1
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()
	# END


	c = mmod.CatalogInventory()
	c.product_name = 'Nikon D7100 DSLR Camera with 18-140mm VR DX Lens' 
	c.description = '24.1MP DX-format CMOS sensor'
	c.manufacturer = 'Nikon'
	c.average_cost = 990.00
	c.commission_rate = .1
	c.product_category = 'Camera'
	c.sku = random.randrange(1000,99999)
	c.active = True
	c.sale_price = 1445.99
	c.image = 'nikon_camera_1.jpg'
	c.save()

	# Start instance of 
	u = mmod.Product()
	u.catalog_inventory_id = c.id
	u.store_id = s.id
	u.shelf_location = 'Storage Room'
	u.purchase_date = datetime.now().date()
	u.serial_number = random.randrange(1000,99999)
	u.active = True
	u.is_rental = False
	u.save()
	# END

	###############################################################
	revSrc = mmod.Loan()
	revSrc.amount = c.average_cost
	revSrc.note = 'Prodcut Purchase'
	revSrc.save()

	journ = mmod.JournalEntry()
	journ.revenueSource_id = revSrc.id
	journ.save()

	# debit lta for amount of store
	ent = mmod.Debit()
	ent.GeneralLedgerName_id = 4
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()

	# credit cash for amount of store
	ent = mmod.Credit()
	ent.GeneralLedgerName_id = 1
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()
	# END



	c = mmod.CatalogInventory()
	c.product_name = 'Nikon D610 DSLR Camera' 
	c.description = 'Body only, no lens. 24.3MP FX-format CMOS sensor'
	c.manufacturer = 'Nikon'
	c.average_cost = 1320.00
	c.commission_rate = .1
	c.product_category = 'Camera'
	c.sku = random.randrange(1000,99999)
	c.active = True
	c.sale_price = 1895.99
	c.image = 'nikon_camera_2.jpg'
	c.save()

	# Start instance of 
	u = mmod.Product()
	u.catalog_inventory_id = c.id
	u.store_id = s.id
	u.shelf_location = 'Storage Room'
	u.purchase_date = datetime.now().date()
	u.serial_number = random.randrange(1000,99999)
	u.active = True
	u.is_rental = False
	u.save()
	# END

	###############################################################
	revSrc = mmod.Loan()
	revSrc.amount = c.average_cost
	revSrc.note = 'Prodcut Purchase'
	revSrc.save()

	journ = mmod.JournalEntry()
	journ.revenueSource_id = revSrc.id
	journ.save()

	# debit lta for amount of store
	ent = mmod.Debit()
	ent.GeneralLedgerName_id = 4
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()

	# credit cash for amount of store
	ent = mmod.Credit()
	ent.GeneralLedgerName_id = 1
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()
	# END

	c = mmod.CatalogInventory()
	c.product_name = 'Canon EOS 5D Mark III DSLR Camera' 
	c.description = 'Body only, no lens. 22.3MP FX-format CMOS sensor, DIGIC 5+ image sensor'
	c.manufacturer = 'Nikon'
	c.average_cost = 2520.00
	c.commission_rate = .1
	c.product_category = 'Camera'
	c.sku = random.randrange(1000,99999)
	c.active = True
	c.sale_price = 3999.99
	c.image = 'nikon_camera_3.jpg'
	c.save()

	# Start instance of 
	u = mmod.Product()
	u.catalog_inventory_id = c.id
	u.store_id = s.id
	u.shelf_location = 'Storage Room'
	u.purchase_date = datetime.now().date()
	u.serial_number = random.randrange(1000,99999)
	u.active = True
	u.is_rental = False
	u.save()
	# END

	###############################################################
	revSrc = mmod.Loan()
	revSrc.amount = c.average_cost
	revSrc.note = 'Prodcut Purchase'
	revSrc.save()

	journ = mmod.JournalEntry()
	journ.revenueSource_id = revSrc.id
	journ.save()

	# debit lta for amount of store
	ent = mmod.Debit()
	ent.GeneralLedgerName_id = 4
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()

	# credit cash for amount of store
	ent = mmod.Credit()
	ent.GeneralLedgerName_id = 1
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()
	# END

	c = mmod.CatalogInventory()
	c.product_name = 'Nikon D800 Digital SLR Camera' 
	c.description = 'Body only, no lens. 35.9 x 24.0mm CMOS FX format sensor, EXPEED 3 image sensor'
	c.manufacturer = 'Nikon'
	c.average_cost = 1500.00
	c.commission_rate = .1
	c.product_category = 'Camera'
	c.sku = random.randrange(1000,99999)
	c.active = True
	c.sale_price = 2779.99
	c.image = 'nikon_camera_4.jpg'
	c.save()

	# Start instance of 
	u = mmod.Product()
	u.catalog_inventory_id = c.id
	u.store_id = s.id
	u.shelf_location = 'Storage Room'
	u.purchase_date = datetime.now().date()
	u.serial_number = random.randrange(1000,99999)
	u.active = True
	u.is_rental = False
	u.save()
	# END

	###############################################################
	revSrc = mmod.Loan()
	revSrc.amount = c.average_cost
	revSrc.note = 'Prodcut Purchase'
	revSrc.save()

	journ = mmod.JournalEntry()
	journ.revenueSource_id = revSrc.id
	journ.save()

	# debit lta for amount of store
	ent = mmod.Debit()
	ent.GeneralLedgerName_id = 4
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()

	# credit cash for amount of store
	ent = mmod.Credit()
	ent.GeneralLedgerName_id = 1
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()
	# END


	c = mmod.CatalogInventory()
	c.product_name = 'Nikon D3200 DSLR Camera with 18-55mm and 55-200mm Lenses (Black)' 
	c.description = '24.2MP DX-format CMOS senson, comes with shoulder bag'
	c.manufacturer = 'Nikon'
	c.average_cost = 480.00
	c.commission_rate = .1
	c.product_category = 'Camera'
	c.sku = random.randrange(1000,99999)
	c.active = True
	c.sale_price = 598.99
	c.image = 'nikon_camera_5.jpg'
	c.save()

	# Start instance of 
	u = mmod.Product()
	u.catalog_inventory_id = c.id
	u.store_id = s.id
	u.shelf_location = 'Storage Room'
	u.purchase_date = datetime.now().date()
	u.serial_number = random.randrange(1000,99999)
	u.active = True
	u.is_rental = False
	u.save()
	# END

	###############################################################
	revSrc = mmod.Loan()
	revSrc.amount = c.average_cost
	revSrc.note = 'Prodcut Purchase'
	revSrc.save()

	journ = mmod.JournalEntry()
	journ.revenueSource_id = revSrc.id
	journ.save()

	# debit lta for amount of store
	ent = mmod.Debit()
	ent.GeneralLedgerName_id = 4
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()

	# credit cash for amount of store
	ent = mmod.Credit()
	ent.GeneralLedgerName_id = 1
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()
	# END



	c = mmod.CatalogInventory()
	c.product_name = 'Sony Cyber-shot DSC-RX100 II Digital Camera' 
	c.description = '20.2MP 1" exmor R BSI CMOS sensor'
	c.manufacturer = 'Sony'
	c.average_cost = 450.00
	c.commission_rate = .1
	c.product_category = 'Camera'
	c.sku = random.randrange(1000,99999)
	c.active = True
	c.sale_price = 698.99
	c.image = 'sony_camera_1.jpg'
	c.save()

	# Start instance of 
	u = mmod.Product()
	u.catalog_inventory_id = c.id
	u.store_id = s.id
	u.shelf_location = 'Storage Room'
	u.purchase_date = datetime.now().date()
	u.serial_number = random.randrange(1000,99999)
	u.active = True
	u.is_rental = False
	u.save()
	# END

	###############################################################
	revSrc = mmod.Loan()
	revSrc.amount = c.average_cost
	revSrc.note = 'Prodcut Purchase'
	revSrc.save()

	journ = mmod.JournalEntry()
	journ.revenueSource_id = revSrc.id
	journ.save()

	# debit lta for amount of store
	ent = mmod.Debit()
	ent.GeneralLedgerName_id = 4
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()

	# credit cash for amount of store
	ent = mmod.Credit()
	ent.GeneralLedgerName_id = 1
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()
	# END

	c = mmod.CatalogInventory()
	c.product_name = 'Sony Cyber-shot DSC-RX10 Digital Camera' 
	c.description = '20.2MP 1" exmor R BSI CMOS sensor, Carl Zeiss 24-200mm f/2.8 lens (35mm Eq)'
	c.manufacturer = 'Sony'
	c.average_cost = 950.00
	c.commission_rate = .1
	c.product_category = 'Camera'
	c.sku = random.randrange(1000,99999)
	c.active = True
	c.sale_price = 1298.99
	c.image = 'sony_camera_2.jpg'
	c.save()

	# Start instance of 
	u = mmod.Product()
	u.catalog_inventory_id = c.id
	u.store_id = s.id
	u.shelf_location = 'Storage Room'
	u.purchase_date = datetime.now().date()
	u.serial_number = random.randrange(1000,99999)
	u.active = True
	u.is_rental = False
	u.save()
	# END

	###############################################################
	revSrc = mmod.Loan()
	revSrc.amount = c.average_cost
	revSrc.note = 'Prodcut Purchase'
	revSrc.save()

	journ = mmod.JournalEntry()
	journ.revenueSource_id = revSrc.id
	journ.save()

	# debit lta for amount of store
	ent = mmod.Debit()
	ent.GeneralLedgerName_id = 4
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()

	# credit cash for amount of store
	ent = mmod.Credit()
	ent.GeneralLedgerName_id = 1
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()
	# END


	c = mmod.CatalogInventory()
	c.product_name = 'Sony Alpha A6000 Mirrorless Digital Camera with 16-50mm Lens (Black)' 
	c.description = '24.3MP APS-C exmor APS HD CMOS sensor, built in WiFi connectivity with NFC'
	c.manufacturer = 'Sony'
	c.average_cost = 300.00
	c.commission_rate = .1
	c.product_category = 'Camera'
	c.sku = random.randrange(1000,99999)
	c.active = True
	c.sale_price = 799.99
	c.image = 'sony_camera_3.jpg'
	c.save()

	# Start instance of 
	u = mmod.Product()
	u.catalog_inventory_id = c.id
	u.store_id = s.id
	u.shelf_location = 'Storage Room'
	u.purchase_date = datetime.now().date()
	u.serial_number = random.randrange(1000,99999)
	u.active = True
	u.is_rental = False
	u.save()
	# END

	###############################################################
	revSrc = mmod.Loan()
	revSrc.amount = c.average_cost
	revSrc.note = 'Prodcut Purchase'
	revSrc.save()

	journ = mmod.JournalEntry()
	journ.revenueSource_id = revSrc.id
	journ.save()

	# debit lta for amount of store
	ent = mmod.Debit()
	ent.GeneralLedgerName_id = 4
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()

	# credit cash for amount of store
	ent = mmod.Credit()
	ent.GeneralLedgerName_id = 1
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()
	# END

	c = mmod.CatalogInventory()
	c.product_name = 'Sony Alpha a7 Mirrorless Digital Camera with FE 28-70mm f/3.5-5.6 OSS Lens' 
	c.description = '24.3MP APS-C exmor APS HD CMOS sensor, fast hybrid autofocus; 5 fps burst rate'
	c.manufacturer = 'Sony'
	c.average_cost = 1100.00
	c.commission_rate = .1
	c.product_category = 'Camera'
	c.sku = random.randrange(1000,99999)
	c.active = True
	c.sale_price = 1999.99
	c.image = 'sony_camera_4.jpg'
	c.save()

	# Start instance of 
	u = mmod.Product()
	u.catalog_inventory_id = c.id
	u.store_id = s.id
	u.shelf_location = 'Storage Room'
	u.purchase_date = datetime.now().date()
	u.serial_number = random.randrange(1000,99999)
	u.active = True
	u.is_rental = False
	u.save()
	# END

	###############################################################
	revSrc = mmod.Loan()
	revSrc.amount = c.average_cost
	revSrc.note = 'Prodcut Purchase'
	revSrc.save()

	journ = mmod.JournalEntry()
	journ.revenueSource_id = revSrc.id
	journ.save()

	# debit lta for amount of store
	ent = mmod.Debit()
	ent.GeneralLedgerName_id = 4
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()

	# credit cash for amount of store
	ent = mmod.Credit()
	ent.GeneralLedgerName_id = 1
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()
	# END

	c = mmod.CatalogInventory()
	c.product_name = 'Sony Cyber-shot DSC-TX30 Digital Camera (Black)' 
	c.description = '18.2MP exmor R CMOS sensor, touch screen back'
	c.manufacturer = 'Sony'
	c.average_cost = 100.00
	c.commission_rate = .1
	c.product_category = 'Camera'
	c.sku = random.randrange(1000,99999)
	c.active = True
	c.sale_price = 179.99
	c.image = 'sony_camera_5.jpg'
	c.save()

	# Start instance of 
	u = mmod.Product()
	u.catalog_inventory_id = c.id
	u.store_id = s.id
	u.shelf_location = 'Storage Room'
	u.purchase_date = datetime.now().date()
	u.serial_number = random.randrange(1000,99999)
	u.active = True
	u.is_rental = False
	u.save()
	# END

	###############################################################
	revSrc = mmod.Loan()
	revSrc.amount = c.average_cost
	revSrc.note = 'Prodcut Purchase'
	revSrc.save()

	journ = mmod.JournalEntry()
	journ.revenueSource_id = revSrc.id
	journ.save()

	# debit lta for amount of store
	ent = mmod.Debit()
	ent.GeneralLedgerName_id = 4
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()

	# credit cash for amount of store
	ent = mmod.Credit()
	ent.GeneralLedgerName_id = 1
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()
	# END




	# END CAMERA #################################################################

	# Start LENSES#################################################################


	c = mmod.CatalogInventory()
	c.product_name = 'Canon EF 24-70mm f/2.8L II USM Lens' 
	c.description = 'Aperture range: f/2.8-22'
	c.manufacturer = 'Canon'
	c.average_cost = 2000.00
	c.commission_rate = .1
	c.product_category = 'Lens'
	c.sku = random.randrange(1000,99999)
	c.active = True
	c.sale_price = 2299.99
	c.image = 'canon_lens_1.jpg'
	c.save()

	# Start instance of 
	u = mmod.Product()
	u.catalog_inventory_id = c.id
	u.store_id = s.id
	u.shelf_location = 'Storage Room'
	u.purchase_date = datetime.now().date()
	u.serial_number = random.randrange(1000,99999)
	u.active = True
	u.is_rental = False
	u.save()
	# END

	###############################################################
	revSrc = mmod.Loan()
	revSrc.amount = c.average_cost
	revSrc.note = 'Prodcut Purchase'
	revSrc.save()

	journ = mmod.JournalEntry()
	journ.revenueSource_id = revSrc.id
	journ.save()

	# debit lta for amount of store
	ent = mmod.Debit()
	ent.GeneralLedgerName_id = 4
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()

	# credit cash for amount of store
	ent = mmod.Credit()
	ent.GeneralLedgerName_id = 1
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()
	# END

	c = mmod.CatalogInventory()
	c.product_name = 'Canon EF 75-300mm f/4-5.6 III Lens' 
	c.description = 'Aperture range: f/4-45'
	c.manufacturer = 'Canon'
	c.average_cost = 100.00
	c.commission_rate = .1
	c.product_category = 'Lens'
	c.sku = random.randrange(1000,99999)
	c.active = True
	c.sale_price = 299.99
	c.image = 'canon_lens_2.jpg'
	c.save()

	# Start instance of 
	u = mmod.Product()
	u.catalog_inventory_id = c.id
	u.store_id = s.id
	u.shelf_location = 'Storage Room'
	u.purchase_date = datetime.now().date()
	u.serial_number = random.randrange(1000,99999)
	u.active = True
	u.is_rental = False
	u.save()
	# END

	###############################################################
	revSrc = mmod.Loan()
	revSrc.amount = c.average_cost
	revSrc.note = 'Prodcut Purchase'
	revSrc.save()

	journ = mmod.JournalEntry()
	journ.revenueSource_id = revSrc.id
	journ.save()

	# debit lta for amount of store
	ent = mmod.Debit()
	ent.GeneralLedgerName_id = 4
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()

	# credit cash for amount of store
	ent = mmod.Credit()
	ent.GeneralLedgerName_id = 1
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()
	# END


	c = mmod.CatalogInventory()
	c.product_name = 'Canon EF 85mm f/1.8 USM Lens' 
	c.description = 'Aperture range: f/1.8-22'
	c.manufacturer = 'Canon'
	c.average_cost = 200.00
	c.commission_rate = .1
	c.product_category = 'Lens'
	c.sku = random.randrange(1000,99999)
	c.active = True
	c.sale_price = 429.99
	c.image = 'canon_lens_3.jpg'
	c.save()

	# Start instance of 
	u = mmod.Product()
	u.catalog_inventory_id = c.id
	u.store_id = s.id
	u.shelf_location = 'Storage Room'
	u.purchase_date = datetime.now().date()
	u.serial_number = random.randrange(1000,99999)
	u.active = True
	u.is_rental = False
	u.save()
	# END

	###############################################################
	revSrc = mmod.Loan()
	revSrc.amount = c.average_cost
	revSrc.note = 'Prodcut Purchase'
	revSrc.save()

	journ = mmod.JournalEntry()
	journ.revenueSource_id = revSrc.id
	journ.save()

	# debit lta for amount of store
	ent = mmod.Debit()
	ent.GeneralLedgerName_id = 4
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()

	# credit cash for amount of store
	ent = mmod.Credit()
	ent.GeneralLedgerName_id = 1
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()
	# END


	c = mmod.CatalogInventory()
	c.product_name = 'Canon EF 70-200mm f/4L IS USM Lens' 
	c.description = 'Aperture range: f/4-32'
	c.manufacturer = 'Canon'
	c.average_cost = 2000.00
	c.commission_rate = .1
	c.product_category = 'Lens'
	c.sku = random.randrange(1000,99999)
	c.active = True
	c.sale_price = 2999.99
	c.image = 'canon_lens_4.jpg'
	c.save()

	# Start instance of 
	u = mmod.Product()
	u.catalog_inventory_id = c.id
	u.store_id = s.id
	u.shelf_location = 'Storage Room'
	u.purchase_date = datetime.now().date()
	u.serial_number = random.randrange(1000,99999)
	u.active = True
	u.is_rental = False
	u.save()
	# END

	###############################################################
	revSrc = mmod.Loan()
	revSrc.amount = c.average_cost
	revSrc.note = 'Prodcut Purchase'
	revSrc.save()

	journ = mmod.JournalEntry()
	journ.revenueSource_id = revSrc.id
	journ.save()

	# debit lta for amount of store
	ent = mmod.Debit()
	ent.GeneralLedgerName_id = 4
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()

	# credit cash for amount of store
	ent = mmod.Credit()
	ent.GeneralLedgerName_id = 1
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()
	# END


	c = mmod.CatalogInventory()
	c.product_name = 'Canon EF 85mm f/1.2L II USM Lens' 
	c.description = 'Aperture range: f/1.6-16'
	c.manufacturer = 'Canon'
	c.average_cost = 1800.00
	c.commission_rate = .1
	c.product_category = 'Lens'
	c.sku = random.randrange(1000,99999)
	c.active = True
	c.sale_price = 2399.99
	c.image = 'canon_lens_5.jpg'
	c.save()

	# Start instance of 
	u = mmod.Product()
	u.catalog_inventory_id = c.id
	u.store_id = s.id
	u.shelf_location = 'Storage Room'
	u.purchase_date = datetime.now().date()
	u.serial_number = random.randrange(1000,99999)
	u.active = True
	u.is_rental = False
	u.save()
	# END

	###############################################################
	revSrc = mmod.Loan()
	revSrc.amount = c.average_cost
	revSrc.note = 'Prodcut Purchase'
	revSrc.save()

	journ = mmod.JournalEntry()
	journ.revenueSource_id = revSrc.id
	journ.save()

	# debit lta for amount of store
	ent = mmod.Debit()
	ent.GeneralLedgerName_id = 4
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()

	# credit cash for amount of store
	ent = mmod.Credit()
	ent.GeneralLedgerName_id = 1
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()
	# END


	c = mmod.CatalogInventory()
	c.product_name = 'Nikon AF-S Nikkor 16-35mm f/4G ED VR Wide Angle Zoom Lens' 
	c.description = 'Vibration reduction (VR II)'
	c.manufacturer = 'Nikon'
	c.average_cost = 800.00
	c.commission_rate = .1
	c.product_category = 'Lens'
	c.sku = random.randrange(1000,99999)
	c.active = True
	c.sale_price = 1299.99
	c.image = 'nikon_lens_1.jpg'
	c.save()

	# Start instance of 
	u = mmod.Product()
	u.catalog_inventory_id = c.id
	u.store_id = s.id
	u.shelf_location = 'Storage Room'
	u.purchase_date = datetime.now().date()
	u.serial_number = random.randrange(1000,99999)
	u.active = True
	u.is_rental = False
	u.save()
	# END

	###############################################################
	revSrc = mmod.Loan()
	revSrc.amount = c.average_cost
	revSrc.note = 'Prodcut Purchase'
	revSrc.save()

	journ = mmod.JournalEntry()
	journ.revenueSource_id = revSrc.id
	journ.save()

	# debit lta for amount of store
	ent = mmod.Debit()
	ent.GeneralLedgerName_id = 4
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()

	# credit cash for amount of store
	ent = mmod.Credit()
	ent.GeneralLedgerName_id = 1
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()
	# END



	c = mmod.CatalogInventory()
	c.product_name = 'Nikon AF-S Nikkor 24-70mm f/2.8G ED Autofocus Lens (Black)' 
	c.description = 'Includes free luminesque 77mm UV and circular polarizer multi coated pro filter kit'
	c.manufacturer = 'Nikon'
	c.average_cost = 1000.00
	c.commission_rate = .1
	c.product_category = 'Lens'
	c.sku = random.randrange(1000,99999)
	c.active = True
	c.sale_price = 1886.99
	c.image = 'nikon_lens_2.jpg'
	c.save()

	# Start instance of 
	u = mmod.Product()
	u.catalog_inventory_id = c.id
	u.store_id = s.id
	u.shelf_location = 'Storage Room'
	u.purchase_date = datetime.now().date()
	u.serial_number = random.randrange(1000,99999)
	u.active = True
	u.is_rental = False
	u.save()
	# END

	###############################################################
	revSrc = mmod.Loan()
	revSrc.amount = c.average_cost
	revSrc.note = 'Prodcut Purchase'
	revSrc.save()

	journ = mmod.JournalEntry()
	journ.revenueSource_id = revSrc.id
	journ.save()

	# debit lta for amount of store
	ent = mmod.Debit()
	ent.GeneralLedgerName_id = 4
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()

	# credit cash for amount of store
	ent = mmod.Credit()
	ent.GeneralLedgerName_id = 1
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()
	# END




	c = mmod.CatalogInventory()
	c.product_name = 'Nikon AF-S DX NIKKOR 18-200mm f/3.5-5.6G ED VR II Zoom Lens' 
	c.description = 'For DX-Format D-SLRs'
	c.manufacturer = 'Nikon'
	c.average_cost = 500.00
	c.commission_rate = .1
	c.product_category = 'Lens'
	c.sku = random.randrange(1000,99999)
	c.active = True
	c.sale_price = 844.99
	c.image = 'nikon_lens_3.jpg'
	c.save()

	# Start instance of 
	u = mmod.Product()
	u.catalog_inventory_id = c.id
	u.store_id = s.id
	u.shelf_location = 'Storage Room'
	u.purchase_date = datetime.now().date()
	u.serial_number = random.randrange(1000,99999)
	u.active = True
	u.is_rental = False
	u.save()
	# END

	###############################################################
	revSrc = mmod.Loan()
	revSrc.amount = c.average_cost
	revSrc.note = 'Prodcut Purchase'
	revSrc.save()

	journ = mmod.JournalEntry()
	journ.revenueSource_id = revSrc.id
	journ.save()

	# debit lta for amount of store
	ent = mmod.Debit()
	ent.GeneralLedgerName_id = 4
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()

	# credit cash for amount of store
	ent = mmod.Credit()
	ent.GeneralLedgerName_id = 1
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()
	# END

	c = mmod.CatalogInventory()
	c.product_name = 'Nikon AF-S NIKKOR 28-300mm f/3.5-5.6G ED VR Zoom Lens' 
	c.description = 'FX-Format zoom, has vr II image stabilization'
	c.manufacturer = 'Nikon'
	c.average_cost = 600.00
	c.commission_rate = .1
	c.product_category = 'Lens'
	c.sku = random.randrange(1000,99999)
	c.active = True
	c.sale_price = 1046.99
	c.image = 'nikon_lens_4.jpg'
	c.save()

	# Start instance of 
	u = mmod.Product()
	u.catalog_inventory_id = c.id
	u.store_id = s.id
	u.shelf_location = 'Storage Room'
	u.purchase_date = datetime.now().date()
	u.serial_number = random.randrange(1000,99999)
	u.active = True
	u.is_rental = False
	u.save()
	# END

	###############################################################
	revSrc = mmod.Loan()
	revSrc.amount = c.average_cost
	revSrc.note = 'Prodcut Purchase'
	revSrc.save()

	journ = mmod.JournalEntry()
	journ.revenueSource_id = revSrc.id
	journ.save()

	# debit lta for amount of store
	ent = mmod.Debit()
	ent.GeneralLedgerName_id = 4
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()

	# credit cash for amount of store
	ent = mmod.Credit()
	ent.GeneralLedgerName_id = 1
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()
	# END


	c = mmod.CatalogInventory()
	c.product_name = 'Nikon AF-S NIKKOR 80-400mm f/4.5-5.6G ED VR Lens' 
	c.description = 'Has Nikon F Mount, 120-600mm Equivalent in DX Format'
	c.manufacturer = 'Nikon'
	c.average_cost = 2200.00
	c.commission_rate = .1
	c.product_category = 'Lens'
	c.sku = random.randrange(1000,99999)
	c.active = True
	c.sale_price = 2799.99
	c.image = 'nikon_lens_5.jpg'
	c.save()

	# Start instance of 
	u = mmod.Product()
	u.catalog_inventory_id = c.id
	u.store_id = s.id
	u.shelf_location = 'Storage Room'
	u.purchase_date = datetime.now().date()
	u.serial_number = random.randrange(1000,99999)
	u.active = True
	u.is_rental = False
	u.save()
	# END

	###############################################################
	revSrc = mmod.Loan()
	revSrc.amount = c.average_cost
	revSrc.note = 'Prodcut Purchase'
	revSrc.save()

	journ = mmod.JournalEntry()
	journ.revenueSource_id = revSrc.id
	journ.save()

	# debit lta for amount of store
	ent = mmod.Debit()
	ent.GeneralLedgerName_id = 4
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()

	# credit cash for amount of store
	ent = mmod.Credit()
	ent.GeneralLedgerName_id = 1
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()
	# END


	c = mmod.CatalogInventory()
	c.product_name = 'Sony 55-300mm f/4.5-5.6 DT Alpha A-Mount Telephoto Zoom Lens' 
	c.description = '35mm equivalent: 82.5-450mm'
	c.manufacturer = 'Sony'
	c.average_cost = 100.00
	c.commission_rate = .1
	c.product_category = 'Lens'
	c.sku = random.randrange(1000,99999)
	c.active = True
	c.sale_price = 299.99
	c.image = 'sony_lens_1.jpg'
	c.save()

	# Start instance of 
	u = mmod.Product()
	u.catalog_inventory_id = c.id
	u.store_id = s.id
	u.shelf_location = 'Storage Room'
	u.purchase_date = datetime.now().date()
	u.serial_number = random.randrange(1000,99999)
	u.active = True
	u.is_rental = False
	u.save()
	# END

	###############################################################
	revSrc = mmod.Loan()
	revSrc.amount = c.average_cost
	revSrc.note = 'Prodcut Purchase'
	revSrc.save()

	journ = mmod.JournalEntry()
	journ.revenueSource_id = revSrc.id
	journ.save()

	# debit lta for amount of store
	ent = mmod.Debit()
	ent.GeneralLedgerName_id = 4
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()

	# credit cash for amount of store
	ent = mmod.Credit()
	ent.GeneralLedgerName_id = 1
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()
	# END


	c = mmod.CatalogInventory()
	c.product_name = 'Sony 24-70mm f/2.8 Carl Zeiss T* Alpha A-Mount Standard Zoom Lens' 
	c.description = 'Aperture range: f/2.8-22, Carl Zeiss T* glass coating'
	c.manufacturer = 'Sony'
	c.average_cost = 980.00
	c.commission_rate = .1
	c.product_category = 'Lens'
	c.sku = random.randrange(1000,99999)
	c.active = True
	c.sale_price = 1899.99
	c.image = 'sony_lens_2.jpg'
	c.save()

	# Start instance of 
	u = mmod.Product()
	u.catalog_inventory_id = c.id
	u.store_id = s.id
	u.shelf_location = 'Storage Room'
	u.purchase_date = datetime.now().date()
	u.serial_number = random.randrange(1000,99999)
	u.active = True
	u.is_rental = False
	u.save()
	# END

	###############################################################
	revSrc = mmod.Loan()
	revSrc.amount = c.average_cost
	revSrc.note = 'Prodcut Purchase'
	revSrc.save()

	journ = mmod.JournalEntry()
	journ.revenueSource_id = revSrc.id
	journ.save()

	# debit lta for amount of store
	ent = mmod.Debit()
	ent.GeneralLedgerName_id = 4
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()

	# credit cash for amount of store
	ent = mmod.Credit()
	ent.GeneralLedgerName_id = 1
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()
	# END


	c = mmod.CatalogInventory()
	c.product_name = 'Sony 70-400mm f/4-5.6 G Alpha A-Mount Telephoto Zoom Lens' 
	c.description = 'Aperture range: f/4-32, for Alpha & Minolta Maxxum DSLRs'
	c.manufacturer = 'Sony'
	c.average_cost = 980.00
	c.commission_rate = .1
	c.product_category = 'Lens'
	c.sku = random.randrange(1000,99999)
	c.active = True
	c.sale_price = 1899.99
	c.image = 'sony_lens_3.jpg'
	c.save()

	# Start instance of 
	u = mmod.Product()
	u.catalog_inventory_id = c.id
	u.store_id = s.id
	u.shelf_location = 'Storage Room'
	u.purchase_date = datetime.now().date()
	u.serial_number = random.randrange(1000,99999)
	u.active = True
	u.is_rental = False
	u.save()
	# END

	###############################################################
	revSrc = mmod.Loan()
	revSrc.amount = c.average_cost
	revSrc.note = 'Prodcut Purchase'
	revSrc.save()

	journ = mmod.JournalEntry()
	journ.revenueSource_id = revSrc.id
	journ.save()

	# debit lta for amount of store
	ent = mmod.Debit()
	ent.GeneralLedgerName_id = 4
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()

	# credit cash for amount of store
	ent = mmod.Credit()
	ent.GeneralLedgerName_id = 1
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()
	# END


	c = mmod.CatalogInventory()
	c.product_name = 'Sony 28-75mm f/2.8 Alpha A-Mount Standard Zoom Lens' 
	c.description = 'Aperture range: f/2.8-32, for Alpha & Minolta Maxxum DSLRs, 4x aspherical glass lens elements'
	c.manufacturer = 'Sony'
	c.average_cost = 560.00
	c.commission_rate = .1
	c.product_category = 'Lens'
	c.sku = random.randrange(1000,99999)
	c.active = True
	c.sale_price = 899.00
	c.image = 'sony_lens_4.jpg'
	c.save()

	# Start instance of 
	u = mmod.Product()
	u.catalog_inventory_id = c.id
	u.store_id = s.id
	u.shelf_location = 'Storage Room'
	u.purchase_date = datetime.now().date()
	u.serial_number = random.randrange(1000,99999)
	u.active = True
	u.is_rental = False
	u.save()
	# END

	###############################################################
	revSrc = mmod.Loan()
	revSrc.amount = c.average_cost
	revSrc.note = 'Prodcut Purchase'
	revSrc.save()

	journ = mmod.JournalEntry()
	journ.revenueSource_id = revSrc.id
	journ.save()

	# debit lta for amount of store
	ent = mmod.Debit()
	ent.GeneralLedgerName_id = 4
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()

	# credit cash for amount of store
	ent = mmod.Credit()
	ent.GeneralLedgerName_id = 1
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()
	# END


	c = mmod.CatalogInventory()
	c.product_name = 'Sony 70-400mm f/4-5.6 G2 Telephoto Zoom Lens' 
	c.description = 'Sony alpha mount for full-frame sensors'
	c.manufacturer = 'Sony'
	c.average_cost = 1980.00
	c.commission_rate = .1
	c.product_category = 'Lens'
	c.sku = random.randrange(1000,99999)
	c.active = True
	c.sale_price = 2399.99
	c.image = 'sony_lens_5.jpg'
	c.save()

	# Start instance of 
	u = mmod.Product()
	u.catalog_inventory_id = c.id
	u.store_id = s.id
	u.shelf_location = 'Storage Room'
	u.purchase_date = datetime.now().date()
	u.serial_number = random.randrange(1000,99999)
	u.active = True
	u.is_rental = False
	u.save()
	# END

	###############################################################
	revSrc = mmod.Loan()
	revSrc.amount = c.average_cost
	revSrc.note = 'Prodcut Purchase'
	revSrc.save()

	journ = mmod.JournalEntry()
	journ.revenueSource_id = revSrc.id
	journ.save()

	# debit lta for amount of store
	ent = mmod.Debit()
	ent.GeneralLedgerName_id = 4
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()

	# credit cash for amount of store
	ent = mmod.Credit()
	ent.GeneralLedgerName_id = 1
	ent.journalEntry_id = journ.id
	ent.amount = revSrc.amount
	ent.save()
	# END





	# End LENSES#################################################################

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
	u.save()

	u = mmod.User.objects.get(id=1)
	u.first_name = 'David'
	u.last_name = 'Hanks'
	u.street = '915 N 150 E'
	u.street2 = 'Apt 205'
	u.city = 'Provo'
	u.state = 'UT'
	u.zipCode = '84604'
	u.phone = '(541) 531-1462'
	u.is_active = True
	u.active = True
	u.is_staff = True
	u.is_superuser = True
	u.save()



	return HttpResponseRedirect('/manager/dashboard/')



