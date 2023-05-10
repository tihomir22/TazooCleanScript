from selenium import webdriver
 #-*- coding: utf-8 -*-
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import warnings
import re
import json
warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas as pd
urls = ['https://xativa.callejero.net/directorio.html', 
        'https://xativa.callejero.net/directorio-2.html',
        'https://xativa.callejero.net/directorio-3.html',
        'https://xativa.callejero.net/directorio-4.html',
        'https://xativa.callejero.net/directorio-5.html',
        'https://xativa.callejero.net/directorio-6.html']

street_list = []
options = Options()

options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(service=Service(
    ChromeDriverManager().install()), options=options)

def getStreets(url):
    global df
    driver.get(url)
    elements = driver.find_elements('xpath','//div[contains(@class,"itemDirectorio")]/a')
    for element in elements:
        street_list.append(element.text)
    return street_list

for url in urls:
    street_list = getStreets(url)
with open('streets.json', 'w',encoding='utf-8') as file:
    json.dump(street_list, file,ensure_ascii=False)