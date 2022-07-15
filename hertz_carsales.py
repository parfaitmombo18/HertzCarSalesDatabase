import requests
import os
import pandas as pd
import urllib.request
import certifi
import ssl
from time import sleep

import urllib3

car_name = []
model = []
image_uri = []
image_name = []
price = []
fuel_type = []
mileage = []
transmission = []
location = []

for page in range(1, 27):
    
    headers = {
        'authority': 'www.hertzcarsales.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'referer': 'https://www.hertzcarsales.com/morrow/used-cars.htm?geoRadius=0&make=INFINITI&geoZip=&start=0',
        'sec-ch-ua': '^\^',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '^\^Windows^^',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'no-cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36 Edg/103.0.1264.49',
    }

    params = (
        ('pageStart', str(page)),
        ('pageSize', 18)
    )

    response = requests.get('https://www.hertzcarsales.com/apis/widget/LOCATION_VLP_MORROW:inventory-data-bus1/getInventory?geoRadius=0&make=INFINITI&geoZip=&start=0', 
                            headers=headers, params=params)
    
    # json
    result_json = response.json()
        
    # results
    inventory_results = result_json['inventory']    
        
    for result in inventory_results:
        # car name 
        try:
            car_name.append(result['title'][0])
        except:
            car_name.append('')

        # model 
        try:
            model.append(result['model'])
        except:
            model.append('')

        # image_uri 
        try:
            image_uri.append(result['images'][0]['uri'])
        except:
            image_uri.append('')
            
        # image_name 
        try:
            image_name.append(result['images'][0]['alt'])
        except:
            image_name.append('')
        
        # price
        try:
            price.append(result['pricing']['retailPrice'].strip('$'))
        except:
            price.append('')
            
        # fuel type
        try:
            fuel_type.append(result['fuelType'])
        except:
            fuel_type.append('')
        
        # mileage
        try:
            mileage.append(result['attributes'][1]['value'].strip('miles '))
        except:
            mileage.append('')
            
        # transmission
        try:
            transmission.append(result['pricing']['vehicle']['category'])
        except:
            transmission.append('')
            
        # location
        try:
            location.append(result['attributes'][0]['value'])
        except:
            location.append('')
            
    
    # inventory dataframe
    inventory = {
        'Car Name': car_name,
        'Model': model,
        'Price ($)': price,
        'Fuel Type': fuel_type,
        'Mileage': mileage,
        'Transmission': transmission,
        'Location': location,
        'Image Name': image_name,
        'Image URI': image_uri
        
    }
    
    """The code below downloads each car image and save it in a specified folder
       that I named "CarImages" and located within the working directory
    """
    number = 1
    page_number = str(page)
    print(f'------- Page: {page} -----------')
    for item in range(0, len(inventory_results)):
        folder_path = os.path.join(os.getcwd(), 'CarImages')
        # im_name = str(number) + '.jpg'
        record_number =  str(number) + '-'
        im_name = page_number + record_number + inventory_results[item]['images'][0]['alt'] + '.jpg'
        image_path = os.path.join(folder_path, im_name)    
        image_link = inventory_results[item]['images'][0]['uri']
        resource = urllib.request.urlopen(image_link,
                                context=ssl.create_default_context(cafile=certifi.where()))
        output = open(image_path,"wb")
        output.write(resource.read())
        output.close()
        print(f'Image { im_name } downloaded')
        number += 1
        sleep(0.1)
    sleep(0.1)
    
    
inventory_df = pd.DataFrame(inventory)
inventory_df.to_csv('HertzCarsSalesDatabase.csv')
print('Web Scraping Complete!')
        