import datetime

now = datetime.datetime.now()

one_month_ago = now - datetime.timedelta(days=30)

cmod.Rendtal.objects.filter(due_date__gte=one_month_ago, due_date__lte=now).exclude(active=False)