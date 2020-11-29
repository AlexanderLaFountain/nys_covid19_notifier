import pandas as pd
from pathlib import Path

# add recipients to csv file

def user_info_collection():
    user_info = []
    while True:
        first_name = input('Enter first name: ')
        if first_name == '':
            break
        last_name = input('Enter last name: ')
        zipcode = input('Enter zip code: ')
        number = input('Enter cell number without [(,),-]: ') 
        cellphone_number = '+1' + number
        user_info.append([first_name, last_name, zipcode, cellphone_number])
    return user_info

user_info = user_info_collection()
user_data_df = pd.DataFrame(data=user_info, columns=['first_name', 'last_name', 'zipcode', 'cellphone_number'])
print(user_data_df)

save_location = ('../nys_covid_notifier/env/data/user/user_info.csv')
file_path = Path(save_location)
if file_path.is_file:
    user_data_df.to_csv(save_location, index=False, mode='a', header=False) 
else:
    user_data_df.to_csv(save_location, index=False, mode='w')
