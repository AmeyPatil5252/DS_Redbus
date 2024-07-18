import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import numpy as np

# Initialize the WebDriver
driver = webdriver.Chrome() 
driver.get('https://www.redbus.in/online-booking/rtc-directory'); #url to scrape

# Fetch all government bus links
gov_link = driver.find_elements(By.XPATH, "//li[@class='D113_item_rtc']/a")
gov_link_list = [element.get_attribute('href') for element in gov_link]

# Initialize DataFrame to store the results
df = pd.DataFrame(columns=[
        'route_name','route_link','route_start', 'route_end', 'bus_name', 'bustype',
        'departing_time', 'duration', 'reaching_time', 
        'star_rating', 'price', 'seats_available'
    ])

# Main scraping loop
for link in gov_link_list:
    
    pagination = driver.find_elements(By.XPATH, "//div[contains(@class, 'DC_117_paginationTable')]/div[contains(@class, 'DC_117_pageTabs')]")
    driver.get(link);
    time.sleep(3)
    
    # Iterate through each pagination button
    for page in pagination:
        page.click()
        time.sleep(2)
        scrape_current_page()

    route_link = driver.find_elements(By.XPATH, "//div[@class='route_details']/a")
    route_link_list = [element.get_attribute('href') for element in route_link]
    
    for link in route_link_list:
        driver.get(link);
        time.sleep(3)
        
        route_name1 = driver.find_elements(By.XPATH, '//span[@property="name"]')
        route_name1_list = [element.text for element in route_name1]
        print(route_name1)
        route_link1 = driver.current_url

         # Handle multiple buttons to click
        buttons = driver.find_elements(By.XPATH, '//div[@class="button"]')
        if buttons:
            buttons[0].click()

        # Scroll to load all bus elements
        last_height = driver.execute_script("return document.body.scrollHeight") # Scroll element
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
            
        # Find elements for buses
        buses = driver.find_elements(By.XPATH, '//div[@class="clearfix bus-item"]')
        for bus in buses:
            try:
                route_start = bus.find_element(By.XPATH, './/div[@class="dp-loc l-color w-wrap f-12 m-top-42"]').text
            except:
                route_start = np.nan
            
            try:
                route_end = bus.find_element(By.XPATH, './/div[@class="bp-loc l-color w-wrap f-12 m-top-8"]').text
            except:
                route_end = np.nan
    
            try:
                bus_name = bus.find_element(By.XPATH, './/div[@class="travels lh-24 f-bold d-color"]').text
            except:
                bus_name = np.nan
    
            try:
                bustype = bus.find_element(By.XPATH, './/div[@class="bus-type f-12 m-top-16 l-color evBus"]').text
            except:
                bustype = np.nan
    
            try:
                departing_time = bus.find_element(By.XPATH, './/div[@class="dp-time f-19 d-color f-bold"]').text
            except:
                departing_time = np.nan
    
            try:
                duration = bus.find_element(By.XPATH, './/div[@class="dur l-color lh-24"]').text
            except:
                duration = np.nan
    
            try:
                reaching_time = bus.find_element(By.XPATH, './/div[@class="bp-time f-19 d-color disp-Inline"]').text
            except:
                reaching_time = np.nan
    
            try:
                star_rating = bus.find_element(By.XPATH, ".//div[@class='rating-sec lh-24']").text
            except:
                star_rating = np.nan
    
            try:
                price = bus.find_element(By.XPATH, './/div[@class="fare d-block"]').text
            except:
                price = np.nan
                
            try:
                seats_available = bus.find_element(By.XPATH, './/div[@class="column-eight w-15 fl"]/div').text
            except:
                seats_available = np.nan
                
            # Create a temporary DataFrame with the extracted data
            temp_df = pd.DataFrame([{
                'route_name': route_name1_list,
                'route_link': route_link1,
                'route_start': route_start,
                'route_end': route_end,
                'bus_name': bus_name,
                'bustype': bustype,
                'departing_time': departing_time,
                'duration': duration,
                'reaching_time': reaching_time,
                'star_rating': star_rating,
                'price': price,
                'seats_available': seats_available
            }])
    
            df = pd.concat([df, temp_df], ignore_index=True)
    
        driver.back()
        time.sleep(3)
    
    driver.back()
df
df.to_excel("Redbus_data.xlsx")   