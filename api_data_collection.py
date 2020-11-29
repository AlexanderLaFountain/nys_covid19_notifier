import pandas as pd
from sodapy import Socrata
import datetime
import requests
from credentials import nys_covid, covid_act_now

def main(user_county, user_fips):

    county = user_county
    fips = user_fips

    def nys_covid_api(county):

        cred = nys_covid()
        nys_username = cred['username']
        nys_password = cred['password']
        nys_app_token = cred['app_token']

        MyAppToken = nys_app_token
        client = Socrata('health.data.ny.gov',
                        MyAppToken,
                        username=nys_username,
                        password=nys_password)

        # Results, returned as JSON from API / converted to Python list of dictionaries by sodapy.
        results = client.get("xdss-u53e", limit=49999) 

        # Convert to pandas DataFrame
        results_df = pd.DataFrame.from_records(results, columns=['test_date', 'county', 'new_positives', 'cumulative_number_of_positives', 'total_number_of_tests', 'cumulative_number_of_tests'])
       
        # from results_df select only user_county
        user_county_df = results_df.loc[results_df['county'] == county, ['test_date', 'new_positives','cumulative_number_of_positives', 'total_number_of_tests', 'cumulative_number_of_tests']]
        user_county_df.reset_index(drop=True, inplace=True) # index df from 0

        for i, day in enumerate(user_county_df['test_date']): 
            date_current = day[0:10] # grabs just the date from string; YYYY-MM-DD
            user_county_df.test_date[i] = date_current # update test_date in user_county_df
    
        list_length = (len(user_county_df) - 1)

        new_cases_today = user_county_df.new_positives[list_length]

        lastsevendays = user_county_df.new_positives[-7:]
        new_cases_lastsevendays = 0
        for item in lastsevendays:
            new_cases_lastsevendays = int(item) + new_cases_lastsevendays

        # total_cases
        total_cases = user_county_df.cumulative_number_of_positives[list_length]

        # time stamp
        time_now = datetime.datetime.now()
        date_today = time_now.strftime('%m/%d/%Y')
        time_stamp = time_now.strftime('%H:%M:%S')
        
        return new_cases_today, new_cases_lastsevendays, total_cases, date_today, time_stamp, user_county_df

    county_data = nys_covid_api(county)
    new_cases_today = county_data[0]
    new_cases_lastsevendays = county_data[1]
    total_cases = county_data[2]
    date_today = county_data[3]
    time_stamp = county_data[4]
    user_county_df = county_data[5]

    def covid_act_now_api(fips):

        fips_code = fips
        cred = covid_act_now()
        api_Key = cred['api_key']

        data = requests.get(f'https://api.covidactnow.org/v2/county/{fips_code}.json?apiKey={api_Key}')
        data_json = data.json()
        metrics = data_json['metrics']
        infectionRate = metrics['infectionRate']
        return infectionRate

    try:
        infectionRate = covid_act_now_api(fips)
    except:
        return 'fips_code does not match user_county'


    def save_county_data(county):
        county_lower = county.lower()
        try:
            string_list = county_lower.split('. ')
            county_str = string_list[0] + string_list[1]
        except:
            county_str = county_lower
        save_location = ('../nys_covid_notifier/env/data/' + county_str + '_data.csv')
        user_county_df.to_csv(save_location, index=True, mode='w')

    save_county_data(county)

    return {
        'new_cases_today': new_cases_today,
        'new_cases_lastsevendays': new_cases_lastsevendays,
        'total_cases': total_cases,
        'infection_rate': infectionRate,
        'date_today': date_today,
        'time_stamp': time_stamp
    }
