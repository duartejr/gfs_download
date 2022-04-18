
#%%
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import calendar
import time
import os

src = "https://www.ncei.noaa.gov/has/HAS.FileAppRouter?datasetname=GFSGRB24&subqueryby=STATION&applname=&outdest=FILE"
geckodriver = 'D:\\Doutorado\\OneDrive - Universidade Federal do Ceará\\projeto_doutorado\\projeto\\src\\geckodriver\\geckodriver.exe'
year = 2011
my_email = 'duarte.jr105@gmail.com'

c = calendar.Calendar(firstweekday=calendar.SUNDAY)
driver = webdriver.Firefox(executable_path=geckodriver)
wait = WebDriverWait(driver, 60)

#%%
def set_inicial_date(year, month, day):
    # Set year
    elem = driver.find_element(by=By.CSS_SELECTOR,
                                value="select.date-select:nth-child(11)")
    select = Select(elem)
    select.select_by_visible_text(year)
    # Set month
    elem = driver.find_element(by=By.CSS_SELECTOR,
                                value="select.date-select:nth-child(12)")
    select = Select(elem)
    select.select_by_visible_text(month)
    # Set day
    elem = driver.find_element(by=By.CSS_SELECTOR,
                                value="select.date-select:nth-child(13)")
    select = Select(elem)
    select.select_by_visible_text(day)

def set_final_date(year, month, day):
    # set year
    elem = driver.find_element(by=By.CSS_SELECTOR,
                                value="select.date-select:nth-child(18)")
    Select(elem).select_by_visible_text(year)
    # set month
    elem = driver.find_element(by=By.CSS_SELECTOR,
                                value="select.date-select:nth-child(19)")
    Select(elem).select_by_visible_text(month)
    # set day
    elem = driver.find_element(by=By.CSS_SELECTOR,
                                value="select.date-select:nth-child(20)")
    Select(elem).select_by_visible_text(day)

def set_batch():
    elem = driver.find_element(by=By.CSS_SELECTOR,
                                value=".hascontent > form:nth-child(1) > input:nth-child(31)").click()

def set_email(email):
    elem = driver.find_element(by=By.CSS_SELECTOR,
                                value=".hascontent > form:nth-child(1) > input:nth-child(36)")
    elem.clear()
    elem.send_keys(email)#%%

def request_data(email, start_year, start_month, start_day, end_year, end_month, end_day):
    set_inicial_date(start_year, start_month, start_day)
    set_final_date(end_year, end_month, end_day)
    set_batch()
    set_email(email)
    elem = driver.find_element(by=By.CSS_SELECTOR,
                                value="button.HASButton:nth-child(1)").click()


for month in range(1, 13):
    monthcal = c.monthdatescalendar(year, month)

    fridays = [day for week in monthcal for day in week \
                if (day.weekday() == calendar.FRIDAY and day.month == month and day.year == year)]
    
    for day in fridays:
        day = day.day
       
        driver.get(src)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "select.date-select:nth-child(11)")))

        str_month = f'{month:02d}'
        str_day = f'{day:02d}'
        request_data(my_email, str(year), str_month, str_day,
                      str(year), str_month, str_day)
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".button")))
            elem = driver.find_element(by=By.CSS_SELECTOR, value=".button").click()
            
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".has-progress-bar > a:nth-child(7)")))
            elem = driver.find_element(by=By.CSS_SELECTOR, value=".has-progress-bar > a:nth-child(7)")
            url_download = elem.get_attribute('innerHTML')

            with open('gfs_download_urls.txt', '+a') as file:
                file.write("\n")
                file.write(url_download)
        except:
            if driver.find_element(by=By.CSS_SELECTOR, value="#messageContainer > p:nth-child(1)"):
                print(f"Don't have data for this date {year}-{str_month}-{str_day}")
# %%
