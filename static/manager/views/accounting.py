from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from homepage.models import *
from manager import models as mmod
from . import templater


def process_request(request):
    '''Sends user to the dashboard'''

    #Gets the user BO in order to pass information
    u = request.user

    #Checks for an Authenticated User
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/homepage/')
    if not request.user.is_staff:
        return HttpResponseRedirect('/homepage/')

    cashEntries = mmod.Debit.objects.filter(GeneralLedgerName_id=1)
    salesEntries = mmod.Debit.objects.filter(GeneralLedgerName_id=2)
    COGSEntries = mmod.Debit.objects.filter(GeneralLedgerName_id=3)
    inventoryEntries = mmod.Debit.objects.filter(GeneralLedgerName_id=4)
    AREntries = mmod.Debit.objects.filter(GeneralLedgerName_id=5)
    otherEntries = mmod.Debit.objects.filter(GeneralLedgerName_id=6)
    long_term_assetEntries = mmod.Debit.objects.filter(GeneralLedgerName_id=7)
    APEntries = mmod.Debit.objects.filter(GeneralLedgerName_id=8)
    salariesPayableEntries = mmod.Debit.objects.filter(GeneralLedgerName_id=9)
    long_term_debtEntries = mmod.Debit.objects.filter(GeneralLedgerName_id=10)
    CSEntries = mmod.Debit.objects.filter(GeneralLedgerName_id=11)
    retainedEarningsEntries = mmod.Debit.objects.filter(GeneralLedgerName_id=12)

    cred_cashEntries = mmod.Credit.objects.filter(GeneralLedgerName_id=1)
    cred_salesEntries = mmod.Credit.objects.filter(GeneralLedgerName_id=2)
    cred_COGSEntries = mmod.Credit.objects.filter(GeneralLedgerName_id=3)
    cred_inventoryEntries = mmod.Credit.objects.filter(GeneralLedgerName_id=4)
    cred_AREntries = mmod.Credit.objects.filter(GeneralLedgerName_id=5)
    cred_otherEntries = mmod.Credit.objects.filter(GeneralLedgerName_id=6)
    cred_long_term_assetEntries = mmod.Credit.objects.filter(GeneralLedgerName_id=7)
    cred_APEntries = mmod.Credit.objects.filter(GeneralLedgerName_id=8)
    cred_salariesPayableEntries = mmod.Credit.objects.filter(GeneralLedgerName_id=9)
    cred_long_term_debtEntries = mmod.Credit.objects.filter(GeneralLedgerName_id=10)
    cred_CSEntries = mmod.Credit.objects.filter(GeneralLedgerName_id=11)
    cred_retainedEarningsEntries = mmod.Credit.objects.filter(GeneralLedgerName_id=12)


    cash_amount = 0
    sales_amount = 0
    COGS_amount = 0
    inv_amount = 0
    AR_amount = 0
    other_amount = 0
    lta_amount = 0



    AP_amount = 0
    salaries_amount = 0
    ltd_amount = 0
    CS_amount = 0
    retainedEarnings_amount = 0
    

    for ent in cashEntries:
        cash_amount += ent.amount

    for ent in inventoryEntries:
        inv_amount += ent.amount


    for ent in cred_cashEntries:
        cash_amount -= ent.amount


    for ent in cred_inventoryEntries:
        inv_amount -= ent.amount

    for ent in long_term_assetEntries:
        lta_amount += ent.amount

    for ent in cred_long_term_assetEntries:
        lta_amount -= ent.amount

    total_assets = cash_amount + inv_amount + AR_amount + other_amount + lta_amount


    for ent in long_term_debtEntries:
        ltd_amount -= ent.amount

    for ent in cred_long_term_debtEntries:
        ltd_amount += ent.amount

    total_liabilities = AP_amount + salaries_amount + ltd_amount

    for ent in CSEntries:
        CS_amount -= ent.amount

    for ent in cred_CSEntries:
        CS_amount += ent.amount

    for ent in retainedEarningsEntries:
        retainedEarnings_amount -= ent.amounts

    for ent in cred_retainedEarningsEntries:
        retainedEarnings_amount += ent.amount


    



    ##########Income Statement
    for ent in salesEntries:
        sales_amount -= ent.amount

    for ent in COGSEntries:
        COGS_amount += ent.amount

    for ent in cred_salesEntries:
        sales_amount += ent.amount

    for ent in cred_COGSEntries:
        COGS_amount -= ent.amount

    retainedEarnings_amount = sales_amount - COGS_amount


    total_equity = CS_amount + retainedEarnings_amount


    template_vars = {
        'user': u,
        'cash': cash_amount,
        'sales': sales_amount,
        'COGS': COGS_amount,
        'inv': inv_amount,
        'AR': AR_amount,
        'other': other_amount,
        'lta': lta_amount,
        'AP': AP_amount,
        'salaries': salaries_amount,
        'ltd': ltd_amount,
        'CS': CS_amount,
        'RE': retainedEarnings_amount,
        'total_assets': total_assets,
        'total_liabilities': total_liabilities,
        'total_equity': total_equity,
    }

    return templater.render_to_response(request, 'accounting.html', template_vars)