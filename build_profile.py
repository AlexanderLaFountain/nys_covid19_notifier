# use uszipcode to calculate all variables for api 
from uszipcode import SearchEngine
# use addfips to calculate county fips id 
import addfips

def main(zipcode):
    
    try:
        user_zipcode = int(zipcode)
    except ValueError:
        return 'quoted string input containing aA <build_profile>'
    except TypeError:
        return 'string input containing aA <build_profile>'

    # state, county, population 
    def get_location_data(zipcode):
        '''
        Use uszipcode module to determine location based on entered zipcode
        '''
        search = SearchEngine(simple_zipcode=False) # use rich info zipcode database; requires download 450+MB

        zipcode = search.by_zipcode(zipcode)

        city = zipcode.major_city
        state = zipcode.state
        county = zipcode.county
        population = zipcode.population

        return state, city, county, population
    
    location_data = get_location_data(user_zipcode)

    state = location_data[0]
    city = location_data[1]
    county = location_data[2]
    population = location_data[3]
    
    def get_fips_code(county, state_abr):
        af = addfips.AddFIPS()
        code = af.get_county_fips(county, state=state_abr)
        return code

    try:
        fips_code = get_fips_code(county, state)
    except AttributeError:
            return 'target does not exist <build_profile>'

    return {'state': state,
            'city': city,
            'county': county,
            'fips': fips_code,
            'population': population
            }
