import build_profile as profile
import api_data_collection as data_collection
import csv
from sms_twilio import send_message

with open('../nys_covid_notifier/env/data/user/user_info.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0 
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
            try:
                zipcode = row[2]
            except IndexError:
                print('Complete')
                break
            name = row[0] + ' ' + row[1]
            cellphone_number = row[3]
            line_count += 1 
            
            data = profile.main(zipcode)

            state = data['state']
            city = data['city']
            county = data['county']
            fips = data['fips']
            population = data['population']
            county_name = county.split(' County')

            # api data collection

            api_data = data_collection.main(county_name[0], fips)
            
            new_cases_today = api_data['new_cases_today']
            new_cases_lastsevendays = api_data['new_cases_lastsevendays']
            infection_rate = round(api_data['infection_rate'], 2)
            total_cases = api_data['total_cases']
            date_today = api_data['date_today']
            time_stamp = api_data['time_stamp']

            send_message(
                cellphone_number, 
                new_cases_today, 
                new_cases_lastsevendays, 
                infection_rate, 
                total_cases, 
                date_today
            )