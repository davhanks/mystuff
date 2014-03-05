from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from manager import models


class SaleItem(models.Model):
  '''The Transaction class'''
  employee = models.ForeignKey('Employee')
  product = models.ForeignKey('Product')
  date = models.DateTimeField(auto_now_add=True)
  sub_total = models.DecimalField(blank=True, null=True)
  shipping_cost = models.DecimalField(blank=True, null=True)
  tax_ammount = models.DecimalField(blank=True, null=True)

  

 class Commission(models.Model):
 	employee = models.ForeignKey('Employee')
 	transaction = models.OneToOneField('SaleItem')
 	amount = models.DecimalField(blank=True, null=True)
 	date = models.DateTimeField(auto_now_add=True)

    
  
  
# from polls import models as pmod
# questions = pmod.Question.objects.all()
# pmod.Question.objects.filter(question_text='This is the third question')
# q1 = pmod.Question.objects.get(id=2)
# .exclude()   you can chain them together