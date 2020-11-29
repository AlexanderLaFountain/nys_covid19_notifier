import os
from twilio.rest import Client
from credentials import twilio_info

def send_message(cellphone_number, new_cases_today, new_cases_lastsevendays, infection_rate, total_cases, date_today):
    
    cred = twilio_info()
    account_sid = cred['account_sid']
    auth_token = cred['auth_token']
    twilio_number = cred['twilio_number']

    client = Client(account_sid, auth_token)

    message_template = (
        f'Date: {date_today}\n\
New Cases (24hr): {new_cases_today}\n\
New Cases (7days): {new_cases_lastsevendays}\n\
Total Cases: {total_cases}\n\
Infection Rate: {infection_rate}%'
    )

    message = client.messages.create(
                        body=message_template,
                        from_=twilio_number,
                        to=cellphone_number
                    )

    print(f'Message sent to {cellphone_number}: {message.sid}')
