import requests
from geopy.distance import geodesic
import pandas as pd
import logging
import os

def filter(df: pd.DataFrame) -> pd.DataFrame:
    '''
    this function will take a dataframe,
    filter for USA country,
    remove rows that have at least one missing value.
    the API is accurate only for USA.
    '''
    return df[df['country'].isin(['USA', 'US'])].dropna(subset=['address', 'city', 'state', 'zip', 'country'])

def get_lat_long(address, api_key):
    url = "https://api.geoapify.com/v1/geocode/search"

    params = {
        "text": address,
        "apiKey": api_key
    }

    headers = {"Accept": "application/json"}

    try:
        resp = requests.get(url, headers=headers, params=params)

        if resp.status_code == 200:
            features = resp.json().get("features")
            if features:
                coordinates = features[0].get("geometry").get("coordinates")
                return coordinates[1], coordinates[0]  # Returning as (lat, long)
        else:
            logging.error(f"Error with status code: {resp.status_code}, address: {address}")
            return None, None

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}, address: {address}")
        return None, None
        

def get_distance_km(school_lat_long,institute_lat_long):
    '''
    return true if the distance between school and institues is less than threshold
    '''
    distance = geodesic(school_lat_long, institute_lat_long).km
    return distance 


if __name__=="__main__":
    
    # Enter Path and read CSV files 
    path_schools = os.environ['path_schools']
    path_institutes = os.environ['path_institutes']
    api_key = os.environ['api_key']


    schools_df = pd.read_csv(path_schools)
    institutes_df = pd.read_csv(path_institutes)
    
    # clean dataframe only include USA schools and institues and remove rows that has missing information
    schools_usa_df = filter(schools_df)
    institutes_usa_df = filter(institutes_df)
    
    close_schools = []

    # get distance between each school and institute 
    for index, school_usa_df in schools_usa_df.iterrows():
        schools_usa_address = f"{school_usa_df.address}, {school_usa_df.city} {school_usa_df.zip}, {school_usa_df.country}"
        school_lat_long = get_lat_long(schools_usa_address,api_key=api_key)
        
        for index, institute_usa_df in institutes_usa_df.iterrows():
            institute_usa_address = f"{institute_usa_df.address},{institute_usa_df.city} {institute_usa_df.zip}, {institute_usa_df.country}"
            
            institute_lat_long = get_lat_long(institute_usa_address,api_key=api_key)
            
            distance = get_distance_km(school_lat_long,institute_lat_long)
            if distance < 100: 
                '''
                check for distance less than 100 km
                '''
                # print(school_usa_df.id,institute_usa_df.id,distance)
                close_schools.append((school_usa_df.id,institute_usa_df.id,distance))
    
    print(close_schools)
