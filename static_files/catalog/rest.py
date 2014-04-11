API_URL = 'http://dithers.cs.byu.edu/iscore/api/v1/charges'
API_KEY = ''
r = requests.post(API_URL, data={
	'apikey':APY_KEY,
	'currency': usd,
	'amount' :
	'type' :
	'number' :
	'exp_month' :
	'exp_year':
	'cvc':
	'name':
	'description':
})

resp = r.json()

print(resp['ID'])