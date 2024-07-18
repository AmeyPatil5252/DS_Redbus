import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import numpy as np

# Initialize the WebDriver
driver = webdriver.Chrome()  # Optional argument, if not specified will search path.
driver.get('https://www.redbus.in/online-booking/uttar-pradesh-state-road-transport-corporation-upsrtc/?utm_source=rtchometile')  # url to scrape

# Initialize an empty DataFrame
df = pd.DataFrame(columns=[
    'route_start', 'route_end', 'bus_name', 'bustype',
    'departing_time', 'duration', 'reaching_time', 
    'star_rating', 'price', 'seats_available'
])

# Get the initial list of route links
route_links = driver.find_elements(By.XPATH, "//div[@class='route_details']/a")

# Loop through each route link
for i in range(len(route_links)):
    # Re-find the route links to avoid StaleElementReferenceException
    route_links = driver.find_elements(By.XPATH, "//div[@class='route_details']/a")
    
    if i >= len(route_links):
        print(f"Skipping index {i} as it's out of range after re-fetching route_links")
        continue
    
    # Click the current route link
    route_links[i].click()
    time.sleep(3)

    # Click the 'View More' button if it exists
    buttons = driver.find_elements(By.XPATH, '//div[@class="button"]')
    if buttons:
        buttons[0].click()
        time.sleep(3)
    
    # Find elements for buses
    buses = driver.find_elements(By.XPATH, '//div[@class="clearfix bus-item"]')
    
    for bus in buses:
        # Extract data for each bus
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
            price = bus.find_element(By.XPATH, './/span[@class="f-19 f-bold"]').text
        except:
            price = np.nan

        try:
            seats_available = bus.find_element(By.XPATH, './/div[@class="column-eight w-15 fl"]/div').text
        except:
            seats_available = np.nan

        # Create a temporary DataFrame with the extracted data
        temp_df = pd.DataFrame([{
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

        # Append the data to the main DataFrame
        df = pd.concat([df, temp_df], ignore_index=True)

    # Go back to the main page to scrape the next route
    driver.back()
    time.sleep(3)

print(df)

# Close the driver
driver.quit()
