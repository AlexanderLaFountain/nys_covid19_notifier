
# https://dev.socrata.com/foundry/health.data.ny.gov/xdss-u53e
def nys_covid():
    cred = {
        'username': 'username',
        'password': 'password',
        'app_token': 'app_token'
    }
    return cred

# https://covidactnow.org/tools#api
def covid_act_now():
    cred = {
        'api_key': 'api_key'
    }
    return cred

def twilio_info():
    cred = {
        'account_sid': 'account_sid',
        'auth_token': 'auth_token',
        'twilio_number': 'twilio_number'
    }
    return cred