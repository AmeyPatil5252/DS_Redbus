import time
import arrow
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import date
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd


driver = webdriver.Chrome()  # Optional argument, if not specified will search path.
driver.get('https://www.redbus.in/online-booking/uttar-pradesh-state-road-transport-corporation-upsrtc/?utm_source=rtchometile'); #url to scrape

route_links = driver.find_elements(By.XPATH, "//div[@class='route_details']/a")
if route_links:
    route_links[0].click()
time.sleep(3)
buttons = driver.find_elements(By.XPATH, '//div[@class="button"]')
if buttons:
    buttons[0].click()

route_start= driver.find_elements(By.XPATH,'//div[@class="dp-loc l-color w-wrap f-12 m-top-42"]') 
route_End = driver.find_elements(By.XPATH,'//div[@class="bp-loc l-color w-wrap f-12 m-top-8"]') 
bus_name = driver.find_elements(By.XPATH,'//div[@class="travels lh-24 f-bold d-color"]')
busname = driver.find_elements(By.XPATH,'//div[@class="travels lh-24 f-bold d-color"]')
bustype = driver.find_elements(By.XPATH,'//div[@class="bus-type f-12 m-top-16 l-color evBus"]')
departing_time = driver.find_elements(By.XPATH,'//div[@class="dp-time f-19 d-color f-bold"]')
duration = driver.find_elements(By.XPATH,'//div[@class="dur l-color lh-24"]')
reaching_time = driver.find_elements(By.XPATH,'//div[@class="bp-time f-19 d-color disp-Inline"]')
star_rating = driver.find_elements(By.XPATH,"//div[@class='rating-sec lh-24']")
price = driver.find_elements(By.XPATH,'//span[@class="f-19 f-bold"]')
seats_available = driver.find_elements(By.XPATH,'//div[@class="column-eight w-15 fl"]/div')

#Creat dict
route_start_list = [element.text for element in route_start]
route_end_list = [element.text for element in route_End]
bus_name_list = [element.text for element in bus_name]
bustype_list = [element.text for element in bustype]
departing_time_list = [element.text for element in departing_time]
duration_list = [element.text for element in duration]
reaching_time_list = [element.text for element in reaching_time]
star_rating_list = [element.text for element in star_rating]
price_list = [element.text for element in price]
seats_available_list = [element.text for element in seats_available]

# Create the DataFrame
df = pd.DataFrame({
    'route_start': route_start_list,
    'route_end': route_end_list,
    'bus_name': bus_name_list,
    'bustype': bustype_list,
    'departing_time': departing_time_list,
    'duration': duration_list,
    'reaching_time': reaching_time_list,
    'star_rating': star_rating_list,
    'price':price_list,
    'seats_available': seats_available_list
})

df.columns()