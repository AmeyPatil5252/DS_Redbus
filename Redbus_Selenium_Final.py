import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import numpy as np

# Initialize the WebDriver
driver = webdriver.Chrome()
driver.get('https://www.redbus.in/online-booking/rtc-directory')  # URL to scrape

# Fetch all government bus links
gov_links = driver.find_elements(By.XPATH, "//li[@class='D113_item_rtc']/a")
gov_link_list = [element.get_attribute('href') for element in gov_links]

# Initialize DataFrame to store the results
df = pd.DataFrame(columns=[
    'route_name', 'route_link', 'route_start', 'route_end', 'bus_name', 'bustype',
    'departing_time', 'duration', 'reaching_time',
    'star_rating', 'price', 'seats_available'
])

# Function to scrape each page of results
def scrape_current_page(driver, df):
    # Find all route links on the current page
    route_links = driver.find_elements(By.XPATH, "//div[@class='route_details']/a")
    route_link_list = [element.get_attribute('href') for element in route_links]

    rows_to_append = []

    for link in route_link_list:
        driver.get(link)
        time.sleep(3)

        try:
            route_name = driver.find_element(By.XPATH, '//li[@property="itemListElement"][2]').text
            print(route_name)
        except:
            route_name = np.nan

        route_link = driver.current_url

        # Scroll to load all bus elements
        last_height = driver.execute_script("return document.body.scrollHeight")
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

            # Collect the row data in a list
            rows_to_append.append({
                'route_name': route_name,
                'route_link': route_link,
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
            })

        driver.back()
        time.sleep(3)

    # Append the collected rows to the DataFrame using pd.concat
    if rows_to_append:
        temp_df = pd.DataFrame(rows_to_append)
        df = pd.concat([df, temp_df], ignore_index=True)

    return df

# Main scraping loop
for gov_link in gov_link_list:
    driver.get(gov_link)
    time.sleep(3)

    # Scrape the first page
    df = scrape_current_page(driver, df)

    # Check for pagination
    while True:
        try:
            pagination = driver.find_element(By.XPATH, "//div[contains(@class, 'DC_117_paginationTable')]")
            pages = pagination.find_elements(By.XPATH, ".//div[contains(@class, 'DC_117_pageTabs')]/a")
            for page in pages:
                page.click()
                time.sleep(2)
                df = scrape_current_page(driver, df)
        except Exception as e:
            print(f"Error clicking page: {e}")
            break

# Save DataFrame to Excel
df.to_excel("Redbus_data.xlsx", index=False)

# Quit WebDriver
driver.quit()
