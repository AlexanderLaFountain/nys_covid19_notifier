# nys_covid19_notifier
Send daily SMS messages to friends and family informing them of COVID-19 new cases and county infection rate.

NOTE: File paths will need to be modified for the script to run properly

1. Create a blank folder for data, then a blank folder inside the data folder for user data.

2. API keys and APP tokens must be acquired from their respective websites.

    - New York State Statewide COVID-19 Testing 
    https://dev.socrata.com/foundry/health.data.ny.gov/xdss-u53e
    
    - Covid Act Now API
    https://apidocs.covidactnow.org/

3. A new copy of the dataset is released and saved daily. If you want this project to run daily at a specified time, then you will need to utilize a task scheduler, such as Windows Task Scheduler.

4. Sending SMS through Twilio costs roughly $0.0075 per text.